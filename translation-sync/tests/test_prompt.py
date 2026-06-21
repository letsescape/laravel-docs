import tempfile
import unittest
from pathlib import Path

from sync import prompt


class PromptTests(unittest.TestCase):
    def test_loads_prompt_file_verbatim(self):
        with tempfile.TemporaryDirectory() as tmp:
            prompt_path = Path(tmp) / "prompt.md"
            prompt_path.write_text("# Prompt\n\nRules.\n", encoding="utf-8")

            self.assertEqual(prompt.load_prompt(prompt_path), "# Prompt\n\nRules.")

    def test_missing_prompt_file_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            prompt_path = Path(tmp) / "missing.md"

            with self.assertRaises(prompt.PromptError):
                prompt.load_prompt(prompt_path)


if __name__ == "__main__":
    unittest.main()
