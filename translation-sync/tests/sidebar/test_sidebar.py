"""sidebar 동작과 경계 조건 검증."""

import hashlib
import importlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from sync import sidebar


class SidebarSyncTests(unittest.TestCase):
    """sidebar 동기화 동작과 경계 조건 테스트 모음."""

    def test_sync_sidebar_attribute_is_the_sidebar_package(self) -> None:
        """sync.sidebar 공개 속성이 sidebar package를 가리키는지 검증."""

        package = importlib.import_module("sync.sidebar")
        generator = importlib.import_module("sync.sidebar.generator")

        self.assertIs(sidebar, package)
        self.assertIs(sidebar.generator, generator)

    def test_load_versions_rejects_duplicates_and_misordered_stable_versions(self) -> None:
        """중복되거나 역순이 아닌 안정 버전 목록 거부 검증."""

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

    def test_load_versions_requires_at_least_one_stable_version(self) -> None:
        """안정 버전이 없는 버전 목록 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "versions.json").write_text('["master"]\n', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "stable version"):
                sidebar.load_versions(root)

    def test_load_versions_rejects_symlink(self) -> None:
        """저장소 밖 versions.json symlink를 따라 읽지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repo"
            root.mkdir()
            target = base / "versions.json"
            target.write_text('["master", "12.x"]\n', encoding="utf-8")
            (root / "versions.json").symlink_to(target)

            with self.assertRaisesRegex(
                ValueError,
                "versions.json path must not be a symlink",
            ):
                sidebar.load_versions(root)

    def _write_repo(self, root: Path) -> None:
        """사이드바 동기화용 테스트 저장소 구성."""

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
                            "key": "category:Getting Started",
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
        """영문 목차 기준 사이드바 생성과 override 삭제 검증."""

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
                        "key": "doc:installation",
                    },
                    {
                        "type": "doc",
                        "id": "ai",
                        "label": "Agentic Development",
                        "key": "doc:ai",
                    },
                    {
                        "type": "link",
                        "label": "Jetstream",
                        "href": "https://jetstream.laravel.com",
                        "key": "link:"
                        + hashlib.sha256(
                            b"https://jetstream.laravel.com"
                        ).hexdigest(),
                    },
                ],
            )
            self.assertEqual(synced["tutorialSidebar"][1]["label"], "The Basics")
            self.assertEqual(
                synced["tutorialSidebar"][2]["items"][0],
                {
                    "type": "doc",
                    "id": "dusk",
                    "label": "Dusk",
                    "key": "doc:dusk",
                },
            )
            self.assertEqual(
                synced["tutorialSidebar"][3]["items"][0],
                {
                    "type": "doc",
                    "id": "dusk",
                    "label": "Browser Tests",
                    "key": "doc:dusk:2",
                },
            )
            self.assertEqual(
                synced["tutorialSidebar"][4],
                {
                    "type": "link",
                    "label": "API Documentation",
                    "href": "https://api.laravel.com/docs/12.x",
                    "key": "link:"
                    + hashlib.sha256(
                        b"https://api.laravel.com/docs/11.x"
                    ).hexdigest(),
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
        """locale sidebar symlink만 삭제하고 대상 파일은 보존하는지 검증."""

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
        """사이드바 hardlink 교체 시 다른 이름의 inode 보존 검증."""

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

    def test_written_sidebar_bytes_use_recursive_utf8_key_order(self):
        """생성 JSON의 재귀적인 UTF-8 byte key 순서 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(result.issues, [])
            output = (
                root / "versioned_sidebars/version-master-sidebars.json"
            ).read_text(encoding="utf-8")
            self.assertIn(
                '    {\n'
                '      "collapsed": false,\n'
                '      "items": [\n'
                '        {\n'
                '          "id": "installation",\n'
                '          "key": "doc:installation",\n'
                '          "label": "Installation",\n'
                '          "type": "doc"\n'
                '        },',
                output,
            )
            self.assertTrue(output.endswith("\n"))

    def test_versioned_sidebar_preserves_historical_api_link(self):
        """안정 버전 사이드바의 과거 API 링크 보존 검증."""

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
                    "key": "link:"
                    + hashlib.sha256(
                        b"https://api.laravel.com/docs/12.x"
                    ).hexdigest(),
                },
            )

    def test_verify_mode_reports_stale_sidebar_and_locale_json(self):
        """검증 모드의 stale 사이드바와 locale override 보고 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)

            result = sidebar.sync_version("master", write=False, repo_root=root)

            self.assertIn("sidebar JSON out of sync", result.issues)
            self.assertTrue(
                any("locale sidebar JSON remains" in issue for issue in result.issues)
            )

    def test_all_version_validation_finishes_before_any_write_or_delete(self):
        """모든 버전 검증이 쓰기와 삭제보다 먼저 끝나는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            sidebar_path = root / "versioned_sidebars/version-master-sidebars.json"
            original_sidebar = sidebar_path.read_bytes()
            locale_paths = [
                root
                / "i18n"
                / locale
                / "docusaurus-plugin-content-docs/version-master.json"
                for locale in ("ko", "ja")
            ]

            results = sidebar.sync_versions(
                ["master", "12.x"],
                write=True,
                repo_root=root,
            )

            self.assertEqual(results[0].issues, [])
            self.assertEqual(
                results[1].issues,
                ["missing documentation.md for 12.x"],
            )
            self.assertEqual(sidebar_path.read_bytes(), original_sidebar)
            self.assertTrue(all(path.exists() for path in locale_paths))

    def test_all_version_candidate_applies_outputs_and_deletions_together(self):
        """모든 버전의 출력과 override 삭제를 함께 적용하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            docs = root / "i18n/en/docusaurus-plugin-content-docs/version-12.x"
            docs.mkdir(parents=True)
            (docs / "documentation.md").write_text(
                "- ## Stable\n"
                "    - [Installation](/docs/{{version}}/installation)\n",
                encoding="utf-8",
            )
            (docs / "installation.md").write_text(
                "# Installation\n",
                encoding="utf-8",
            )
            stable_locale_paths = [
                root
                / "i18n"
                / locale
                / "docusaurus-plugin-content-docs/version-12.x.json"
                for locale in ("ko", "ja")
            ]
            for path in stable_locale_paths:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}\n", encoding="utf-8")

            results = sidebar.sync_versions(
                ["master", "12.x"],
                write=True,
                repo_root=root,
            )

            self.assertTrue(all(result.issues == [] for result in results))
            stable_sidebar = json.loads(
                (
                    root / "versioned_sidebars/version-12.x-sidebars.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(
                stable_sidebar["tutorialSidebar"][0]["key"],
                "category:Stable",
            )
            self.assertTrue(all(not path.exists() for path in stable_locale_paths))

    def test_candidate_input_hash_change_aborts_before_write_or_delete(self):
        """적용 직전 입력 hash 변경 시 쓰기와 삭제 중단 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            sidebar_path = root / "versioned_sidebars/version-master-sidebars.json"
            documentation_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-master"
                / "documentation.md"
            )
            original_sidebar = sidebar_path.read_bytes()
            original_plan = sidebar.generator._plan_version
            plan_calls = 0

            def mutate_after_first_plan(version, *, repo_root):
                """첫 계획 이후 입력 문서를 변경하는 테스트 대역."""

                nonlocal plan_calls
                plan = original_plan(version, repo_root=repo_root)
                plan_calls += 1
                if plan_calls == 1:
                    documentation_path.write_bytes(
                        documentation_path.read_bytes() + b"\n"
                    )
                return plan

            with patch.object(
                sidebar.generator,
                "_plan_version",
                side_effect=mutate_after_first_plan,
            ):
                results = sidebar.sync_versions(
                    ["master"],
                    write=True,
                    repo_root=root,
                )

            self.assertEqual(plan_calls, 2)
            self.assertEqual(
                results[0].issues,
                ["sidebar candidate inputs changed before apply"],
            )
            self.assertEqual(sidebar_path.read_bytes(), original_sidebar)
            for locale in ("ko", "ja"):
                self.assertTrue(
                    (
                        root
                        / "i18n"
                        / locale
                        / "docusaurus-plugin-content-docs/version-master.json"
                    ).exists()
                )

    def test_candidate_input_hash_uses_the_documented_canonical_envelope(self):
        """입력 hash의 canonical envelope 구성 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            versions_json = b'["master","12.x"]\n'
            documentation = b"- ## Getting Started\n"
            generated_sidebar = b'{"tutorialSidebar":[]}\n'
            override_paths = (
                root
                / "i18n/ko/docusaurus-plugin-content-docs/version-master.json",
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-master.json",
            )
            plan = sidebar.generator._SidebarPlan(
                version="master",
                expected={"tutorialSidebar": []},
                documentation_bytes=documentation,
                approved_sidebar_bytes=None,
                generated_sidebar_bytes=generated_sidebar,
                sidebar_changed=True,
                locale_paths_to_remove=override_paths,
                issues=(),
            )
            expected_envelope = {
                "override_deletions": [
                    "i18n/ja/docusaurus-plugin-content-docs/version-master.json",
                    "i18n/ko/docusaurus-plugin-content-docs/version-master.json",
                ],
                "schema_version": 1,
                "versions": [
                    {
                        "baseline_sidebar_sha256": None,
                        "documentation_sha256": hashlib.sha256(
                            documentation
                        ).hexdigest(),
                        "generated_sidebar_sha256": hashlib.sha256(
                            generated_sidebar
                        ).hexdigest(),
                        "version": "master",
                    }
                ],
                "versions_sha256": hashlib.sha256(versions_json).hexdigest(),
            }
            canonical_envelope = (
                json.dumps(
                    expected_envelope,
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode("utf-8")
                + b"\n"
            )

            actual = sidebar.generator._candidate_input_hash(
                versions_json,
                [plan],
                repo_root=root,
            )

            self.assertEqual(
                actual,
                hashlib.sha256(canonical_envelope).hexdigest(),
            )

    def test_sync_versions_uses_versions_json_order_for_candidate_entries(self):
        """적용 후보가 versions.json 순서를 따르는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            stable_docs = (
                root / "i18n/en/docusaurus-plugin-content-docs/version-12.x"
            )
            stable_docs.mkdir(parents=True)
            (stable_docs / "documentation.md").write_text(
                "- ## Stable\n"
                "    - [Installation](/docs/{{version}}/installation)\n",
                encoding="utf-8",
            )
            (stable_docs / "installation.md").write_text(
                "# Installation\n",
                encoding="utf-8",
            )

            results = sidebar.sync_versions(
                ["12.x", "master"],
                write=False,
                repo_root=root,
            )

            self.assertEqual(
                [result.version for result in results],
                ["master", "12.x"],
            )

    def test_reports_invalid_tutorial_sidebar_schema(self):
        """tutorialSidebar가 배열이 아닌 기준본의 schema issue 검증."""

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

    def test_reports_missing_tutorial_sidebar_schema(self) -> None:
        """tutorialSidebar 필드가 없는 기준본의 schema issue 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            sidebar_path.write_text("{}\n", encoding="utf-8")

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                result.issues,
                [
                    "invalid sidebar JSON schema: "
                    "tutorialSidebar is required"
                ],
            )

    def test_non_boolean_existing_collapsed_fails_closed_without_write(self):
        """boolean이 아닌 기존 collapsed 값의 fail-closed 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            sidebar_path = root / "versioned_sidebars/version-master-sidebars.json"
            current = json.loads(sidebar_path.read_text(encoding="utf-8"))
            current["tutorialSidebar"][0]["collapsed"] = "false"
            original = json.dumps(current, ensure_ascii=False, indent=2) + "\n"
            sidebar_path.write_text(original, encoding="utf-8")

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                result.issues,
                [
                    "invalid sidebar JSON schema: category collapsed must be boolean: "
                    "category:Getting Started"
                ],
            )
            self.assertEqual(sidebar_path.read_text(encoding="utf-8"), original)
            for locale in ("ko", "ja"):
                self.assertTrue(
                    (
                        root
                        / "i18n"
                        / locale
                        / "docusaurus-plugin-content-docs/version-master.json"
                    ).exists()
                )

    def test_new_category_defaults_to_collapsed_true(self):
        """새 category의 collapsed 기본값 true 검증."""

        items, issues = sidebar.parse_documentation(
            "- ## Getting Started\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertTrue(items[0]["collapsed"])

    def test_sync_version_refuses_sidebar_output_symlink(self):
        """사이드바 출력 symlink와 대상 파일 보존 검증."""

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

    def test_sync_version_rejects_sidebar_output_directory(self) -> None:
        """사이드바 출력 위치의 디렉터리를 적용 전에 거부."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            sidebar_path.unlink()
            sidebar_path.mkdir()
            locale_path = (
                root
                / "i18n/ko/docusaurus-plugin-content-docs/version-master.json"
            )

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                result.issues,
                ["sidebar JSON path must be a regular file"],
            )
            self.assertFalse(result.changed)
            self.assertTrue(sidebar_path.is_dir())
            self.assertTrue(locale_path.is_file())

    def test_sync_version_rejects_documentation_directory(self) -> None:
        """영문 목차 위치의 디렉터리를 적용 전에 거부."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            documentation_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/"
                "version-master/documentation.md"
            )
            documentation_path.unlink()
            documentation_path.mkdir()
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            original_sidebar = sidebar_path.read_bytes()
            locale_path = (
                root
                / "i18n/ko/docusaurus-plugin-content-docs/version-master.json"
            )

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                result.issues,
                [
                    "documentation.md path must be a regular file for master"
                ],
            )
            self.assertFalse(result.changed)
            self.assertEqual(sidebar_path.read_bytes(), original_sidebar)
            self.assertTrue(locale_path.is_file())

    def test_sync_version_rejects_documentation_symlink(self) -> None:
        """영문 목차 symlink를 따라 읽지 않고 적용 전에 거부."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            documentation_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/"
                "version-master/documentation.md"
            )
            target = root / "external-documentation.md"
            target.write_bytes(documentation_path.read_bytes())
            documentation_path.unlink()
            documentation_path.symlink_to(target)
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            original_sidebar = sidebar_path.read_bytes()

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                result.issues,
                [
                    "documentation.md path must not be a symlink for master"
                ],
            )
            self.assertFalse(result.changed)
            self.assertEqual(sidebar_path.read_bytes(), original_sidebar)

    def test_sync_version_rejects_source_doc_symlink(self) -> None:
        """사이드바가 참조하는 영문 문서 symlink 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/"
                "version-master/installation.md"
            )
            target = root / "external-installation.md"
            target.write_bytes(source_path.read_bytes())
            source_path.unlink()
            source_path.symlink_to(target)
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            original_sidebar = sidebar_path.read_bytes()

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                result.issues,
                ["source doc path must not be a symlink: installation"],
            )
            self.assertFalse(result.changed)
            self.assertEqual(sidebar_path.read_bytes(), original_sidebar)

    def test_sync_version_rejects_locale_override_directory(self) -> None:
        """locale override 위치의 디렉터리를 적용 전에 거부."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)
            sidebar_path = (
                root / "versioned_sidebars/version-master-sidebars.json"
            )
            original_sidebar = sidebar_path.read_bytes()
            locale_path = (
                root
                / "i18n/ko/docusaurus-plugin-content-docs/version-master.json"
            )
            locale_path.unlink()
            locale_path.mkdir()
            other_locale_path = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-master.json"
            )

            result = sidebar.sync_version("master", write=True, repo_root=root)

            self.assertEqual(
                result.issues,
                [
                    "locale sidebar JSON path must be a regular file: "
                    "i18n/ko/docusaurus-plugin-content-docs/version-master.json"
                ],
            )
            self.assertFalse(result.changed)
            self.assertEqual(sidebar_path.read_bytes(), original_sidebar)
            self.assertTrue(locale_path.is_dir())
            self.assertTrue(other_locale_path.is_file())

    def test_rejects_unsafe_version_before_building_paths(self):
        """경로 생성 전 안전하지 않은 버전 token 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_repo(root)

            with self.assertRaises(ValueError):
                sidebar.sync_version("../12.x", write=True, repo_root=root)

    def test_safe_repo_path_rejects_lexical_path_outside_repo(self):
        """저장소 밖의 lexical 경로 거부 검증."""

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
        """사이드바 상위 디렉터리 symlink의 외부 쓰기 거부 검증."""

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
        """versions.json에 추가된 미래 버전 지원 검증."""

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
        """지원 문법 밖의 목차 링크를 issue로 보고하는지 검증."""

        cases = (
            '- [Installation](/docs/{{version}}/installation "Install")',
            "- [API](https://api.example.com/a_(b))",
            "- [   ](https://example.com)",
            "- [Invalid URL](http://[invalid)",
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
        """category 밖의 들여쓰지 않은 문서 링크 보고 검증."""

        items, issues = sidebar.parse_documentation(
            "- ## Getting Started\n"
            "- [Installation](/docs/{{version}}/installation)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(items[0]["items"], [])
        self.assertEqual(issues, ["line 2: doc link is outside a category"])

    def test_malformed_category_closes_previous_category(self):
        """잘못된 category가 이전 category 문맥을 닫는지 검증."""

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

    def test_reports_indented_category(self) -> None:
        """들여쓴 category 선언의 지원하지 않는 문법 보고 검증."""

        items, issues = sidebar.parse_documentation(
            "    - ## Getting Started\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(items, [])
        self.assertEqual(
            issues,
            ["line 1: unsupported or malformed category"],
        )

    def test_reports_indented_link_outside_category(self) -> None:
        """category 없는 들여쓴 링크의 루트 승격 방지 검증."""

        items, issues = sidebar.parse_documentation(
            "    - [Support](https://example.com/support)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(items, [])
        self.assertEqual(issues, ["line 1: link is outside a category"])

    def test_relative_link_outside_docs_path_remains_link(self):
        """문서 경로 밖의 상대 링크 보존 검증."""

        items, issues = sidebar.parse_documentation(
            "- ## Resources\n"
            "    - [Support](/support)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertEqual(
            items[0]["items"],
            [
                {
                    "type": "link",
                    "label": "Support",
                    "href": "/support",
                    "key": "link:"
                    + hashlib.sha256(b"/support").hexdigest(),
                }
            ],
        )

    def test_internal_deep_url_remains_link(self) -> None:
        """내부 deep URL의 버전 치환과 링크 항목 보존 검증."""

        href = "/docs/{{version}}/starter-kits#laravel-breeze"
        items, issues = sidebar.parse_documentation(
            "- ## Packages\n"
            f"    - [Breeze]({href})\n",
            version="10.x",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertEqual(
            items[0]["items"],
            [
                {
                    "type": "link",
                    "label": "Breeze",
                    "href": "/docs/10.x/starter-kits#laravel-breeze",
                    "key": "link:"
                    + hashlib.sha256(href.encode("utf-8")).hexdigest(),
                }
            ],
        )

    def test_master_preserves_deep_api_link(self):
        """master 사이드바의 deep API 링크 보존 검증."""

        href = "https://api.laravel.com/docs/12.x/deep#anchor"
        items, issues = sidebar.parse_documentation(
            f"- [Deep API]({href})\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertEqual(
            items,
            [
                {
                    "type": "link",
                    "label": "Deep API",
                    "href": href,
                    "key": "link:"
                    + hashlib.sha256(href.encode("utf-8")).hexdigest(),
                }
            ],
        )

    def test_master_normalizes_only_root_api_documentation_link(self):
        """master 루트 API Documentation 링크만 정규화하는지 검증."""

        old_href = "https://api.laravel.com/docs/12.x"
        items, issues = sidebar.parse_documentation(
            "- ## Resources\n"
            f"    - [API Documentation]({old_href})\n"
            f"- [Other API]({old_href})\n"
            f"- [API Documentation]({old_href})\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertEqual(items[0]["items"][0]["href"], old_href)
        self.assertEqual(items[1]["href"], old_href)
        self.assertEqual(
            items[2]["href"],
            "https://api.laravel.com/docs/13.x",
        )

    def test_reports_duplicate_category_translation_key(self):
        """중복 category translation key의 issue 보고 검증."""

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

    def test_reports_colliding_doc_translation_keys(self) -> None:
        """서로 다른 문서 ID가 만든 중복 doc key의 issue 보고 검증."""

        items, issues = sidebar.parse_documentation(
            "- ## First\n"
            "    - [Guide](/docs/{{version}}/guide)\n"
            "    - [Guide Again](/docs/{{version}}/guide)\n"
            "- ## Second\n"
            "    - [Collision](/docs/{{version}}/guide:2)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(
            items[1]["items"][0]["key"],
            "doc:guide:2",
        )
        self.assertEqual(
            issues,
            ["line 5: duplicate doc translation key: doc:guide:2"],
        )

    def test_generates_canonical_keys_with_global_occurrence_suffixes(self):
        """전역 등장 순서 suffix를 포함한 canonical key 생성 검증."""

        target = "https://example.test/reference"
        digest = hashlib.sha256(target.encode("utf-8")).hexdigest()
        items, issues = sidebar.parse_documentation(
            "- ## First\n"
            "    - [Shared](/docs/{{version}}/shared)\n"
            f"    - [Reference]({target})\n"
            "- ## Second\n"
            "    - [Shared Again](/docs/{{version}}/shared)\n"
            f"    - [Reference Again]({target})\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertEqual(items[0]["key"], "category:First")
        self.assertEqual(items[1]["key"], "category:Second")
        self.assertEqual(items[0]["items"][0]["key"], "doc:shared")
        self.assertEqual(items[1]["items"][0]["key"], "doc:shared:2")
        self.assertEqual(items[0]["items"][1]["key"], f"link:{digest}")
        self.assertEqual(items[1]["items"][1]["key"], f"link:{digest}:2")

    def test_same_label_different_targets_use_distinct_link_keys(self):
        """같은 label의 서로 다른 링크 대상 key 분리 검증."""

        items, issues = sidebar.parse_documentation(
            "- [Same](https://first.example)\n"
            "- [Same](https://second.example)\n",
            version="master",
            latest_stable="13.x",
        )

        self.assertEqual(issues, [])
        self.assertEqual(
            [item["key"] for item in items],
            [
                "link:"
                + hashlib.sha256(b"https://first.example").hexdigest(),
                "link:"
                + hashlib.sha256(b"https://second.example").hexdigest(),
            ],
        )

    def test_reports_link_digest_collision_for_different_raw_targets(self):
        """서로 다른 링크 대상의 digest 충돌 보고 검증."""

        with patch.object(sidebar.generator, "_link_digest", return_value="a" * 64):
            _items, issues = sidebar.parse_documentation(
                "- [First](https://first.example)\n"
                "- [Second](https://second.example)\n",
                version="master",
                latest_stable="13.x",
            )

        self.assertEqual(
            issues,
            [f"line 2: link digest collision: {'a' * 64}"],
        )

    def test_cli_rejects_all_with_version(self):
        """명령줄의 --all과 --version 동시 사용 거부 검증."""

        stderr = io.StringIO()
        with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            sidebar.main(["--all", "--version", "master"])

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("not allowed with argument", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
