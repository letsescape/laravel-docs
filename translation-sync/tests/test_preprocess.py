import unittest

from sync import preprocess


class PreprocessTests(unittest.TestCase):
    def test_converts_indented_code_blocks_to_fenced_code_blocks(self):
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
        source = (
            "- First item\n"
            "    - Nested item\n"
            "    - Another nested item\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_long_fenced_code_blocks_intact(self):
        source = (
            "````markdown\n"
            "```php\n"
            "<style>.example { color: red; }</style>\n"
            "```\n"
            "````\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_inline_style_tag_references(self):
        source = (
            "Pulse will include this file within a `<style>` tag so it does not "
            "need to be published.\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)

    def test_keeps_indented_children_with_unindented_directive_parent(self):
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
        source = (
            "features:\n"
            "- elasticsearch:\n"
            "    version: 7.9.0\n"
        )

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, source)


if __name__ == "__main__":
    unittest.main()
