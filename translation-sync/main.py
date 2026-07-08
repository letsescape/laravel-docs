#!/usr/bin/env python3
"""번역 동기화 엔트리포인트.

translation-sync/docs/00-workflow-summary.md의 단계 순서를 따른다:
원문 동기화 → 변경 감지 → 전처리(01) → 번역(02) → 후처리(03) → 사이드바 갱신(06) → 검증(04) → 출력.

출력 로케일: ko(versioned_docs), ja(i18n/ja).
프롬프트: ko=prompt.md, ja=prompt_jp.md.
실행: uv run python main.py
"""
from __future__ import annotations

import sys
from dataclasses import replace
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
    sidebar,
    translate,
    upstream,
    verify,
)

SYNC_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SYNC_ROOT.parent
PROMPT_PATH = SYNC_ROOT / "prompt.md"
JA_PROMPT_PATH = SYNC_ROOT / "prompt_jp.md"
PRESERVED_MARKUP_FIXABLE = {
    "link target mismatch",
    "link label mismatch",
    "link pair mismatch",
    "heading mismatch",
    "heading text mismatch",
}
SEGMENT_RETRYABLE_VERIFICATION_ISSUES = {
    "link target mismatch",
    "link label mismatch",
    "link pair mismatch",
}
MAX_SEGMENT_VERIFICATION_ATTEMPTS = 2


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


def _delete_outputs(change: diff.SourceChange) -> None:
    for path in (_ko_output(change), _ja_output(change)):
        if path.exists():
            path.unlink()


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

    en_root = REPO_ROOT / "i18n" / "en" / "docusaurus-plugin-content-docs"
    changes: list[diff.SourceChange] = []
    for path in sorted(en_root.glob("version-*/*.md")):
        change = diff.SourceChange(path=str(path.relative_to(REPO_ROOT)), status="M")
        if _matches_filters(change, version=version, doc=doc):
            changes.append(change)
    return changes


def _translation_input(
    source: str,
    existing_translation: str | None,
    *,
    diff_text: str | None = None,
    verification_feedback: str | None = None,
) -> str:
    existing = existing_translation.rstrip() if existing_translation else "(none)"
    diff_section = f"## English Diff\n\n```diff\n{diff_text.rstrip()}\n```\n\n" if diff_text else ""
    feedback_section = (
        "## Previous Output Verification Failure\n\n"
        f"{verification_feedback.rstrip()}\n\n"
        if verification_feedback
        else ""
    )
    return (
        "# Translation Sync Input\n\n"
        f"{diff_section}"
        "## English Source\n\n"
        f"{source.rstrip()}\n\n"
        "## Existing Translation Context\n\n"
        f"{existing}\n\n"
        f"{feedback_section}"
        "## Output\n\n"
        "Return only the translated Markdown block(s) for the English Source."
    )


def _verification_feedback(issues: list[str]) -> str:
    return (
        f"The previous output failed verification: {', '.join(issues)}.\n"
        "Translate the English Source again. Preserve every Markdown link label "
        "and target, heading, anchor, inline code span, fenced code block, and "
        "list marker exactly as it appears in the English Source."
    )


def _translate_added_document(
    change: diff.SourceChange, cfg: config.Config, prompt: str, dest: Path
) -> list[str]:
    src = (REPO_ROOT / change.path).read_text(encoding="utf-8")
    pre = preprocess.preprocess(src)
    existing = dest.read_text(encoding="utf-8") if dest.exists() else None
    try:
        translated = "".join(
            translate.translate_text(
                _translation_input(source_chunk, existing),
                cfg,
                prompt,
                split=False,
            )
            for source_chunk in translate.split_chunks(pre.text)
        )
    except translate.IncompleteTranslation as exc:
        return [f"incomplete translation: {exc}"]
    out = postprocess.postprocess(translated, change.version, pre.placeholders)
    expected_source = postprocess.postprocess(pre.text, change.version, pre.placeholders)

    issues = verify.verify(out, source=expected_source)
    if issues:
        return issues

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    return []


def _translate_segment(
    change: diff.SourceChange,
    segment: patch_utils.Segment,
    cfg: config.Config,
    prompt: str,
    existing: str,
) -> str:
    source = patch_utils.source_text(segment)
    pre = preprocess.preprocess(source)
    expected_source = postprocess.postprocess(pre.text, change.version, pre.placeholders)
    existing_context = patch_utils.existing_context(existing, segment)
    diff_text = patch_utils.diff_text(segment)
    feedback: str | None = None
    last_out = ""

    for _attempt in range(MAX_SEGMENT_VERIFICATION_ATTEMPTS):
        translated = translate.translate_text(
            _translation_input(
                pre.text,
                existing_context,
                diff_text=diff_text,
                verification_feedback=feedback,
            ),
            cfg,
            prompt,
            split=False,
        )
        out = postprocess.postprocess(translated, change.version, pre.placeholders)
        last_out = _repair_segment_translation(expected_source, out, change.version)
        issues = verify.verify(last_out, source=expected_source)
        if not issues:
            return last_out
        if not SEGMENT_RETRYABLE_VERIFICATION_ISSUES.intersection(issues):
            return last_out
        feedback = _verification_feedback(issues)

    return last_out


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

    best = min(candidates, key=lambda candidate: len(verify.verify(candidate, source=source)))
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


def _normalize_comment_anchor(text: str | None, version: str) -> str | None:
    if text is None:
        return None
    normalized = postprocess.postprocess(text, version, {})
    return " ".join(normalized.split())


def _normalize_segment_anchors(
    segment: patch_utils.Segment, version: str
) -> patch_utils.Segment:
    return replace(
        segment,
        old_lines=tuple(
            _normalize_comment_anchor(line, version) or "" for line in segment.old_lines
        ),
        before_context=_normalize_comment_anchor(segment.before_context, version),
        after_context=_normalize_comment_anchor(segment.after_context, version),
    )


def _translate_one(
    change: diff.SourceChange, cfg: config.Config, prompt: str, dest: Path
) -> list[str]:
    """원문 한 건을 한 로케일로 번역·후처리·검증해 dest에 기록한다. 위반 목록 반환."""
    if change.status == "A":
        return _translate_added_document(change, cfg, prompt, dest)
    if not dest.exists():
        return ["missing existing translation for partial sync"]
    if not change.hunks:
        return ["missing diff hunks for partial sync"]

    src = (REPO_ROOT / change.path).read_text(encoding="utf-8")
    pre = preprocess.preprocess(src)
    expected_source = postprocess.postprocess(pre.text, change.version, pre.placeholders)
    existing = dest.read_text(encoding="utf-8")
    segments = [
        _normalize_segment_anchors(segment, change.version)
        for segment in patch_utils.segments_from_hunks(change.hunks, src)
    ]

    translated_blocks: list[str] = []
    try:
        for segment in segments:
            if segment.needs_translation:
                translated_blocks.append(
                    _translate_segment(change, segment, cfg, prompt, existing)
                )
        out = patch_utils.apply_segments(existing, segments, translated_blocks)
    except patch_utils.PatchError as exc:
        return [f"partial patch failed: {exc}"]
    except translate.IncompleteTranslation as exc:
        return [f"partial translation failed: {exc}"]

    issues = verify.verify(out, source=expected_source)
    if issues:
        return issues

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
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

            issues = verify.verify(dest.read_text(encoding="utf-8"), source=expected_source)
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
            if not dest.exists():
                continue

            original = dest.read_text(encoding="utf-8")
            original_issues = verify.verify(original, source=expected_source)
            if not original_issues:
                continue
            if "missing original comment" not in original_issues:
                continue

            annotated, drifts = annotate.annotate(expected_source, original, change.version)
            out = postprocess.postprocess(annotated, change.version, {})
            blocking_drifts = [drift for drift in drifts if drift.op == "delete"]
            if blocking_drifts:
                counts: dict[str, int] = {}
                for drift in blocking_drifts:
                    counts[drift.op] = counts.get(drift.op, 0) + 1
                failures.append(f"{label}: drift {counts}")
                continue
            issues = verify.verify(out, source=expected_source)
            if "missing original comment" in issues:
                failures.append(f"{label}: {', '.join(issues)}")
                continue

            writable += 1
            if apply:
                dest.write_text(out, encoding="utf-8")

    return writable, failures


def _fix_preserved_markup_file(
    label: str, dest: Path, expected_source: str, *, apply: bool
) -> tuple[int, str | None]:
    if not dest.exists():
        return 0, None

    original = dest.read_text(encoding="utf-8")
    original_issues = verify.verify(original, source=expected_source)
    if not original_issues:
        return 0, None
    if not set(original_issues).issubset(PRESERVED_MARKUP_FIXABLE):
        return 0, f"{label}: {', '.join(original_issues)}"

    try:
        result = repair.repair_preserved_markup(expected_source, original)
    except repair.RepairError as exc:
        return 0, f"{label}: {exc}"

    if not result.changed:
        return 0, None

    repaired_issues = verify.verify(result.text, source=expected_source)
    if repaired_issues:
        return 0, f"{label}: {', '.join(repaired_issues)}"

    if apply:
        dest.write_text(result.text, encoding="utf-8")
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
                label, dest, expected_source, apply=apply
            )
            writable += written
            if failure:
                failures.append(failure)

    return writable, failures


def _arg_value(args: list[str], flag: str) -> str | None:
    if flag not in args:
        return None
    index = args.index(flag)
    if index + 1 >= len(args) or args[index + 1].startswith("--"):
        raise config.ConfigError(f"{flag} requires a value")
    return args[index + 1]


def main() -> int:
    args = sys.argv[1:]
    migrate_existing = "--migrate-existing" in args
    check_annotations = "--check-annotations" in args
    annotate_existing = "--annotate-existing" in args
    fix_preserved_markup = "--fix-preserved-markup" in args
    require_filters = "--require-filters" in args
    fail_fast = "--fail-fast" in args
    apply_annotations = "--apply" in args
    version = _arg_value(args, "--version")
    doc = _arg_value(args, "--doc")

    if require_filters and (not version or not doc):
        print(
            "--require-filters requires both --version and --doc",
            file=sys.stderr,
        )
        return 2

    if annotate_existing:
        written, failures = _annotate_existing(
            apply=apply_annotations, version=version, doc=doc
        )
        for failure in failures:
            print(f"annotate failed: {failure}", file=sys.stderr)
        if failures:
            print(f"{len(failures)} annotation migration(s) failed", file=sys.stderr)
            return 1
        action = "written" if apply_annotations else "would write"
        print(f"existing translation annotations {action}: {written}")
        return 0

    if fix_preserved_markup:
        written, failures = _fix_preserved_markup(
            apply=apply_annotations, version=version, doc=doc
        )
        action = "written" if apply_annotations else "would write"
        print(f"existing preserved markup fixes {action}: {written}")
        for failure in failures:
            print(f"preserved markup fix skipped: {failure}", file=sys.stderr)
        if failures:
            print(f"{len(failures)} preserved markup fix(es) skipped", file=sys.stderr)
            return 1
        return 0

    if check_annotations:
        failures = _check_existing_annotations(version=version, doc=doc)
        for failure in failures:
            print(f"verify failed: {failure}", file=sys.stderr)
        if failures:
            print(f"{len(failures)} annotation check(s) failed", file=sys.stderr)
            return 1
        print("existing translation annotations verified")
        return 0

    # 1. 원문 동기화 (i18n/en 적재)
    upstream.main()

    # 2. 변경 감지
    changes = _select_changes(migrate_existing=migrate_existing, version=version, doc=doc)
    if not changes:
        sidebar_failures = _sync_sidebars(_sidebar_versions([], version))
        for failure in sidebar_failures:
            print(f"sidebar sync failed: {failure}", file=sys.stderr)
        if sidebar_failures:
            print(f"{len(sidebar_failures)} sidebar sync failure(s)", file=sys.stderr)
            return 1
        print("no source changes to translate")
        return 0

    # 3. 설정 확인 (실패 시 중단 — docs/01)
    cfg = config.load_config()
    prompts = _load_prompts()

    # 4. 변경 문서: ko·ja 각각 전처리 → 번역 → 후처리 → 검증 → 출력
    failures: list[str] = []
    for change in changes:
        if change.status == "D":
            _delete_outputs(change)
            continue

        for locale, locale_prompt, dest in (
            ("ko", prompts["ko"], _ko_output(change)),
            ("ja", prompts["ja"], _ja_output(change)),
        ):
            print(f"translating: {locale} {change.path}", file=sys.stderr, flush=True)
            issues = _translate_one(change, cfg, locale_prompt, dest)
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
