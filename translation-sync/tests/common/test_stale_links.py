"""stale 링크 registry의 canonical 형식과 대상 조회 검증."""

import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlsplit

from sync.common.markdown import markdown_links
from sync.common.stale_links import (
    DEFAULT_STALE_LINK_REGISTRY,
    StaleLinkRegistryError,
    canonical_stale_link_target,
    load_stale_link_registry,
)
from sync.common.versions import load_versions


_REPO_ROOT = Path(__file__).resolve().parents[3]
_ENGLISH_DOCS_ROOT = (
    _REPO_ROOT / "i18n/en/docusaurus-plugin-content-docs"
)
_ANCHOR_RE = re.compile(
    r'''<a\s+(?:name|id)\s*=\s*["']([^"']+)["']''',
    re.IGNORECASE,
)


def _load_english_documents() -> dict[str, dict[str, str]]:
    """지원 버전별 영어 Markdown 문서 로드.

    Returns:
        버전과 파일명으로 조회할 수 있는 문서 본문.
    """

    versions = load_versions(_REPO_ROOT / "versions.json")
    return {
        version: {
            path.name: path.read_text(encoding="utf-8")
            for path in (
                _ENGLISH_DOCS_ROOT / f"version-{version}"
            ).glob("*.md")
        }
        for version in versions
    }


def _target_resolves(
    target: str,
    version: str,
    source_file: str,
    documents: dict[str, dict[str, str]],
) -> bool:
    """영어 문서 링크의 파일·명시적 앵커 연결 여부 확인.

    Args:
        target: Markdown 링크 대상.
        version: 링크가 포함된 문서 버전.
        source_file: 링크가 포함된 Markdown 파일명.
        documents: 지원 버전별 영어 문서 본문.

    Returns:
        검증 대상이 아닌 외부·사이트 링크이거나 내부 대상 파일과 명시된 앵커가 존재하면 ``True``.
    """

    parsed = urlsplit(target)
    if parsed.scheme:
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.netloc != "laravel.com"
            or not parsed.path.startswith("/docs/")
        ):
            return True
        path = parsed.path
    else:
        path = parsed.path
    fragment = parsed.fragment

    if path.startswith("/docs/"):
        version_token, separator, path = path.removeprefix("/docs/").partition("/")
        if not separator:
            return True
        target_version = version if version_token == "{{version}}" else version_token
    elif path.startswith("/"):
        return True
    else:
        target_version = version

    if not path:
        target_file = source_file
    else:
        target_file = path.rstrip("/").split("/")[-1]
        if not target_file.endswith(".md"):
            target_file += ".md"
    body = documents.get(target_version, {}).get(target_file)
    if body is None:
        return False
    return not fragment or fragment in set(_ANCHOR_RE.findall(body))


class StaleLinkRegistryTests(unittest.TestCase):
    """stale 링크 registry의 schema·정렬·digest 경계 테스트."""

    def test_external_targets_never_match_internal_suffix_rules(self):
        """외부 링크는 내부 suffix 규칙에서 제외하고 Laravel 문서 링크만 보정하는지 검증."""

        targets = (
            "//example.com/docs/migrations#writing-migrations",
            "mailto:migrations#writing-migrations",
            "https://example.com/docs/migrations#writing-migrations",
        )

        for target in targets:
            with self.subTest(target=target):
                self.assertIsNone(
                    DEFAULT_STALE_LINK_REGISTRY.matching_rule(target, "10.x")
                )
                self.assertEqual(
                    canonical_stale_link_target(target, "10.x"),
                    target,
                )

        laravel_target = (
            "https://laravel.com/docs/10.x/migrations#writing-migrations"
        )
        self.assertEqual(
            canonical_stale_link_target(laravel_target, "10.x"),
            "https://laravel.com/docs/10.x/migrations#generating-migrations",
        )

    def test_registry_covers_only_current_broken_internal_links(self):
        """registry가 현재 영어 원문의 깨진 내부 링크만 포함하고 교체 대상은 유효하며 모든 규칙이 사용되는지 검증."""

        documents = _load_english_documents()
        matched_rules: set[tuple[str, str]] = set()
        valid_link_matches: list[tuple[str, str, str]] = []
        unhandled_links: list[tuple[str, str, str]] = []
        invalid_targets: list[tuple[str, str, str]] = []

        for version, version_documents in documents.items():
            for filename, body in version_documents.items():
                for link in markdown_links(body):
                    if link.image:
                        continue
                    resolves = _target_resolves(
                        link.target,
                        version,
                        filename,
                        documents,
                    )
                    rule = DEFAULT_STALE_LINK_REGISTRY.matching_rule(
                        link.target,
                        version,
                    )
                    if resolves:
                        if rule is not None:
                            valid_link_matches.append(
                                (version, filename, link.target)
                            )
                        continue
                    if rule is None:
                        unhandled_links.append(
                            (version, filename, link.target)
                        )
                        continue

                    matched_rules.add((rule.version, rule.source))
                    canonical = canonical_stale_link_target(
                        link.target,
                        version,
                    )
                    if canonical is not None and not _target_resolves(
                        canonical,
                        version,
                        filename,
                        documents,
                    ):
                        invalid_targets.append(
                            (version, filename, canonical)
                        )

        expected_rules = {
            (rule.version, rule.source)
            for rule in DEFAULT_STALE_LINK_REGISTRY.rules
        }
        self.assertEqual(valid_link_matches, [])
        self.assertEqual(unhandled_links, [])
        self.assertEqual(invalid_targets, [])
        self.assertEqual(matched_rules, expected_rules)

    def test_loads_a_canonical_registry_snapshot(self):
        """canonical JSON 원문·SHA-256 digest와 링크 보정 결과 보존."""

        payload = {
            "schema_version": 1,
            "links": [
                {
                    "version": "master",
                    "from": "#old",
                    "to": "#new",
                    "retire_mode": None,
                }
            ],
        }
        raw = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "stale-links.json"
            path.write_text(raw, encoding="utf-8", newline="")

            registry = load_stale_link_registry(path)

        self.assertEqual(registry.raw, raw.encode("utf-8"))
        self.assertEqual(registry.sha256, hashlib.sha256(registry.raw).hexdigest())
        self.assertEqual(
            canonical_stale_link_target(
                "#old",
                "master",
                registry=registry,
            ),
            "#new",
        )

    def test_rejects_noncanonical_json(self):
        """정해진 들여쓰기와 줄바꿈을 사용하지 않은 compact JSON 거부."""

        payload = {
            "schema_version": 1,
            "links": [
                {
                    "version": "master",
                    "from": "#old",
                    "to": "#new",
                    "retire_mode": None,
                }
            ],
        }
        compact = json.dumps(payload, ensure_ascii=False) + "\n"

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "stale-links.json"
            path.write_text(compact, encoding="utf-8", newline="")

            with self.assertRaisesRegex(
                StaleLinkRegistryError,
                "canonical JSON",
            ):
                load_stale_link_registry(path)

    def test_rejects_invalid_schema_and_order(self):
        """추가 필드·중복·정렬·폐기 방식의 schema 위반 거부."""

        valid_entry = {
            "version": "master",
            "from": "#old",
            "to": "#new",
            "retire_mode": None,
        }
        cases = (
            {
                "schema_version": 1,
                "links": [valid_entry],
                "extra": True,
            },
            {
                "schema_version": 1,
                "links": [
                    valid_entry,
                    {
                        "version": "master",
                        "from": "#old",
                        "to": "#newer",
                        "retire_mode": None,
                    },
                ],
            },
            {
                "schema_version": 1,
                "links": [
                    {
                        "version": "master",
                        "from": "#z-last",
                        "to": "#new",
                        "retire_mode": None,
                    },
                    valid_entry,
                ],
            },
            {
                "schema_version": 1,
                "links": [
                    {
                        "version": "master",
                        "from": "#retired",
                        "to": None,
                        "retire_mode": None,
                    },
                ],
            },
            {
                "schema_version": 1,
                "links": [
                    {
                        "version": "master",
                        "from": "#retired",
                        "to": None,
                        "retire_mode": [],
                    },
                ],
            },
        )

        for payload in cases:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "stale-links.json"
                path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                    newline="",
                )

                with self.assertRaises(StaleLinkRegistryError):
                    load_stale_link_registry(path)

    def test_rejects_non_utf8_unicode_scalar(self):
        """UTF-8로 직렬화할 수 없는 서로게이트 코드 포인트 거부."""

        payload = {
            "schema_version": 1,
            "links": [
                {
                    "version": "master",
                    "from": chr(0xD800),
                    "to": "#new",
                    "retire_mode": None,
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "stale-links.json"
            path.write_text(
                json.dumps(payload, ensure_ascii=True, indent=2) + "\n",
                encoding="utf-8",
                newline="",
            )

            with self.assertRaisesRegex(StaleLinkRegistryError, "UTF-8"):
                load_stale_link_registry(path)
