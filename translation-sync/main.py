#!/usr/bin/env python3
"""번역 동기화 엔트리포인트.

translation-sync/docs/00-workflow-summary.md의 단계 순서를 따른다:
설정·프롬프트 확인 → 원문 동기화 → 변경 감지 → 전처리(01) → 번역(02) → 후처리(03) → 검증·출력(04) → 사이드바 갱신(06).

출력 로케일: ko(versioned_docs), ja(i18n/ja).
프롬프트: ko=prompt.md, ja=prompt_jp.md.
실행: uv run --locked python main.py
"""
from __future__ import annotations

import sys
from pathlib import Path

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
from sync.common.files import atomic_write_text, unlink_file

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
# Fresh provider responses already compare fenced code contents in the response
# contract. A code mismatch found only after patching is therefore a plan/context
# failure that retranslating the same segment cannot repair.
SEGMENT_RETRYABLE_VERIFICATION_ISSUES = {
    "admonition body outside blockquote",
    "anchor mismatch",
    "duplicate admonition marker",
    "heading mismatch",
    "heading text mismatch",
    "inline code mismatch",
    "link target mismatch",
    "link label mismatch",
    "link pair mismatch",
    "list marker mismatch",
    "missing original comment",
}
MAX_SEGMENT_VERIFICATION_ATTEMPTS = translate.MAX_COMPLETED_RESPONSE_ATTEMPTS


class OutputPathError(ValueError):
    """A translation output path is not safe to mutate."""


class SourcePathError(ValueError):
    """An English source path is not safe to read."""


def _validated_output_path(path: Path) -> Path:
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
    return REPO_ROOT / "versioned_docs" / f"version-{change.version}" / change.name


def _ja_output(change: diff.SourceChange) -> Path:
    return (
        REPO_ROOT
        / "i18n"
        / "ja"
        / "docusaurus-plugin-content-docs"
        / f"version-{change.version}"
        / change.name
    )


def _delete_outputs(change: diff.SourceChange) -> list[str]:
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


def _sidebar_versions(changes: list[diff.SourceChange], version: str | None) -> list[str]:
    if version:
        return [version]
    versions = [change.version for change in changes]
    versions.append("master")
    return list(dict.fromkeys(versions))


def _load_prompts() -> dict[str, str]:
    return {
        "ko": prompt.load_prompt(PROMPT_PATH),
        "ja": prompt.load_prompt(JA_PROMPT_PATH),
    }


def _matches_filters(
    change: diff.SourceChange, *, version: str | None, doc: str | None
) -> bool:
    if version and change.version != version:
        return False
    if doc:
        name = doc if doc.endswith(".md") else f"{doc}.md"
        if change.name != name:
            return False
    return True


def _select_changes(
    *, migrate_existing: bool = False, version: str | None = None, doc: str | None = None
) -> list[diff.SourceChange]:
    if not migrate_existing:
        return [
            change
            for change in diff.changed_sources()
            if _matches_filters(change, version=version, doc=doc)
        ]

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
        for path in sorted(version_root.iterdir()):
            if path.suffix != ".md":
                continue
            if path.is_symlink() or not path.is_file():
                raise SourcePathError(f"unsafe English source path: {path}")
            change = diff.SourceChange(
                path=str(path.relative_to(repo_root)),
                status="M",
            )
            if _matches_filters(change, version=version, doc=doc):
                changes.append(change)
    return changes


def _translation_request(
    source: str,
    existing_translation: str | None,
    *,
    diff_text: str | None = None,
    verification_feedback: str | None = None,
) -> translate.TranslationRequest:
    return translate.TranslationRequest(
        source=source,
        existing_translation=existing_translation,
        diff_text=diff_text,
        verification_feedback=verification_feedback,
    )


def _verification_feedback(issues: list[str]) -> str:
    return translate.verification_feedback(issues)


def _contract_issues(
    translated: str,
    source: str,
    cfg: config.Config,
    change: diff.SourceChange,
    locale: str | None,
) -> list[str]:
    if cfg.provider == "identity":
        return []
    return response_contract.verify(
        translated,
        source,
        locale=locale,
        allow_source_echo=change.name == "license.md",
    )


def _translate_added_document(
    change: diff.SourceChange,
    cfg: config.Config,
    prompt: str,
    dest: Path,
    *,
    locale: str | None = None,
) -> list[str]:
    try:
        dest = _validated_output_path(dest)
    except OutputPathError as exc:
        return [str(exc)]

    src = (REPO_ROOT / change.path).read_text(encoding="utf-8")
    pre = preprocess.preprocess(src)
    existing = dest.read_text(encoding="utf-8") if dest.exists() else None
    try:
        source_chunks = translate.split_chunks(pre.text)
        translated_chunks: list[str] = []
        for source_chunk in source_chunks:
            feedback: str | None = None
            contract_issues: list[str] = []
            for _attempt in range(MAX_SEGMENT_VERIFICATION_ATTEMPTS):
                translated_chunk = translate.translate_request(
                    _translation_request(
                        source_chunk,
                        existing,
                        verification_feedback=feedback,
                    ),
                    cfg,
                    prompt,
                )
                contract_issues = _contract_issues(
                    translated_chunk, source_chunk, cfg, change, locale
                )
                if not contract_issues:
                    translated_chunks.append(translated_chunk)
                    break
                feedback = _verification_feedback(contract_issues)
            else:
                return [
                    "provider response contract failed: "
                    + ", ".join(contract_issues)
                ]
        translated = translate.join_chunk_outputs(source_chunks, translated_chunks)
    except translate.IncompleteTranslation as exc:
        return [f"incomplete translation: {exc}"]
    expected_source = postprocess.postprocess(pre.text, change.version, pre.placeholders)
    out = postprocess.postprocess(translated, change.version, pre.placeholders)
    if cfg.provider == "identity":
        out = _repair_segment_translation(expected_source, out, change.version)

    issues = verify.verify(
        out,
        source=expected_source,
        version=change.version,
        allow_source_echo=cfg.provider == "identity",
    )
    if issues:
        return issues

    dest.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(dest, out)
    return []


def _translate_block_change(
    change: diff.SourceChange,
    block_change: patch_utils.BlockChange,
    cfg: config.Config,
    prompt: str,
    existing: str,
    *,
    locale: str | None = None,
) -> str:
    source = patch_utils.source_text(block_change)
    pre = preprocess.preprocess(source)
    expected_source = postprocess.postprocess(pre.text, change.version, pre.placeholders)
    existing_context = patch_utils.existing_context(existing, block_change)
    diff_text = patch_utils.diff_text(block_change)
    feedback: str | None = None
    last_out = ""
    contract_issues: list[str] = []

    for _attempt in range(MAX_SEGMENT_VERIFICATION_ATTEMPTS):
        translated = translate.translate_request(
            _translation_request(
                pre.text,
                existing_context,
                diff_text=diff_text,
                verification_feedback=feedback,
            ),
            cfg,
            prompt,
        )
        contract_issues = _contract_issues(translated, pre.text, cfg, change, locale)
        if contract_issues:
            feedback = _verification_feedback(contract_issues)
            continue

        out = postprocess.postprocess(translated, change.version, pre.placeholders)
        last_out = _repair_segment_translation(expected_source, out, change.version)
        issues = verify.verify(
            last_out,
            source=expected_source,
            version=change.version,
            allow_source_echo=cfg.provider == "identity",
        )
        if not issues:
            return last_out
        if not SEGMENT_RETRYABLE_VERIFICATION_ISSUES.intersection(issues):
            return last_out
        feedback = _verification_feedback(issues)

    if contract_issues:
        raise translate.IncompleteTranslation(
            "provider response contract failed: " + ", ".join(contract_issues)
        )
    return last_out


def _render_provider_free_change(
    change: diff.SourceChange, block_change: patch_utils.BlockChange
) -> str:
    source = patch_utils.source_text(block_change)
    pre = preprocess.preprocess(source)
    expected_source = postprocess.postprocess(
        pre.text, change.version, pre.placeholders
    )
    return _repair_segment_translation(
        expected_source,
        expected_source,
        change.version,
    )


def _repair_segment_translation(source: str, translated: str, version: str) -> str:
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


def _repair_blockquote_segment(source: str, translated: str) -> str:
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
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def _normalize_plan_source(source: str, version: str) -> str:
    pre = preprocess.preprocess(source)
    return postprocess.postprocess(pre.text, version, pre.placeholders)


def _translate_one(
    change: diff.SourceChange,
    cfg: config.Config,
    prompt: str,
    dest: Path,
    *,
    locale: str | None = None,
) -> list[str]:
    """원문 한 건을 한 로케일로 번역·후처리·검증해 dest에 기록한다. 위반 목록 반환."""
    if change.status == "A":
        return _translate_added_document(change, cfg, prompt, dest, locale=locale)
    try:
        dest = _validated_output_path(dest)
    except OutputPathError as exc:
        return [str(exc)]
    if not dest.exists():
        return ["missing existing translation for partial sync"]
    if not change.hunks:
        return ["missing diff hunks for partial sync"]

    src = (REPO_ROOT / change.path).read_text(encoding="utf-8")
    pre = preprocess.preprocess(src)
    expected_source = postprocess.postprocess(pre.text, change.version, pre.placeholders)
    existing = dest.read_text(encoding="utf-8")

    translated_blocks: list[str] = []
    try:
        plan = patch_utils.build_plan(
            change.hunks,
            src,
            normalize_source=lambda source: _normalize_plan_source(
                source,
                change.version,
            ),
        )
        state = patch_utils.plan_state(existing, plan)
        if (
            state is patch_utils.PlanState.UNGUARDED
            and plan.old_code_blocks != plan.new_code_blocks
            and not verify.verify(
                existing,
                source=expected_source,
                version=change.version,
                allow_source_echo=cfg.provider == "identity",
            )
        ):
            return []
        for block_change in plan.changes:
            if block_change.needs_translation:
                if block_change.provider_free:
                    translated_blocks.append(
                        _render_provider_free_change(change, block_change)
                    )
                elif state is patch_utils.PlanState.TARGET and (
                    block_change.old_anchors or block_change.new_anchors
                ):
                    translated_blocks.append(
                        patch_utils.existing_context(existing, block_change)
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
                        )
                    )
        out = patch_utils.apply_plan(existing, plan, translated_blocks)
    except patch_utils.PatchError as exc:
        return [f"partial patch failed: {exc}"]
    except translate.IncompleteTranslation as exc:
        return [f"partial translation failed: {exc}"]

    # A partial patch preserves unaffected locale context. Normalize that context
    # together with the patched blocks before the full-document verifier runs:
    # legacy admonitions and their source annotations otherwise remain stale.
    out = _repair_segment_translation(expected_source, out, change.version)

    issues = verify.verify(
        out,
        source=expected_source,
        version=change.version,
        allow_source_echo=cfg.provider == "identity",
    )
    if issues:
        return issues

    dest.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(dest, out)
    return []


def _expected_source(change: diff.SourceChange) -> str:
    """검증 기준 원문: raw source에 전처리/후처리를 적용한 번역 파이프라인 기준본."""
    src = (REPO_ROOT / change.path).read_text(encoding="utf-8")
    pre = preprocess.preprocess(src)
    return postprocess.postprocess(pre.text, change.version, pre.placeholders)


def _check_existing_annotations(
    *, version: str | None = None, doc: str | None = None
) -> list[str]:
    """기존 ko/ja 문서가 영어 원문 주석 병기 형식인지 검증한다."""
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
    failures: list[str] = []
    for result in sidebar.sync_versions(versions, write=True, repo_root=REPO_ROOT):
        for issue in result.issues:
            failures.append(f"{result.version}: {issue}")
    return failures


def _annotate_existing(
    *, apply: bool = False, version: str | None = None, doc: str | None = None
) -> tuple[int, list[str]]:
    """기존 ko/ja 문서에 영어 원문 주석을 병기한다. 안전한 파일만 기록한다."""
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
    """기존 ko/ja 문서의 비번역 markup만 원문 기준으로 복구한다."""
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
    "--fail-fast",
    "--fix-preserved-markup",
}
_MAINTENANCE_OPTIONS = {
    "--annotate-existing",
    "--check-annotations",
    "--fix-preserved-markup",
}


def _parse_args(args: list[str]) -> tuple[set[str], dict[str, str]]:
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
    if maintenance and "--fail-fast" in flags:
        raise config.ConfigError(
            "--fail-fast is only valid for translation sync"
        )

    return flags, values


def main() -> int:
    try:
        flags, values = _parse_args(sys.argv[1:])
    except config.ConfigError as exc:
        print(f"configuration failed: {exc}", file=sys.stderr)
        return 2

    check_annotations = "--check-annotations" in flags
    annotate_existing = "--annotate-existing" in flags
    fix_preserved_markup = "--fix-preserved-markup" in flags
    fail_fast = "--fail-fast" in flags
    apply_annotations = "--apply" in flags
    version = values.get("--version")
    doc = values.get("--doc")
    if doc and not doc.endswith(".md"):
        doc = f"{doc}.md"

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

    # 1. 설정 확인 (실패 시 원문 캐시를 변경하지 않음)
    try:
        cfg = config.load_config()
    except config.ConfigError as exc:
        print(f"configuration failed: {exc}", file=sys.stderr)
        return 2

    try:
        prompts = _load_prompts()
    except prompt.PromptError as exc:
        print(f"prompt loading failed: {exc}", file=sys.stderr)
        return 2

    # 2. 원문 동기화 (i18n/en 적재)
    if upstream.main(version=version, doc=doc) != 0:
        print("upstream sync failed", file=sys.stderr)
        return 1

    # 3. 변경 감지
    changes = _select_changes(version=version, doc=doc)
    if not changes:
        sidebar_failures = _sync_sidebars(_sidebar_versions([], version))
        for failure in sidebar_failures:
            print(f"sidebar sync failed: {failure}", file=sys.stderr)
        if sidebar_failures:
            print(f"{len(sidebar_failures)} sidebar sync failure(s)", file=sys.stderr)
            return 1
        print("no source changes to translate")
        return 0

    # 4. 변경 문서: ko·ja 각각 전처리 → 번역 → 후처리 → 검증 → 출력
    failures: list[str] = []
    for change in changes:
        if change.status == "D":
            issues = _delete_outputs(change)
            if issues:
                failure = f"{change.path}: {', '.join(issues)}"
                failures.append(failure)
                print(f"delete failed: {failure}", file=sys.stderr, flush=True)
                if fail_fast:
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
            )
            if issues:
                failure = f"{locale} {change.path}: {', '.join(issues)}"
                failures.append(failure)
                print(
                    f"verify failed: {locale} {change.path}: {issues}",
                    file=sys.stderr,
                    flush=True,
                )
                if fail_fast:
                    print("stopping after first verification failure", file=sys.stderr, flush=True)
                    return 1

    if failures:
        print(f"{len(failures)} target(s) failed verification", file=sys.stderr)
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
