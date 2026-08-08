"""보존된 Markdown markup의 선택적 복구 도구.

본문을 번역하지 않고 영어 원문과 동일해야 하는 heading, Markdown 링크·이미지,
inline code, named anchor와 목록 표식만 복구.
"""
from __future__ import annotations

import re
from collections.abc import Hashable, Iterator, Sequence
from dataclasses import dataclass, field

from ..common.markdown import (
    closes_fence,
    fence_token,
    is_heading_line,
    is_named_anchor_line,
    markdown_links,
    strip_html_comments,
    strip_title_attr_line,
)

_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_LIST_ITEM_RE = re.compile(r"^(\s*)([-*+])(\s+)(\S.*)$")


class RepairError(ValueError):
    """원문과 번역 Markdown의 구조가 일치하지 않는 복구 오류."""


@dataclass(frozen=True)
class RepairResult:
    """복구된 Markdown과 실제 변경 여부."""

    text: str
    changed: bool


@dataclass
class _RepairState:
    """문서 순회 중 남은 원문 markup과 보호 범위 상태."""

    source_headings: Iterator[str]
    source_links: Iterator[tuple[str, str, str]]
    source_images: Iterator[tuple[str, str]] = field(default_factory=lambda: iter(()))
    source_inline_codes: list[str] = field(default_factory=list)
    source_inline_index: int = 0
    in_code: bool = False
    fence: str = ""
    in_comment: bool = False


def _split_line_ending(line: str) -> tuple[str, str]:
    """문자열을 본문과 원래 줄바꿈 구분자로 분리."""

    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def _heading_lines(text: str) -> list[str]:
    """code와 HTML 주석 밖의 heading을 class 없는 원문 줄로 추출."""

    headings: list[str] = []
    for line in strip_html_comments(_without_code_blocks(text)).splitlines():
        if is_heading_line(line):
            headings.append(strip_title_attr_line(line).strip())
    return headings


def _links(text: str) -> list[tuple[str, str, str]]:
    """code와 HTML 주석 밖의 Markdown 링크 label·target·title 추출."""

    return [
        (" ".join(link.label.split()), link.target, link.title)
        for link in markdown_links(strip_html_comments(_without_code_blocks(text)))
        if not link.image
    ]


def _images(text: str) -> list[tuple[str, str]]:
    """code와 HTML 주석 밖의 Markdown 이미지 target·title 추출."""

    return [
        (link.target, link.title)
        for link in markdown_links(strip_html_comments(_without_code_blocks(text)))
        if link.image
    ]


def _inline_codes(text: str) -> list[str]:
    """주석·fenced code·heading 밖의 inline code 내용 추출."""

    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    codes: list[str] = []
    for line in text.splitlines():
        if _is_comment_line(line, state) or _is_code_line(line, state):
            continue
        if is_heading_line(line):
            continue
        codes.extend(match.group(1) for match in _INLINE_CODE_RE.finditer(line))
    return codes


def _without_code_blocks(text: str) -> str:
    """fenced code 블록 전체를 제외한 Markdown 반환."""

    out: list[str] = []
    in_code = False
    fence = ""
    for line in text.splitlines(keepends=True):
        token = fence_token(line)
        if token:
            if not in_code:
                in_code, fence = True, token
                continue
            if closes_fence(line, fence):
                in_code = False
                continue
        if not in_code:
            out.append(line)
    return "".join(out)


def _contains_reordered_values(
    source: Sequence[Hashable],
    translated: Sequence[Hashable],
) -> bool:
    """서로 다른 위치의 값 집합이 교차해 기존 markup이 재배치됐는지 판정."""

    mismatched = [
        (source_value, translated_value)
        for source_value, translated_value in zip(source, translated)
        if source_value != translated_value
    ]
    return bool(
        {source_value for source_value, _translated_value in mismatched}
        & {translated_value for _source_value, translated_value in mismatched}
    )


def _replace_links(
    line: str,
    links: Iterator[tuple[str, str, str]],
    images: Iterator[tuple[str, str]],
) -> str:
    """번역 줄의 링크·이미지 markup을 대응하는 원문 값으로 복구."""

    out: list[str] = []
    index = 0
    for link in markdown_links(line):
        out.append(line[index : link.start])
        if link.image:
            try:
                target, title = next(images)
            except StopIteration as exc:
                raise RepairError(
                    "translated document has more Markdown images than source"
                ) from exc
            out.append(f"![{link.label}]({target}{title})")
            index = link.end
            continue
        try:
            label, target, title = next(links)
        except StopIteration as exc:
            raise RepairError(
                "translated document has more Markdown links than source"
            ) from exc
        out.append(f"[{label}]({target}{title})")
        index = link.end
    out.append(line[index:])
    return "".join(out)


def restore_blank_markdown_link_labels(source: str, translated: str) -> RepairResult:
    """번역문에서 비어 있는 Markdown 링크 label만 대응 원문에서 복원.

    Raises:
        RepairError: 원문과 번역문의 링크 수 불일치.
    """

    source_links = _links(source)
    translated_links = _links(translated)
    if len(source_links) != len(translated_links):
        raise RepairError(
            "translated document has a different number of Markdown links"
        )

    link_index = 0
    changed = False
    out: list[str] = []
    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    for original_line in translated.splitlines(keepends=True):
        if _is_comment_line(original_line, state) or _is_code_line(
            original_line,
            state,
        ):
            out.append(original_line)
            continue

        line: list[str] = []
        cursor = 0
        for link in markdown_links(original_line):
            line.append(original_line[cursor : link.start])
            if link.image:
                line.append(original_line[link.start : link.end])
                cursor = link.end
                continue
            source_label, _source_target, _source_title = source_links[link_index]
            link_index += 1
            if not " ".join(link.label.split()) and source_label:
                line.append(f"[{source_label}]({link.target}{link.title})")
                changed = True
            else:
                line.append(original_line[link.start : link.end])
            cursor = link.end
        line.append(original_line[cursor:])
        out.append("".join(line))

    if link_index != len(source_links):
        raise RepairError("translated document has fewer Markdown links than source")
    return RepairResult(text="".join(out), changed=changed)


def _next_inline_code(state: _RepairState) -> str:
    """원문 순서의 다음 inline code 내용을 반환하고 위치 전진."""

    if state.source_inline_index >= len(state.source_inline_codes):
        raise RepairError("translated document has more inline code spans than source")
    code = state.source_inline_codes[state.source_inline_index]
    state.source_inline_index += 1
    return code


def _replace_inline_codes(line: str, state: _RepairState) -> str:
    """번역 줄의 inline code를 원문 순서로 복구하고 누락된 구분자 보완."""

    def replace(_match: re.Match[str]) -> str:
        """현재 inline code span을 다음 원문 내용으로 교체."""

        return f"`{_next_inline_code(state)}`"

    repaired = _INLINE_CODE_RE.sub(replace, line)
    while state.source_inline_index < len(state.source_inline_codes):
        code = state.source_inline_codes[state.source_inline_index]
        wrapped = _wrap_first_raw_inline_code(repaired, code)
        if wrapped == repaired:
            break
        state.source_inline_index += 1
        repaired = wrapped
    return repaired


def _wrap_first_raw_inline_code(line: str, code: str) -> str:
    """기존 inline code 밖에서 유일하게 일치하는 원문 token을 backtick으로 감쌈."""

    if not code:
        return line

    positions: list[int] = []
    cursor = 0
    for match in _INLINE_CODE_RE.finditer(line):
        segment = line[cursor : match.start()]
        positions.extend(
            cursor + position
            for position in _raw_code_positions(segment, code)
        )
        cursor = match.end()

    positions.extend(
        cursor + position
        for position in _raw_code_positions(line[cursor:], code)
    )
    if not positions:
        return line
    if len(positions) > 1:
        raise RepairError(f"translated document has ambiguous raw inline code: {code}")
    start = positions[0]
    end = start + len(code)
    return f"{line[:start]}`{code}`{line[end:]}"


def _raw_code_positions(segment: str, code: str) -> list[int]:
    """일반 문자열 구간에서 식별자 경계가 분명한 원문 token 위치 추출."""

    positions: list[int] = []
    start = segment.find(code)
    while start != -1:
        end = start + len(code)
        if _has_raw_code_boundaries(segment, start, end):
            positions.append(start)
        start = segment.find(code, start + 1)
    return positions


def _has_raw_code_boundaries(segment: str, start: int, end: int) -> bool:
    """원문 token 앞뒤가 식별자 경계인지 여부."""

    before = segment[start - 1] if start > 0 else ""
    after = segment[end] if end < len(segment) else ""
    return not _is_identifier_char(before) and not _is_identifier_char(after)


def _is_identifier_char(char: str) -> bool:
    """문자가 기술 식별자의 일부로 해석되는지 여부."""

    return char.isalnum() or char in {"_", "\\"}


def _comment_candidate(line: str) -> str:
    """blockquote 표식을 제거한 HTML 주석 판정 대상 반환."""

    candidate = line.lstrip()
    while candidate.startswith(">"):
        candidate = candidate[1:].lstrip()
    return candidate


def _is_comment_line(line: str, state: _RepairState) -> bool:
    """줄이 HTML 주석 범위에 속하는지 판정하고 순회 상태 갱신."""

    if state.in_comment:
        if "-->" in line:
            state.in_comment = False
        return True

    candidate = _comment_candidate(line)
    if not candidate.startswith("<!--"):
        return False

    state.in_comment = "-->" not in candidate
    return True


def _is_code_line(line: str, state: _RepairState) -> bool:
    """줄이 fenced code 범위에 속하는지 판정하고 순회 상태 갱신."""

    token = fence_token(line)
    if token:
        if not state.in_code:
            state.in_code = True
            state.fence = token
        elif closes_fence(line, state.fence):
            state.in_code = False
            state.fence = ""
        return True

    return state.in_code


def _repair_heading_line(ending: str, state: _RepairState) -> str:
    """다음 원문 heading과 번역 줄의 기존 줄바꿈 결합."""

    try:
        source_heading = next(state.source_headings)
    except StopIteration as exc:
        raise RepairError("translated document has more headings than source") from exc
    return source_heading + ending


def _repair_translated_line(original_line: str, state: _RepairState) -> str:
    """단일 번역 줄의 보호 markup을 원문 순서로 복구."""

    line, ending = _split_line_ending(original_line)

    if _is_comment_line(line, state) or _is_code_line(line, state):
        return original_line

    if is_heading_line(line):
        return _repair_heading_line(ending, state)

    return _replace_inline_codes(
        _replace_links(original_line, state.source_links, state.source_images),
        state,
    )


def _ensure_exhausted(iterator: Iterator, message: str) -> None:
    """원문 markup iterator가 모두 소비됐는지 확인."""

    try:
        next(iterator)
    except StopIteration:
        return
    raise RepairError(message)


def _ensure_inline_codes_exhausted(state: _RepairState) -> None:
    """원문의 inline code가 모두 번역문에 대응됐는지 확인."""

    if state.source_inline_index < len(state.source_inline_codes):
        raise RepairError("translated document has fewer inline code spans than source")


def _visible_lines(text: str) -> list[str]:
    """HTML 주석과 fenced code를 제외한 표시 줄 추출."""

    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    lines: list[str] = []
    for line in text.splitlines():
        if _is_comment_line(line, state) or _is_code_line(line, state):
            continue
        lines.append(line)
    return lines


def _anchor_lines(text: str) -> list[str]:
    """표시 영역의 named anchor 줄을 문서 순서로 추출."""

    return [line.strip() for line in _visible_lines(text) if is_named_anchor_line(line)]


def _source_anchor_bindings(source: str) -> list[tuple[str, str | None]]:
    """각 원문 named anchor와 뒤따르는 heading 결합."""

    visible = _visible_lines(source)
    bindings: list[tuple[str, str | None]] = []
    for index, line in enumerate(visible):
        if not is_named_anchor_line(line):
            continue
        heading = None
        for next_line in visible[index + 1 :]:
            if is_named_anchor_line(next_line):
                break
            if is_heading_line(next_line):
                heading = strip_title_attr_line(next_line).strip()
                break
        bindings.append((line.strip(), heading))
    return bindings


def _find_heading_index(lines: list[str], heading: str) -> int | None:
    """번역 줄 목록에서 class를 제외한 heading의 위치 탐색."""

    for index, line in enumerate(lines):
        if strip_title_attr_line(line).strip() == heading:
            return index
    return None


def _anchor_insert_index(lines: list[str], heading_index: int) -> int:
    """heading 소유 주석보다 앞선 named anchor 삽입 위치 계산."""

    index = heading_index
    while index > 0 and lines[index - 1].strip().startswith("<!--"):
        index -= 1
    return index


def _repair_anchor_lines(source: str, translated: str) -> RepairResult:
    """누락된 named anchor를 대응 heading과 소유 주석 앞에 복구."""

    source_anchors = _anchor_lines(source)
    if not source_anchors:
        return RepairResult(translated, False)
    if _anchor_lines(translated) == source_anchors:
        return RepairResult(translated, False)

    lines = translated.splitlines()
    present = set(_anchor_lines(translated))
    changed = False
    for anchor, heading in _source_anchor_bindings(source):
        if anchor in present:
            continue
        if heading is None:
            raise RepairError(f"missing translated anchor without heading: {anchor}")
        heading_index = _find_heading_index(lines, heading)
        if heading_index is None:
            raise RepairError(f"missing translated heading for anchor: {heading}")
        lines.insert(_anchor_insert_index(lines, heading_index), anchor)
        present.add(anchor)
        changed = True

    repaired = "\n".join(lines) + ("\n" if translated.endswith("\n") else "")
    if _anchor_lines(repaired) != source_anchors:
        raise RepairError("translated document anchors do not match source")
    return RepairResult(repaired, changed)


def _source_list_markers(source: str) -> list[str] | None:
    """`source`가 순수 unordered list일 때 항목별 marker prefix 추출.

    의미 있는 모든 비주석·비code 줄이 list item인 경우 indent, marker 및
    spacing을 반환하고 그 밖의 경우 ``None`` 반환.
    """
    markers: list[str] = []
    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    for line in source.splitlines():
        if _is_comment_line(line, state) or _is_code_line(line, state):
            continue
        if not line.strip():
            continue
        match = _LIST_ITEM_RE.match(line)
        if not match:
            return None
        markers.append(f"{match.group(1)}{match.group(2)}{match.group(3)}")
    return markers or None


def restore_list_markers(source: str, translated: str) -> str:
    """순수 list 원문 블록에서 누락된 unordered-list marker 재적용.

    원문이 순수 list이고 번역 블록의 내용 줄 수가 같지만 list marker가 적을 때
    원문 marker를 순서대로 추가. 구조를 1:1로 대응할 수 없으면 입력을 그대로
    반환하는 fail-open 처리 후 verification 단계에 불일치 판정 위임.
    """
    markers = _source_list_markers(source)
    if not markers:
        return translated

    lines = translated.splitlines()
    state = _RepairState(source_headings=iter(()), source_links=iter(()))
    content_indexes: list[int] = []
    already_marked = 0
    for index, line in enumerate(lines):
        if _is_comment_line(line, state) or _is_code_line(line, state):
            continue
        if not line.strip():
            continue
        content_indexes.append(index)
        if _LIST_ITEM_RE.match(line):
            already_marked += 1

    if already_marked >= len(markers):
        return translated
    if len(content_indexes) != len(markers):
        return translated

    for marker, index in zip(markers, content_indexes):
        if _LIST_ITEM_RE.match(lines[index]):
            continue
        lines[index] = f"{marker}{lines[index].lstrip()}"

    return "\n".join(lines) + ("\n" if translated.endswith("\n") else "")


def repair_preserved_markup(source: str, translated: str) -> RepairResult:
    """원문의 heading·링크·이미지·inline code·anchor를 번역 Markdown에 복원.

    주석과 fenced code 밖만 변경하며 markup 수가 다르거나 이미 보존된 markup의
    재배치가 감지되면 fail-closed 오류 반환.

    Raises:
        RepairError: markup 수 불일치, 재배치 또는 유일하게 복구할 수 없는 구조.
    """

    source_headings = _heading_lines(source)
    translated_headings = _heading_lines(translated)
    if _contains_reordered_values(source_headings, translated_headings):
        raise RepairError("translated document headings are reordered")

    source_links = _links(source)
    translated_links = _links(translated)
    source_link_destinations = [
        (target, title) for _label, target, title in source_links
    ]
    translated_link_destinations = [
        (target, title) for _label, target, title in translated_links
    ]
    if _contains_reordered_values(
        source_link_destinations,
        translated_link_destinations,
    ):
        raise RepairError("translated Markdown link targets are reordered")

    source_images = _images(source)
    translated_images = _images(translated)
    if _contains_reordered_values(source_images, translated_images):
        raise RepairError("translated Markdown image targets are reordered")

    source_inline_codes = _inline_codes(source)
    translated_inline_codes = _inline_codes(translated)
    if _contains_reordered_values(source_inline_codes, translated_inline_codes):
        raise RepairError("translated inline code spans are reordered")

    state = _RepairState(
        source_headings=iter(source_headings),
        source_links=iter(source_links),
        source_images=iter(source_images),
        source_inline_codes=source_inline_codes,
    )
    changed = False
    out: list[str] = []

    for original_line in translated.splitlines(keepends=True):
        repaired = _repair_translated_line(original_line, state)
        changed = changed or repaired != original_line
        out.append(repaired)

    _ensure_exhausted(
        state.source_headings,
        "translated document has fewer headings than source",
    )
    _ensure_exhausted(
        state.source_links,
        "translated document has fewer Markdown links than source",
    )
    _ensure_exhausted(
        state.source_images,
        "translated document has fewer Markdown images than source",
    )
    _ensure_inline_codes_exhausted(state)

    repaired = "".join(out)
    anchor_result = _repair_anchor_lines(source, repaired)
    return RepairResult(
        text=anchor_result.text,
        changed=changed or anchor_result.changed,
    )
