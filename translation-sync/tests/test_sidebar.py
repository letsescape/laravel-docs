import json
import tempfile
import unittest
from pathlib import Path

from sync import sidebar


class SidebarSyncTests(unittest.TestCase):
    def _write_repo(self, root: Path) -> None:
        (root / "versions.json").write_text(
            json.dumps(["master", "12.x"]),
            encoding="utf-8",
        )
        docs = root / "i18n/en/docusaurus-plugin-content-docs/version-master"
        docs.mkdir(parents=True)
        (docs / "documentation.md").write_text(
            "\n".join(
                [
                    "- ## Getting Started",
                    "    - [Installation](/docs/{{version}}/installation)",
                    "    - [Agentic Development](/docs/master/ai)",
                    "    - [Jetstream](https://jetstream.laravel.com)",
                    "- ## The Basics",
                    "    - [Requests](/docs/{{version}}/requests)",
                    "- ## Packages",
                    "    - [Dusk](/docs/{{version}}/dusk)",
                    "- ## Testing",
                    "    - [Browser Tests](/docs/{{version}}/dusk)",
                    "- [API Documentation](https://api.laravel.com/docs/11.x)",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        for doc in ("installation", "ai", "requests", "dusk"):
            (docs / f"{doc}.md").write_text(f"# {doc}\n", encoding="utf-8")

        sidebar_path = root / "versioned_sidebars/version-master-sidebars.json"
        sidebar_path.parent.mkdir(parents=True)
        sidebar_path.write_text(
            json.dumps(
                {
                    "tutorialSidebar": [
                        {
                            "type": "category",
                            "label": "시작하기",
                            "collapsed": False,
                            "items": [
                                {
                                    "type": "doc",
                                    "id": "installation",
                                    "label": "설치",
                                    "key": "installation",
                                }
                            ],
                            "key": "Getting Started",
                        }
                    ]
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        for locale in ("ko", "ja"):
            locale_path = (
                root
                / "i18n"
                / locale
                / "docusaurus-plugin-content-docs"
                / "version-master.json"
            )
            locale_path.parent.mkdir(parents=True)
            locale_path.write_text("{}", encoding="utf-8")

    def test_sync_version_writes_sidebar_from_documentation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(result.issues, [])
            self.assertTrue(result.changed)
            synced = json.loads(
                (root / "versioned_sidebars/version-master-sidebars.json").read_text(
                    encoding="utf-8"
                )
            )
            first = synced["tutorialSidebar"][0]
            self.assertEqual(first["label"], "Getting Started")
            self.assertFalse(first["collapsed"])
            self.assertEqual(
                first["items"],
                [
                    {
                        "type": "doc",
                        "id": "installation",
                        "label": "Installation",
                        "key": "installation",
                    },
                    {
                        "type": "doc",
                        "id": "ai",
                        "label": "Agentic Development",
                        "key": "ai",
                    },
                    {
                        "type": "link",
                        "label": "Jetstream",
                        "href": "https://jetstream.laravel.com",
                    },
                ],
            )
            self.assertEqual(synced["tutorialSidebar"][1]["label"], "The Basics")
            self.assertEqual(
                synced["tutorialSidebar"][2]["items"][0],
                {"type": "doc", "id": "dusk", "label": "Dusk", "key": "dusk"},
            )
            self.assertEqual(
                synced["tutorialSidebar"][3]["items"][0],
                {
                    "type": "doc",
                    "id": "dusk",
                    "label": "Browser Tests",
                    "key": "dusk-testing",
                },
            )
            self.assertEqual(
                synced["tutorialSidebar"][4],
                {
                    "type": "link",
                    "label": "API Documentation",
                    "href": "https://api.laravel.com/docs/12.x",
                },
            )
            self.assertFalse(
                (
                    root
                    / "i18n/ko/docusaurus-plugin-content-docs/version-master.json"
                ).exists()
            )
            self.assertFalse(
                (
                    root
                    / "i18n/ja/docusaurus-plugin-content-docs/version-master.json"
                ).exists()
            )

    def test_verify_mode_reports_stale_sidebar_and_locale_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)

            result = sidebar.sync_version("master", write=False, repo_root=root)

            self.assertIn("sidebar JSON out of sync", result.issues)
            self.assertTrue(
                any("locale sidebar JSON remains" in issue for issue in result.issues)
            )


if __name__ == "__main__":
    unittest.main()
