import re


def extract_anchor_definitions(markdown_text):
    """
    마크다운 텍스트에서 <a name="..."> 앵커 정의를 추출합니다.

    Parameters:
        markdown_text (str): 마크다운 텍스트

    Returns:
        set: 앵커 이름 집합
    """
    pattern = r'<a\s+name=["\']([^"\']+)["\']\s*(?:>|/>)'
    return set(re.findall(pattern, markdown_text))


def extract_anchor_references(markdown_text):
    """
    마크다운 텍스트에서 동일 문서 내 앵커 참조 (#anchor)를 추출합니다.
    [텍스트](#anchor) 형식만 추출하고, [텍스트](/path#anchor) 등 외부 참조는 제외합니다.

    Parameters:
        markdown_text (str): 마크다운 텍스트

    Returns:
        set: 참조된 앵커 이름 집합
    """
    pattern = r'\[[^\]]*\]\(#([^)]+)\)'
    return set(re.findall(pattern, markdown_text))


def validate_anchors(original_text, translated_text):
    """
    원본과 번역된 마크다운 간의 앵커 정합성을 검증합니다.

    검증 항목:
    1. 원본의 모든 <a name="..."> 앵커가 번역본에도 존재하는지 확인
    2. 번역본의 모든 내부 앵커 참조(#anchor)가 번역본 내 앵커 정의에 존재하는지 확인

    Parameters:
        original_text (str): 원본 마크다운 텍스트
        translated_text (str): 번역된 마크다운 텍스트

    Returns:
        tuple: (is_valid, errors)
            - is_valid (bool): 앵커 정합성 통과 여부
            - errors (list): 오류 메시지 목록
    """
    original_anchors = extract_anchor_definitions(original_text)
    translated_anchors = extract_anchor_definitions(translated_text)
    references = extract_anchor_references(translated_text)

    errors = []

    # 원본에 있는 앵커가 번역본에서 누락된 경우
    missing_anchors = original_anchors - translated_anchors
    if missing_anchors:
        errors.append(f"번역본에서 누락된 앵커: {sorted(missing_anchors)}")

    # 번역본의 앵커 참조가 앵커 정의에 없는 경우
    broken_refs = references - translated_anchors
    if broken_refs:
        errors.append(f"정의되지 않은 앵커 참조: {sorted(broken_refs)}")

    return len(errors) == 0, errors
