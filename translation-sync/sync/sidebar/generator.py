"""``documentation.md`` 기반 사이드바 동기화.

영어 ``documentation.md``의 제목과 문서 링크에서 버전별 사이드바 생성.
동기화 시 대상 버전의 번역별 사이드바 오버라이드 JSON 파일 제거.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from ..common.files import atomic_write_text, unlink_file
from ..common.versions import (
    load_versions as _load_versions,
    validate_version_token as _validate_version_token,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_LINK_RE = re.compile(r"^\s*-\s*\[([^\]\n]+)]\(([^)\s]+)\)\s*$")
API_DOCS_HREF_RE = re.compile(
    r"^https://api\.laravel\.com/docs/(?:master|\d+\.x)/?$"
)
SIDEBAR_LOCALES = ("ko", "ja")


@dataclass(frozen=True)
class SidebarResult:
    """버전별 사이드바 동기화 결과."""

    version: str
    changed: bool
    issues: list[str]


@dataclass(frozen=True)
class _SidebarPlan:
    """버전 하나의 입력 스냅숏과 검증·적용 계획."""

    version: str
    expected: dict
    documentation_bytes: bytes | None
    approved_sidebar_bytes: bytes | None
    generated_sidebar_bytes: bytes
    sidebar_changed: bool
    locale_paths_to_remove: tuple[Path, ...]
    issues: tuple[str, ...]

    @property
    def changed(self) -> bool:
        """사이드바 갱신 또는 번역별 오버라이드 삭제 필요 여부."""

        return self.sidebar_changed or bool(self.locale_paths_to_remove)


@dataclass(frozen=True)
class _SidebarCandidateSet:
    """모든 대상 버전의 검증 가능한 원자적 적용 후보 집합."""

    plans: tuple[_SidebarPlan, ...]
    input_hash: str | None


def load_versions(repo_root: Path = REPO_ROOT) -> list[str]:
    """검증된 지원 버전 목록 로딩."""

    return _load_versions(_versions_path(repo_root))


def _supported_version(version: str, repo_root: Path = REPO_ROOT) -> str:
    """지원 목록에 포함된 안전한 버전 반환."""

    version = _validate_version_token(version)
    for supported in load_versions(repo_root):
        if supported == version:
            _sidebar_filename(supported)
            _locale_sidebar_filename(supported)
            return supported
    raise ValueError(f"unknown version: {version}")


def _safe_repo_path(path: Path, repo_root: Path) -> Path:
    """대상과 저장소 루트의 포함 관계 및 부모 경로의 심볼릭 링크 부재 검증."""

    lexical_root = Path(os.path.abspath(repo_root))
    lexical_path = Path(os.path.abspath(path))
    try:
        relative = lexical_path.relative_to(lexical_root)
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {path}") from exc

    resolved_root = repo_root.resolve()
    if not relative.parts:
        return lexical_root

    parent = lexical_root
    for part in relative.parts[:-1]:
        parent /= part
        if parent.is_symlink():
            raise ValueError(f"path escapes repository: {path}")

    resolved_parent = lexical_path.parent.resolve()
    try:
        resolved_parent.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {path}") from exc
    return lexical_path


def _versions_path(repo_root: Path) -> Path:
    """저장소 내부의 일반 파일인 ``versions.json`` 경로 반환."""

    path = _safe_repo_path(repo_root / "versions.json", repo_root)
    if path.is_symlink():
        raise ValueError("versions.json path must not be a symlink")
    if not path.is_file():
        raise ValueError("versions.json path must be a regular file")
    return path


def _repo_relative(path: Path, repo_root: Path) -> Path:
    """검증된 경로의 저장소 상대 경로 반환."""

    lexical_root = Path(os.path.abspath(repo_root))
    return _safe_repo_path(path, repo_root).relative_to(lexical_root)


def latest_stable_version(repo_root: Path = REPO_ROOT) -> str:
    """최신 안정 버전 반환."""

    return load_versions(repo_root)[1]


def resolve_versions(
    *, all_versions: bool = False, version: str | None = None, repo_root: Path = REPO_ROOT
) -> list[str]:
    """명령줄 옵션에 맞는 대상 버전 목록 결정."""

    versions = load_versions(repo_root)
    if all_versions:
        return versions
    if version:
        if version not in versions:
            raise ValueError(f"unknown version: {version}")
        return [version]
    return ["master"]


def _documentation_path(repo_root: Path, version: str) -> Path:
    """영문 목차 문서 경로 생성."""

    return (
        repo_root
        / "i18n"
        / "en"
        / "docusaurus-plugin-content-docs"
        / f"version-{version}"
        / "documentation.md"
    )


def _source_doc_path(repo_root: Path, version: str, doc_id: str) -> Path:
    """사이드바 문서 ID에 대응하는 영문 원문 경로 생성."""

    return (
        repo_root
        / "i18n"
        / "en"
        / "docusaurus-plugin-content-docs"
        / f"version-{version}"
        / f"{doc_id}.md"
    )


def _sidebar_filename(version: str) -> str:
    """버전별 사이드바 파일명 생성."""

    return f"version-{_validate_version_token(version)}-sidebars.json"


def _locale_sidebar_filename(version: str) -> str:
    """번역별 사이드바 오버라이드 파일명 생성."""

    return f"version-{_validate_version_token(version)}.json"


def _sidebar_path(repo_root: Path, version: str) -> Path:
    """버전별 사이드바 출력 경로 생성."""

    return repo_root / "versioned_sidebars" / _sidebar_filename(version)


def locale_sidebar_paths(repo_root: Path, version: str) -> list[Path]:
    """삭제할 번역별 사이드바 오버라이드 경로 생성."""

    filename = _locale_sidebar_filename(version)
    return [
        repo_root
        / "i18n"
        / locale
        / "docusaurus-plugin-content-docs"
        / filename
        for locale in SIDEBAR_LOCALES
    ]


def _doc_id_from_href(href: str) -> str | None:
    """쿼리와 프래그먼트가 없는 ``/docs/<version>/<id>`` 경로에서 문서 ID 추출."""

    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        return None

    segments = [segment for segment in parsed.path.split("/") if segment]
    if (
        parsed.path.startswith("/docs/")
        and len(segments) == 3
        and segments[0] == "docs"
    ):
        return segments[-1]
    return None


def _category_label(line: str) -> str | None:
    """``- ## <label>`` 형식의 루트 카테고리 선언에서 레이블 추출."""

    if line != line.lstrip():
        return None

    stripped = line.strip()
    if not stripped.startswith("-"):
        return None

    after_dash = stripped[1:].lstrip()
    if not after_dash.startswith("##"):
        return None

    after_hashes = after_dash[2:]
    if not after_hashes or not after_hashes[0].isspace():
        return None

    label = after_hashes.strip()
    return label or None


def _normalize_link_href(
    href: str,
    *,
    label: str,
    is_root: bool,
    version: str,
    latest_stable: str,
) -> str:
    """버전 플레이스홀더와 ``master`` 루트의 API 문서 링크 정규화."""

    normalized = href.replace("{{version}}", version)
    if (
        version == "master"
        and is_root
        and label == "API Documentation"
        and API_DOCS_HREF_RE.fullmatch(normalized)
    ):
        return f"https://api.laravel.com/docs/{latest_stable}"
    return normalized


def _link_digest(raw_target: str) -> str:
    """원본 링크 대상에서 안정적인 키용 SHA-256 해시 생성."""

    return hashlib.sha256(raw_target.encode("utf-8")).hexdigest()


def _doc_key(doc_id: str, occurrences: dict[str, int]) -> str:
    """전역 등장 순서를 반영한 문서 키 생성."""

    occurrence = occurrences.get(doc_id, 0) + 1
    occurrences[doc_id] = occurrence
    key = f"doc:{doc_id}"
    return key if occurrence == 1 else f"{key}:{occurrence}"


def _append_external_link(
    *,
    items: list[dict],
    current_category: dict | None,
    label: str,
    raw_href: str,
    is_indented: bool,
    line_number: int,
    version: str,
    latest_stable: str,
    issues: list[str],
    targets_by_digest: dict[str, str],
    occurrences: dict[str, int],
) -> dict | None:
    """외부·앵커 링크 항목을 현재 카테고리 또는 루트에 추가.

    Args:
        items: 루트 사이드바 항목 목록.
        current_category: 현재 카테고리.
        label: 링크 표시 레이블.
        raw_href: 원문 링크 대상.
        is_indented: 카테고리 하위 들여쓰기 여부.
        line_number: 진단용 원문 줄 번호.
        version: 대상 문서 버전.
        latest_stable: 최신 안정 버전.
        issues: 형식 문제 누적 목록.
        targets_by_digest: digest 충돌 검사용 링크 mapping.
        occurrences: 링크 대상별 등장 횟수.

    Returns:
        다음 줄에 적용할 현재 카테고리.
    """

    if current_category is None and is_indented:
        issues.append(f"line {line_number}: link is outside a category")
        return current_category
    href = _normalize_link_href(
        raw_href,
        label=label,
        is_root=not is_indented,
        version=version,
        latest_stable=latest_stable,
    )
    digest = _link_digest(raw_href)
    previous_target = targets_by_digest.setdefault(digest, raw_href)
    if previous_target != raw_href:
        issues.append(f"line {line_number}: link digest collision: {digest}")
    occurrence = occurrences.get(raw_href, 0) + 1
    occurrences[raw_href] = occurrence
    key = f"link:{digest}"
    if occurrence > 1:
        key = f"{key}:{occurrence}"
    link_item = {"type": "link", "label": label, "href": href, "key": key}
    if current_category is not None and is_indented:
        current_category["items"].append(link_item)
        return current_category
    items.append(link_item)
    return None


def _append_document_link(
    *,
    current_category: dict | None,
    doc_id: str,
    label: str,
    is_indented: bool,
    line_number: int,
    issues: list[str],
    occurrences: dict[str, int],
    keys: set[str],
) -> None:
    """문서 링크를 현재 카테고리에 추가하고 번역 key 검증.

    Args:
        current_category: 현재 카테고리.
        doc_id: 정규 문서 식별자.
        label: 문서 표시 레이블.
        is_indented: 카테고리 하위 들여쓰기 여부.
        line_number: 진단용 원문 줄 번호.
        issues: 형식 문제 누적 목록.
        occurrences: 문서별 등장 횟수.
        keys: 이미 사용한 문서 번역 key 집합.
    """

    if current_category is None or not is_indented:
        issues.append(f"line {line_number}: doc link is outside a category")
        return
    key = _doc_key(doc_id, occurrences)
    if key in keys:
        issues.append(f"line {line_number}: duplicate doc translation key: {key}")
    keys.add(key)
    current_category["items"].append(
        {"type": "doc", "id": doc_id, "label": label, "key": key}
    )


def _documentation_link(
    line: str,
    line_number: int,
    issues: list[str],
) -> tuple[str, str, str | None, bool] | None:
    """영문 목차 한 줄에서 검증된 링크 구성 요소 추출.

    Args:
        line: 영문 목차 물리 줄.
        line_number: 진단용 줄 번호.
        issues: 형식 문제 누적 목록.

    Returns:
        레이블, 원문 대상, 문서 ID, 들여쓰기 여부. 링크가 아니면 ``None``.
    """

    link_match = DOC_LINK_RE.match(line)
    if link_match is None:
        if re.match(r"^\s*-\s*\[", line):
            issues.append(
                f"line {line_number}: unsupported or malformed documentation link"
            )
        return None
    label = link_match.group(1).strip()
    raw_href = link_match.group(2).strip()
    if not label:
        issues.append(
            f"line {line_number}: unsupported or malformed documentation link"
        )
        return None
    try:
        doc_id = _doc_id_from_href(raw_href)
    except ValueError:
        issues.append(
            f"line {line_number}: unsupported or malformed documentation link"
        )
        return None
    is_indented = bool(line[: len(line) - len(line.lstrip())])
    return label, raw_href, doc_id, is_indented


def parse_documentation(
    text: str, *, version: str, latest_stable: str
) -> tuple[list[dict], list[str]]:
    """영문 목차를 사이드바 항목과 형식 문제 목록으로 파싱."""

    items: list[dict] = []
    current_category: dict | None = None
    issues: list[str] = []
    doc_occurrences: dict[str, int] = {}
    doc_keys: set[str] = set()
    category_keys: set[str] = set()
    link_targets_by_digest: dict[str, str] = {}
    link_occurrences: dict[str, int] = {}

    for line_number, line in enumerate(text.splitlines(), start=1):
        label = _category_label(line)
        if label:
            if label in category_keys:
                issues.append(
                    f"line {line_number}: duplicate category translation key: {label}"
                )
            category_keys.add(label)
            current_category = {
                "type": "category",
                "label": label,
                "collapsed": True,
                "items": [],
                "key": f"category:{label}",
            }
            items.append(current_category)
            continue

        if re.match(r"^\s*-\s*#", line):
            issues.append(f"line {line_number}: unsupported or malformed category")
            current_category = None
            continue

        link = _documentation_link(line, line_number, issues)
        if link is None:
            continue
        label, raw_href, doc_id, is_indented = link

        if doc_id is None:
            current_category = _append_external_link(
                items=items,
                current_category=current_category,
                label=label,
                raw_href=raw_href,
                is_indented=is_indented,
                line_number=line_number,
                version=version,
                latest_stable=latest_stable,
                issues=issues,
                targets_by_digest=link_targets_by_digest,
                occurrences=link_occurrences,
            )
            continue
        _append_document_link(
            current_category=current_category,
            doc_id=doc_id,
            label=label,
            is_indented=is_indented,
            line_number=line_number,
            issues=issues,
            occurrences=doc_occurrences,
            keys=doc_keys,
        )

    return items, issues


def _existing_collapsed(sidebar: dict) -> tuple[dict[str, bool], list[str]]:
    """기준 사이드바 카테고리의 유효한 접힘 상태 수집."""

    collapsed: dict[str, bool] = {}
    issues: list[str] = []
    for node in sidebar.get("tutorialSidebar", []):
        if not isinstance(node, dict) or node.get("type") != "category":
            continue
        key = node.get("key")
        value = node.get("collapsed")
        if not isinstance(value, bool):
            identifier = key if isinstance(key, str) else node.get("label", "<unknown>")
            issues.append(
                "invalid sidebar JSON schema: category collapsed must be boolean: "
                f"{identifier}"
            )
            continue
        if isinstance(key, str):
            collapsed[key] = value
    return collapsed, issues


def _apply_existing_collapsed(items: list[dict], current: dict) -> list[str]:
    """동일한 카테고리 키에 기존 접힘 상태 적용."""

    collapsed, issues = _existing_collapsed(current)
    for node in items:
        if not isinstance(node, dict) or node.get("type") != "category":
            continue
        key = node.get("key")
        if isinstance(key, str) and key in collapsed:
            node["collapsed"] = collapsed[key]
    return issues


def _doc_ids(items: list[dict]) -> list[str]:
    """생성된 카테고리에서 문서 ID 목록 수집."""

    ids: list[str] = []
    for node in items:
        if isinstance(node, dict) and node.get("type") == "category":
            ids.extend(
                item["id"]
                for item in node.get("items", [])
                if isinstance(item, dict) and item.get("type") == "doc"
            )
    return ids


def _read_documentation_snapshot(
    version: str, *, repo_root: Path
) -> tuple[bytes | None, list[str]]:
    """영문 목차의 정확한 바이트와 경로 문제 읽기."""

    path = _safe_repo_path(_documentation_path(repo_root, version), repo_root)
    if path.is_symlink():
        return None, [
            f"documentation.md path must not be a symlink for {version}"
        ]
    if not path.exists():
        return None, [f"missing documentation.md for {version}"]
    if not path.is_file():
        return None, [
            f"documentation.md path must be a regular file for {version}"
        ]
    try:
        return path.read_bytes(), []
    except OSError as exc:
        return None, [f"failed to read documentation.md for {version}: {exc}"]


def _build_sidebar_from_documentation(
    version: str,
    documentation_bytes: bytes | None,
    *,
    current: dict,
    repo_root: Path,
) -> tuple[dict, list[str]]:
    """영문 목차 바이트에서 기대 사이드바와 문제 목록 생성."""

    latest_stable = latest_stable_version(repo_root)
    if documentation_bytes is None:
        return {}, []
    try:
        documentation = documentation_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        return {}, [f"invalid UTF-8 documentation.md for {version}: {exc}"]

    items, issues = parse_documentation(
        documentation,
        version=version,
        latest_stable=latest_stable,
    )
    issues.extend(_apply_existing_collapsed(items, current))

    for doc_id in _doc_ids(items):
        source_path = _safe_repo_path(
            _source_doc_path(repo_root, version, doc_id), repo_root
        )
        if source_path.is_symlink():
            issues.append(f"source doc path must not be a symlink: {doc_id}")
        elif not source_path.is_file():
            issues.append(f"missing source doc for sidebar item: {doc_id}")

    return {"tutorialSidebar": items}, issues


def build_sidebar(
    version: str, *, current: dict | None = None, repo_root: Path = REPO_ROOT
) -> tuple[dict, list[str]]:
    """저장소 입력으로 버전별 기대 사이드바 생성."""

    version = _supported_version(version, repo_root)
    documentation_bytes, issues = _read_documentation_snapshot(
        version,
        repo_root=repo_root,
    )
    expected, build_issues = _build_sidebar_from_documentation(
        version,
        documentation_bytes,
        current=current or {},
        repo_root=repo_root,
    )
    return expected, [*issues, *build_issues]


def _read_sidebar_snapshot(
    version: str, *, repo_root: Path = REPO_ROOT
) -> tuple[dict, bytes | None, list[str]]:
    """기준 사이드바의 구조와 정확한 바이트 읽기."""

    safe_path = _safe_repo_path(_sidebar_path(repo_root, version), repo_root)
    if safe_path.is_symlink():
        return {}, None, ["sidebar JSON path must not be a symlink"]
    if not safe_path.exists():
        return {}, None, []
    if not safe_path.is_file():
        return {}, None, ["sidebar JSON path must be a regular file"]
    content = safe_path.read_bytes()
    try:
        sidebar = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {}, content, [f"invalid sidebar JSON: {exc}"]
    if not isinstance(sidebar, dict):
        return {}, content, ["invalid sidebar JSON schema: root must be an object"]
    if "tutorialSidebar" not in sidebar:
        return {}, content, [
            "invalid sidebar JSON schema: tutorialSidebar is required"
        ]
    if not isinstance(sidebar["tutorialSidebar"], list):
        return {}, content, [
            "invalid sidebar JSON schema: tutorialSidebar must be a list"
        ]
    return sidebar, content, []


def _read_sidebar(
    version: str, *, repo_root: Path = REPO_ROOT
) -> tuple[dict, list[str]]:
    """기준 사이드바 구조 읽기."""

    sidebar, _content, issues = _read_sidebar_snapshot(
        version,
        repo_root=repo_root,
    )
    return sidebar, issues


def _sort_json_keys(value: object) -> object:
    """JSON 객체 키를 재귀적으로 UTF-8 바이트 순서로 정렬."""

    if isinstance(value, dict):
        return {
            key: _sort_json_keys(value[key])
            for key in sorted(value, key=lambda item: item.encode("utf-8"))
        }
    if isinstance(value, list):
        return [_sort_json_keys(item) for item in value]
    return value


def _serialize_sidebar(sidebar: dict) -> str:
    """사이드바를 결정적인 JSON 문자열로 직렬화."""

    return json.dumps(
        _sort_json_keys(sidebar),
        ensure_ascii=False,
        indent=2,
    ) + "\n"


def _sha256(content: bytes) -> str:
    """콘텐츠의 SHA-256 해시 생성."""

    return hashlib.sha256(content).hexdigest()


def _candidate_input_hash(
    versions_json_bytes: bytes,
    plans: list[_SidebarPlan],
    *,
    repo_root: Path,
) -> str:
    """적용 후보 입력 봉투의 정규 SHA-256 해시 생성."""

    override_deletions = [
        _repo_relative(path, repo_root).as_posix()
        for plan in plans
        for path in plan.locale_paths_to_remove
    ]
    if len(override_deletions) != len(set(override_deletions)):
        raise ValueError("duplicate locale sidebar override deletion")
    envelope = {
        "override_deletions": sorted(
            override_deletions,
            key=lambda path: path.encode("utf-8"),
        ),
        "schema_version": 1,
        "versions": [
            {
                "baseline_sidebar_sha256": (
                    _sha256(plan.approved_sidebar_bytes)
                    if plan.approved_sidebar_bytes is not None
                    else None
                ),
                "documentation_sha256": (
                    _sha256(plan.documentation_bytes)
                    if plan.documentation_bytes is not None
                    else None
                ),
                "generated_sidebar_sha256": _sha256(
                    plan.generated_sidebar_bytes
                ),
                "version": plan.version,
            }
            for plan in plans
        ],
        "versions_sha256": _sha256(versions_json_bytes),
    }
    if any(
        entry["documentation_sha256"] is None
        for entry in envelope["versions"]
    ):
        raise ValueError("sidebar candidate is missing documentation bytes")
    canonical = json.dumps(
        _sort_json_keys(envelope),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    return hashlib.sha256(canonical).hexdigest()


def _write_sidebar(
    version: str, sidebar: dict, *, repo_root: Path = REPO_ROOT
) -> None:
    """검증된 저장소 경로에 사이드바 원자적 기록."""

    safe_path = _safe_repo_path(_sidebar_path(repo_root, version), repo_root)
    safe_path.parent.mkdir(parents=True, exist_ok=True)
    if safe_path.is_symlink():
        raise ValueError("sidebar JSON path must not be a symlink")
    atomic_write_text(safe_path, _serialize_sidebar(sidebar))


def _existing_repo_paths(
    paths: list[Path], repo_root: Path
) -> tuple[list[Path], list[str]]:
    """삭제 가능한 저장소 파일과 잘못된 경로 형태 문제 수집."""

    safe_paths: list[Path] = []
    issues: list[str] = []
    for path in paths:
        safe_path = _safe_repo_path(path, repo_root)
        if safe_path.is_symlink():
            safe_paths.append(safe_path)
            continue
        if not safe_path.exists():
            continue
        if not safe_path.is_file():
            issues.append(
                "locale sidebar JSON path must be a regular file: "
                f"{_repo_relative(safe_path, repo_root)}"
            )
            continue
        safe_paths.append(safe_path)
    return safe_paths, issues


def _plan_version(version: str, *, repo_root: Path) -> _SidebarPlan:
    """버전 하나의 사이드바 생성 및 삭제 계획 수립."""

    version = _supported_version(version, repo_root)
    documentation_bytes, documentation_issues = _read_documentation_snapshot(
        version,
        repo_root=repo_root,
    )
    current, approved_sidebar_bytes, issues = _read_sidebar_snapshot(
        version,
        repo_root=repo_root,
    )
    issues.extend(documentation_issues)
    expected, build_issues = _build_sidebar_from_documentation(
        version,
        documentation_bytes,
        current=current,
        repo_root=repo_root,
    )
    issues.extend(build_issues)
    generated_sidebar_bytes = _serialize_sidebar(expected).encode("utf-8")
    locale_paths = locale_sidebar_paths(repo_root, version)
    existing_locale_paths, locale_issues = _existing_repo_paths(
        locale_paths, repo_root
    )
    issues.extend(locale_issues)
    locale_paths_to_remove = tuple(existing_locale_paths)
    return _SidebarPlan(
        version=version,
        expected=expected,
        documentation_bytes=documentation_bytes,
        approved_sidebar_bytes=approved_sidebar_bytes,
        generated_sidebar_bytes=generated_sidebar_bytes,
        sidebar_changed=not issues
        and approved_sidebar_bytes != generated_sidebar_bytes,
        locale_paths_to_remove=locale_paths_to_remove,
        issues=tuple(issues),
    )


def _plan_candidate_set(
    versions: list[str], *, repo_root: Path
) -> _SidebarCandidateSet:
    """모든 대상 버전의 입력 해시로 봉인된 적용 후보 생성."""

    versions_json_bytes = _versions_path(repo_root).read_bytes()
    plans = [_plan_version(version, repo_root=repo_root) for version in versions]
    return _SidebarCandidateSet(
        plans=tuple(plans),
        input_hash=(
            None
            if any(plan.issues for plan in plans)
            else _candidate_input_hash(
                versions_json_bytes,
                plans,
                repo_root=repo_root,
            )
        ),
    )


def _stale_issues(plan: _SidebarPlan, *, repo_root: Path) -> list[str]:
    """검증 모드에서 오래된 산출물 문제 생성."""

    issues = list(plan.issues)
    if issues:
        return issues
    if plan.sidebar_changed:
        issues.append("sidebar JSON out of sync")
    issues.extend(
        f"locale sidebar JSON remains: {_repo_relative(path, repo_root)}"
        for path in plan.locale_paths_to_remove
    )
    return issues


def _apply_plans(plans: list[_SidebarPlan], *, repo_root: Path) -> list[SidebarResult]:
    """재검증된 계획의 출력과 삭제를 후보 트리에 적용."""

    for plan in plans:
        if plan.sidebar_changed:
            _write_sidebar(plan.version, plan.expected, repo_root=repo_root)
        for locale_path in plan.locale_paths_to_remove:
            unlink_file(locale_path, missing_ok=True)

    results: list[SidebarResult] = []
    for plan in plans:
        issues: list[str] = []
        sidebar_path = _safe_repo_path(
            _sidebar_path(repo_root, plan.version), repo_root
        )
        if (
            sidebar_path.is_symlink()
            or not sidebar_path.exists()
            or sidebar_path.read_bytes() != plan.generated_sidebar_bytes
        ):
            issues.append("sidebar JSON out of sync")
        remaining_locale_paths, locale_issues = _existing_repo_paths(
            locale_sidebar_paths(repo_root, plan.version), repo_root
        )
        issues.extend(locale_issues)
        for locale_path in remaining_locale_paths:
            issues.append(
                f"locale sidebar JSON remains: {_repo_relative(locale_path, repo_root)}"
            )
        results.append(
            SidebarResult(
                version=plan.version,
                changed=plan.changed,
                issues=issues,
            )
        )
    return results


def sync_version(
    version: str, *, write: bool = False, repo_root: Path = REPO_ROOT
) -> SidebarResult:
    """버전 하나의 사이드바 검증 또는 동기화."""

    return sync_versions([version], write=write, repo_root=repo_root)[0]


def sync_versions(
    versions: list[str], *, write: bool = False, repo_root: Path = REPO_ROOT
) -> list[SidebarResult]:
    """대상 버전 전체의 사이드바 검증 또는 일괄 동기화.

    검증 모드에서는 기존 산출물과 기대 산출물의 차이 보고.
    쓰기 모드에서는 모든 버전의 계획이 유효하고 재검증한 입력 해시가 같을 때만 일괄 적용.
    """

    if not versions:
        return []
    requested_versions = {
        _supported_version(version, repo_root) for version in versions
    }
    unique_versions = [
        version
        for version in load_versions(repo_root)
        if version in requested_versions
    ]
    candidate = _plan_candidate_set(unique_versions, repo_root=repo_root)
    plans = list(candidate.plans)
    if not write:
        return [
            SidebarResult(
                version=plan.version,
                changed=plan.changed,
                issues=_stale_issues(plan, repo_root=repo_root),
            )
            for plan in plans
        ]
    if any(plan.issues for plan in plans):
        return [
            SidebarResult(
                version=plan.version,
                changed=False,
                issues=list(plan.issues),
            )
            for plan in plans
        ]
    rechecked = _plan_candidate_set(unique_versions, repo_root=repo_root)
    if (
        any(plan.issues for plan in rechecked.plans)
        or rechecked.input_hash != candidate.input_hash
    ):
        return [
            SidebarResult(
                version=plan.version,
                changed=False,
                issues=["sidebar candidate inputs changed before apply"],
            )
            for plan in plans
        ]
    return _apply_plans(plans, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """명령줄 진입점 실행."""

    parser = argparse.ArgumentParser(description="Sync versioned sidebars from documentation.md")
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--version")
    target.add_argument("--all", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    try:
        versions = resolve_versions(
            all_versions=args.all,
            version=args.version,
            repo_root=REPO_ROOT,
        )
    except ValueError as exc:
        print(exc)
        return 1

    results = sync_versions(versions, write=args.write, repo_root=REPO_ROOT)
    failed = False
    for result in results:
        if result.issues:
            failed = True
            for issue in result.issues:
                print(f"{result.version}: {issue}")
            continue
        status = "updated" if result.changed and args.write else "verified"
        print(f"{result.version}: sidebar {status}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
