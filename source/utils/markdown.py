import re


_STYLE_BLOCK_PATTERN = re.compile(r"<style>(.*?)</style>", re.DOTALL | re.IGNORECASE)
_IMG_TAG_PATTERN = re.compile(r"<img\b([^>]*?)(?<!/)>", re.IGNORECASE)


def _split_fenced_segments(markdown_text):
    """마크다운을 코드 펜스 영역과 일반 영역으로 나눕니다."""
    lines = markdown_text.splitlines(keepends=True)
    segments = []
    buffer = []
    in_fence = False
    fence_delimiter = None

    for line in lines:
        stripped = line.lstrip()
        is_fence_line = stripped.startswith("```") or stripped.startswith("~~~")

        if not in_fence and is_fence_line:
            if buffer:
                segments.append((False, "".join(buffer)))
                buffer = []
            in_fence = True
            fence_delimiter = stripped[:3]
            buffer.append(line)
            continue

        if in_fence:
            buffer.append(line)
            if is_fence_line and stripped.startswith(fence_delimiter):
                segments.append((True, "".join(buffer)))
                buffer = []
                in_fence = False
                fence_delimiter = None
            continue

        buffer.append(line)

    if buffer:
        segments.append((in_fence, "".join(buffer)))

    return segments


def _wrap_style_block(match):
    content = match.group(1)
    stripped = content.strip()

    if stripped.startswith("{`") and stripped.endswith("`}"):
        return match.group(0)

    return f"<style>{{`{content}`}}</style>"


def _split_inline_code_segments(segment):
    """일반 마크다운 영역을 인라인 코드와 그 외 영역으로 나눕니다."""
    segments = []
    buffer = []
    i = 0

    while i < len(segment):
        if segment[i] != "`":
            buffer.append(segment[i])
            i += 1
            continue

        tick_count = 1
        while i + tick_count < len(segment) and segment[i + tick_count] == "`":
            tick_count += 1

        delimiter = "`" * tick_count
        end = segment.find(delimiter, i + tick_count)
        if end == -1:
            buffer.append(segment[i:])
            break

        if buffer:
            segments.append((False, "".join(buffer)))
            buffer = []

        end += tick_count
        segments.append((True, segment[i:end]))
        i = end

    if buffer:
        segments.append((False, "".join(buffer)))

    return segments


def _sanitize_non_fenced_segment(segment):
    transformed = []

    for is_code, part in _split_inline_code_segments(segment):
        if is_code:
            transformed.append(part)
            continue

        part = _STYLE_BLOCK_PATTERN.sub(_wrap_style_block, part)
        transformed.append(_IMG_TAG_PATTERN.sub(lambda match: f"<img{match.group(1)} />", part))

    return "".join(transformed)


def sanitize_markdown_for_mdx(markdown_text):
    """Laravel 문서에서 확인된 MDX 민감 HTML 패턴만 최소 변환합니다."""
    segments = _split_fenced_segments(markdown_text)
    transformed = []

    for is_fenced, segment in segments:
        if is_fenced:
            transformed.append(segment)
        else:
            transformed.append(_sanitize_non_fenced_segment(segment))

    return "".join(transformed)
