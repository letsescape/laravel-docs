import os
import tempfile
from unittest.mock import patch

import pytest

from utils.translation import AnchorValidationError, split_text_into_chunks, translate_file


def _get_unwrapped(func):
    """데코레이터를 제거한 원본 함수를 반환합니다."""
    while hasattr(func, '__wrapped__'):
        func = func.__wrapped__
    return func


# 데코레이터(@retry, @timeout)를 제거한 원본 함수로 테스트
_translate_file = _get_unwrapped(translate_file)

ORIGINAL_CONTENT = (
    '<a name="introduction"></a>\n'
    '## Introduction\n\n'
    '- [Installation](#installation)\n\n'
    '<a name="installation"></a>\n'
    '### Installation\n'
)

VALID_TRANSLATION = (
    '<a name="introduction"></a>\n'
    '## 소개 (Introduction)\n\n'
    '- [설치](#installation)\n\n'
    '<a name="installation"></a>\n'
    '### 설치\n'
)

BROKEN_TRANSLATION = (
    '<a name="소개"></a>\n'
    '## 소개 (Introduction)\n\n'
    '- [설치](#installation)\n\n'
    '### 설치\n'
)

ORIGINAL_WITH_MDX_SENSITIVE_HTML = (
    '<a name="introduction"></a>\n'
    '## Introduction\n\n'
    '<style>\n'
    '.badge { color: red; }\n'
    '</style>\n\n'
    '<img src="https://example.com/docs.png">\n'
)


class TestSplitTextIntoChunks:
    def test_splits_text_by_max_chunk_size(self):
        result = split_text_into_chunks("alpha\nbeta\ngamma\n", 11)
        assert result == ["alpha\nbeta\n", "gamma\n"]

    def test_does_not_split_inside_code_fence(self):
        source = "intro\n```php\n" + ("echo 'x';\n" * 4) + "```\noutro\n"
        result = split_text_into_chunks(source, 20)
        fenced_chunks = [chunk for chunk in result if "```php\n" in chunk]
        assert len(fenced_chunks) == 1
        assert fenced_chunks[0].endswith("```\n")

    def test_does_not_close_fence_with_different_marker(self):
        source = "intro\n```php\n" + ("~~~\necho 'x';\n" * 4) + "```\noutro\n"
        result = split_text_into_chunks(source, 20)
        fenced_chunks = [chunk for chunk in result if "```php\n" in chunk]
        assert len(fenced_chunks) == 1
        assert fenced_chunks[0].endswith("```\n")

    def test_rejects_non_positive_chunk_size(self):
        with pytest.raises(ValueError):
            split_text_into_chunks("content", 0)


class TestTranslateFileIntegration:
    @patch('utils.translation._get_system_prompt', return_value='system prompt')
    @patch('utils.translation.translate_text_with_openai', return_value=VALID_TRANSLATION)
    def test_valid_translation_writes_file(self, mock_translate, mock_prompt):
        """검증 통과 시 번역 파일이 저장되고 True를 반환한다."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, 'source.md')
            target = os.path.join(tmpdir, 'target.md')

            with open(source, 'w', encoding='utf-8') as f:
                f.write(ORIGINAL_CONTENT)

            result = _translate_file(source, target)

            assert result is True
            assert os.path.exists(target)
            with open(target, 'r', encoding='utf-8') as f:
                assert f.read() == VALID_TRANSLATION

    @patch('utils.translation._get_system_prompt', return_value='system prompt')
    @patch('utils.translation.translate_text_with_openai', side_effect=lambda chunk, _: chunk)
    def test_chunked_translation_combines_chunks(self, mock_translate, mock_prompt):
        """청킹된 번역 결과를 순서대로 결합해 저장한다."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, 'source.md')
            target = os.path.join(tmpdir, 'target.md')

            with open(source, 'w', encoding='utf-8') as f:
                f.write(ORIGINAL_CONTENT)

            with patch.dict(os.environ, {'TRANSLATION_CHUNK_SIZE': '20'}):
                result = _translate_file(source, target)

            assert result is True
            assert mock_translate.call_count >= 2
            with open(target, 'r', encoding='utf-8') as f:
                assert f.read() == ORIGINAL_CONTENT

    @patch('utils.translation._get_system_prompt', return_value='system prompt')
    @patch('utils.translation.translate_text_with_openai', return_value=ORIGINAL_WITH_MDX_SENSITIVE_HTML)
    def test_sanitizes_mdx_sensitive_html_before_write(self, mock_translate, mock_prompt):
        """MDX에서 깨지는 HTML 패턴을 저장 전에 보정한다."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, 'source.md')
            target = os.path.join(tmpdir, 'target.md')

            with open(source, 'w', encoding='utf-8') as f:
                f.write(ORIGINAL_WITH_MDX_SENSITIVE_HTML)

            result = _translate_file(source, target)

            assert result is True
            with open(target, 'r', encoding='utf-8') as f:
                saved = f.read()
            assert "<style>{`\n.badge { color: red; }\n`}</style>" in saved
            assert '<img src="https://example.com/docs.png" />' in saved

    @patch('utils.translation._get_system_prompt', return_value='system prompt')
    @patch('utils.translation.translate_text_with_openai', return_value=BROKEN_TRANSLATION)
    def test_broken_anchors_raises_error(self, mock_translate, mock_prompt):
        """앵커 검증 실패 시 AnchorValidationError가 발생하고 파일이 저장되지 않는다."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, 'source.md')
            target = os.path.join(tmpdir, 'target.md')

            with open(source, 'w', encoding='utf-8') as f:
                f.write(ORIGINAL_CONTENT)

            with pytest.raises(AnchorValidationError):
                _translate_file(source, target)

            assert not os.path.exists(target)

    @patch('utils.translation._get_system_prompt', return_value='system prompt')
    @patch('utils.translation.translate_text_with_openai')
    def test_empty_file_returns_false(self, mock_translate, mock_prompt):
        """빈 파일은 번역하지 않고 False를 반환한다."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, 'source.md')
            target = os.path.join(tmpdir, 'target.md')

            with open(source, 'w', encoding='utf-8') as f:
                f.write('   \n\n  ')

            result = _translate_file(source, target)

            assert result is False
            assert not os.path.exists(target)
            mock_translate.assert_not_called()

    @patch('utils.translation._get_system_prompt', return_value='system prompt')
    @patch('utils.translation.translate_text_with_openai')
    @patch('utils.common.time.sleep', return_value=None)
    def test_retry_on_anchor_failure_then_success(self, mock_sleep, mock_translate, mock_prompt):
        """첫 번째 시도에서 앵커 검증 실패 후 재시도에서 성공하는 시나리오."""
        mock_translate.side_effect = [BROKEN_TRANSLATION, VALID_TRANSLATION]

        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, 'source.md')
            target = os.path.join(tmpdir, 'target.md')

            with open(source, 'w', encoding='utf-8') as f:
                f.write(ORIGINAL_CONTENT)

            result = translate_file(source, target)
            assert result is True
            assert os.path.exists(target)
            assert mock_translate.call_count == 2
