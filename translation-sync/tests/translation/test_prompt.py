"""운영 프롬프트 로딩과 locale별 보존 규칙 검증."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync import prompt


class PromptTests(unittest.TestCase):
    """프롬프트 파일 입력 경계 검증."""

    def test_loads_prompt_file_verbatim(self):
        """본문 내부 공백 보존과 바깥 공백 제거."""

        with tempfile.TemporaryDirectory() as tmp:
            prompt_path = Path(tmp) / "prompt.md"
            prompt_path.write_text("# Prompt\n\nRules.\n", encoding="utf-8")

            self.assertEqual(prompt.load_prompt(prompt_path), "# Prompt\n\nRules.")

    def test_missing_prompt_file_is_an_error(self):
        """존재하지 않는 프롬프트 파일 거부."""

        with tempfile.TemporaryDirectory() as tmp:
            prompt_path = Path(tmp) / "missing.md"

            with self.assertRaises(prompt.PromptError):
                prompt.load_prompt(prompt_path)

    def test_unreadable_prompt_file_is_an_error(self):
        """읽을 수 없는 프롬프트 파일과 상세 오류 비공개."""

        prompt_path = Path("/fixture/prompt.md")

        with patch.object(
            Path,
            "read_text",
            side_effect=OSError("sensitive filesystem detail"),
        ):
            with self.assertRaisesRegex(
                prompt.PromptError,
                "could not read prompt file",
            ) as raised:
                prompt.load_prompt(prompt_path)

        self.assertNotIn("sensitive filesystem detail", str(raised.exception))

    def test_invalid_utf8_prompt_file_is_an_error(self):
        """UTF-8로 해석할 수 없는 프롬프트 파일 거부."""

        prompt_path = Path("/fixture/prompt.md")
        decode_error = UnicodeDecodeError(
            "utf-8",
            b"\xff",
            0,
            1,
            "invalid start byte",
        )

        with patch.object(
            Path,
            "read_text",
            side_effect=decode_error,
        ), self.assertRaisesRegex(prompt.PromptError, "could not read prompt file"):
            prompt.load_prompt(prompt_path)

    def test_japanese_prompt_forbids_dropping_a_markdown_link_target(self):
        """일본어 프롬프트의 Markdown 링크 대상 보존 규칙."""

        prompt_text = prompt.load_prompt(
            Path(__file__).resolve().parents[2] / "prompt_jp.md"
        )

        self.assertIn(
            "`[atomic locks](#atomic-locks)` を `[atomic locks]`",
            prompt_text,
        )

    def test_japanese_prompt_requires_a_leading_html_anchor(self):
        """일본어 프롬프트의 선행 HTML anchor 보존 규칙."""

        prompt_text = prompt.load_prompt(
            Path(__file__).resolve().parents[2] / "prompt_jp.md"
        )

        self.assertIn(
            "入力が `<a name=\"cache-locks\"></a>` で始まる場合",
            prompt_text,
        )

    def test_korean_prompt_forbids_expanding_a_markdown_link_target(self):
        """한국어 프롬프트의 Markdown 링크 대상 확장 금지 규칙."""

        prompt_text = prompt.load_prompt(
            Path(__file__).resolve().parents[2] / "prompt.md"
        )

        self.assertIn(
            "`[atomic locks](#atomic-locks)`를 "
            "`[atomic locks](/docs/{{version}}/cache#atomic-locks)`로",
            prompt_text,
        )

    def test_locale_prompts_require_canonical_paragraph_and_comment_output(self):
        """두 locale의 단일 물리 줄 문단과 주석 escape 규칙."""

        root = Path(__file__).resolve().parents[2]
        korean = prompt.load_prompt(root / "prompt.md")
        japanese = prompt.load_prompt(root / "prompt_jp.md")

        self.assertIn("물리적 한 줄로 출력", korean)
        self.assertIn("物理的な一行で出力", japanese)
        self.assertIn("`--&gt;`", korean)
        self.assertIn("`--&gt;`", japanese)

    def test_locale_prompts_forbid_external_tools(self):
        """두 locale의 파일 접근과 외부 도구 호출 금지 규칙."""

        root = Path(__file__).resolve().parents[2]
        korean = prompt.load_prompt(root / "prompt.md")
        japanese = prompt.load_prompt(root / "prompt_jp.md")

        self.assertIn("파일을 읽거나 쓰지 않고, 도구를 호출하지 않습니다", korean)
        self.assertIn("ファイルを読み書きせず、ツールを呼び出しません", japanese)

    def test_japanese_prompt_preserves_navigation_attributes_and_backticks(self):
        """일본어 프롬프트의 navigation 속성과 backtick 보존 규칙."""

        prompt_text = prompt.load_prompt(
            Path(__file__).resolve().parents[2] / "prompt_jp.md"
        )

        self.assertIn("`title`, `label` は英語原文のまま", prompt_text)
        self.assertIn("バッククォートは原文にある場合だけ", prompt_text)


if __name__ == "__main__":
    unittest.main()
