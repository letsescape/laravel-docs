import os
import time

import openai
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from utils.common import retry, timeout
from utils.filtering import filter_markdown
from utils.token_counter import get_token_count

SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_translation_client():
    """
    Retrieve an AI translation client and model name based on environment variables.
    
    Returns:
        tuple: A tuple containing the AI client instance and the model name.
    
    Raises:
        ValueError: If required environment variables are missing or if the translation provider is unsupported.
    """
    provider = os.environ.get("TRANSLATION_PROVIDER", "openai").lower()
    model = os.environ.get("TRANSLATION_MODEL", "gpt-4.1")

    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 미설정")

        openai.api_key = api_key
        client = openai.OpenAI()
        return client, model

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
        return client, model

    else:
        raise ValueError(f"미지원 번역 제공자: {provider}")


def translate_text_with_openai(text_to_translate, system_prompt):
    """
    Translates the given text using an AI chat completion API and a specified system prompt.
    
    Parameters:
        text_to_translate (str): The text to be translated.
        system_prompt (str): The system prompt guiding the translation.
    
    Returns:
        str: The translated text.
    
    Raises:
        Exception: If the API call fails.
    """
    client, model = get_translation_client()
    system_message = ChatCompletionSystemMessageParam(role="system", content=system_prompt)
    user_message = ChatCompletionUserMessageParam(role="user", content=text_to_translate)

    # 번역 요청
    response = client.chat.completions.create(
        model=model,
        messages=[system_message, user_message]
    )
    return response.choices[0].message.content


@retry(max_attempts=3, delay=3, backoff=2, exceptions=(Exception,))
@timeout(seconds=1000)
def translate_file(source_file, target_file, source_lang="en", target_lang="ko"):
    """
    Translates a markdown file from the source language to the target language using the OpenAI API and saves the result.
    
    Reads the source markdown file, applies version-based filtering, constructs a system prompt, and translates the content in a single API call. The translated content is written to the specified target file. Handles rate limiting and general exceptions during the translation process.
    
    Parameters:
        source_file (str): Path to the source markdown file.
        target_file (str): Path where the translated file will be saved.
        source_lang (str): Source language code (default: "en").
        target_lang (str): Target language code (default: "ko").
    
    Returns:
        bool: True if translation succeeds and the file is saved; False if the source file is empty.
    """
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            print(f"빈 파일: {source_file}")
            return False

        print(f"번역 시작: {source_file}")

        # 버전 정보 추출
        version = None
        abs_target_path = os.path.abspath(target_file).replace("\\", "/")
        if '/version-8.x/' in abs_target_path:
            version = '8.x'
        elif '/version-9.x/' in abs_target_path:
            version = '9.x'
        elif '/version-10.x/' in abs_target_path:
            version = '10.x'
        elif '/version-11.x/' in abs_target_path:
            version = '11.x'
        elif '/version-12.x/' in abs_target_path:
            version = '12.x'
        elif '/version-master/' in abs_target_path:
            version = 'master'

        content = filter_markdown(content, version)

        # 시스템 프롬프트 설정
        prompt_path = os.path.join(SOURCE_DIR, "prompt.md")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt_template = f.read()
        system_prompt = system_prompt_template.format(source_lang=source_lang, target_lang=target_lang)

        content_tokens = get_token_count(content)
        print(f"{source_file}: {content_tokens:,} 토큰")

        translated_content = translate_text_with_openai(content, system_prompt)
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
