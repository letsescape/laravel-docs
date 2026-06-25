"""번역 전 전처리. translation-sync/docs/01.

원문 source(i18n/en)는 raw로 두고, 번역 파이프라인을 통과하는 작업 사본에만 적용한다.
- base64 이미지 → placeholder 치환(+매핑), 후처리에서 복원
- 페이지 디자인 전용 <style> 제거 (fenced code block 밖에서만)
- 제목 옆 {.class} 스타일 클래스 제거

애매한 구조(목록 들여쓰기 vs 코드 블록 등)는 docs/01 예외 원칙에 따라 변경하지 않는다.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..common.markdown import closes_fence, strip_title_attrs

# data:image/...;base64,.... (Markdown/HTML 이미지 양쪽)
_BASE64_RE = re.compile(r"data:image/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/=]+(?=[)\"'\s])")
# fenced code block (``` 또는 ~~~)
_FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})", re.MULTILINE)
_INDENTED_CODE_RE = re.compile(r"^(?: {4}|\t)(.*)$")
_LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s)")
_STYLE_OPEN = "<style"
_STYLE_CLOSE = "</style>"


@dataclass
class Preprocessed:
    text: str
    placeholders: dict[str, str] = field(default_factory=dict)


def _split_code_segments(text: str) -> list[tuple[str, bool]]:
    """텍스트를 (구간, is_code) 목록으로 나눈다. fenced code block 보호용."""
    segments: list[tuple[str, bool]] = []
    in_code = False
    fence = ""
    last = 0
    for m in _FENCE_RE.finditer(text):
        token = m.group(2)
        if not in_code:
            in_code, fence = True, token
            segments.append((text[last:m.start()], False))
            last = m.start()
        elif closes_fence(token, fence):
            in_code = False
            segments.append((text[last:m.end()], True))
            last = m.end()
    segments.append((text[last:], in_code))
    return segments


# 줄 시작 구조로 코드/설정을 식별하는 패턴(Blade 디렉티브, .env, YAML, shell, 경로 등).
# 들여쓰기 블록이 이런 구조면 코드 블록으로 보고 fenced로 변환해, 영어 주석이 코드에
# 잘못 병기되는 것을 막는다.
_STRUCT_CODE_PATS = (
    re.compile(r"^\s*@\w+"),                        # Blade/Envoy 디렉티브 (@auth, @once 등)
    re.compile(r"^\s*[A-Za-z][\w-]*="),             # .env·설정 (STRIPE_KEY=..., process_name=...)
    re.compile(r"^\s*(//|#\s|/\*)"),               # 코드 주석
    re.compile(r"^\s*[\w./-]+:\s\S"),               # YAML/설정 key: value
    re.compile(r"^\s*[\w-]+:\s*$"),                 # YAML key:
    re.compile(
        r"^\s*[\w.]+\s*-\s*(integer|string|timestamp|bigInteger|boolean"
        r"|text|date|float|increments|json|uuid|id|datetime|char|decimal|enum|binary)\b"
    ),                                              # DB 스키마 컬럼 (id - integer 등)
    re.compile(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"),  # IP 주소
    re.compile(r"^\s*[a-z_][\w]*\s*$"),             # 단일 소문자 토큰 (테이블명 등)
    re.compile(r"^\s*[\w-]+\.\w{1,6}\s*$"),         # 파일명 (messages.php 등)
    re.compile(
        r"^\s*</?(?!(?:div|span|img|p|a|br|hr|i|b|em|strong|small|sup|sub"
        r"|ul|ol|li|h[1-6]|blockquote|figure|figcaption)\b)[a-zA-Z][\w-]*[\s/>]"
    ),  # 코드 예제 HTML/Blade 태그만 (콘텐츠/인라인 태그 제외)
    re.compile(r"^\s*/[\w][\w./-]*\s*$"),           # 경로/디렉터리 트리
    re.compile(r"^\s*(alias\s|php\d|ssh\s|cd\s|ls\s|git\s|vendor/bin)"),  # shell
    re.compile(r"^\s*\[[\w:.-]+\]\s*$"),            # INI 섹션 ([program:horizon] 등)
    re.compile(r"^\s*[a-zA-Z_]\w*(\.\w+)*\("),      # 함수 호출 (mix.js(...) 등)
)


def _looks_like_code(lines: list[str]) -> bool:
    markers = (
        "<?php",
        "=>",
        "::",
        "->",
        "$",
        "{",
        "}",
        ";",
        "php artisan",
        "composer ",
        "npm ",
        "Route::",
        "use ",
        "namespace ",
        "class ",
        "function ",
        "/**",
        "*/",
    )
    if any(any(marker in line for marker in markers) for line in lines):
        return True
    nonblank = [line for line in lines if line.strip()]
    if not nonblank:
        return False
    hits = sum(
        1 for line in nonblank if any(pat.match(line) for pat in _STRUCT_CODE_PATS)
    )
    return hits >= max(1, (len(nonblank) + 1) // 2)


def _strip_code_indent(line: str) -> str:
    if line.startswith("\t"):
        return line[1:]
    return line[4:] if line.startswith("    ") else line


def _strip_style_blocks(text: str) -> str:
    out: list[str] = []
    lower = text.lower()
    index = 0

    def inside_inline_code(position: int) -> bool:
        line_start = text.rfind("\n", 0, position) + 1
        prefix = text[line_start:position]
        return prefix.count("`") % 2 == 1

    while index < len(text):
        start = lower.find(_STYLE_OPEN, index)
        if start < 0:
            out.append(text[index:])
            break
        if inside_inline_code(start):
            out.append(text[index : start + len(_STYLE_OPEN)])
            index = start + len(_STYLE_OPEN)
            continue
        tag_end = text.find(">", start + len(_STYLE_OPEN))
        if tag_end < 0:
            out.append(text[index:])
            break

        remove_start = start
        while remove_start > index and text[remove_start - 1] in " \t":
            remove_start -= 1

        close_start = lower.find(_STYLE_CLOSE, tag_end + 1)
        if close_start < 0:
            out.append(text[index:remove_start])
            break

        remove_end = close_start + len(_STYLE_CLOSE)
        while remove_end < len(text) and text[remove_end] in " \t\r\n":
            remove_end += 1

        out.append(text[index:remove_start])
        index = remove_end
    return "".join(out)


def _is_ordered_item_opener(stripped: str) -> bool:
    marker_end = 0
    while marker_end < len(stripped) and stripped[marker_end].isdigit():
        marker_end += 1
    if marker_end == 0 or marker_end >= len(stripped) or stripped[marker_end] != ".":
        return False
    remainder = stripped[marker_end + 1:]
    return bool(remainder[:1].isspace() and remainder.rstrip().endswith(":"))


def _is_named_child_opener(stripped: str) -> bool:
    if not stripped.endswith(":"):
        return False
    name = stripped[:-1].strip()
    return bool(name) and all(char.isalnum() or char in "_.-" for char in name)


def _opens_indented_children(line: str) -> bool:
    stripped = line.lstrip()
    if stripped.startswith("@"):
        return True
    if _is_ordered_item_opener(stripped):
        return True
    if stripped[:2] in ("- ", "* ", "+ ") and stripped.rstrip().endswith(":"):
        return True
    return _is_named_child_opener(stripped)


def _has_indented_parent(lines: list[str], index: int) -> bool:
    cursor = index - 1
    while cursor >= 0:
        line = lines[cursor]
        if line == "":
            return False
        if _INDENTED_CODE_RE.match(line):
            cursor -= 1
            continue
        return _opens_indented_children(line)
    return False


def _convert_indented_code_blocks(text: str) -> str:
    """fenced code block 밖의 확실한 4-space 코드 블록만 fenced block으로 바꾼다."""
    rebuilt_segments: list[str] = []
    for segment, is_code in _split_code_segments(text):
        if is_code:
            rebuilt_segments.append(segment)
            continue

        lines = segment.split("\n")
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            match = _INDENTED_CODE_RE.match(line)
            if not match or _LIST_MARKER_RE.match(match.group(1)):
                out.append(line)
                i += 1
                continue
            if _has_indented_parent(lines, i):
                out.append(line)
                i += 1
                continue

            block: list[str] = []
            while i < len(lines):
                current = lines[i]
                current_match = _INDENTED_CODE_RE.match(current)
                if current == "":
                    next_nonblank = next(
                        (lines[k] for k in range(i + 1, len(lines)) if lines[k] != ""),
                        "",
                    )
                    next_match = _INDENTED_CODE_RE.match(next_nonblank)
                    if next_match and (
                        not _LIST_MARKER_RE.match(next_match.group(1))
                        or _looks_like_code(block)
                    ):
                        block.append("")
                        i += 1
                        continue
                    break
                if not current_match:
                    break
                stripped = current_match.group(1)
                if _LIST_MARKER_RE.match(stripped) and not _looks_like_code(block):
                    break
                block.append(_strip_code_indent(current))
                i += 1

            if _looks_like_code(block):
                out.append("```")
                out.extend(block)
                out.append("```")
            else:
                out.extend(("    " + item) if item else "" for item in block)

        rebuilt_segments.append("\n".join(out))
    return "".join(rebuilt_segments)


def preprocess(content: str) -> Preprocessed:
    result = Preprocessed(text=content)

    # 1) base64 이미지 → placeholder (전체 텍스트 대상; 토큰 절약 + 번역 제외)
    def _sub_b64(match: re.Match[str]) -> str:
        key = f"__BASE64_IMAGE_{len(result.placeholders) + 1:03d}__"
        result.placeholders[key] = match.group(0)
        return key

    text = _BASE64_RE.sub(_sub_b64, result.text)

    # 2) 코드 블록 밖에서만 <style>·제목 {.class} 제거.
    #    들여쓰기 변환보다 먼저 한다. 먼저 변환하면 <style> 내부의 들여쓰기 CSS가
    #    fenced 코드 블록이 되어 <style> strip을 막고 태그가 남는다.
    rebuilt: list[str] = []
    for segment, is_code in _split_code_segments(text):
        if is_code:
            rebuilt.append(segment)
            continue
        segment = _strip_style_blocks(segment)
        segment = strip_title_attrs(segment)
        rebuilt.append(segment)
    text = "".join(rebuilt)

    # 3) 확실한 들여쓰기 코드 블록을 fenced block으로 변환해 후속 단계에서 보호한다.
    text = _convert_indented_code_blocks(text)

    result.text = text
    return result
