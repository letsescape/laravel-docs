"""들여쓰기 코드 블록의 보수적 fenced code 변환 검증."""

import unittest

from sync import preprocess


class IndentedCodeTests(unittest.TestCase):
    """코드·목록·문장 들여쓰기 판별 경계 검증."""

    def test_converts_indented_code_blocks_to_fenced_code_blocks(self):
        """명확한 들여쓰기 코드를 fenced code block으로 변환."""

        source = (
            "Configure the commands array:\n\n"
            "    'commands' => [\n"
            "        // App\\Console\\Commands\\ExampleCommand::class,\n"
            "    ],\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(
            result.text,
            "Configure the commands array:\n\n"
            "```\n"
            "'commands' => [\n"
            "    // App\\Console\\Commands\\ExampleCommand::class,\n"
            "],\n"
            "```\n",
        )

    def test_keeps_blank_lines_inside_indented_code_blocks(self):
        """들여쓰기 코드 내부 빈 줄 보존."""

        source = (
            "Example:\n\n"
            "    <?php\n"
            "\n"
            "    namespace App\\Console\\Commands;\n"
            "\n"
            "    use Illuminate\\Console\\Command;\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(
            result.text,
            "Example:\n\n"
            "```\n"
            "<?php\n"
            "\n"
            "namespace App\\Console\\Commands;\n"
            "\n"
            "use Illuminate\\Console\\Command;\n"
            "```\n",
        )

    def test_keeps_phpdoc_lines_inside_indented_code_blocks(self):
        """들여쓰기 코드 내부 PHPDoc 구조 보존."""

        source = (
            "Example:\n\n"
            "    class SendEmails extends Command\n"
            "    {\n"
            "        /**\n"
            "         * Execute the console command.\n"
            "         */\n"
            "        public function handle(): void\n"
            "        {\n"
            "            // ...\n"
            "        }\n"
            "    }\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(
            result.text,
            "Example:\n\n"
            "```\n"
            "class SendEmails extends Command\n"
            "{\n"
            "    /**\n"
            "     * Execute the console command.\n"
            "     */\n"
            "    public function handle(): void\n"
            "    {\n"
            "        // ...\n"
            "    }\n"
            "}\n"
            "```\n",
        )

    def test_does_not_convert_indented_nested_lists_to_code_blocks(self):
        """중첩 목록을 code block으로 변환하지 않음."""

        source = (
            "- First item\n"
            "    - Nested item\n"
            "    - Another nested item\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_ambiguous_indented_prose(self):
        """코드임을 확정할 수 없는 들여쓰기 문장 보존."""

        source = "Paragraph.\n\n    This is indented prose, not code.\n"

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_keeps_indented_children_with_unindented_directive_parent(self):
        """들여쓰기된 Blade directive 하위 구조 보존."""

        source = (
            "@once\n"
            "    @push('scripts')\n"
            "        <script>\n"
            "            // ...\n"
            "        </script>\n"
            "    @endpush\n"
            "@endonce\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_indented_yaml_children_with_list_parent(self):
        """목록 아래 YAML 하위 구조 보존."""

        source = (
            "features:\n"
            "- elasticsearch:\n"
            "    version: 7.9.0\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_code_looking_list_continuations_indented(self):
        """코드처럼 보이는 목록 설명의 들여쓰기 보존."""

        cases = (
            "- Configure the worker\n"
            "    Run php artisan queue:work in the project.\n",
            "1. Configure the worker\n\n"
            "    APP_ENV=local\n",
        )
        for source in cases:
            with self.subTest(source=source):
                self.assertEqual(preprocess.preprocess(source).text, source)

    def test_keeps_parenthesized_ordered_list_continuations_indented(self):
        """괄호형 순서 목록의 들여쓰기 설명 보존."""

        source = "1) Configure the worker\n\n    APP_ENV=local\n"

        self.assertEqual(preprocess.preprocess(source).text, source)

    def test_converts_indented_literal_fence_as_code_content(self):
        """코드 내용의 backtick보다 긴 fence 선택."""

        source = "Example:\n\n    echo one;\n    ```\n    echo two;\n"

        self.assertEqual(
            preprocess.preprocess(source).text,
            "Example:\n\n````\necho one;\n```\necho two;\n````\n",
        )


if __name__ == "__main__":
    unittest.main()
