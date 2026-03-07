import os
import time

import openai
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from utils.anchor import validate_anchors
from utils.common import retry, timeout


class AnchorValidationError(Exception):
    """앵커 검증 실패 시 발생하는 예외. retry 데코레이터가 재시도할 수 있도록 예외로 처리."""
    pass

SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_cached_client = None
_cached_model = None
_cached_prompt = None


def get_translation_client():
    """
    Retrieve an AI translation client and model name based on environment variables.

    Returns:
        tuple: A tuple containing the AI client instance and the model name.

    Raises:
        ValueError: If required environment variables are missing or if the translation provider is unsupported.
    """
    global _cached_client, _cached_model
    if _cached_client is not None:
        return _cached_client, _cached_model

    provider = os.environ.get("TRANSLATION_PROVIDER", "openai").lower()
    model = os.environ.get("TRANSLATION_MODEL", "gpt-4.1")

    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 미설정")

        client = openai.OpenAI(api_key=api_key)

    elif provider == "azure":
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-05-01-preview")

        if not api_key or not endpoint:
            raise ValueError("AZURE_OPENAI_API_KEY 또는 AZURE_OPENAI_ENDPOINT 미설정")

        client = openai.AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )

    else:
        raise ValueError(f"미지원 번역 제공자: {provider}")

    _cached_client = client
    _cached_model = model
    return client, model


def _get_system_prompt():
    """시스템 프롬프트를 캐싱하여 반환"""
    global _cached_prompt
    if _cached_prompt is None:
        prompt_path = os.path.join(SOURCE_DIR, "prompt.md")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            _cached_prompt = f.read()
    return _cached_prompt


def translate_text_with_openai(text_to_translate, system_prompt):
    """
    Translates the given text using an AI chat completion API and a specified system prompt.

    Parameters:
        text_to_translate (str): The text to be translated.
        system_prompt (str): The system prompt guiding the translation.

    Returns:
        str: The translated text.

    Raises:
        ValueError: If the API returns an empty response.
    """
    client, model = get_translation_client()
    system_message = ChatCompletionSystemMessageParam(role="system", content=system_prompt)
    user_message = ChatCompletionUserMessageParam(role="user", content=text_to_translate)

    response = client.chat.completions.create(
        model=model,
        messages=[system_message, user_message]
    )

    if not response.choices:
        raise ValueError("API returned empty choices")

    result = response.choices[0].message.content
    if result is None:
        raise ValueError("API returned empty content")
    return result


@retry(max_attempts=3, delay=3, backoff=2, exceptions=(Exception,))
@timeout(seconds=1000)
def translate_file(source_file, target_file):
    """
    Translates a markdown file from English to Korean using the OpenAI API and saves the result.

    After translation, validates that all internal anchors from the original file are preserved
    and that all anchor references in the translated file point to valid anchor definitions.
    If validation fails, the translated file is not saved.

    Parameters:
        source_file (str): Path to the source markdown file.
        target_file (str): Path where the translated file will be saved.

    Returns:
        bool: True if translation succeeds and the file is saved; False if the source file is empty.

    Raises:
        AnchorValidationError: If anchor validation fails (triggers retry).
    """
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            print(f"빈 파일: {source_file}")
            return False

        print(f"번역 시작: {source_file}")

        system_prompt = _get_system_prompt()
        translated_content = translate_text_with_openai(content, system_prompt)

        is_valid, errors = validate_anchors(content, translated_content)
        if not is_valid:
            error_msg = f"앵커 검증 실패: {source_file}"
            for error in errors:
                error_msg += f"\n  - {error}"
            print(error_msg)
            raise AnchorValidationError(error_msg)

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"번역 완료: {source_file} -> {target_file}")
        return True

    except openai.RateLimitError as e:
        print(f"RateLimitError: {e}")
        time.sleep(30)
        raise
    except Exception as e:
        print(f"번역 오류: {type(e).__name__}")
        raise
