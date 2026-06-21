"""영어 원문 주석 병기 (docs/05 T2, docs/02 출력 형식).

기존 한국어 문서(versioned_docs)에 i18n/en 영어 원문을 `<!-- ... -->` 주석으로
병기한다. en/ko는 구조가 평행하므로 블록 단위로 정렬한다. 코드 블록과 `<a name>`
앵커는 양쪽이 byte-identical이라 정렬 동기화 지점으로 쓰고, 병기하지 않는다.

- 병기 대상: 제목(H1~H6), 문단, 목록, 표 행, admonition/인용 등 모든 텍스트.
- 비대상: 코드 블록, `<a name>` 앵커, front matter, 빈 줄, 표 구분행, en==ko 동일 줄.
- 주석 내용: 대응 영어 원문 줄(또는 블록). {{version}} 치환·<img/> self-close 적용.
- ko 본문은 한 글자도 바꾸지 않고 주석 줄만 삽입한다.

정렬이 깨지면(en 블록이 ko에 없거나 종류가 어긋나면) 원문 갱신 미반영(drift)으로
보고하고, 해당 블록은 기계적으로 만들지 않는다(번역 갱신 필요).
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

from . import postprocess as _postprocess, preprocess as _preprocess
from .postprocess import img_self_closing, replace_version

_FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
_ANCHOR = re.compile(r"^[ \t]*<a\s+[^>]*\bname=[\"'][^\"']+[\"'][^>]*>\s*(?:</a>)?\s*$", re.I)
_HEADING = re.compile(r"^#{1,6}\s")
_TABLESEP = re.compile(r"^[ \t]*\|?[ \t]*:?-{1,}:?[ \t]*(\|[ \t]*:?-{1,}:?[ \t]*)+\|?[ \t]*$")
_BLANK = re.compile(r"^[ \t]*$")
_TITLE_ATTR = re.compile(r"^(#{1,6}\s+.+?)\s+\{[.#][^}]*\}\s*$")


@dataclass
class Block:
    kind: str  # frontmatter|code|anchor|heading|text
    start: int  # inclusive line index in original
    end: int    # exclusive
    lines: list[str]


@dataclass
class Drift:
    """정렬 실패 구간 보고."""
    op: str            # delete(en-only) | insert(ko-only) | replace
    en_lines: list[str] = field(default_factory=list)
    ko_lines: list[str] = field(default_factory=list)


def split_blocks(lines: list[str]) -> list[Block]:
    blocks: list[Block] = []
    i = 0
    n = len(lines)
    # front matter
    if n and lines[0].strip() == "---":
        j = 1
        while j < n and lines[j].strip() != "---":
            j += 1
        if j < n:
            blocks.append(Block("frontmatter", 0, j + 1, lines[0:j + 1]))
            i = j + 1
    while i < n:
        ln = lines[i]
        if _BLANK.match(ln):
            i += 1
            continue
        if _FENCE.match(ln):
            tok = ln.lstrip()[:3]
            j = i + 1
            while j < n and not (lines[j].lstrip().startswith(tok)):
                j += 1
            j = min(j + 1, n)  # include closing fence
            blocks.append(Block("code", i, j, lines[i:j]))
            i = j
            continue
        if _ANCHOR.match(ln):
            blocks.append(Block("anchor", i, i + 1, [ln]))
            i += 1
            continue
        if _HEADING.match(ln):
            blocks.append(Block("heading", i, i + 1, [ln]))
            i += 1
            continue
        # text: maximal run until blank / fence / anchor / heading / subkind change
        j = i
        subkind = _text_subkind(lines[i])
        while j < n:
            l2 = lines[j]
            if _BLANK.match(l2) or _FENCE.match(l2) or _ANCHOR.match(l2) or _HEADING.match(l2):
                break
            if j > i and _starts_new_text_block(l2, subkind):
                break
            j += 1
        blocks.append(Block("text", i, j, lines[i:j]))
        i = j
    return blocks


def _norm_code(block: Block, version: str) -> str:
    return img_self_closing(replace_version("\n".join(block.lines), version))


def _sig(block: Block, version: str) -> tuple:
    if block.kind == "code":
        return ("code", _norm_code(block, version))
    if block.kind == "anchor":
        return ("anchor", block.lines[0].strip())
    if block.kind == "heading":
        line = block.lines[0].lstrip()
        level = len(line) - len(line.lstrip("#"))
        return ("heading", level)
    if block.kind == "frontmatter":
        return ("frontmatter",)
    sub = _text_subkind(block.lines[0])
    return ("text", sub)


def _text_subkind(line: str) -> str:
    s = line.lstrip()
    if s.startswith("|"):
        return "table"
    if s.startswith(">"):
        return "quote"
    if s[:2] in ("- ", "* ", "+ ") or re.match(r"^\d+\.\s", s):
        return "list"
    if s.startswith("@"):
        return "directive"
    if s.startswith("<"):
        return "html"
    return "para"


def _starts_new_text_block(line: str, current_subkind: str) -> bool:
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


def _is_skip_line(line: str) -> str:
    """verify._required_comments가 문단에서 제외하고 건너뛰는 줄.

    text 블록 안에는 제목·앵커가 없으므로 TOC 링크, 인용(`>`), 표(`|`), 기존 주석만 본다.
    """
    s = line.strip()
    if s.startswith(("<!--", ">", "|")):
        return True
    if s.startswith(("- [", "* [")) and "](#" in s:
        return True
    return False


def _csub(s: str, version: str) -> str:
    """주석에 넣을 영어 원문 정제: 버전 치환, img self-close, 제목 {.class} 제거, --> 무력화."""
    s = replace_version(s, version)
    s = img_self_closing(s)
    s = _TITLE_ATTR.sub(r"\1", s)
    s = s.replace("-->", "--&gt;")
    return s


def _comment_for(en: Block, ko: Block, version: str, inserts: dict[int, list[str]]) -> None:
    """ko 블록 위(또는 줄별)에 en 주석을 inserts에 등록한다.

    verify._required_comments와 같은 세그멘테이션을 따른다: 제목·문단은 필수 주석,
    문단은 연속 일반 줄을 하나로 합쳐 단일 주석으로 낸다. TOC 링크·`>`·`|` 줄은
    docs/02 출력 규칙에 따라 병기하지 않는다.
    """
    if en.kind == "heading":
        inserts.setdefault(ko.start, []).append(f"<!-- {_csub(en.lines[0].rstrip(), version)} -->")
        return

    en_lines = en.lines
    ko_lines = ko.lines
    aligned = len(en_lines) == len(ko_lines)

    def make_comment(run: list[str]) -> list[str]:
        body = [_csub(l.rstrip(), version) for l in run]
        if len(body) == 1:
            return [f"<!-- {body[0]} -->"]
        return ["<!--", *body, "-->"]

    i = 0
    n = len(en_lines)
    while i < n:
        el = en_lines[i]
        if _is_skip_line(el):
            i += 1
            continue
        # verify._required_comments는 `#`로 시작하는 줄(들여쓰기 코드 안의 `#items:`,
        # PHP 속성 `#[...]` 등 포함)을 제목으로 보고 단독 주석으로 요구한다. 같은 규칙으로
        # 런을 끊고 단독 주석을 낸다.
        if el.strip().startswith("#"):
            at = ko.start + i if aligned else ko.start
            inserts.setdefault(at, []).append(f"<!-- {_csub(el.strip(), version)} -->")
            i += 1
            continue
        # 문단 런: 연속 일반 줄을 하나로
        j = i
        while j < n and not _is_skip_line(en_lines[j]) and not en_lines[j].strip().startswith("#"):
            j += 1
        run = en_lines[i:j]
        at = ko.start + i if aligned else ko.start
        inserts.setdefault(at, []).extend(make_comment(run))
        i = j


def strip_annotations(ko_text: str) -> str:
    """코드 블록 밖의 단독 `<!-- ... -->` 병기 주석을 제거(멱등성용 재실행 대비).

    코드 블록 안 주석과 줄 중간 인라인 주석은 보존한다.
    """
    lines = ko_text.split("\n")
    out: list[str] = []
    in_code = False
    fence = ""
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        s = ln.lstrip()
        if _FENCE.match(ln):
            tok = s[:3]
            if not in_code:
                in_code, fence = True, tok
            elif s.startswith(fence):
                in_code = False
            out.append(ln)
            i += 1
            continue
        if not in_code and s.startswith("<!--"):
            if "-->" in ln:
                i += 1
                continue
            j = i + 1
            while j < n and "-->" not in lines[j]:
                j += 1
            i = j + 1
            continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def annotate(en_text: str, ko_text: str, version: str) -> tuple[str, list[Drift]]:
    """ko_text에 en_text를 병기. (annotated_ko, drifts) 반환.

    drifts가 비어 있으면 완전 정렬(기계적 병기 성공). 이미 병기된 입력도 안전하게
    재처리하도록 기존 병기 주석을 먼저 제거한다.

    en_text는 raw 원문을 받아 내부에서 preprocess+postprocess한 정규본(verify가 쓰는
    `expected`와 동일: 들여쓰기→fenced, <style> 제거, {{version}} 치환, img self-close,
    base64 복원)으로 맞춘다. 그래야 KO(fenced/치환된 본문)와 정렬되고 verify와 일치한다.

    ko_text도 동일하게 정규화한다. 그렇지 않으면 KO에 남은 페이지 디자인 <style> 블록이나
    들여쓰기 코드 블록이 텍스트로 오인돼, 영어 주석이 <style> 안에 삽입되거나 들여쓰기
    코드가 주석으로 중복 병기되는 오류가 생긴다.
    """
    ko_text = strip_annotations(ko_text)
    _kpre = _preprocess.preprocess(ko_text)
    ko_text = _postprocess.postprocess(_kpre.text, version, _kpre.placeholders)
    _pre = _preprocess.preprocess(en_text)
    en_text = _postprocess.postprocess(_pre.text, version, _pre.placeholders)
    en_lines = en_text.split("\n")
    ko_lines = ko_text.split("\n")
    en_blocks = split_blocks(en_lines)
    ko_blocks = split_blocks(ko_lines)

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
                    _comment_for(eb, kb, version, inserts)
        elif op == "replace" and (i2 - i1) == (j2 - j1):
            # 같은 개수: 위치 대응으로 병기하되 drift로 보고
            for k in range(i2 - i1):
                eb, kb = en_blocks[i1 + k], ko_blocks[j1 + k]
                if eb.kind in ("heading", "text") and kb.kind in ("heading", "text"):
                    _comment_for(eb, kb, version, inserts)
                drifts.append(Drift("replace", eb.lines, kb.lines))
        else:
            if i2 > i1:
                en_seg = [l for b in en_blocks[i1:i2] for l in b.lines]
                # ko에 없는 en 블록: 번역 갱신 필요(코드/앵커만이면 무시)
                meaningful = any(b.kind in ("heading", "text") for b in en_blocks[i1:i2])
                if meaningful:
                    drifts.append(Drift("delete", en_lines=en_seg))
            if j2 > j1:
                ko_seg = [l for b in ko_blocks[j1:j2] for l in b.lines]
                meaningful = any(b.kind in ("heading", "text") for b in ko_blocks[j1:j2])
                if meaningful:
                    drifts.append(Drift("insert", ko_lines=ko_seg))

    # 재구성: 원본 ko 줄을 유지하고 주석만 삽입(+ 코드 밖 형식 정제)
    out: list[str] = []
    in_code = False
    fence = ""
    for idx, ln in enumerate(ko_lines):
        for c in inserts.get(idx, []):
            out.append(c)
        s = ln.lstrip()
        if _FENCE.match(ln):
            tok = s[:3]
            if not in_code:
                in_code, fence = True, tok
            elif s.startswith(fence):
                in_code = False
            out.append(ln)
            continue
        if not in_code:
            ln = img_self_closing(ln)
            ln = _TITLE_ATTR.sub(r"\1", ln)
        out.append(ln)
    return "\n".join(out), drifts
