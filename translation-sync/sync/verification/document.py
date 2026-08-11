"""hash에 결속되고 저장소 쓰기를 하지 않는 최종 문서 검증 계약.

이 모듈의 함수는 불변 값만 변환하고 저장소 파일을 직접 읽거나 쓰지 않음.
실패한 candidate가 검증된 산출물로 유출되지 않는 구조.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from ..common import stale_links
from ..common.markdown import (
    html_comment_spans,
    mask_fenced_code_contents,
    strip_title_attr_line,
)
from ..common.stale_links import StaleLinkRegistry
from ..common.versions import validate_version_token
from . import response_contract
from . import verify as legacy_verify
from .structure import (
    blockquote_structure_signature,
    front_matter_contract,
    list_structure_signature,
    table_structure_signature,
)


_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_ANNOTATION_RE = re.compile(r"<!-- ([^\r\n]*) -->")
_EXPECTED_MAP_KEYS = ("schema_version", "entries")
_EXPECTED_ENTRY_KEYS = ("structural_address", "occurrence", "annotation")
_HEADING_ANNOTATION_RE = re.compile(r"^(#{1,6})\s+(.+)$")
_HEADING_ATTRIBUTES_RE = re.compile(
    r"\{((?:[.#][^}\s]+)(?:\s+[.#][^}\s]+)*)\}\s*$"
)
_LIST_ANNOTATION_PATTERN = r"^(?:[-*+]\s+|\d+[.)]\s+)"
_LIST_ANNOTATION_RE = re.compile(_LIST_ANNOTATION_PATTERN)
_LEGACY_TABLE_ANNOTATION_RE = re.compile(
    r"(?:^|\s):?-{3,}:?\s*\|\s*:?-{3,}:?(?:\s|$)"
)
_INVALID_VERIFICATION_INPUT = "verification input is missing, invalid, or noncanonical"


def _utf8(value: str) -> bytes:
    """문자열을 UTF-8 바이트로 인코딩."""

    return value.encode("utf-8")


def _canonical_pretty_json(value: object) -> bytes:
    """값을 들여쓰기된 canonical JSON 바이트로 직렬화."""

    try:
        return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode(
            "utf-8"
        )
    except UnicodeEncodeError as exc:
        raise ValueError("canonical JSON values must be UTF-8") from exc


def _canonical_compact_json(value: object) -> bytes:
    """값을 공백 없는 canonical JSON 바이트로 직렬화."""

    return (
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


@dataclass(frozen=True)
class ExpectedAnnotationEntry:
    """영어 원문 annotation 한 건의 예상 위치와 canonical 문자열.

    Attributes:
        structural_address: annotation 소유 블록의 구조 주소.
        occurrence: 같은 구조 주소 안에서 1부터 시작하는 출현 순번.
        annotation: 완전한 canonical HTML comment 문자열.
    """

    structural_address: str
    occurrence: int
    annotation: str

    def __post_init__(self) -> None:
        """필드가 canonical annotation 계약을 만족하는지 검증."""

        if (
            type(self.structural_address) is not str
            or not self.structural_address
            or self.structural_address.strip() != self.structural_address
            or any(ord(char) < 0x20 for char in self.structural_address)
        ):
            raise ValueError("invalid structural_address")
        try:
            self.structural_address.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise ValueError("structural_address must be UTF-8") from exc
        if type(self.occurrence) is not int or self.occurrence <= 0:
            raise ValueError("invalid annotation occurrence")
        if type(self.annotation) is not str:
            raise ValueError("annotation must be one canonical comment")
        try:
            self.annotation.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise ValueError("annotation must be UTF-8") from exc
        match = _ANNOTATION_RE.fullmatch(self.annotation)
        if match is None:
            raise ValueError("annotation must be one canonical comment")
        body = match.group(1)
        if (
            not body
            or body != " ".join(body.split())
            or "-->" in body
        ):
            raise ValueError("annotation comment is not canonical")


@dataclass(frozen=True)
class ExpectedAnnotationMap:
    """문서 순서로 정렬된 예상 annotation 집합.

    Attributes:
        schema_version: annotation map 스키마 버전.
        entries: 문서 순서의 annotation 항목.
    """

    schema_version: int
    entries: tuple[ExpectedAnnotationEntry, ...]

    def __post_init__(self) -> None:
        """스키마와 occurrence 연속성을 검증."""

        if type(self.schema_version) is not int or self.schema_version != 1:
            raise ValueError("unsupported expected annotation map schema")
        try:
            entries = tuple(self.entries)
        except TypeError as exc:
            raise ValueError("expected annotation map entries must be iterable") from exc
        object.__setattr__(self, "entries", entries)
        next_occurrence: dict[str, int] = {}
        for entry in self.entries:
            if type(entry) is not ExpectedAnnotationEntry:
                raise ValueError("invalid expected annotation map entry")
            expected = next_occurrence.get(entry.structural_address, 1)
            if entry.occurrence != expected:
                raise ValueError(
                    "annotation occurrence must start at 1 and be contiguous"
                )
            next_occurrence[entry.structural_address] = expected + 1

    def canonical_bytes(self) -> bytes:
        """고정된 필드 순서와 형식의 JSON 바이트 반환."""

        return _canonical_pretty_json(
            {
                "schema_version": self.schema_version,
                "entries": [
                    {
                        "structural_address": entry.structural_address,
                        "occurrence": entry.occurrence,
                        "annotation": entry.annotation,
                    }
                    for entry in self.entries
                ],
            }
        )


def parse_expected_annotation_map(raw: bytes) -> ExpectedAnnotationMap:
    """Canonical JSON 바이트에서 예상 annotation map 파싱.

    Args:
        raw: UTF-8과 고정 형식을 만족해야 하는 JSON 바이트.

    Returns:
        검증된 예상 annotation map.

    Raises:
        ValueError: 바이트가 canonical 형식이나 map 계약을 위반한 경우.
    """

    if not isinstance(raw, bytes):
        raise ValueError("expected annotation map must be bytes")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("expected annotation map is not canonical JSON") from exc
    if not isinstance(value, dict) or tuple(value) != _EXPECTED_MAP_KEYS:
        raise ValueError("expected annotation map fields are not canonical")
    entries = value.get("entries")
    if not isinstance(entries, list):
        raise ValueError("expected annotation map entries must be an array")
    try:
        canonical = _canonical_pretty_json(value)
    except ValueError as exc:
        raise ValueError("expected annotation map is not canonical UTF-8") from exc
    if raw != canonical:
        raise ValueError("expected annotation map bytes are not canonical")

    parsed: list[ExpectedAnnotationEntry] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or tuple(entry) != _EXPECTED_ENTRY_KEYS:
            raise ValueError(
                f"expected annotation map entry {index} fields are not canonical"
            )
        parsed.append(
            ExpectedAnnotationEntry(
                structural_address=entry["structural_address"],
                occurrence=entry["occurrence"],
                annotation=entry["annotation"],
            )
        )
    result = ExpectedAnnotationMap(value["schema_version"], tuple(parsed))
    if result.canonical_bytes() != raw:
        raise ValueError("expected annotation map bytes are not canonical")
    return result


def _heading_section_slug(body: str) -> str:
    """Heading annotation에서 안정적인 section slug 생성."""

    heading = _HEADING_ANNOTATION_RE.fullmatch(body)
    if heading is None:
        raise ValueError("heading annotation is malformed")
    text = heading.group(2)
    attributes = _HEADING_ATTRIBUTES_RE.search(text)
    if attributes is not None:
        for attribute in attributes.group(1).split():
            if attribute.startswith("#"):
                return attribute[1:]
    text = re.sub(r"\[([^]\n]+)]\([^\n)]*\)", r"\1", text)
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"\s*\{[^}]*}\s*$", "", text)
    normalized = unicodedata.normalize("NFC", text).casefold()
    slug = re.sub(r"[^\w.-]+", "-", normalized).strip("-._")
    slug = slug.replace("_", "-")
    if slug:
        return slug
    return f"heading-{hashlib.sha256(_utf8(body)).hexdigest()[:12]}"


def _map_from_canonical_annotations(
    annotations: tuple[str, ...],
) -> ExpectedAnnotationMap:
    """문서 순서의 canonical annotation으로 예상 map 생성."""

    section = "document"
    occurrences: dict[str, int] = {}
    entries: list[ExpectedAnnotationEntry] = []
    for annotation in annotations:
        match = _ANNOTATION_RE.fullmatch(annotation)
        if match is None:
            raise ValueError("pipeline annotation byte is not canonical")
        body = match.group(1)
        heading = _HEADING_ANNOTATION_RE.fullmatch(body)
        if heading is not None:
            section = _heading_section_slug(body)
            owner = f"heading:{len(heading.group(1))}"
        elif _LIST_ANNOTATION_RE.match(body):
            owner = "list:1"
        elif body.startswith("|") or _LEGACY_TABLE_ANNOTATION_RE.search(body):
            owner = "table:1"
        else:
            owner = "paragraph:1"
        address = f"section:{section}/{owner}"
        occurrence = occurrences.get(address, 0) + 1
        occurrences[address] = occurrence
        entries.append(
            ExpectedAnnotationEntry(address, occurrence, annotation)
        )
    return ExpectedAnnotationMap(1, tuple(entries))


def build_expected_annotation_map(
    annotation_source: str | bytes,
) -> ExpectedAnnotationMap:
    """Stale-link 보정 전 원문에서 예상 annotation map 생성.

    Args:
        annotation_source: version과 placeholder 복원이 끝난 영어 원문.

    Returns:
        원문 소유 블록과 occurrence가 결합된 예상 annotation map.

    Raises:
        ValueError: 원문이 UTF-8 텍스트가 아니거나 annotation이 유효하지 않은 경우.
    """

    if isinstance(annotation_source, bytes):
        try:
            source = annotation_source.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("annotation source must be UTF-8") from exc
    elif isinstance(annotation_source, str):
        source = annotation_source
    else:
        raise ValueError("annotation source must be UTF-8 text or bytes")
    return _map_from_canonical_annotations(_canonical_source_annotations(source))


@dataclass(frozen=True)
class VerificationIssue:
    """안정적인 코드와 구조 주소가 결합된 문서 검증 문제.

    Attributes:
        code: 기계 판독 가능한 안정적 문제 코드.
        structural_address: 문제가 발생한 구조 주소. 문서 전체면 ``None``.
        message: 사람이 확인할 수 있는 문제 설명.
    """

    code: str
    structural_address: str | None
    message: str


@dataclass(frozen=True)
class VerificationInput:
    """Canonical envelope hash에 결속된 문서 검증 입력.

    Attributes:
        locale_bytes: 검증할 locale 문서 바이트.
        english_view_bytes: 비교 기준 영어 verification view 바이트.
        annotation_map_bytes: 예상 annotation map의 canonical JSON 바이트.
        version: 문서 버전.
        registry_sha256: stale-link registry digest.
        envelope_bytes: 입력 digest를 묶은 canonical envelope 바이트.
        verification_input_sha256: envelope의 SHA-256 digest.
    """

    locale_bytes: bytes
    english_view_bytes: bytes
    annotation_map_bytes: bytes
    version: str
    registry_sha256: str
    envelope_bytes: bytes
    verification_input_sha256: str


@dataclass(frozen=True)
class VerifiedLocaleArtifact:
    """검증 입력 hash에 결속된 적재 가능 locale 산출물.

    Attributes:
        schema_version: 산출물 계약 버전.
        locale_bytes: 검증을 통과한 locale 문서 바이트.
        version: 문서 버전.
        registry_sha256: 검증에 사용한 stale-link registry digest.
        verification_input_sha256: 검증 입력 envelope digest.
    """

    schema_version: int
    locale_bytes: bytes
    version: str
    registry_sha256: str
    verification_input_sha256: str


@dataclass(frozen=True)
class VerificationResult:
    """안정적인 문제 목록 또는 검증된 locale 산출물.

    Attributes:
        issues: 코드와 구조 주소로 정렬된 검증 문제.
        verification_input_sha256: 유효한 시작 입력의 envelope digest.
        artifact: 문제가 없을 때만 생성된 locale 산출물.
    """

    issues: tuple[VerificationIssue, ...]
    verification_input_sha256: str | None
    artifact: VerifiedLocaleArtifact | None


def _verification_envelope(
    *,
    locale_bytes: bytes,
    english_view_bytes: bytes,
    annotation_map_bytes: bytes,
    version: str,
    registry_sha256: str,
) -> bytes:
    """검증 입력 구성 요소의 digest를 canonical envelope로 결합."""

    return _canonical_compact_json(
        {
            "annotation_map_sha256": hashlib.sha256(
                annotation_map_bytes
            ).hexdigest(),
            "english_view_sha256": hashlib.sha256(
                english_view_bytes
            ).hexdigest(),
            "locale_sha256": hashlib.sha256(locale_bytes).hexdigest(),
            "registry_sha256": registry_sha256,
            "schema_version": 1,
            "version": version,
        }
    )


def create_verification_input(
    *,
    locale_document: str | bytes,
    english_view: str | bytes,
    annotation_source: str | bytes,
    version: str,
    registry_sha256: str,
    expected_annotation_map: ExpectedAnnotationMap | None = None,
) -> VerificationInput:
    """후처리 산출물에서 hash에 결속된 검증 입력 생성.

    Args:
        locale_document: 검증할 최종 locale 문서.
        english_view: stale-link 보정이 적용된 영어 비교 기준.
        annotation_source: stale-link 보정 전 annotation 소유 기준 원문.
        version: 문서 버전.
        registry_sha256: 비교에 사용한 stale-link registry digest.
        expected_annotation_map: 호출자가 미리 구성한 예상 map. 제공하면 ``annotation_source``에서 다시 만든 map과 같아야 함.

    Returns:
        Canonical envelope와 SHA-256 digest가 포함된 불변 입력.

    Raises:
        ValueError: 문서, 버전, registry digest 또는 annotation map이 계약을 위반한 경우.
    """

    try:
        version = validate_version_token(version)
    except ValueError as exc:
        raise ValueError("invalid verification version") from exc
    if (
        not isinstance(registry_sha256, str)
        or _SHA256_RE.fullmatch(registry_sha256) is None
    ):
        raise ValueError("invalid stale-link registry digest")
    if not isinstance(locale_document, (str, bytes)):
        raise ValueError("locale document must be UTF-8 text or bytes")
    if not isinstance(english_view, (str, bytes)):
        raise ValueError("English verification view must be UTF-8 text or bytes")
    try:
        locale_bytes = (
            locale_document.encode("utf-8")
            if isinstance(locale_document, str)
            else bytes(locale_document)
        )
        english_view_bytes = (
            english_view.encode("utf-8")
            if isinstance(english_view, str)
            else bytes(english_view)
        )
    except UnicodeEncodeError as exc:
        raise ValueError("verification documents must be UTF-8") from exc
    source_annotation_map = build_expected_annotation_map(annotation_source)
    if expected_annotation_map is None:
        expected_annotation_map = source_annotation_map
    elif type(expected_annotation_map) is not ExpectedAnnotationMap:
        raise ValueError("invalid expected annotation map")
    elif expected_annotation_map != source_annotation_map:
        raise ValueError("expected annotation map does not match annotation_source")
    annotation_map_bytes = expected_annotation_map.canonical_bytes()
    envelope = _verification_envelope(
        locale_bytes=locale_bytes,
        english_view_bytes=english_view_bytes,
        annotation_map_bytes=annotation_map_bytes,
        version=version,
        registry_sha256=registry_sha256,
    )
    return VerificationInput(
        locale_bytes=locale_bytes,
        english_view_bytes=english_view_bytes,
        annotation_map_bytes=annotation_map_bytes,
        version=version,
        registry_sha256=registry_sha256,
        envelope_bytes=envelope,
        verification_input_sha256=hashlib.sha256(envelope).hexdigest(),
    )


def _issue(
    code: str,
    structural_address: str | None,
    message: str,
) -> VerificationIssue:
    """검증 문제 생성."""

    return VerificationIssue(code, structural_address, message)


def _issue_key(issue: VerificationIssue) -> tuple[bytes, bytes, bytes]:
    """검증 문제의 결정적 UTF-8 정렬 키 반환."""

    return (
        _utf8(issue.code),
        _utf8(issue.structural_address or ""),
        _utf8(issue.message),
    )


def _stable_issues(
    issues: Iterable[VerificationIssue],
) -> tuple[VerificationIssue, ...]:
    """문제를 코드·구조 주소로 중복 제거하고 결정적으로 정렬."""

    unique: dict[tuple[str, str | None], VerificationIssue] = {}
    for issue in sorted(issues, key=_issue_key):
        unique.setdefault((issue.code, issue.structural_address), issue)
    return tuple(sorted(unique.values(), key=_issue_key))


def _input_integrity_issues(inputs: object) -> list[VerificationIssue]:
    """검증 입력의 타입, canonical 바이트와 digest 무결성 검사."""

    if type(inputs) is not VerificationInput:
        return [
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                _INVALID_VERIFICATION_INPUT,
            )
        ]
    assert isinstance(inputs, VerificationInput)
    if not (
        type(inputs.locale_bytes) is bytes
        and type(inputs.english_view_bytes) is bytes
        and type(inputs.annotation_map_bytes) is bytes
        and type(inputs.version) is str
        and type(inputs.registry_sha256) is str
        and type(inputs.envelope_bytes) is bytes
        and type(inputs.verification_input_sha256) is str
    ):
        return [
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                _INVALID_VERIFICATION_INPUT,
            )
        ]
    try:
        inputs.locale_bytes.decode("utf-8")
        inputs.english_view_bytes.decode("utf-8")
        parse_expected_annotation_map(inputs.annotation_map_bytes)
        validate_version_token(inputs.version)
    except (UnicodeDecodeError, ValueError):
        return [
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                _INVALID_VERIFICATION_INPUT,
            )
        ]
    if (
        _SHA256_RE.fullmatch(inputs.registry_sha256) is None
        or _SHA256_RE.fullmatch(inputs.verification_input_sha256) is None
    ):
        return [
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                _INVALID_VERIFICATION_INPUT,
            )
        ]
    expected_envelope = _verification_envelope(
        locale_bytes=inputs.locale_bytes,
        english_view_bytes=inputs.english_view_bytes,
        annotation_map_bytes=inputs.annotation_map_bytes,
        version=inputs.version,
        registry_sha256=inputs.registry_sha256,
    )
    if (
        inputs.envelope_bytes != expected_envelope
        or hashlib.sha256(inputs.envelope_bytes).hexdigest()
        != inputs.verification_input_sha256
    ):
        return [
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                "verification input digest does not match its canonical envelope",
            )
        ]
    return []


def _canonical_source_annotations(source: str) -> tuple[str, ...]:
    """원문 소유 단위에서 canonical annotation 문자열 생성."""

    return tuple(
        f"<!-- {comment.replace('-->', '--&gt;')} -->"
        for comment in response_contract._required_comments(source)
    )


def _pipeline_annotation_owner_invalid(
    masked: str,
    *,
    start: int,
    end: int,
    normalized: str,
    table_annotations: frozenset[str],
) -> bool:
    """pipeline annotation의 독립 줄 배치와 다음 구조 소유자 검증.

    Args:
        masked: 코드 펜스가 제거된 locale 문서.
        start: 주석 시작 위치.
        end: 주석 끝 위치.
        normalized: 정규화된 주석 본문.
        table_annotations: 표 소유 주석 본문 집합.

    Returns:
        annotation 소유 위치가 잘못됐는지 여부.
    """

    line_start = masked.rfind("\n", 0, start) + 1
    prefix = masked[line_start:start]
    line_end = masked.find("\n", end)
    if line_end < 0:
        line_end = len(masked)
    suffix = masked[end:line_end].removesuffix("\r")
    if prefix or suffix:
        return True
    following = legacy_verify._line_after_comment(masked, end)
    if following is None:
        return True
    return _pipeline_following_owner_invalid(
        masked,
        line_start=line_start,
        following=following[0],
        normalized=normalized,
        table_annotations=table_annotations,
    )


def _pipeline_following_owner_invalid(
    masked: str,
    *,
    line_start: int,
    following: str,
    normalized: str,
    table_annotations: frozenset[str],
) -> bool:
    """pipeline annotation 다음 줄의 구조 종류와 내용 검증.

    Args:
        masked: 코드 펜스가 제거된 locale 문서.
        line_start: annotation 물리 줄 시작 위치.
        following: annotation 다음 물리 줄.
        normalized: 정규화된 주석 본문.
        table_annotations: 표 소유 주석 본문 집합.

    Returns:
        다음 구조 소유자가 잘못됐는지 여부.
    """

    following_line = following.lstrip()
    heading = _HEADING_ANNOTATION_RE.fullmatch(normalized) is not None
    table = normalized in table_annotations
    previous_lines = masked[:line_start].splitlines()
    previous_line = previous_lines[-1] if previous_lines else ""
    if not following_line or following_line.startswith("<!--"):
        return True
    if heading and not legacy_verify._structural_line_matches(
        strip_title_attr_line(normalized),
        following,
    ):
        return True
    if not heading and not table and following_line.startswith(("#", "|", ">")):
        return True
    if table and ("|" not in following_line or "|" in previous_line):
        return True
    if _LIST_ANNOTATION_RE.match(normalized) and not _LIST_ANNOTATION_RE.match(
        following_line
    ):
        return True
    expected_kind = response_contract._annotation_owner_kind(
        normalized,
        table_annotations,
    )
    actual_kind = response_contract._following_owner_kind(
        following,
        table_expected=expected_kind == "table",
        allow_indented=False,
    )
    return actual_kind != expected_kind


def _actual_pipeline_annotations(
    text: str,
    source: str,
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    """Locale 문서의 pipeline annotation과 소유 위치가 잘못된 annotation 인덱스 수집."""

    masked = mask_fenced_code_contents(text)
    table_annotations = response_contract._required_table_comments(source)
    positions = legacy_verify._comment_positions(text)
    source_indexes = legacy_verify._source_comment_indexes(positions, source)
    source_indexes = source_indexes or set()
    annotations: list[str] = []
    invalid_owners: list[int] = []
    for index, (start, end, body) in enumerate(html_comment_spans(masked)):
        if index in source_indexes:
            continue
        raw_annotation = masked[start:end]
        annotation_match = _ANNOTATION_RE.fullmatch(raw_annotation)
        if annotation_match is None:
            continue
        normalized = response_contract._normalize_comment(
            annotation_match.group(1)
        )
        line_start = masked.rfind("\n", 0, start) + 1
        prefix = masked[line_start:start]
        # 기존 인용 블록이 소유한 annotation은 호환 형식으로 유지하며 현재 expected annotation map의 owner entry에는 포함하지 않음.
        if re.fullmatch(r"[ \t]*(?:>[ \t]*)+", prefix):
            continue
        annotations.append(raw_annotation)
        annotation_index = len(annotations) - 1
        if _pipeline_annotation_owner_invalid(
            masked,
            start=start,
            end=end,
            normalized=normalized,
            table_annotations=table_annotations,
        ):
            invalid_owners.append(annotation_index)

    return tuple(annotations), tuple(invalid_owners)


def _first_annotation_mismatch_address(
    expected_map: ExpectedAnnotationMap,
    actual_map: ExpectedAnnotationMap | None,
    invalid_owners: tuple[int, ...],
) -> str:
    """첫 annotation 불일치의 안정적인 구조 주소 반환."""

    mismatches = set(invalid_owners)
    for index in range(
        max(
            len(expected_map.entries),
            len(actual_map.entries) if actual_map is not None else 0,
        )
    ):
        expected = (
            expected_map.entries[index]
            if index < len(expected_map.entries)
            else None
        )
        actual = (
            actual_map.entries[index]
            if actual_map is not None and index < len(actual_map.entries)
            else None
        )
        if expected != actual:
            mismatches.add(index)
    first = min(mismatches, default=0)
    if first < len(expected_map.entries):
        return expected_map.entries[first].structural_address
    return "annotations"


def _optional_quote_comment_is_preserved(
    *,
    body: str,
    start_line: int,
    end_line: int,
    depth: int,
    lines: list[str],
    optional: dict[tuple[str, int, int], int],
) -> bool:
    """선택적 인용 annotation의 깊이·순번·다음 본문 보존 여부 검증.

    Args:
        body: HTML 주석 본문.
        start_line: 주석 시작 줄 위치.
        end_line: 주석 마지막 줄 위치.
        depth: 인용 깊이.
        lines: locale 문서 줄.
        optional: 원문에서 허용한 선택적 인용 annotation 횟수.

    Returns:
        선택적 인용 주석 계약 충족 여부.
    """

    normalized = response_contract._normalize_comment(body)
    key = (
        normalized,
        depth,
        response_contract._quote_block_ordinal(lines, start_line + 1),
    )
    next_line = end_line + 1
    if next_line >= len(lines):
        return False
    next_body = lines[next_line].lstrip()
    while next_body.startswith(">"):
        next_body = next_body[1:].lstrip()
    if (
        not response_contract._optional_quote_annotation_starts_block(
            lines,
            start_line,
        )
        or not optional[key]
        or response_contract._quote_depth(lines[next_line]) != depth
        or not next_body
    ):
        return False
    optional[key] -= 1
    return True


def _non_source_comment_is_valid(
    masked: str,
    *,
    start: int,
    end: int,
    body: str,
    record: tuple[str, int, int, object],
    lines: list[str],
    optional: dict[tuple[str, int, int], int],
) -> bool:
    """원문 작성 주석이 아닌 annotation 또는 선택적 인용 주석 검증.

    Args:
        masked: 코드 펜스가 제거된 locale 문서.
        start: 주석 시작 문자 위치.
        end: 주석 끝 문자 위치.
        body: HTML 주석 본문.
        record: 주석 본문·시작 줄·끝 줄·위치 레코드.
        lines: locale 문서 줄.
        optional: 허용된 선택적 인용 주석 횟수.

    Returns:
        pipeline 또는 선택적 인용 주석으로 유효한지 여부.
    """

    _record_body, start_line, end_line, _position = record
    match = (
        response_contract._ONE_LINE_COMMENT_RE.fullmatch(lines[start_line])
        if start_line == end_line and start_line < len(lines)
        else None
    )
    depth = response_contract._quote_depth(match.group(1)) if match else 0
    if depth:
        return _optional_quote_comment_is_preserved(
            body=body,
            start_line=start_line,
            end_line=end_line,
            depth=depth,
            lines=lines,
            optional=optional,
        )
    return _ANNOTATION_RE.fullmatch(masked[start:end]) is not None


def _source_authored_comments_are_preserved(text: str, source: str) -> bool:
    """원문 작성 HTML comment의 값·순서·소유 위치 보존 여부."""

    preserved, source_indexes = response_contract._matched_source_comment_indexes(
        text,
        source,
    )
    if not preserved:
        return False

    masked = mask_fenced_code_contents(text)
    spans = html_comment_spans(masked)
    records = response_contract._comment_records(text)
    if len(spans) != len(records):
        return False
    optional = response_contract._optional_quoted_comments(source)
    lines = text.splitlines()
    for index, ((start, end, body), record) in enumerate(
        zip(spans, records, strict=True)
    ):
        if index in source_indexes:
            continue
        if not _non_source_comment_is_valid(
            masked,
            start=start,
            end=end,
            body=body,
            record=record,
            lines=lines,
            optional=optional,
        ):
            return False
    return True


def _legacy_issue(label: str) -> VerificationIssue:
    """기존 verifier label을 안정적인 문서 검증 문제로 변환."""

    if label.startswith("front matter"):
        return _issue("FRONT_MATTER_MISMATCH", "front-matter", label)
    if "list" in label or "table" in label:
        return _issue(
            "LIST_TABLE_STRUCTURE_MISMATCH",
            "list-or-table",
            label,
        )
    if label in {
        "unreplaced {{version}}",
        "unrestored base64 placeholder",
        "legacy note marker",
        "unclosed img tag",
        "title style class",
    }:
        return _issue("RESIDUAL_PATTERN", "document", label)
    if "source comment" in label or label == "missing original comment":
        return _issue("SOURCE_COMMENT_MISMATCH", "comments", label)
    return _issue("SOURCE_STRUCTURE_MISMATCH", "document", label)


def _snapshot_changed(
    initial: VerificationInput,
    final: VerificationInput,
) -> bool:
    """시작·종료 검증 입력의 canonical 값 변경 여부."""

    return bool(
        _input_integrity_issues(final)
        or (
            initial.locale_bytes,
            initial.english_view_bytes,
            initial.annotation_map_bytes,
            initial.version,
            initial.registry_sha256,
            initial.envelope_bytes,
            initial.verification_input_sha256,
        )
        != (
            final.locale_bytes,
            final.english_view_bytes,
            final.annotation_map_bytes,
            final.version,
            final.registry_sha256,
            final.envelope_bytes,
            final.verification_input_sha256,
        )
    )


def _registry_snapshot_is_valid(registry: object) -> bool:
    """Registry 객체가 canonical 원본 바이트와 규칙에 일치하는지 검사."""

    if not (
        type(registry) is StaleLinkRegistry
        and type(registry.raw) is bytes
        and type(registry.sha256) is str
        and type(registry.rules) is tuple
        and _SHA256_RE.fullmatch(registry.sha256)
        and hashlib.sha256(registry.raw).hexdigest() == registry.sha256
    ):
        return False
    try:
        value = stale_links._decode_registry(registry.raw)
        schema_version = value["schema_version"]
        entries = value["links"]
        if (
            type(schema_version) is not int
            or schema_version != stale_links.SCHEMA_VERSION
            or not isinstance(entries, list)
        ):
            return False
        rules = [
            stale_links._parse_rule(entry, index)
            for index, entry in enumerate(entries)
        ]
        stale_links._validate_rules(rules, registry.raw, value)
    except (stale_links.StaleLinkRegistryError, UnicodeEncodeError):
        return False
    return bool(
        all(
            type(rule) is stale_links.StaleLinkRule
            and type(rule.version) is str
            and type(rule.source) is str
            and (rule.target is None or type(rule.target) is str)
            and (rule.retire_mode is None or type(rule.retire_mode) is str)
            for rule in registry.rules
        )
        and tuple(
            (rule.version, rule.source, rule.target, rule.retire_mode)
            for rule in registry.rules
        )
        == tuple(
            (rule.version, rule.source, rule.target, rule.retire_mode)
            for rule in rules
        )
    )


_FINAL_STAGE_EXCLUDED_LEGACY_ISSUES = frozenset(
    {
        # 최종 검증의 pipeline annotation 바이트와 occurrence는 stale-link 보정 이후 영어 view가 아닌 expected annotation map이 소유.
        "missing original comment",
        "source comment mismatch",
        # 문장 수와 미번역 원문은 live 응답 평가에서 검사.
        # 최종 candidate 검증은 provider 독립적으로 재현 가능한 구조 검사만 수행.
        "sentence cardinality mismatch",
        "untranslated source text",
    }
)


def _document_structure_issues(source: str, text: str) -> tuple[list[VerificationIssue], bool]:
    """머리말·목록·표·인용·블록 구조 차이 검사.

    Args:
        source: 최종 영어 view.
        text: locale 번역 문서.

    Returns:
        구조 문제 목록과 블록 구조 불일치 여부.
    """

    issues: list[VerificationIssue] = []
    source_front_matter = front_matter_contract(source)
    translated_front_matter = front_matter_contract(text)
    if (
        not source_front_matter.valid
        or not translated_front_matter.valid
        or source_front_matter.present != translated_front_matter.present
        or source_front_matter.signature != translated_front_matter.signature
    ):
        issues.append(
            _issue(
                "FRONT_MATTER_MISMATCH",
                "front-matter",
                "front matter key order, scalar structure, or source-owned value differs",
            )
        )
    if (
        list_structure_signature(source) != list_structure_signature(text)
        or table_structure_signature(source) != table_structure_signature(text)
    ):
        issues.append(
            _issue(
                "LIST_TABLE_STRUCTURE_MISMATCH",
                "list-or-table",
                "list or table ordered structural signature differs",
            )
        )
    if blockquote_structure_signature(source) != blockquote_structure_signature(text):
        issues.append(
            _issue(
                "SOURCE_STRUCTURE_MISMATCH",
                "blockquote",
                "blockquote depth, occurrence, or hard-break structure differs",
            )
        )
    block_mismatch = tuple(
        response_contract._signature(block)
        for block in response_contract._blocks(source)
    ) != tuple(
        response_contract._signature(block)
        for block in response_contract._blocks(text)
    )
    if block_mismatch:
        issues.append(
            _issue(
                "SOURCE_STRUCTURE_MISMATCH",
                "document-blocks",
                "Markdown block kind, order, or structural layout differs",
            )
        )
    return issues, block_mismatch


def _pipeline_annotation_issues(
    text: str,
    source: str,
    expected_map: ExpectedAnnotationMap,
    *,
    block_mismatch: bool,
) -> list[VerificationIssue]:
    """pipeline annotation 바이트·순서·소유 위치를 expected map과 비교.

    Args:
        text: locale 번역 문서.
        source: 최종 영어 view.
        expected_map: 원문 소유 단위별 기대 annotation map.
        block_mismatch: 문서 블록 구조 불일치 여부.

    Returns:
        annotation 문제 목록.
    """

    actual_annotations, invalid_owners = _actual_pipeline_annotations(text, source)
    if block_mismatch and expected_map.entries:
        invalid_owners = (*invalid_owners, len(actual_annotations))
    try:
        actual_map = _map_from_canonical_annotations(actual_annotations)
    except ValueError:
        actual_map = None
    if actual_map == expected_map and not invalid_owners:
        return []
    address = _first_annotation_mismatch_address(
        expected_map,
        actual_map,
        invalid_owners,
    )
    return [
        _issue(
            "PIPELINE_ANNOTATION_MISMATCH",
            address,
            "pipeline annotation byte, order, occurrence, or owner differs",
        )
    ]


def _legacy_document_issues(
    text: str,
    source: str,
    version: str,
    registry: StaleLinkRegistry,
) -> list[VerificationIssue]:
    """원문 작성 주석과 기존 구조 verifier 호환 계약 검사.

    Args:
        text: locale 번역 문서.
        source: 최종 영어 view.
        version: 문서 버전.
        registry: 시작 시점 오래된 링크 registry.

    Returns:
        원문 주석과 기존 verifier 문제 목록.
    """

    issues: list[VerificationIssue] = []
    if not _source_authored_comments_are_preserved(text, source):
        issues.append(
            _issue(
                "SOURCE_COMMENT_MISMATCH",
                "comments",
                "source-authored comment value, order, or structural address differs",
            )
        )
    legacy_issues = legacy_verify.verify(
        text,
        source=source,
        version=version,
        registry=registry,
    )
    issues.extend(
        _legacy_issue(label)
        for label in legacy_issues
        if label not in _FINAL_STAGE_EXCLUDED_LEGACY_ISSUES
    )
    return issues


def _capture_final_snapshot(
    final_snapshot: Callable[[], tuple[VerificationInput, StaleLinkRegistry]] | None,
) -> tuple[
    VerificationInput | None,
    StaleLinkRegistry | None,
    list[VerificationIssue],
]:
    """종료 시점 검증 입력과 registry를 정확히 한 번 다시 구성.

    Args:
        final_snapshot: 소유 원본에서 종료 snapshot을 구성하는 callback.

    Returns:
        종료 검증 입력, registry, snapshot 문제 목록.
    """

    issues: list[VerificationIssue] = []
    if not callable(final_snapshot):
        issues.append(
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                "verification final snapshot could not be rebuilt",
            )
        )
        return None, None, issues
    try:
        captured = final_snapshot()
    except stale_links.StaleLinkRegistryError:
        issues.append(
            _issue(
                "STALE_LINK_REGISTRY_CHANGED",
                "stale-link-registry",
                "stale-link registry could not be reloaded after verification",
            )
        )
        return None, None, issues
    except Exception:
        issues.append(
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                "verification final snapshot could not be rebuilt",
            )
        )
        return None, None, issues
    if type(captured) is tuple and len(captured) == 2:
        return captured[0], captured[1], issues
    issues.append(
        _issue(
            "VERIFICATION_INPUT_CHANGED",
            "verification-input",
            "verification final snapshot is invalid",
        )
    )
    return None, None, issues


def _final_snapshot_issues(
    inputs: VerificationInput,
    registry_at_start: StaleLinkRegistry | None,
    final_input: VerificationInput | None,
    registry_at_end: StaleLinkRegistry | None,
) -> list[VerificationIssue]:
    """종료 snapshot의 독립 객체·입력 불변·registry digest 계약 검사.

    Args:
        inputs: 시작 검증 입력.
        registry_at_start: 시작 registry snapshot.
        final_input: 종료 검증 입력.
        registry_at_end: 종료 registry snapshot.

    Returns:
        종료 snapshot 문제 목록.
    """

    issues: list[VerificationIssue] = []
    if (
        type(final_input) is not VerificationInput
        or final_input is inputs
        or _snapshot_changed(inputs, final_input)
    ):
        issues.append(
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                "verification input changed before artifact creation",
            )
        )
    if (
        type(registry_at_end) is not StaleLinkRegistry
        or registry_at_end is registry_at_start
        or not _registry_snapshot_is_valid(registry_at_end)
        or registry_at_end.sha256 != inputs.registry_sha256
    ):
        issues.append(
            _issue(
                "STALE_LINK_REGISTRY_CHANGED",
                "stale-link-registry",
                "stale-link registry changed during document verification",
            )
        )
    return issues


def verify_document(
    inputs: VerificationInput,
    *,
    registry_at_start: StaleLinkRegistry | None = None,
    final_snapshot: Callable[
        [], tuple[VerificationInput, StaleLinkRegistry]
    ]
    | None = None,
) -> VerificationResult:
    """문서 구조와 종료 snapshot을 검증하고 안전한 산출물 반환.

    Args:
        inputs: 시작 시점의 canonical 검증 입력.
        registry_at_start: 영어 view와 링크 비교에 사용한 registry snapshot.
        final_snapshot: 산출물 생성 직전에 소유 원본에서 검증 입력과 registry를 다시 구성하는 callback. 정확히 한 번 호출.

    Returns:
        검증 결과. 문제가 없으면 hash에 결속된 locale 산출물 포함.
    """

    integrity_issues = _input_integrity_issues(inputs)
    reported_input_hash = (
        None if integrity_issues else inputs.verification_input_sha256
    )
    issues = list(integrity_issues)
    if not callable(final_snapshot):
        issues.append(
            _issue(
                "VERIFICATION_INPUT_CHANGED",
                "verification-input",
                "verification start and end snapshots are required",
            )
        )
    if type(registry_at_start) is not StaleLinkRegistry:
        issues.append(
            _issue(
                "STALE_LINK_REGISTRY_CHANGED",
                "stale-link-registry",
                "stale-link registry start snapshot is invalid",
            )
        )
    if (
        type(inputs) is VerificationInput
        and type(registry_at_start) is StaleLinkRegistry
        and (
            not _registry_snapshot_is_valid(registry_at_start)
            or registry_at_start.sha256 != inputs.registry_sha256
        )
    ):
        issues.append(
            _issue(
                "STALE_LINK_REGISTRY_CHANGED",
                "stale-link-registry",
                "stale-link registry changed before document verification",
            )
        )
    if issues:
        return VerificationResult(
            issues=_stable_issues(issues),
            verification_input_sha256=reported_input_hash,
            artifact=None,
        )

    source = inputs.english_view_bytes.decode("utf-8")
    text = inputs.locale_bytes.decode("utf-8")
    expected_map = parse_expected_annotation_map(inputs.annotation_map_bytes)

    structure_issues, block_structure_mismatch = _document_structure_issues(
        source,
        text,
    )
    issues.extend(structure_issues)
    issues.extend(
        _pipeline_annotation_issues(
            text,
            source,
            expected_map,
            block_mismatch=block_structure_mismatch,
        )
    )
    if type(registry_at_start) is StaleLinkRegistry:
        issues.extend(
            _legacy_document_issues(
                text,
                source,
                inputs.version,
                registry_at_start,
            )
        )

    final_input, registry_at_end, snapshot_issues = _capture_final_snapshot(
        final_snapshot
    )
    issues.extend(snapshot_issues)
    issues.extend(
        _final_snapshot_issues(
            inputs,
            registry_at_start,
            final_input,
            registry_at_end,
        )
    )

    issues.extend(_input_integrity_issues(inputs))
    stable = _stable_issues(issues)
    if stable:
        return VerificationResult(
            issues=stable,
            verification_input_sha256=reported_input_hash,
            artifact=None,
        )
    return VerificationResult(
        issues=(),
        verification_input_sha256=reported_input_hash,
        artifact=VerifiedLocaleArtifact(
            schema_version=1,
            locale_bytes=inputs.locale_bytes,
            version=inputs.version,
            registry_sha256=inputs.registry_sha256,
            verification_input_sha256=inputs.verification_input_sha256,
        ),
    )


__all__ = (
    "ExpectedAnnotationEntry",
    "ExpectedAnnotationMap",
    "VerificationInput",
    "VerificationIssue",
    "VerificationResult",
    "VerifiedLocaleArtifact",
    "build_expected_annotation_map",
    "create_verification_input",
    "parse_expected_annotation_map",
    "verify_document",
)
