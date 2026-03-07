import os
import tempfile
from unittest.mock import patch

from utils.translation import AnchorValidationError, translate_file


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
    @patch('utils.translation.translate_text_with_openai', return_value=BROKEN_TRANSLATION)
    def test_broken_anchors_raises_error(self, mock_translate, mock_prompt):
        """앵커 검증 실패 시 AnchorValidationError가 발생하고 파일이 저장되지 않는다."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, 'source.md')
            target = os.path.join(tmpdir, 'target.md')

            with open(source, 'w', encoding='utf-8') as f:
                f.write(ORIGINAL_CONTENT)

            try:
                _translate_file(source, target)
                assert False, "AnchorValidationError가 발생해야 합니다"
            except AnchorValidationError:
                pass

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
    def test_retry_on_anchor_failure_then_success(self, mock_translate, mock_prompt):
        """첫 번째 시도에서 앵커 검증 실패 후 재시도에서 성공하는 시나리오."""
        mock_translate.side_effect = [BROKEN_TRANSLATION, VALID_TRANSLATION]

        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, 'source.md')
            target = os.path.join(tmpdir, 'target.md')

            with open(source, 'w', encoding='utf-8') as f:
                f.write(ORIGINAL_CONTENT)

            # 첫 호출: AnchorValidationError
            try:
                _translate_file(source, target)
                assert False, "AnchorValidationError가 발생해야 합니다"
            except AnchorValidationError:
                pass

            assert not os.path.exists(target)

            # 두 번째 호출: 성공
            result = _translate_file(source, target)
            assert result is True
            assert os.path.exists(target)
