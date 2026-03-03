import re


def is_list_item(line: str) -> bool:
    """마크다운 줄이 리스트 항목인지 확인

    Args:
        line: 확인할 마크다운 줄 문자열

    Returns:
        줄이 리스트 항목이면 True, 그렇지 않으면 False
    """
    stripped_line = line.lstrip()
    if stripped_line.startswith(("- ", "* ", "+ ")):
        return True
    if stripped_line.find(". ") > 0:  # 예: "1. ", "10. "
        potential_number = stripped_line[:stripped_line.find(". ")]
        if potential_number.isdigit():
            return True
    return False


def convert_indented_code_blocks(content: str) -> str:
    """마크다운 내용에서 들여쓰기 코드 블록을 펜스(백틱) 코드 블록으로 변환

    언어 태그 없이 단순 백틱(```)만을 사용

    Args:
        content: 처리할 마크다운 원본 문자열

    Returns:
        들여쓰기 코드 블록이 언어 태그 없는 펜스 코드 블록으로 변환된 마크다운 문자열
    """
    lines = content.splitlines()
    new_lines = []
    in_indented_code_block = False
    in_fenced_code_block = False
    indent_prefix = "    "
    num_lines = len(lines)

    for i, line in enumerate(lines):
        # 기존 펜스 코드 블록 처리
        if line.strip().startswith("```"):
            if not in_fenced_code_block:
                if in_indented_code_block:
                    new_lines.append("```")
                    in_indented_code_block = False
                in_fenced_code_block = True
            else:
                in_fenced_code_block = False
            new_lines.append(line)
            continue

        if in_fenced_code_block:
            new_lines.append(line)
            continue

        # 들여쓰기 코드 블록 처리
        is_currently_indented_line = line.startswith(indent_prefix)
        current_line_is_just_whitespace = not line.strip()

        if not in_indented_code_block:
            if is_currently_indented_line and not is_list_item(line):
                prev_line_justifies_code_block = (i == 0) or \
                                                 (not lines[i - 1].strip()) or \
                                                 (not lines[i - 1].startswith(indent_prefix) and not is_list_item(
                                                     lines[i - 1]))
                if prev_line_justifies_code_block:
                    in_indented_code_block = True
                    new_lines.append("```")  # 언어 태그 없이 바로 ``` 추가
                    new_lines.append(line[len(indent_prefix):])
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:  # 들여쓰기 코드 블록 내부
            if is_currently_indented_line:
                new_lines.append(line[len(indent_prefix):])
            elif current_line_is_just_whitespace:
                is_next_line_indented_code = False
                if i + 1 < num_lines:
                    next_line = lines[i + 1]
                    if next_line.startswith(indent_prefix) and not is_list_item(next_line):
                        is_next_line_indented_code = True
                if is_next_line_indented_code:
                    new_lines.append("")
                else:
                    new_lines.append("```")
                    in_indented_code_block = False
                    new_lines.append(line)
            else:
                new_lines.append("```")
                in_indented_code_block = False
                new_lines.append(line)

    if in_indented_code_block:
        new_lines.append("```")
    return "\n".join(new_lines)


def remove_style_tags(content: str) -> str:
    """마크다운 내용에서 <style> 태그와 그 내부 내용을 모두 제거

    제거 시 추가적인 개행 문자나 빈 줄을 남기지 않고, 태그와 내용만 완전히 삭제

    Args:
        content: 처리할 마크다운 원본 문자열

    Returns:
        <style> 태그와 그 내용이 완전히 제거된 마크다운 문자열
    """
    pattern = r"<style.*?>.*?</style>"
    return re.sub(pattern, "", content, flags=re.DOTALL | re.IGNORECASE)


def ensure_ends_with_blank_line(content: str) -> str:
    """파일 끝이 하나의 빈 줄로 끝나도록 표준화

    - 파일에 내용이 있다면, 마지막 내용 줄 뒤에 두 개의 개행 문자(\\n\\n)를 두어
      하나의 빈 줄이 보이도록 함
    - 파일 끝의 여러 빈 줄이나 공백은 이 규칙에 맞게 조정
    - 파일이 완전히 비어있거나 공백으로만 이루어져 있다면 빈 문자열을 반환

    Args:
        content: 처리할 마크다운 원본 문자열

    Returns:
        파일 끝이 하나의 빈 줄로 표준화된 마크다운 문자열
    """
    if not content.strip():  # 내용이 전혀 없거나 공백만 있다면 빈 문자열 반환
        return ""

    # 문자열 끝의 모든 종류의 공백 문자(개행 포함) 제거
    processed_content = content.rstrip()

    # 내용이 있다면, 파일 끝에 두 개의 개행 문자 추가 (하나의 빈 줄 생성)
    if processed_content:  # 이 조건은 rstrip() 후에도 내용이 남아있는지 확인
        processed_content += "\n\n"
    else:  # rstrip() 후 내용이 모두 사라졌다면 (원래 공백만 있던 문자열)
        return ""

    return processed_content


def fix_unclosed_img_tags(content: str) -> str:
    """마크다운 내용에서 닫히지 않은 이미지 태그를 자동으로 닫는 태그로 변환

    <img src="..."> 형태를 <img src="..." /> 형태로 변환하여 MDX 빌드 오류 방지

    Args:
        content: 처리할 마크다운 원본 문자열

    Returns:
        이미지 태그가 올바르게 닫힌 마크다운 문자열
    """
    pattern = r'<img([^>]*?)(?<!/)>'
    replacement = r'<img\1 />'
    return re.sub(pattern, replacement, content)


def replace_version_placeholder(content: str, version: str) -> str:
    """마크다운 내용에서 {{version}} 플레이스홀더를 지정된 버전으로 치환

    Args:
        content: 처리할 마크다운 원본 문자열
        version: 치환할 버전 문자열 ("master", "12.x" 등)

    Returns:
        버전 플레이스홀더가 치환된 마크다운 문자열
    """
    # {{version}} 플레이스홀더를 지정된 버전으로 치환
    pattern = r'\{\{\s*version\s*\}\}'
    return re.sub(pattern, version, content)


def remove_title_braces(content: str) -> str:
    """마크다운 제목 옆에 있는 중괄호와 그 내용을 제거

    예:
    - "#### `after()` {.collection-method .first-collection-method}" -> "#### `after()`"
    - "### `all()` {.collection-method}" -> "### `all()`"

    Args:
        content: 처리할 마크다운 원본 문자열

    Returns:
        제목에서 중괄호가 제거된 마크다운 문자열
    """
    pattern = r'^(#+\s+.+?)\s+\{[^}]*\}\s*$'

    lines = content.splitlines()
    result_lines = []

    for line in lines:
        match = re.match(pattern, line)
        if match:
            result_lines.append(match.group(1))
        else:
            result_lines.append(line)

    return "\n".join(result_lines)


def standardize_callouts(content: str) -> str:
    """
    Standardizes various Markdown callout formats into a consistent blockquote style.
    
    Converts lines such as `> {tip} message`, `> {note} message`, `> [!NOTE] message`, and `> **Note**` into a unified format using `> [!TYPE]` followed by the message. The function processes each line and transforms recognized callout patterns to ensure consistent documentation formatting.
    
    Returns:
        The Markdown string with all callout and tooltip formats standardized.
    """
    # 패턴 1: > {tip} message 형태
    pattern1 = r'^(\s*)>\s*\{(tip|note)\}\s*(.+)$'

    # 패턴 2: > [!NOTE] message 형태 (한 줄에 노트와 메시지가 함께 있는 경우)
    # 메시지가 있는 경우에만 매치하도록 수정
    pattern2 = r'^(\s*)>\s*\[!(NOTE|WARNING|TIP)\]\s+([^\s].+)$'

    # 패턴 3: > **Note** 형태
    pattern3 = r'^(\s*)>\s*\*\*(note|warning|tip)\*\*\s*(.*)$'

    # 줄별 처리
    lines = content.splitlines()
    result_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # 패턴 1 처리: > {tip} message -> > [!TIP]\n> message
        match1 = re.match(pattern1, line)
        if match1:
            indent, callout_type, message = match1.groups()
            # tip -> TIP, note -> NOTE
            callout_type = callout_type.upper()
            result_lines.append(f"{indent}> [!{callout_type}]")
            result_lines.append(f"{indent}> {message}")
            i += 1
            continue

        # 패턴 2 처리: > [!NOTE] message -> > [!NOTE]\n> message
        match2 = re.match(pattern2, line)
        if match2:
            indent, callout_type, message = match2.groups()
            result_lines.append(f"{indent}> [!{callout_type}]")
            result_lines.append(f"{indent}> {message}")
            i += 1
            continue

        # 패턴 3 처리: > **Note** -> > [!NOTE]
        match3 = re.match(pattern3, line, re.IGNORECASE)
        if match3:
            indent, callout_type, message = match3.groups()
            # note -> NOTE, warning -> WARNING, tip -> TIP
            callout_type = callout_type.upper()
            result_lines.append(f"{indent}> [!{callout_type}]")

            # 메시지가 있는 경우에만 추가
            if message:
                result_lines.append(f"{indent}> {message}")

            i += 1
            continue

        # 다른 패턴이 아니면 그대로 추가
        result_lines.append(line)
        i += 1

    return "\n".join(result_lines)


def filter_markdown(content: str, version: str = None) -> str:
    """
    Applies a sequence of filters to the given Markdown content for formatting and syntax normalization.
    
    The function performs the following transformations in order:
    1. Converts indented code blocks to fenced code blocks.
    2. Removes all <style> HTML tags and their contents.
    3. Converts unclosed <img> tags to self-closing <img /> tags.
    4. Removes curly braces and their contents adjacent to headers.
    5. Standardizes various callout and note formats.
    6. Replaces all {{version}} placeholders with the provided version string, if specified.
    7. Ensures the content ends with exactly one blank line.
    
    Parameters:
        content (str): The original Markdown string to filter.
        version (str, optional): The version string to replace {{version}} placeholders.
    
    Returns:
        str: The fully filtered and normalized Markdown string.
    """
    content = convert_indented_code_blocks(content)
    content = remove_style_tags(content)
    content = fix_unclosed_img_tags(content)
    content = remove_title_braces(content)
    content = standardize_callouts(content)

    if version is not None:
        content = replace_version_placeholder(content, version)

    content = ensure_ends_with_blank_line(content)
    return content
