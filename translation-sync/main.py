#!/usr/bin/env python3
"""번역 동기화 엔트리포인트.

설정·프롬프트 확인 → 원문 동기화 → 변경 감지 → 전처리 → 번역 → 후처리 → 문서 검증·출력 → 사이드바 갱신 순서로 후보 산출물 생성.

출력 로케일: ko(versioned_docs), ja(i18n/ja).
프롬프트: ko=prompt.md, ja=prompt_jp.md.
실행: uv run --locked python main.py
"""
from __future__ import annotations

import os
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

from sync import (
    annotate,
    config,
    diff,
    patch as patch_utils,
    postprocess,
    preprocess,
    prompt,
    repair,
    response_contract,
    sidebar,
    translate,
    upstream,
    verify,
)
from sync.common import stale_links
from sync.common.files import atomic_write_bytes, atomic_write_text, unlink_file
from sync.verification import document as document_verification

SYNC_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SYNC_ROOT.parent
PROMPT_PATH = SYNC_ROOT / "prompt.md"
JA_PROMPT_PATH = SYNC_ROOT / "prompt_jp.md"
PRESERVED_MARKUP_FIXABLE = {
    "link target mismatch",
    "link label mismatch",
    "link pair mismatch",
    "link title mismatch",
    "heading mismatch",
    "heading text mismatch",
}
MAX_SEGMENT_VERIFICATION_ATTEMPTS = translate.MAX_COMPLETED_RESPONSE_ATTEMPTS


class OutputPathError(ValueError):
    """안전하게 변경할 수 없는 번역 출력 경로 오류."""


class SourcePathError(ValueError):
    """안전하게 읽을 수 없는 영어 원문 경로 오류."""


@dataclass(frozen=True)
class _PreparedBlockTranslation:
    """프로바이더 호출 전에 확정한 블록 원문·문맥·복원 정보."""

    request_source: str
    existing_context: str
    diff_text: str
    expected_source: str
    placeholders: Mapping[str, str]


@dataclass(frozen=True)
class _PreparedTranslationTarget:
    """로케일 하나의 입력 바이트·패치 계획·블록별 사전 검증 결과."""

    source: str
    existing: str | None
    existing_bytes: bytes | None
    plan: patch_utils.PatchPlan
    state: patch_utils.PlanState
    placeholders: Mapping[str, str]
    block_requests: Mapping[int, _PreparedBlockTranslation]


def _validated_output_path(path: Path) -> Path:
    """허용된 로케일 루트 안에서 심볼릭 링크를 거치지 않는 출력 경로 검증."""

    root = REPO_ROOT.absolute()
    candidate = path.absolute()
    allowed_roots = (
        root / "versioned_docs",
        root / "i18n" / "ja" / "docusaurus-plugin-content-docs",
    )
    if not any(candidate.is_relative_to(allowed) for allowed in allowed_roots):
        raise OutputPathError(f"unsafe translation output path: {path}")

    relative = candidate.relative_to(root)
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise OutputPathError(f"unsafe translation output path: {path}")

    resolved = candidate.resolve(strict=False)
    resolved_root = REPO_ROOT.resolve()
    resolved_allowed_roots = (
        resolved_root / "versioned_docs",
        resolved_root / "i18n" / "ja" / "docusaurus-plugin-content-docs",
    )
    if not any(
        resolved.is_relative_to(allowed) for allowed in resolved_allowed_roots
    ):
        raise OutputPathError(f"unsafe translation output path: {path}")
    if candidate.exists() and not candidate.is_file():
        raise OutputPathError(f"unsafe translation output path: {path}")
    return candidate


def _ko_output(change: diff.SourceChange) -> Path:
    """원문 변경에 대응하는 한국어 출력 경로 반환."""

    return (
        REPO_ROOT
        / "versioned_docs"
        / f"version-{change.version}"
        / change.document
    )


def _ja_output(change: diff.SourceChange) -> Path:
    """원문 변경에 대응하는 일본어 출력 경로 반환."""

    return (
        REPO_ROOT
        / "i18n"
        / "ja"
        / "docusaurus-plugin-content-docs"
        / f"version-{change.version}"
        / change.document
    )


def _validate_file_states(changes: list[diff.SourceChange]) -> list[str]:
    """첫 로케일 변경 전에 모든 영어·한국어·일본어 파일 상태 검증."""
    issues: list[str] = []
    for change in changes:
        source = REPO_ROOT / change.path
        try:
            locale_paths = (
                ("ko", _validated_output_path(_ko_output(change))),
                ("ja", _validated_output_path(_ja_output(change))),
            )
        except OutputPathError as exc:
            issues.append(f"{change.path}: {exc}")
            continue

        if change.status not in {"A", "M", "D"}:
            issues.append(f"{change.path}: unsupported source status {change.status!r}")
            continue
        if change.status == "M" and not change.hunks:
            issues.append(f"{change.path}: M requires raw diff hunks")

        source_exists = source.is_file() and not source.is_symlink()
        expected_source = change.status in {"A", "M"}
        if source_exists != expected_source:
            expectation = "existing" if expected_source else "absent"
            issues.append(
                f"{change.path}: {change.status} requires {expectation} English source"
            )

        expected_locale = change.status in {"M", "D"}
        for locale, path in locale_paths:
            locale_exists = path.is_file() and not path.is_symlink()
            if locale_exists != expected_locale:
                expectation = "existing" if expected_locale else "absent"
                issues.append(
                    f"{change.path}: {change.status} requires {expectation} "
                    f"{locale} locale"
                )
    return issues


def _delete_outputs(change: diff.SourceChange) -> list[str]:
    """원문 삭제에 대응하는 한국어·일본어 출력 파일 삭제."""

    try:
        paths = tuple(
            _validated_output_path(path)
            for path in (_ko_output(change), _ja_output(change))
        )
    except OutputPathError as exc:
        return [str(exc)]

    for path in paths:
        unlink_file(path, missing_ok=True)
    return []


def _preflight_all_translation_targets(
    changes: list[diff.SourceChange],
    cfg: config.Config,
    prompts: Mapping[str, str],
) -> tuple[dict[tuple[str, str], _PreparedTranslationTarget], list[str]]:
    """첫 로케일 기록 전에 모든 대상의 계획·입력·요청 예산 검증."""

    prepared: dict[tuple[str, str], _PreparedTranslationTarget] = {}
    issues: list[str] = []
    for change in changes:
        if change.status == "D":
            continue
        for locale, dest in (
            ("ko", _ko_output(change)),
            ("ja", _ja_output(change)),
        ):
            try:
                prepared[(change.path, locale)] = _prepare_translation_target(
                    change,
                    cfg,
                    prompts[locale],
                    dest,
                )
            except OutputPathError as exc:
                issues.append(f"{locale} {change.path}: {exc}")
            except config.ConfigError as exc:
                issues.append(
                    f"{locale} {change.path}: {_translation_config_issue(exc)}"
                )
            except translate.IncompleteTranslation as exc:
                issues.append(
                    f"{locale} {change.path}: translation preflight failed: {exc}"
                )
            except patch_utils.PatchError as exc:
                issues.append(
                    f"{locale} {change.path}: patch preflight failed: {exc}"
                )
            except UnicodeDecodeError as exc:
                issues.append(
                    f"{locale} {change.path}: translation input is not UTF-8: {exc}"
                )
            except ValueError as exc:
                issues.append(
                    f"{locale} {change.path}: translation preflight failed: {exc}"
                )
            except OSError as exc:
                issues.append(
                    f"{locale} {change.path}: translation input read failed: {exc}"
                )
    return prepared, issues


def _sidebar_versions(changes: list[diff.SourceChange], version: str | None) -> list[str]:
    """전체 사이드바 검증에 사용할 정규 버전 순서 반환."""

    del changes, version
    return sidebar.load_versions(REPO_ROOT)


def _load_prompts() -> dict[str, str]:
    """한국어·일본어 운영 프롬프트를 로케일별로 로드."""

    return {
        "ko": prompt.load_prompt(PROMPT_PATH),
        "ja": prompt.load_prompt(JA_PROMPT_PATH),
    }


def _matches_filters(
    change: diff.SourceChange, *, version: str | None, doc: str | None
) -> bool:
    """원문 변경이 정규화된 버전·문서 선택자와 일치하는지 판별."""

    if version and change.version != version:
        return False
    if doc:
        name = doc if doc.endswith(".md") else f"{doc}.md"
        if change.document != name:
            return False
    return True


def _select_changes(
    *, migrate_existing: bool = False, version: str | None = None, doc: str | None = None
) -> list[diff.SourceChange]:
    """선택자와 실행 모드에 맞는 원문 변경 선택."""

    if not migrate_existing:
        return _sort_changes([
            change
            for change in diff.changed_sources()
            if _matches_filters(change, version=version, doc=doc)
        ])

    repo_root = REPO_ROOT.absolute()
    en_root = (
        repo_root / "i18n" / "en" / "docusaurus-plugin-content-docs"
    )
    current = repo_root
    for part in en_root.relative_to(repo_root).parts:
        current /= part
        if current.is_symlink():
            raise SourcePathError(f"unsafe English source path: {current}")
    if not en_root.is_dir():
        raise SourcePathError(f"unsafe English source path: {en_root}")

    changes: list[diff.SourceChange] = []
    for version_root in sorted(en_root.iterdir()):
        if not version_root.name.startswith("version-"):
            continue
        if version_root.suffix == ".json":
            continue
        if version_root.is_symlink():
            raise SourcePathError(
                f"unsafe English source path: {version_root}"
            )
        if not version_root.is_dir():
            continue
        for path in _recursive_source_markdown(version_root):
            change = diff.SourceChange(
                path=str(path.relative_to(repo_root)),
                status="M",
            )
            if _matches_filters(change, version=version, doc=doc):
                changes.append(change)
    return changes


def _sort_changes(
    changes: list[diff.SourceChange],
) -> list[diff.SourceChange]:
    """사이드바 버전 순서와 문서명에 따라 변경 정렬."""

    if not changes:
        return []
    versions = sidebar.load_versions(REPO_ROOT)
    rank = {version: index for index, version in enumerate(versions)}
    unknown = sorted(
        {change.version for change in changes if change.version not in rank},
        key=lambda value: value.encode("utf-8"),
    )
    if unknown:
        raise SourcePathError(
            "source change uses unsupported version(s): " + ", ".join(unknown)
        )
    return sorted(
        changes,
        key=lambda change: (
            rank[change.version],
            change.document.encode("utf-8"),
        ),
    )


def _recursive_source_markdown(root: Path) -> list[Path]:
    """심볼릭 링크를 거부하며 루트 아래의 Markdown 문서를 결정적 순서로 수집."""

    documents: list[Path] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            entries = sorted(
                directory.iterdir(),
                key=lambda path: path.name.encode("utf-8"),
                reverse=True,
            )
        except OSError as exc:
            raise SourcePathError(
                f"unsafe English source path: {directory}"
            ) from exc
        for path in entries:
            if path.is_symlink():
                raise SourcePathError(f"unsafe English source path: {path}")
            if path.is_dir():
                pending.append(path)
            elif path.suffix == ".md":
                if not path.is_file():
                    raise SourcePathError(f"unsafe English source path: {path}")
                documents.append(path)
    return sorted(
        documents,
        key=lambda path: path.relative_to(root).as_posix().encode("utf-8"),
    )


def _translation_request(
    source: str,
    existing_translation: str | None,
    *,
    version: str | None = None,
    diff_text: str | None = None,
    verification_feedback: str | None = None,
) -> translate.TranslationRequest:
    """응답 계약 버전을 포함한 구조화된 번역 요청 생성."""

    return translate.TranslationRequest(
        source=source,
        existing_translation=existing_translation,
        diff_text=diff_text,
        verification_feedback=verification_feedback,
        version=version,
        response_contract_version=response_contract.RESPONSE_CONTRACT_VERSION,
    )


def _verification_feedback(issues: list[str]) -> str:
    """응답 계약 문제를 길이가 제한된 프로바이더 교정 지침으로 변환."""

    return translate.verification_feedback(issues)


def _contract_issues(
    translated: str,
    source: str,
    cfg: config.Config,
    change: diff.SourceChange,
    locale: str | None,
) -> list[str]:
    """프로바이더 응답을 현재 로케일과 고정된 응답 계약으로 검증."""

    contract_source = (
        response_contract.identity_source_view(source, change.version)
        if cfg.provider == "identity"
        else source
    )
    return response_contract.verify(
        translated,
        contract_source,
        locale=None if cfg.provider == "identity" else locale,
        contract_version=response_contract.RESPONSE_CONTRACT_VERSION,
    )


def _translate_added_document(
    change: diff.SourceChange,
    cfg: config.Config,
    prompt: str,
    dest: Path,
    *,
    locale: str | None = None,
    deadline: float | None = None,
    prepared_target: _PreparedTranslationTarget | None = None,
) -> list[str]:
    """추가된 문서 번역."""

    try:
        dest = _validated_output_path(dest)
        target = prepared_target or _prepare_translation_target(
            change,
            cfg,
            prompt,
            dest,
        )
        if target.state is not patch_utils.PlanState.CREATE:
            raise patch_utils.PatchError("added document is not in create state")
        translated_blocks: list[str] = []
        for owner in target.plan.create_blocks:
            if not owner.provider_required:
                continue
            request_source = owner.source
            feedback: str | None = None
            contract_issues: list[str] = []
            for attempt in range(MAX_SEGMENT_VERIFICATION_ATTEMPTS):
                translated_block = translate.translate_request(
                    _translation_request(
                        request_source,
                        None,
                        version=change.version,
                        verification_feedback=feedback,
                    ),
                    cfg,
                    prompt,
                    deadline=deadline,
                )
                contract_issues = _contract_issues(
                    translated_block, request_source, cfg, change, locale
                )
                translate.require_run_deadline(deadline)
                if not contract_issues:
                    translated_blocks.append(translated_block)
                    break
                if (
                    attempt + 1 >= MAX_SEGMENT_VERIFICATION_ATTEMPTS
                    or not response_contract.supports_feedback_retry(
                        translated_block,
                        request_source,
                        contract_issues,
                    )
                ):
                    return [
                        "provider response contract failed: "
                        + ", ".join(contract_issues)
                    ]
                feedback = _verification_feedback(contract_issues)
        translated = patch_utils.apply_plan(
            target.existing,
            target.plan,
            translated_blocks,
        )
        out = postprocess.postprocess(
            translated,
            change.version,
            target.placeholders,
        )
    except OutputPathError as exc:
        return [str(exc)]
    except patch_utils.PatchError as exc:
        return [f"create patch failed: {exc}"]
    except config.ConfigError as exc:
        return [_translation_config_issue(exc)]
    except translate.IncompleteTranslation as exc:
        return [f"incomplete translation: {exc}"]
    except UnicodeDecodeError as exc:
        return [f"create translation input is not UTF-8: {exc}"]
    except ValueError as exc:
        return [f"create translation input failed: {exc}"]
    except OSError as exc:
        return [f"create translation input read failed: {exc}"]
    return _verify_and_admit_document(
        dest,
        out,
        target.source,
        change.version,
        target.placeholders,
        write=True,
        canonicalize=True,
    )


def _prepare_block_translation(
    change: diff.SourceChange,
    block_change: patch_utils.BlockChange,
    cfg: config.Config,
    prompt: str,
    existing: str,
    *,
    placeholders: Mapping[str, str] | None = None,
) -> _PreparedBlockTranslation:
    """블록 번역 요청 준비."""

    source = patch_utils.source_text(block_change)
    if placeholders is None:
        pre = preprocess.preprocess(source)
        request_source = pre.text
        restore_map: Mapping[str, str] = MappingProxyType(
            dict(pre.placeholders)
        )
    else:
        request_source = _mask_with_restore_map(source, placeholders)
        restore_map = placeholders
    expected_source = postprocess.postprocess(
        request_source,
        change.version,
        restore_map,
    )
    existing_context = _mask_with_restore_map(
        patch_utils.existing_context(existing, block_change),
        restore_map,
    )
    diff_text = _mask_with_restore_map(
        patch_utils.diff_text(block_change),
        restore_map,
    )
    request = _translation_request(
        request_source,
        existing_context,
        version=change.version,
        diff_text=diff_text,
    )
    translate.preflight_request(request, cfg, prompt)
    return _PreparedBlockTranslation(
        request_source=request_source,
        existing_context=existing_context,
        diff_text=diff_text,
        expected_source=expected_source,
        placeholders=restore_map,
    )


def _mask_with_restore_map(
    text: str,
    placeholders: Mapping[str, str],
) -> str:
    """복원 매핑을 사용해 원문 요소 마스킹."""

    for placeholder, original in sorted(
        placeholders.items(),
        key=lambda item: item[1].encode("utf-8"),
        reverse=True,
    ):
        text = text.replace(original, placeholder)
    return text


def _translate_block_change(
    change: diff.SourceChange,
    block_change: patch_utils.BlockChange,
    cfg: config.Config,
    prompt: str,
    existing: str,
    *,
    locale: str | None = None,
    deadline: float | None = None,
    placeholders: Mapping[str, str] | None = None,
    prepared: _PreparedBlockTranslation | None = None,
) -> str:
    """변경된 블록 번역."""

    prepared = prepared or _prepare_block_translation(
        change,
        block_change,
        cfg,
        prompt,
        existing,
        placeholders=placeholders,
    )
    feedback: str | None = None
    contract_issues: list[str] = []

    for attempt in range(MAX_SEGMENT_VERIFICATION_ATTEMPTS):
        translated = translate.translate_request(
            _translation_request(
                prepared.request_source,
                prepared.existing_context,
                version=change.version,
                diff_text=prepared.diff_text,
                verification_feedback=feedback,
            ),
            cfg,
            prompt,
            deadline=deadline,
        )
        contract_issues = _contract_issues(
            translated,
            prepared.request_source,
            cfg,
            change,
            locale,
        )
        translate.require_run_deadline(deadline)
        if contract_issues:
            if (
                attempt + 1 >= MAX_SEGMENT_VERIFICATION_ATTEMPTS
                or not response_contract.supports_feedback_retry(
                    translated,
                    prepared.request_source,
                    contract_issues,
                )
            ):
                break
            feedback = _verification_feedback(contract_issues)
            continue

        out = postprocess.postprocess(
            translated,
            change.version,
            prepared.placeholders,
        )
        if cfg.provider == "identity":
            return out
        return _repair_segment_translation(
            prepared.expected_source,
            out,
            change.version,
        )

    if contract_issues:
        raise translate.IncompleteTranslation(
            "provider response contract failed: " + ", ".join(contract_issues)
        )
    raise translate.IncompleteTranslation("provider response contract failed")


def _render_provider_free_change(
    change: diff.SourceChange,
    block_change: patch_utils.BlockChange,
    *,
    placeholders: Mapping[str, str] | None = None,
) -> str:
    """프로바이더 호출이 필요 없는 변경 렌더링."""

    source = patch_utils.source_text(block_change)
    if placeholders is None:
        pre = preprocess.preprocess(source)
        source = pre.text
        placeholders = pre.placeholders
    else:
        source = _mask_with_restore_map(source, placeholders)
    expected_source = postprocess.postprocess(
        source,
        change.version,
        placeholders,
    )
    return _repair_segment_translation(
        expected_source,
        expected_source,
        change.version,
    )


def _preview_provider_translation(
    request_source: str,
    version: str,
    placeholders: Mapping[str, str],
) -> str:
    """프로바이더 호출 없이 원문을 복원해 계획 적용용 미리보기 생성."""

    expected = postprocess.postprocess(request_source, version, placeholders)
    return _repair_segment_translation(expected, expected, version)


def _preflight_create_plan(
    change: diff.SourceChange,
    plan: patch_utils.PatchPlan,
    cfg: config.Config,
    prompt: str,
) -> None:
    """문서 생성 계획에서 프로바이더가 필요한 소유 블록의 요청 사전 검증."""

    for owner in plan.create_blocks:
        if not owner.provider_required:
            continue
        request = _translation_request(
            owner.source,
            None,
            version=change.version,
        )
        translate.preflight_request(request, cfg, prompt)


def _preflight_modified_plan(
    change: diff.SourceChange,
    plan: patch_utils.PatchPlan,
    state: patch_utils.PlanState,
    cfg: config.Config,
    prompt: str,
    existing: str,
    placeholders: Mapping[str, str],
) -> dict[int, _PreparedBlockTranslation]:
    """수정 계획의 블록 요청과 프로바이더 비호출 미리보기 적용 가능성 검증."""

    if plan.is_noop or state is patch_utils.PlanState.TARGET:
        return {}

    prepared: dict[int, _PreparedBlockTranslation] = {}
    previews: list[str] = []
    for block_change in plan.changes:
        if not block_change.needs_translation:
            continue
        if block_change.provider_free:
            previews.append(
                _render_provider_free_change(
                    change,
                    block_change,
                    placeholders=placeholders,
                )
            )
            continue
        block_preflight = _prepare_block_translation(
            change,
            block_change,
            cfg,
            prompt,
            existing,
            placeholders=placeholders,
        )
        prepared[id(block_change)] = block_preflight
        previews.append(
            _preview_provider_translation(
                block_preflight.request_source,
                change.version,
                placeholders,
            )
        )
    patch_utils.apply_plan(existing, plan, previews)
    return prepared


def _translation_config_issue(exc: config.ConfigError) -> str:
    """번역 설정 오류를 안정적 문제 코드가 포함된 진단으로 변환."""

    return (
        "translation configuration failed "
        f"[{exc.issue_code.value}]: {exc}"
    )


def _prepare_translation_target(
    change: diff.SourceChange,
    cfg: config.Config,
    prompt: str,
    dest: Path,
) -> _PreparedTranslationTarget:
    """로케일별 번역 대상 사전 준비."""

    dest = _validated_output_path(dest)
    source = (REPO_ROOT / change.path).read_text(encoding="utf-8")

    if change.status == "A":
        preprocessed = preprocess.preprocess(source)
        placeholders: Mapping[str, str] = MappingProxyType(
            dict(preprocessed.placeholders)
        )
        existing_bytes = dest.read_bytes() if dest.exists() else None
        existing = (
            existing_bytes.decode("utf-8")
            if existing_bytes is not None
            else None
        )
        plan = patch_utils.build_create_plan(preprocessed.text)
        state = patch_utils.plan_state(existing, plan)
        _preflight_create_plan(
            change,
            plan,
            cfg,
            prompt,
        )
        return _PreparedTranslationTarget(
            source=preprocessed.text,
            existing=existing,
            existing_bytes=existing_bytes,
            plan=plan,
            state=state,
            placeholders=placeholders,
            block_requests=MappingProxyType({}),
        )

    if change.status != "M":
        raise patch_utils.PatchError(
            f"unsupported translation status {change.status!r}"
        )
    if not change.hunks:
        raise patch_utils.PatchError("missing diff hunks for partial sync")
    if not dest.exists():
        raise patch_utils.PatchError(
            "missing existing translation for partial sync"
        )

    existing_bytes = dest.read_bytes()
    existing = existing_bytes.decode("utf-8")
    plan, pair = _build_modified_plan(change, source)
    placeholders = MappingProxyType(dict(pair.current.placeholders))
    state = patch_utils.plan_state(existing, plan)
    block_requests = _preflight_modified_plan(
        change,
        plan,
        state,
        cfg,
        prompt,
        existing,
        placeholders,
    )
    return _PreparedTranslationTarget(
        source=pair.current.text,
        existing=existing,
        existing_bytes=existing_bytes,
        plan=plan,
        state=state,
        placeholders=placeholders,
        block_requests=MappingProxyType(dict(block_requests)),
    )


def _repair_segment_translation(source: str, translated: str, version: str) -> str:
    """번역 구간의 보존 서식 복구."""

    translated = _repair_blockquote_segment(source, translated)
    translated = repair.restore_list_markers(source, translated)
    candidates = [translated]

    try:
        repaired = repair.repair_preserved_markup(source, translated).text
        candidates.append(repaired)
    except repair.RepairError:
        repaired = translated

    annotated, _drifts = annotate.annotate(source, repaired, version)
    candidates.append(annotated)

    best = min(
        candidates,
        key=lambda candidate: len(
            verify.verify(candidate, source=source, version=version)
        ),
    )
    missing_comments = verify.missing_original_comments(best, source)
    if not missing_comments:
        return best

    comments = "\n".join(
        f"<!-- {comment.replace('-->', '--&gt;')} -->" for comment in missing_comments
    )
    return f"{comments}\n{best.lstrip()}"


def _canonicalize_document_annotations(
    annotation_source: str,
    english_view: str,
    translated: str,
    version: str,
) -> str:
    """문서의 영어 원문 주석을 정규 형식으로 정리."""

    source_comments_preserved, source_comment_indexes = (
        response_contract._matched_source_comment_indexes(
            translated,
            english_view,
        )
    )
    if not source_comments_preserved:
        raise ValueError(
            "locale source comments do not match the English view"
        )
    canonical, drifts = annotate.annotate(
        annotation_source,
        translated,
        version,
        canonical=True,
        alignment_source=english_view,
        preserved_comment_indexes=frozenset(source_comment_indexes),
    )
    if drifts:
        raise ValueError("locale blocks do not align with the English view")
    return canonical


def _repair_blockquote_segment(source: str, translated: str) -> str:
    """인용문 블록 구간 복구."""

    source_lines = [line for line in source.splitlines() if line.strip()]
    if not source_lines or any(not line.lstrip().startswith(">") for line in source_lines):
        return translated

    out: list[str] = []
    for line in translated.splitlines(keepends=True):
        body, ending = _split_line_ending(line)
        if not body.strip() or body.lstrip().startswith(">"):
            out.append(line)
            continue
        out.append(f"> {body}{ending}")
    return "".join(out)


def _split_line_ending(line: str) -> tuple[str, str]:
    """본문과 줄바꿈 문자 분리."""

    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def _normalize_plan_source_pair(
    previous: str,
    current: str,
    version: str,
    *,
    capture: list[preprocess.PreprocessedPair] | None = None,
) -> tuple[str, str]:
    """계획에 사용할 이전·현재 원문 쌍 정규화."""

    pair = preprocess.preprocess_pair(previous, current)
    if capture is not None:
        capture.append(pair)
    return (
        postprocess.postprocess(
            pair.previous.text,
            version,
            pair.previous.placeholders,
        ),
        postprocess.postprocess(
            pair.current.text,
            version,
            pair.current.placeholders,
        ),
    )


def _build_modified_plan(
    change: diff.SourceChange,
    source: str,
) -> tuple[patch_utils.PatchPlan, preprocess.PreprocessedPair]:
    """수정 문서의 패치 계획 구성."""

    pairs: list[preprocess.PreprocessedPair] = []
    plan = patch_utils.build_plan(
        change.hunks,
        source,
        normalize_source_pair=lambda previous, current: _normalize_plan_source_pair(
            previous,
            current,
            change.version,
            capture=pairs,
        ),
    )
    if len(pairs) != 1:
        raise patch_utils.PatchError("source pair preprocessing did not complete once")
    return plan, pairs[0]


def _annotation_source(
    source: str,
    version: str,
    placeholders: Mapping[str, str],
) -> str:
    """원문 보기의 보호용 자리표시자를 복원해 영어 원문 주석 기준 생성."""

    versioned = response_contract.identity_source_view(source, version)
    return postprocess.restore_placeholders(versioned, placeholders)


def _document_verification_result(
    locale_document: str | bytes,
    source: str,
    version: str,
    placeholders: Mapping[str, str],
    *,
    canonicalize: bool,
) -> document_verification.VerificationResult:
    """오래된 링크 레지스트리 스냅샷에 결합된 최종 문서 검증 실행."""

    registry_at_start = stale_links.load_stale_link_registry()
    annotation_source = _annotation_source(source, version, placeholders)
    english_view = postprocess.postprocess(
        source,
        version,
        placeholders,
        registry=registry_at_start,
    )
    if canonicalize:
        if isinstance(locale_document, bytes):
            locale_document = locale_document.decode("utf-8")
        locale_document = _canonicalize_document_annotations(
            annotation_source,
            english_view,
            locale_document,
            version,
        )
    inputs = document_verification.create_verification_input(
        locale_document=locale_document,
        english_view=english_view,
        annotation_source=annotation_source,
        version=version,
        registry_sha256=registry_at_start.sha256,
    )

    def final_snapshot() -> tuple[
        document_verification.VerificationInput,
        stale_links.StaleLinkRegistry,
    ]:
        """레지스트리를 다시 읽어 산출물 생성 직전의 검증 입력 재구성."""

        registry_at_end = stale_links.load_stale_link_registry()
        final_input = document_verification.create_verification_input(
            locale_document=locale_document,
            english_view=postprocess.postprocess(
                source,
                version,
                placeholders,
                registry=registry_at_end,
            ),
            annotation_source=annotation_source,
            version=version,
            registry_sha256=registry_at_end.sha256,
        )
        return final_input, registry_at_end

    return document_verification.verify_document(
        inputs,
        registry_at_start=registry_at_start,
        final_snapshot=final_snapshot,
    )


def _document_verification_issues(
    result: document_verification.VerificationResult,
) -> list[str]:
    """구조화된 문서 문제를 안정적 CLI 진단 문자열로 변환."""

    return [
        f"{issue.code}: {issue.structural_address or 'document'}: {issue.message}"
        for issue in result.issues
    ]


def _verify_and_admit_document(
    dest: Path,
    locale_document: str | bytes,
    source: str,
    version: str,
    placeholders: Mapping[str, str],
    *,
    write: bool,
    canonicalize: bool = False,
) -> list[str]:
    """문서를 검증하고 승인된 결과를 선택적으로 기록."""

    try:
        result = _document_verification_result(
            locale_document,
            source,
            version,
            placeholders,
            canonicalize=canonicalize,
        )
    except (UnicodeDecodeError, ValueError, stale_links.StaleLinkRegistryError) as exc:
        return [f"document verification input failed: {exc}"]
    issues = _document_verification_issues(result)
    if issues:
        return issues
    if result.artifact is None:
        return ["document verification produced no verified locale artifact"]
    if write:
        dest.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_bytes(dest, result.artifact.locale_bytes)
    return []


def _translate_one(
    change: diff.SourceChange,
    cfg: config.Config,
    prompt: str,
    dest: Path,
    *,
    locale: str | None = None,
    deadline: float | None = None,
    prepared_target: _PreparedTranslationTarget | None = None,
) -> list[str]:
    """원문 한 건을 한 로케일로 번역·후처리·검증·기록하고 위반 목록 반환."""
    if change.status == "A":
        return _translate_added_document(
            change,
            cfg,
            prompt,
            dest,
            locale=locale,
            deadline=deadline,
            prepared_target=prepared_target,
        )
    try:
        dest = _validated_output_path(dest)
        if not dest.exists():
            return ["missing existing translation for partial sync"]
        if not change.hunks:
            return ["missing diff hunks for partial sync"]
        target = prepared_target or _prepare_translation_target(
            change,
            cfg,
            prompt,
            dest,
        )
        existing = target.existing
        existing_bytes = target.existing_bytes
        if existing is None or existing_bytes is None:
            raise patch_utils.PatchError(
                "missing existing translation for partial sync"
            )

        if target.plan.is_noop or target.state is patch_utils.PlanState.TARGET:
            return _verify_and_admit_document(
                dest,
                existing_bytes,
                target.source,
                change.version,
                target.placeholders,
                write=False,
            )

        expected_source = postprocess.postprocess(
            target.source,
            change.version,
            target.placeholders,
        )
        if (
            target.state is patch_utils.PlanState.UNGUARDED
            and target.plan.old_code_blocks != target.plan.new_code_blocks
            and not _verify_and_admit_document(
                dest,
                existing_bytes,
                target.source,
                change.version,
                target.placeholders,
                write=False,
            )
        ):
            return []

        translated_blocks: list[str] = []
        for block_change in target.plan.changes:
            if block_change.needs_translation:
                if block_change.provider_free:
                    translated_blocks.append(
                        _render_provider_free_change(
                            change,
                            block_change,
                            placeholders=target.placeholders,
                        )
                    )
                else:
                    translated_blocks.append(
                        _translate_block_change(
                            change,
                            block_change,
                            cfg,
                            prompt,
                            existing,
                            locale=locale,
                            deadline=deadline,
                            placeholders=target.placeholders,
                            prepared=target.block_requests.get(id(block_change)),
                        )
                    )
        out = patch_utils.apply_plan(
            existing,
            target.plan,
            translated_blocks,
        )
        out = postprocess.postprocess(
            out,
            change.version,
            target.placeholders,
        )
    except OutputPathError as exc:
        return [str(exc)]
    except patch_utils.PatchError as exc:
        return [f"partial patch failed: {exc}"]
    except config.ConfigError as exc:
        return [_translation_config_issue(exc)]
    except translate.IncompleteTranslation as exc:
        return [f"partial translation failed: {exc}"]
    except UnicodeDecodeError as exc:
        return [f"partial translation input is not UTF-8: {exc}"]
    except ValueError as exc:
        return [f"partial translation input failed: {exc}"]
    except OSError as exc:
        return [f"partial translation input read failed: {exc}"]

    # 부분 패치는 영향을 받지 않은 로케일 문맥을 보존.
    # 전체 문서 검증 전에 해당 문맥과 패치한 블록을 함께 정규화해야 기존 경고문과 원문 주석이 오래된 상태로 남지 않음.
    out = _repair_segment_translation(expected_source, out, change.version)
    return _verify_and_admit_document(
        dest,
        out,
        target.source,
        change.version,
        target.placeholders,
        write=True,
        canonicalize=True,
    )


def _expected_source(change: diff.SourceChange) -> str:
    """원문에 전처리와 후처리를 적용한 검증 기준 원문 생성."""
    src = (REPO_ROOT / change.path).read_text(encoding="utf-8")
    pre = preprocess.preprocess(src)
    return postprocess.postprocess(pre.text, change.version, pre.placeholders)


def _check_existing_annotations(
    *, version: str | None = None, doc: str | None = None
) -> list[str]:
    """기존 한국어·일본어 문서의 영어 원문 주석 병기 형식 검증."""
    failures: list[str] = []
    for change in _select_changes(migrate_existing=True, version=version, doc=doc):
        expected_source = _expected_source(change)
        for locale, dest in (("ko", _ko_output(change)), ("ja", _ja_output(change))):
            if not dest.exists():
                continue

            issues = verify.verify(
                dest.read_text(encoding="utf-8"),
                source=expected_source,
                version=change.version,
            )
            failures.extend(f"{locale} {change.path}: {issue}" for issue in issues)
    return failures


def _sync_sidebars(versions: list[str]) -> list[str]:
    """사이드바 동기화."""

    failures: list[str] = []
    for result in sidebar.sync_versions(versions, write=True, repo_root=REPO_ROOT):
        for issue in result.issues:
            failures.append(f"{result.version}: {issue}")
    return failures


def _annotate_existing(
    *, apply: bool = False, version: str | None = None, doc: str | None = None
) -> tuple[int, list[str]]:
    """기존 한국어·일본어 문서에 영어 원문 주석을 병기하고 안전한 파일만 기록."""
    writable = 0
    failures: list[str] = []

    for change in _select_changes(migrate_existing=True, version=version, doc=doc):
        expected_source = _expected_source(change)
        for locale, dest in (("ko", _ko_output(change)), ("ja", _ja_output(change))):
            label = f"{locale} {change.path}"
            try:
                dest = _validated_output_path(dest)
            except OutputPathError as exc:
                failures.append(f"{label}: {exc}")
                continue
            if not dest.exists():
                continue

            raw_original = dest.read_text(encoding="utf-8")
            original = raw_original
            original_issues = verify.verify(
                original, source=expected_source, version=change.version
            )
            normalized = postprocess.postprocess(original, change.version, {})
            normalized_issues = verify.verify(
                normalized, source=expected_source, version=change.version
            )
            if not original_issues:
                if normalized != original and not normalized_issues:
                    writable += 1
                    if apply:
                        atomic_write_text(dest, normalized)
                continue
            if normalized != original and set(normalized_issues) < set(original_issues):
                original = normalized
                original_issues = normalized_issues
                if not original_issues:
                    writable += 1
                    if apply:
                        atomic_write_text(dest, original)
                    continue
            try:
                repaired_labels = repair.restore_blank_markdown_link_labels(
                    expected_source, original
                )
            except repair.RepairError:
                repaired_labels = None
            if repaired_labels and repaired_labels.changed:
                candidate = postprocess.postprocess(
                    repaired_labels.text, change.version, {}
                )
                candidate_issues = verify.verify(
                    candidate, source=expected_source, version=change.version
                )
                if set(candidate_issues) < set(original_issues):
                    original = candidate
                    original_issues = candidate_issues
                    if not original_issues:
                        writable += 1
                        if apply:
                            atomic_write_text(dest, original)
                        continue
            if not {
                "missing original comment",
                "source comment mismatch",
            }.intersection(original_issues):
                if original != raw_original:
                    writable += 1
                    if apply:
                        atomic_write_text(dest, original)
                continue

            annotated, drifts = annotate.annotate(expected_source, original, change.version)
            out = postprocess.postprocess(annotated, change.version, {})
            blocking_drifts = [drift for drift in drifts if drift.op == "delete"]
            if blocking_drifts:
                if "missing original comment" in original_issues:
                    counts: dict[str, int] = {}
                    for drift in blocking_drifts:
                        counts[drift.op] = counts.get(drift.op, 0) + 1
                    failures.append(f"{label}: drift {counts}")
                elif original != raw_original:
                    writable += 1
                    if apply:
                        atomic_write_text(dest, original)
                continue
            issues = verify.verify(
                out, source=expected_source, version=change.version
            )
            if "missing original comment" in issues:
                failures.append(f"{label}: {', '.join(issues)}")
                continue
            if set(issues) < set(original_issues):
                original = out
            if original != raw_original:
                writable += 1
                if apply:
                    atomic_write_text(dest, original)

    return writable, failures


def _fix_preserved_markup_file(
    label: str, dest: Path, expected_source: str, *, version: str, apply: bool
) -> tuple[int, str | None]:
    """로케일 문서 하나의 비번역 서식만 검증하고 선택적으로 원자적 기록."""

    try:
        dest = _validated_output_path(dest)
    except OutputPathError as exc:
        return 0, f"{label}: {exc}"
    if not dest.exists():
        return 0, None

    original = dest.read_text(encoding="utf-8")
    original_issues = verify.verify(
        original, source=expected_source, version=version
    )
    if not original_issues:
        return 0, None
    if not set(original_issues).issubset(PRESERVED_MARKUP_FIXABLE):
        return 0, f"{label}: {', '.join(original_issues)}"

    try:
        result = repair.repair_preserved_markup(expected_source, original)
    except repair.RepairError as exc:
        return 0, f"{label}: {exc}"

    if not result.changed:
        return 0, f"{label}: {', '.join(original_issues)}"

    repaired_issues = verify.verify(
        result.text, source=expected_source, version=version
    )
    if repaired_issues:
        return 0, f"{label}: {', '.join(repaired_issues)}"

    if apply:
        atomic_write_text(dest, result.text)
    return 1, None


def _fix_preserved_markup(
    *, apply: bool = False, version: str | None = None, doc: str | None = None
) -> tuple[int, list[str]]:
    """기존 한국어·일본어 문서의 비번역 서식만 원문 기준으로 복구."""
    writable = 0
    failures: list[str] = []

    for change in _select_changes(migrate_existing=True, version=version, doc=doc):
        expected_source = _expected_source(change)
        for locale, dest in (("ko", _ko_output(change)), ("ja", _ja_output(change))):
            label = f"{locale} {change.path}"
            written, failure = _fix_preserved_markup_file(
                label,
                dest,
                expected_source,
                version=change.version,
                apply=apply,
            )
            writable += written
            if failure:
                failures.append(failure)

    return writable, failures


_VALUE_OPTIONS = {"--doc", "--version"}
_FLAG_OPTIONS = {
    "--annotate-existing",
    "--apply",
    "--check-annotations",
    "--fix-preserved-markup",
}
_MAINTENANCE_OPTIONS = {
    "--annotate-existing",
    "--check-annotations",
    "--fix-preserved-markup",
}


def _parse_args(args: list[str]) -> tuple[set[str], dict[str, str]]:
    """명령행 인수 파싱."""

    flags: set[str] = set()
    values: dict[str, str] = {}
    index = 0

    while index < len(args):
        argument = args[index]
        option, separator, inline_value = argument.partition("=")

        if option == "--migrate-existing":
            raise config.ConfigError(
                "--migrate-existing is unsupported; use --annotate-existing "
                "or --fix-preserved-markup"
            )
        if option in _VALUE_OPTIONS:
            if option in values:
                raise config.ConfigError(f"{option} may only be specified once")
            if separator:
                value = inline_value
            else:
                index += 1
                if index >= len(args) or args[index].startswith("-"):
                    raise config.ConfigError(f"{option} requires a value")
                value = args[index]
            if not value:
                raise config.ConfigError(f"{option} requires a value")
            values[option] = value
        elif argument in _FLAG_OPTIONS:
            if argument in flags:
                raise config.ConfigError(f"{argument} may only be specified once")
            flags.add(argument)
        else:
            raise config.ConfigError(f"unknown argument: {argument}")
        index += 1

    maintenance = flags & _MAINTENANCE_OPTIONS
    if len(maintenance) > 1:
        raise config.ConfigError("maintenance modes are mutually exclusive")
    if "--apply" in flags and not maintenance.intersection(
        {"--annotate-existing", "--fix-preserved-markup"}
    ):
        raise config.ConfigError(
            "--apply requires --annotate-existing or --fix-preserved-markup"
        )
    return flags, values


def main() -> int:
    """명령줄 진입점 실행."""

    try:
        flags, values = _parse_args(sys.argv[1:])
    except config.ConfigError as exc:
        print(f"configuration failed: {exc}", file=sys.stderr)
        return 1

    check_annotations = "--check-annotations" in flags
    annotate_existing = "--annotate-existing" in flags
    fix_preserved_markup = "--fix-preserved-markup" in flags
    apply_annotations = "--apply" in flags
    version = values.get("--version")
    doc = values.get("--doc")
    if doc:
        if version is None:
            print(
                "configuration failed: --doc requires --version",
                file=sys.stderr,
            )
            return 1
        if not doc.endswith(".md"):
            doc = f"{doc}.md"
        try:
            doc = upstream.normalize_document_selector(doc)
        except ValueError as exc:
            print(f"configuration failed: {exc}", file=sys.stderr)
            return 1

    if annotate_existing:
        try:
            written, failures = _annotate_existing(
                apply=apply_annotations, version=version, doc=doc
            )
        except SourcePathError as exc:
            print(f"source selection failed: {exc}", file=sys.stderr)
            return 1
        for failure in failures:
            print(f"annotate failed: {failure}", file=sys.stderr)
        if failures:
            print(f"{len(failures)} annotation migration(s) failed", file=sys.stderr)
            return 1
        action = "written" if apply_annotations else "would write"
        print(f"existing translation annotations {action}: {written}")
        return 0

    if fix_preserved_markup:
        try:
            written, failures = _fix_preserved_markup(
                apply=apply_annotations, version=version, doc=doc
            )
        except SourcePathError as exc:
            print(f"source selection failed: {exc}", file=sys.stderr)
            return 1
        action = "written" if apply_annotations else "would write"
        print(f"existing preserved markup fixes {action}: {written}")
        for failure in failures:
            print(f"preserved markup fix skipped: {failure}", file=sys.stderr)
        if failures:
            print(f"{len(failures)} preserved markup fix(es) skipped", file=sys.stderr)
            return 1
        return 0

    if check_annotations:
        try:
            failures = _check_existing_annotations(version=version, doc=doc)
        except SourcePathError as exc:
            print(f"source selection failed: {exc}", file=sys.stderr)
            return 1
        for failure in failures:
            print(f"verify failed: {failure}", file=sys.stderr)
        if failures:
            print(f"{len(failures)} annotation check(s) failed", file=sys.stderr)
            return 1
        print("existing translation annotations verified")
        return 0

    if (
        os.environ.get("TRANSLATION_CANDIDATE") != "1"
        and os.environ.get("TRANSLATION_REPLAY") != "1"
    ):
        print(
            "configuration failed: translation sync requires an isolated candidate",
            file=sys.stderr,
        )
        return 1

    # 1. 설정 확인 (실패 시 원문 캐시를 변경하지 않음)
    try:
        cfg = config.load_config()
    except config.ConfigError as exc:
        print(f"configuration failed: {exc}", file=sys.stderr)
        return 1

    try:
        prompts = _load_prompts()
    except prompt.PromptError as exc:
        print(f"prompt loading failed: {exc}", file=sys.stderr)
        return 1
    try:
        run_deadline = config.required_run_deadline(cfg)
    except config.ConfigError as exc:
        print(f"configuration failed: {exc}", file=sys.stderr)
        return 1

    # 2. 원문 동기화 (i18n/en 적재)
    if upstream.main(version=version, doc=doc) != 0:
        print("upstream sync failed", file=sys.stderr)
        return 1

    # 3. 변경 감지
    try:
        changes = _select_changes(version=version, doc=doc)
    except (SourcePathError, diff.SourceDiffError) as exc:
        print(f"source diff failed: {exc}", file=sys.stderr)
        return 1
    if not changes:
        sidebar_failures = _sync_sidebars(_sidebar_versions([], version))
        for failure in sidebar_failures:
            print(f"sidebar sync failed: {failure}", file=sys.stderr)
        if sidebar_failures:
            print(f"{len(sidebar_failures)} sidebar sync failure(s)", file=sys.stderr)
            return 1
        print("no source changes to translate")
        return 0

    state_issues = _validate_file_states(changes)
    if state_issues:
        for issue in state_issues:
            print(f"file state failed: {issue}", file=sys.stderr)
        return 1

    prepared_targets, preflight_issues = _preflight_all_translation_targets(
        changes,
        cfg,
        prompts,
    )
    if preflight_issues:
        for issue in preflight_issues:
            print(f"translation preflight failed: {issue}", file=sys.stderr)
        return 1

    # 4. 변경 문서: ko·ja 각각 전처리 → 번역 → 후처리 → 검증 → 출력
    for change in changes:
        if change.status == "D":
            issues = _delete_outputs(change)
            if issues:
                failure = f"{change.path}: {', '.join(issues)}"
                print(f"delete failed: {failure}", file=sys.stderr, flush=True)
                return 1
            continue

        for locale, locale_prompt, dest in (
            ("ko", prompts["ko"], _ko_output(change)),
            ("ja", prompts["ja"], _ja_output(change)),
        ):
            print(f"translating: {locale} {change.path}", file=sys.stderr, flush=True)
            issues = _translate_one(
                change,
                cfg,
                locale_prompt,
                dest,
                locale=locale,
                deadline=run_deadline,
                prepared_target=prepared_targets[(change.path, locale)],
            )
            if issues:
                failure = f"{locale} {change.path}: {', '.join(issues)}"
                print(
                    f"verify failed: {locale} {change.path}: {issues}",
                    file=sys.stderr,
                    flush=True,
                )
                print("stopping after first verification failure", file=sys.stderr, flush=True)
                return 1

    sidebar_failures = _sync_sidebars(_sidebar_versions(changes, version))
    for failure in sidebar_failures:
        print(f"sidebar sync failed: {failure}", file=sys.stderr)
    if sidebar_failures:
        print(f"{len(sidebar_failures)} sidebar sync failure(s)", file=sys.stderr)
        return 1

    print(f"translated {len(changes)} doc(s) into ko, ja")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
