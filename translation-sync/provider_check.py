#!/usr/bin/env python3
"""Run a small live-provider translation contract check without editing docs."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

from sync import config, prompt, response_contract, translate, verify

SYNC_ROOT = Path(__file__).resolve().parent
PROMPTS = {
    "ko": SYNC_ROOT / "prompt.md",
    "ja": SYNC_ROOT / "prompt_jp.md",
}
CHECK_SOURCE = (
    '<a name="cache-locks"></a>\n'
    "## Cache Locks\n\n"
    "Use the [atomic locks](#atomic-locks) API with `Cache::lock`.\n\n"
    "```php\n"
    "$lock = Cache::lock('foo', 10);\n"
    "```\n"
)
CHECK_DIFF = (
    '+ <a name="cache-locks"></a>\n'
    "+ ## Cache Locks\n"
    "+\n"
    "+ Use the [atomic locks](#atomic-locks) API with `Cache::lock`.\n"
    "+\n"
    "+ ```php\n"
    "+ $lock = Cache::lock('foo', 10);\n"
    "+ ```"
)
_TARGET_TEXT = {
    "ko": re.compile(r"[가-힣]"),
    "ja": re.compile(r"[ぁ-ゖァ-ヺ]"),
}
_OTHER_TARGET_TEXT = {
    "ko": re.compile(r"[ぁ-ゖァ-ヺ\u3400-\u9fff]"),
    "ja": re.compile(r"[가-힣]"),
}

_FIXTURE_ANCHOR = '<a name="cache-locks"></a>'
_FIXTURE_HEADING_COMMENT = "<!-- ## Cache Locks -->"
_FIXTURE_HEADING = "## Cache Locks"
_FIXTURE_PARAGRAPH_COMMENT = (
    "<!-- Use the [atomic locks](#atomic-locks) API with `Cache::lock`. -->"
)
_FIXTURE_SOURCE_PARAGRAPH = (
    "Use the [atomic locks](#atomic-locks) API with `Cache::lock`."
)
_FIXTURE_CODE = ("```php", "$lock = Cache::lock('foo', 10);", "```")
_FIXTURE_PRESERVED_TEXT = (
    "[atomic locks](#atomic-locks)",
    "`Cache::lock`",
    "API",
)
_ASCII_LETTER = re.compile(r"[A-Za-z]")
_STRUCTURAL_PARAGRAPH_START = re.compile(
    r"^(?:[-*+]\s|\d+[.)]\s|>|\||<|#{1,6}\s|`{3}|~{3})"
)


def _skip_blank(lines: list[str], index: int) -> int:
    while index < len(lines) and not lines[index].strip():
        index += 1
    return index


def _has_expected_fixture_shape(locale: str, translated: str) -> bool:
    lines = translated.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    index = _skip_blank(lines, 0)
    if index >= len(lines) or lines[index] != _FIXTURE_ANCHOR:
        return False

    index = _skip_blank(lines, index + 1)
    if index >= len(lines) or lines[index] != _FIXTURE_HEADING_COMMENT:
        return False
    if index + 1 >= len(lines) or lines[index + 1] != _FIXTURE_HEADING:
        return False

    index = _skip_blank(lines, index + 2)
    if index >= len(lines) or lines[index] != _FIXTURE_PARAGRAPH_COMMENT:
        return False
    index += 1
    if index >= len(lines) or not lines[index].strip():
        return False
    paragraph = lines[index].lstrip()
    if (
        _STRUCTURAL_PARAGRAPH_START.match(paragraph)
        or _FIXTURE_SOURCE_PARAGRAPH in paragraph
    ):
        return False
    translated_prose = paragraph
    for preserved in _FIXTURE_PRESERVED_TEXT:
        translated_prose = translated_prose.replace(preserved, "")
    if (
        _ASCII_LETTER.search(translated_prose)
        or _OTHER_TARGET_TEXT[locale].search(translated_prose)
    ):
        return False
    index += 1
    if index < len(lines) and lines[index].strip():
        return False

    index = _skip_blank(lines, index)
    if tuple(lines[index : index + len(_FIXTURE_CODE)]) != _FIXTURE_CODE:
        return False
    index = _skip_blank(lines, index + len(_FIXTURE_CODE))
    return index == len(lines)


def evaluate_output(locale: str, translated: str) -> list[str]:
    issues: list[str] = []
    if not translated.lstrip().startswith('<a name="cache-locks"></a>'):
        issues.append("unexpected provider response prefix")
    if len(_TARGET_TEXT[locale].findall(translated)) < 3:
        issues.append(f"missing {locale} target-language text")
    if not _has_expected_fixture_shape(locale, translated):
        issues.append("unexpected provider response shape")
    issues.extend(response_contract.verify(translated, CHECK_SOURCE, locale=locale))
    issues.extend(verify.verify(translated, source=CHECK_SOURCE, version="13.x"))
    return list(dict.fromkeys(issues))


def _locales(value: str) -> tuple[str, ...]:
    return ("ko", "ja") if value == "all" else (value,)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Call the configured live provider with a fixed translation fixture."
    )
    parser.add_argument("--locale", choices=("all", "ko", "ja"), default="all")
    args = parser.parse_args()

    try:
        cfg = config.load_config()
    except config.ConfigError as exc:
        print(f"provider check configuration failed: {exc}", file=sys.stderr)
        return 2

    failed = False
    for locale in _locales(args.locale):
        try:
            locale_prompt = prompt.load_prompt(PROMPTS[locale])
        except (prompt.PromptError, OSError) as exc:
            print(f"provider check configuration failed: {exc}", file=sys.stderr)
            return 2
        prompt_hash = hashlib.sha256(
            translate.effective_prompt(locale_prompt).encode()
        ).hexdigest()
        print(
            f"provider={cfg.provider} model={cfg.get('TRANSLATION_MODEL')} "
            f"reasoning={cfg.get('TRANSLATION_REASONING_EFFORT', 'medium')} "
            f"locale={locale} prompt_sha256={prompt_hash}",
            flush=True,
        )
        feedback: str | None = None
        translated = ""
        issues: list[str] = []
        for _attempt in range(translate.MAX_COMPLETED_RESPONSE_ATTEMPTS):
            request = translate.TranslationRequest(
                source=CHECK_SOURCE,
                existing_translation=None,
                diff_text=CHECK_DIFF,
                verification_feedback=feedback,
            )
            try:
                translated = translate.translate_request(request, cfg, locale_prompt)
            except translate.IncompleteTranslation as exc:
                print(f"{locale} provider check failed: {exc}", file=sys.stderr)
                failed = True
                break

            issues = evaluate_output(locale, translated)
            if not issues:
                break
            feedback = translate.verification_feedback(issues)
        else:
            failed = True

        if not translated:
            continue
        print(translated.rstrip())
        if issues:
            print(f"{locale} provider check issues: {issues}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
