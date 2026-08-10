"""번역 문서에 대응하는 영어 원문을 HTML 주석으로 병기.

기존 한국어 문서(``versioned_docs``)에 ``i18n/en`` 영어 원문을 ``<!-- ... -->`` 주석으로 병기.
영어·한국어 문서의 평행 구조를 기준으로 블록 단위 정렬.
양쪽에서 바이트 단위로 같은 코드 블록과 ``<a name>`` 앵커는 정렬 동기화 지점으로만 사용하고 병기 대상에서 제외.

- 병기 대상: 제목(H1~H6), 문단, 목록, 표 행, 경고문, 인용문 등 모든 텍스트
- 제외 대상: 코드 블록, ``<a name>`` 앵커, front matter, 빈 줄, 표 구분 행
- 주석 내용: 대응하는 영어 원문 줄 또는 블록
- 주석 정규화: ``{{version}}`` 치환, ``<img/>`` 자체 닫힘 형식 적용
- 한국어 본문: 전처리·후처리 정규화 후 주석 줄 삽입

영어 블록 누락 또는 종류 불일치로 정렬에 실패하면 원문 갱신 미반영 drift로 판정.
대응할 수 있는 블록의 병기를 계속하고 대응할 수 없는 구간은 호출자가 번역 갱신 필요성 판단.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

from ..common.markdown import (
    closes_fence,
    fence_token,
    html_code_contents,
    html_comment_spans,
    inline_code_contents,
    is_non_annotatable_line,
    is_heading_line,
    is_named_anchor_line,
    is_ordered_list_marker,
    is_structural_html_fragment,
    is_structural_html_line,
    mask_fenced_code_contents,
    normalize_annotation_anchor,
    reference_definition_line_numbers,
    strip_html_code_elements,
    strip_inline_code,
    strip_title_attr_line,
)
from ..postprocessing import postprocess as _postprocess
from ..postprocessing.postprocess import img_self_closing, replace_version
from ..preprocessing import preprocess as _preprocess


@dataclass
class Block:
    """원문 줄 범위와 종류를 보존한 Markdown 정렬 블록."""

    kind: str  # 허용값: frontmatter | code | anchor | structure | heading | text
    start: int  # 원문에서 시작하는 0-based 줄 번호
    end: int    # 원문에서 끝나는 0-based 줄 번호(미포함)
    lines: list[str]


@dataclass
class Drift:
    """정렬 실패 연산과 양쪽 문서의 해당 줄 목록."""
    op: str  # delete(영어만 존재) | insert(한국어만 존재) | replace(양쪽 구조 불일치)
    en_lines: list[str] = field(default_factory=list)
    ko_lines: list[str] = field(default_factory=list)


def split_blocks(lines: list[str]) -> list[Block]:
    """Markdown 줄을 구조와 연속 범위가 보존된 정렬 블록으로 분할."""

    blocks: list[Block] = []
    i = 0
    n = len(lines)
    # 문서 시작의 front matter 블록 분리.
    if n and lines[0].strip() == "---":
        j = 1
        while j < n and lines[j].strip() != "---":
            j += 1
        if j < n:
            blocks.append(Block("frontmatter", 0, j + 1, lines[0:j + 1]))
            i = j + 1
    while i < n:
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        tok = fence_token(ln)
        if tok:
            j = i + 1
            while j < n and not closes_fence(lines[j], tok):
                j += 1
            j = min(j + 1, n)  # 닫는 코드 펜스 포함.
            blocks.append(Block("code", i, j, lines[i:j]))
            i = j
            continue
        if is_named_anchor_line(ln):
            blocks.append(Block("anchor", i, i + 1, [ln]))
            i += 1
            continue
        if is_structural_html_line(ln):
            blocks.append(Block("structure", i, i + 1, [ln]))
            i += 1
            continue
        if is_heading_line(ln):
            blocks.append(Block("heading", i, i + 1, [ln]))
            i += 1
            continue
        # 빈 줄, 코드 펜스, 앵커, 제목 또는 하위 종류 변경 전까지 텍스트 묶음 수집.
        j = i
        subkind = _text_subkind(lines[i])
        while j < n:
            l2 = lines[j]
            if (
                not l2.strip()
                or fence_token(l2)
                or is_named_anchor_line(l2)
                or is_structural_html_line(l2)
                or is_heading_line(l2)
            ):
                break
            if j > i and _starts_new_text_block(l2, subkind):
                break
            j += 1
        blocks.append(Block("text", i, j, lines[i:j]))
        i = j
    return blocks


def _norm_code(block: Block, version: str) -> str:
    """코드 블록의 버전 플레이스홀더와 이미지 태그를 정렬용으로 정규화."""

    return img_self_closing(replace_version("\n".join(block.lines), version))


def _sig(block: Block, version: str) -> tuple:
    """영어와 번역 블록을 대응시킬 구조 서명 생성."""

    if block.kind == "code":
        return ("code", _norm_code(block, version))
    if block.kind == "anchor":
        return ("anchor", block.lines[0].strip())
    if block.kind == "structure":
        return ("structure", block.lines[0].strip())
    if block.kind == "heading":
        line = block.lines[0].lstrip()
        level = len(line) - len(line.lstrip("#"))
        return ("heading", level)
    if block.kind == "frontmatter":
        return ("frontmatter",)
    sub = _text_subkind(block.lines[0])
    return ("text", sub)


def _text_subkind(line: str) -> str:
    """첫 줄 형식에 따라 텍스트 블록의 세부 종류 분류."""

    s = line.lstrip()
    if s.startswith("|"):
        return "table"
    if s.startswith(">"):
        return "quote"
    if s[:2] in ("- ", "* ", "+ ") or is_ordered_list_marker(s):
        return "list"
    if s.startswith("@"):
        return "directive"
    if s.startswith("<"):
        return "html"
    return "para"


def _starts_new_text_block(line: str, current_subkind: str) -> bool:
    """다음 줄이 현재 텍스트 블록과 분리되는 구조 경계인지 판별."""

    next_subkind = _text_subkind(line)
    if current_subkind in ("html", "directive"):
        return False
    if next_subkind == "html" and line.lstrip().startswith("</"):
        return False
    if current_subkind == "para" and next_subkind == "list":
        return False
    if next_subkind == current_subkind:
        return False
    if current_subkind == "list" and line[:1].isspace():
        return False
    return True


def _is_skip_line(line: str) -> bool:
    """verify._required_comments가 문단에서 제외하고 건너뛰는 줄.

    텍스트 블록 안에는 제목·앵커가 없으므로 TOC 링크, 인용문(``>``), 표(``|``), 기존 주석만 검사.
    """
    if is_non_annotatable_line(line):
        return True
    stripped = line.strip()
    list_body = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", stripped)
    return bool(
        list_body != stripped
        and (inline_code_contents(list_body) or html_code_contents(list_body))
        and not strip_html_code_elements(strip_inline_code(list_body)).strip(
            " `*_~.,:;()[]&/,+"
        )
    )


_PRESENCE_MARKER_RE = re.compile(r"\]\(([^)\s]+)\)|`([^`]+)`")


def _presence_markers(lines: list[str]) -> set[str]:
    """원문 블록에서 번역하지 않는 링크 URL과 인라인 코드 토큰 수집."""
    text = "\n".join(lines)
    out: set[str] = set()
    for match in _PRESENCE_MARKER_RE.finditer(text):
        out.update(group for group in match.groups() if group)
    return out


def _content_present(block: Block, translation: str) -> bool:
    """블록에 비번역 토큰이 하나 이상 있고 모두 번역본에 있는지 확인.

    내용은 번역됐지만 주석 정렬만 어긋난 병기 공백과 내용 자체가 누락된 실제 drift 구분.
    병기 공백에만 원문 주석 보강.
    """
    marks = _presence_markers(block.lines)
    return bool(marks) and all(mark in translation for mark in marks)


def _csub(s: str, version: str) -> str:
    """주석용 영어 원문의 버전·이미지·제목 클래스·종료 구분자 정규화."""
    s = replace_version(s, version)
    s = img_self_closing(s)
    s = strip_title_attr_line(s)
    s = s.replace("-->", "--&gt;")
    return s


def _canonical_comment_body(s: str) -> str:
    """병기 원문의 공백과 주석 구분자 표현을 정규 바이트 계약 형식으로 렌더링."""

    return normalize_annotation_anchor(s).replace("-->", "--&gt;")


def _comment_for(
    en: Block,
    ko: Block,
    version: str,
    inserts: dict[int, list[str]],
    *,
    canonical: bool,
) -> None:
    """한국어 블록 위 또는 대응 줄에 삽입할 영어 주석 등록.

    ``verify._required_comments``와 같은 분할 규칙 적용.
    제목과 문단은 필수 주석으로 처리하고 문단의 연속 일반 줄은 단일 주석으로 병합.
    탐색 전용 TOC 링크와 별도 소유자가 검증하는 인용문(``>``)·표(``|``) 줄은 제외.
    """
    if en.kind == "heading":
        body = (
            _canonical_comment_body(en.lines[0])
            if canonical
            else _csub(en.lines[0].rstrip(), version)
        )
        inserts.setdefault(ko.start, []).append(f"<!-- {body} -->")
        return

    en_lines = en.lines
    ko_lines = ko.lines
    if canonical and en_lines and _text_subkind(en_lines[0]) == "table":
        body = _canonical_comment_body(" ".join(en_lines))
        inserts.setdefault(ko.start, []).append(
            f"<!-- {body} -->"
        )
        return
    if is_structural_html_fragment("\n".join(en_lines)):
        return
    reference_lines = reference_definition_line_numbers(
        "\n".join(en_lines)
    )
    aligned = len(en_lines) == len(ko_lines)

    def make_comment(run: list[str]) -> list[str]:
        """영어 원문 묶음의 단일 또는 여러 줄 HTML 주석 생성."""

        if canonical:
            return [f"<!-- {_canonical_comment_body(' '.join(run))} -->"]
        body = [_csub(line.rstrip(), version) for line in run]
        if len(body) == 1:
            return [f"<!-- {body[0]} -->"]
        return ["<!--", *body, "-->"]

    i = 0
    n = len(en_lines)
    while i < n:
        el = en_lines[i]
        if i in reference_lines or _is_skip_line(el):
            i += 1
            continue
        # verify._required_comments는 `#`로 시작하는 줄을 제목으로 보고 단독 주석 요구.
        # 들여쓰기 코드의 `#items:`와 PHP 속성 `#[...]`도 같은 규칙 적용.
        # 검증 규칙에 맞춰 묶음을 분리하고 단독 주석 생성.
        if el.strip().startswith("#"):
            at = ko.start + i if aligned else ko.start
            body = (
                _canonical_comment_body(el)
                if canonical
                else _csub(el.strip(), version)
            )
            inserts.setdefault(at, []).append(f"<!-- {body} -->")
            i += 1
            continue
        # 연속된 일반 문단 줄을 하나의 묶음으로 결합.
        j = i
        while (
            j < n
            and j not in reference_lines
            and not _is_skip_line(en_lines[j])
            and not en_lines[j].strip().startswith("#")
        ):
            j += 1
        run = en_lines[i:j]
        at = ko.start + i if aligned else ko.start
        inserts.setdefault(at, []).extend(make_comment(run))
        i = j


def _source_comment_bodies(source: str | None) -> list[str]:
    """코드 펜스 밖에서 원문에 작성된 HTML 주석 본문 수집."""

    if source is None:
        return []
    return [
        body
        for _start, _end, body in html_comment_spans(
            mask_fenced_code_contents(source)
        )
    ]


def _standalone_comment_start(line: str) -> int | None:
    """독립 병기 주석이 시작하는 열 위치 반환."""

    prefix = re.match(r"^[ \t]*(?:>[ \t]*)*", line)
    assert prefix is not None
    start = prefix.end()
    if not line[start:].startswith("<!--"):
        return None
    if ">" not in prefix.group(0) and start:
        return None
    return start


def _standalone_comment_body(
    lines: list[str], start: int, end: int, opening: int = 0
) -> str:
    """한 줄 또는 여러 줄 독립 주석의 본문 추출."""

    first = lines[start]
    last = lines[end]
    if start == end:
        return first[opening + 4 : first.index("-->")]
    return "\n".join(
        [first[opening + 4 :], *lines[start + 1 : end], last[: last.index("-->")]]
    )


def _comment_record_indexes(text: str) -> dict[tuple[int, int], int]:
    """주석 줄 범위를 문서 내 등장 순번에 연결."""

    masked = mask_fenced_code_contents(text)
    return {
        (
            masked.count("\n", 0, start),
            masked.count("\n", 0, end - 1),
        ): index
        for index, (start, end, _body) in enumerate(html_comment_spans(masked))
    }


def strip_annotations(
    ko_text: str,
    *,
    source: str | None = None,
    preserved_comment_indexes: frozenset[int] | None = None,
) -> str:
    """코드 블록 밖의 단독 ``<!-- ... -->`` 병기 주석 제거.

    멱등성을 보장하도록 재실행 전에 기존 병기 주석 제거.
    코드 블록 내부 주석과 줄 중간 인라인 주석 보존.
    ``source``가 있으면 원문 작성 주석과 순서·본문이 같은 독립 주석 보존.
    ``preserved_comment_indexes``가 있으면 지정한 문서 내 주석 순번만 보존.
    """
    lines = ko_text.split("\n")
    source_comments = _source_comment_bodies(source)
    source_index = 0
    comment_indexes = (
        _comment_record_indexes(ko_text)
        if preserved_comment_indexes is not None
        else {}
    )
    out: list[str] = []
    in_code = False
    fence = ""
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        tok = fence_token(ln)
        if tok:
            if not in_code:
                in_code, fence = True, tok
            elif closes_fence(ln, fence):
                in_code = False
            out.append(ln)
            i += 1
            continue
        comment_start = _standalone_comment_start(ln) if not in_code else None
        if comment_start is not None:
            if "-->" in ln:
                end = i
            else:
                if comment_start:
                    out.append(ln)
                    i += 1
                    continue
                end = i + 1
                while end < n and "-->" not in lines[end]:
                    end += 1
                if end == n:
                    out.extend(lines[i:])
                    break
            body = _standalone_comment_body(lines, i, end, comment_start)
            preserve = (
                comment_indexes.get((i, end)) in preserved_comment_indexes
                if preserved_comment_indexes is not None
                else (
                    source_index < len(source_comments)
                    and body == source_comments[source_index]
                )
            )
            if preserve:
                out.extend(lines[i : end + 1])
                if preserved_comment_indexes is None:
                    source_index += 1
            i = end + 1
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def annotate(
    en_text: str,
    ko_text: str,
    version: str,
    *,
    canonical: bool = False,
    alignment_source: str | None = None,
    preserved_comment_indexes: frozenset[int] | None = None,
) -> tuple[str, list[Drift]]:
    """한국어 문서에 영어 원문을 병기하고 결과와 drift 목록 반환.

    ``drifts``가 비어 있으면 완전 정렬과 기계적 병기에 성공한 상태.
    이미 병기된 입력을 안전하게 재처리하도록 기존 병기 주석 우선 제거.

    기본 모드의 ``en_text``는 원시 원문을 입력받아 내부에서 전처리·후처리한 정규본으로 변환.
    검증 단계의 ``expected``와 같이 들여쓰기 코드를 코드 펜스로 변환하고 ``<style>`` 제거, ``{{version}}`` 치환, 이미지 자체 닫힘 형식 적용, Base64 복원 수행.
    ``canonical=True``이면 버전만 치환한 ``en_text``를 병기 주석 본문으로 사용하고 ``alignment_source``를 구조 정렬 기준으로 사용.

    ``ko_text``에도 같은 정규화 적용.
    한국어 문서에 남은 페이지 디자인용 ``<style>`` 블록과 들여쓰기 코드 블록을 텍스트로 오인해 영어 주석을 잘못 삽입하거나 코드를 중복 병기하는 오류 방지.
    """
    annotation_blocks: list[Block] | None = None
    if canonical:
        annotation_text = replace_version(en_text, version)
        en_text = alignment_source or annotation_text
        annotation_blocks = split_blocks(annotation_text.split("\n"))
    else:
        _pre = _preprocess.preprocess(en_text)
        en_text = _postprocess.postprocess(_pre.text, version, _pre.placeholders)
    ko_text = strip_annotations(
        ko_text,
        source=en_text,
        preserved_comment_indexes=preserved_comment_indexes,
    )
    _kpre = _preprocess.preprocess(ko_text)
    ko_text = _postprocess.postprocess(_kpre.text, version, _kpre.placeholders)
    en_lines = en_text.split("\n")
    ko_lines = ko_text.split("\n")
    en_blocks = split_blocks(en_lines)
    ko_blocks = split_blocks(ko_lines)

    if annotation_blocks is not None and (
        len(annotation_blocks) != len(en_blocks)
        or [block.kind for block in annotation_blocks]
        != [block.kind for block in en_blocks]
    ):
        raise ValueError(
            "canonical annotation source and English view structures differ"
        )

    en_sigs = [_sig(b, version) for b in en_blocks]
    ko_sigs = [_sig(b, version) for b in ko_blocks]

    sm = difflib.SequenceMatcher(a=en_sigs, b=ko_sigs, autojunk=False)
    inserts: dict[int, list[str]] = {}
    drifts: list[Drift] = []

    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                eb, kb = en_blocks[i1 + k], ko_blocks[j1 + k]
                if eb.kind in ("heading", "text"):
                    _comment_for(
                        annotation_blocks[i1 + k]
                        if annotation_blocks is not None
                        else eb,
                        kb,
                        version,
                        inserts,
                        canonical=canonical,
                    )
        elif op == "replace" and (i2 - i1) == (j2 - j1):
            # 블록 수가 같으면 위치별로 병기하되 정렬 불일치로 기록.
            for k in range(i2 - i1):
                eb, kb = en_blocks[i1 + k], ko_blocks[j1 + k]
                if eb.kind in ("heading", "text") and kb.kind in ("heading", "text"):
                    _comment_for(
                        annotation_blocks[i1 + k]
                        if annotation_blocks is not None
                        else eb,
                        kb,
                        version,
                        inserts,
                        canonical=canonical,
                    )
                drifts.append(Drift("replace", eb.lines, kb.lines))
        else:
            if i2 > i1:
                en_seg = [line for block in en_blocks[i1:i2] for line in block.lines]
                # 한국어 문서에 없는 영어 블록은 번역 갱신 필요.
                # 코드 또는 앵커만 있는 구간은 제외.
                meaningful = any(b.kind in ("heading", "text") for b in en_blocks[i1:i2])
                if meaningful:
                    drifts.append(Drift("delete", en_lines=en_seg))
                    # 정렬이 깨져도 원문 주석은 항상 보존.
                    # 불완전한 번역 출력으로 블록이 어긋나도 검증 단계의 원문 주석 누락 오류 방지.
                    # 해당 영어 텍스트·제목 주석을 한국어 블록의 경계 위치에 삽입.
                    at = ko_blocks[j1].start if j1 < len(ko_blocks) else len(ko_lines)
                    anchor = Block("text", at, at, [])
                    for offset, eb in enumerate(en_blocks[i1:i2], start=i1):
                        if eb.kind in ("heading", "text") and _content_present(eb, ko_text):
                            _comment_for(
                                annotation_blocks[offset]
                                if annotation_blocks is not None
                                else eb,
                                anchor,
                                version,
                                inserts,
                                canonical=canonical,
                            )
            if j2 > j1:
                ko_seg = [line for block in ko_blocks[j1:j2] for line in block.lines]
                meaningful = any(b.kind in ("heading", "text") for b in ko_blocks[j1:j2])
                if meaningful:
                    drifts.append(Drift("insert", ko_lines=ko_seg))

    # 원래 한국어 줄을 유지하면서 주석을 삽입하고 코드 밖 형식만 정제.
    out: list[str] = []
    in_code = False
    fence = ""
    for idx, ln in enumerate(ko_lines):
        for c in inserts.get(idx, []):
            out.append(c)
        tok = fence_token(ln)
        if tok:
            if not in_code:
                in_code, fence = True, tok
            elif closes_fence(ln, fence):
                in_code = False
            out.append(ln)
            continue
        if not in_code:
            ln = img_self_closing(ln)
            ln = strip_title_attr_line(ln)
        out.append(ln)
    # 한국어 문서 끝 이후 위치에 등록된 주석도 누락 없이 추가.
    for idx in sorted(k for k in inserts if k >= len(ko_lines)):
        out.extend(inserts[idx])
    return "\n".join(out), drifts
