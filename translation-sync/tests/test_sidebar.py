import importlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from sync import sidebar


class SidebarSyncTests(unittest.TestCase):
    def test_sync_sidebar_attribute_is_the_sidebar_package(self) -> None:
        package = importlib.import_module("sync.sidebar")
        generator = importlib.import_module("sync.sidebar.generator")

        self.assertIs(sidebar, package)
        self.assertIs(sidebar.generator, generator)

    def test_load_versions_rejects_duplicates_and_misordered_stable_versions(self) -> None:
        cases = (
            ["master", "13.x", "13.x", "12.x"],
            ["master", "13.x", "013.x", "12.x"],
            ["master", "12.x", "13.x"],
        )
        for versions in cases:
            with self.subTest(versions=versions), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "versions.json").write_text(
                    json.dumps(versions),
                    encoding="utf-8",
                )

                with self.assertRaisesRegex(ValueError, "versions.json"):
                    sidebar.load_versions(root)

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

    def test_sync_version_unlinks_locale_sidebar_symlink_not_its_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            victim = root / "victim.json"
            victim.write_text('{"preserved": true}\n', encoding="utf-8")
            locale_path = (
                root
                / "i18n/ko/docusaurus-plugin-content-docs/version-master.json"
            )
            locale_path.unlink()
            locale_path.symlink_to(victim)

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(result.issues, [])
            self.assertEqual(
                victim.read_text(encoding="utf-8"),
                '{"preserved": true}\n',
            )
            self.assertFalse(locale_path.is_symlink())

    def test_sync_version_replaces_sidebar_hardlink_without_mutating_other_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            original = sidebar_path.read_text(encoding="utf-8")
            victim = root / "victim-sidebar.json"
            victim.write_text(original, encoding="utf-8")
            sidebar_path.unlink()
            sidebar_path.hardlink_to(victim)

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(result.issues, [])
            self.assertEqual(victim.read_text(encoding="utf-8"), original)
            self.assertNotEqual(
                sidebar_path.read_text(encoding="utf-8"),
                original,
            )
            self.assertFalse(sidebar_path.samefile(victim))

    def test_versioned_sidebar_preserves_historical_api_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            docs = root / "i18n/en/docusaurus-plugin-content-docs/version-12.x"
            docs.mkdir(parents=True)
            (docs / "documentation.md").write_text(
                "\n".join(
                    [
                        "- ## Getting Started",
                        "    - [Installation](/docs/{{version}}/installation)",
                        "- [API Documentation](https://api.laravel.com/docs/12.x)",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (docs / "installation.md").write_text("# installation\n", encoding="utf-8")

            result = sidebar.sync_version("12.x", write=True, repo_root=root)

            self.assertEqual(result.issues, [])
            synced = json.loads(
                (root / "versioned_sidebars/version-12.x-sidebars.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                synced["tutorialSidebar"][1],
                {
                    "type": "link",
                    "label": "API Documentation",
                    "href": "https://api.laravel.com/docs/12.x",
                },
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

    def test_reports_invalid_tutorial_sidebar_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            sidebar_path.write_text(
                json.dumps({"tutorialSidebar": None}),
                encoding="utf-8",
            )

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                result.issues,
                [
                    "invalid sidebar JSON schema: "
                    "tutorialSidebar must be a list"
                ],
            )

    def test_sync_version_refuses_sidebar_output_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            victim = root / "victim-sidebar.json"
            original = '{"tutorialSidebar": []}\n'
            victim.write_text(original, encoding="utf-8")
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            sidebar_path.unlink()
            sidebar_path.symlink_to(victim)

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(victim.read_text(encoding="utf-8"), original)
            self.assertEqual(
                result.issues,
                ["sidebar JSON path must not be a symlink"],
            )
            self.assertTrue(sidebar_path.is_symlink())

    def test_rejects_unsafe_version_before_building_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)

            with self.assertRaises(ValueError):
                sidebar.sync_version("../12.x", write=True, repo_root=root)

    def test_safe_repo_path_rejects_lexical_path_outside_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repo"
            root.mkdir()

            with self.assertRaisesRegex(ValueError, "path escapes repository"):
                sidebar.generator._safe_repo_path(
                    base / "outside.json",
                    root,
                )

    def test_sync_version_rejects_sidebar_parent_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repo"
            root.mkdir()
            self._write_repo(root)
            outside = base / "outside"
            outside.mkdir()
            outside_sidebar = outside / "version-master-sidebars.json"
            original = '{"preserved": true}\n'
            outside_sidebar.write_text(original, encoding="utf-8")
            sidebar_dir = root / "versioned_sidebars"
            (sidebar_dir / "version-master-sidebars.json").unlink()
            sidebar_dir.rmdir()
            sidebar_dir.symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "path escapes repository"):
                sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                outside_sidebar.read_text(encoding="utf-8"),
                original,
            )

    def test_supports_future_version_listed_in_versions_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            (root / "versions.json").write_text(
                json.dumps(["master", "14.x"]), encoding="utf-8"
            )
            docs = root / "i18n/en/docusaurus-plugin-content-docs/version-14.x"
            docs.mkdir(parents=True)
            (docs / "documentation.md").write_text(
                "- ## Getting Started\n"
                "    - [Installation](/docs/{{version}}/installation)\n",
                encoding="utf-8",
            )
            (docs / "installation.md").write_text(
                "# Installation\n", encoding="utf-8"
            )

            result = sidebar.sync_version("14.x", write=True, repo_root=root)

            self.assertEqual(result.issues, [])
            self.assertTrue(
                (root / "versioned_sidebars/version-14.x-sidebars.json").exists()
            )

    def test_reports_documentation_links_outside_supported_grammar(self):
        cases = (
            '- [Installation](/docs/{{version}}/installation "Install")',
            "- [API](https://api.example.com/a_(b))",
        )
        for line in cases:
            with self.subTest(line=line):
                items, issues = sidebar.parse_documentation(
                    line, version="master", latest_stable="13.x"
                )

                self.assertEqual(items, [])
                self.assertEqual(
                    issues,
                    ["line 1: unsupported or malformed documentation link"],
                )

    def test_reports_unindented_doc_link_outside_category(self):
        items, issues = sidebar.parse_documentation(
            "- ## Getting Started\n"
            "- [Installation](/docs/{{version}}/installation)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(items[0]["items"], [])
        self.assertEqual(issues, ["line 2: doc link is outside a category"])

    def test_malformed_category_closes_previous_category(self):
        items, issues = sidebar.parse_documentation(
            "- ## Getting Started\n"
            "- ### The Basics\n"
            "    - [Requests](/docs/{{version}}/requests)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(items[0]["items"], [])
        self.assertEqual(
            issues,
            [
                "line 2: unsupported or malformed category",
                "line 3: doc link is outside a category",
            ],
        )

    def test_relative_link_outside_docs_path_remains_link(self):
        items, issues = sidebar.parse_documentation(
            "- ## Resources\n"
            "    - [Support](/support)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertEqual(
            items[0]["items"],
            [{"type": "link", "label": "Support", "href": "/support"}],
        )

    def test_master_preserves_deep_api_link(self):
        href = "https://api.laravel.com/docs/12.x/deep#anchor"
        items, issues = sidebar.parse_documentation(
            f"- [Deep API]({href})\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertEqual(
            items,
            [{"type": "link", "label": "Deep API", "href": href}],
        )

    def test_reports_duplicate_category_translation_key(self):
        _items, issues = sidebar.parse_documentation(
            "- ## Same\n"
            "- ## Same\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(
            issues,
            ["line 2: duplicate category translation key: Same"],
        )

    def test_reports_duplicate_link_translation_key(self):
        _items, issues = sidebar.parse_documentation(
            "- [Same](https://first.example)\n"
            "- [Same](https://second.example)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(
            issues,
            ["line 2: duplicate link translation key: Same"],
        )

    def test_cli_rejects_all_with_version(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            sidebar.main(["--all", "--version", "master"])

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("not allowed with argument", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
