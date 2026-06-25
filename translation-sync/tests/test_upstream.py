import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync import upstream


class UpstreamSyncTests(unittest.TestCase):
    def test_sync_version_copies_markdown_bytes_without_normalization(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo_dir = root / "upstream"
            repo_dir.mkdir()
            source = repo_dir / "example.md"
            raw = (
                b"# Title  \n"
                b"\n"
                b"> [!NOTE]  \n"
                b"Text with internal  spaces.   \n"
                b"```php\n"
                b"$value = 'kept';   \n"
                b"```"
            )
            source.write_bytes(raw)

            en_root = root / "i18n/en/docusaurus-plugin-content-docs"
            with patch.object(upstream, "EN_ROOT", en_root), patch.object(
                upstream, "_run"
            ):
                count = upstream.sync_version(repo_dir, "13.x")

            self.assertEqual(count, 1)
            self.assertEqual((en_root / "version-13.x/example.md").read_bytes(), raw)


if __name__ == "__main__":
    unittest.main()
