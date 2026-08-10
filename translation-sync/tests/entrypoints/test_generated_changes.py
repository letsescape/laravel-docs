"""generated changes 동작과 경계 조건 검증."""

import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from subprocess import CompletedProcess
from types import SimpleNamespace
from unittest.mock import Mock, patch

import validate_generated_changes
from sync.common.stale_links import DEFAULT_STALE_LINK_REGISTRY
from sync.runtime.failure import IssueCode
from sync.verification.document import VerifiedLocaleArtifact


def _artifact(
    *,
    version: str = "13.x",
    locale_bytes: bytes = b"translated\n",
) -> VerifiedLocaleArtifact:
    """산출물 처리."""

    return VerifiedLocaleArtifact(
        schema_version=1,
        locale_bytes=locale_bytes,
        version=version,
        registry_sha256="a" * 64,
        verification_input_sha256="b" * 64,
    )


def _runner_for(*outputs: bytes):
    """runner for 처리."""

    pending = list(outputs)
    calls: list[tuple[list[str], dict[str, object]]] = []

    def run(args, **kwargs):
        """실행."""

        calls.append((list(args), kwargs))
        return CompletedProcess(args, 0, stdout=pending.pop(0), stderr=b"")

    return run, calls


class GeneratedChangeTests(unittest.TestCase):
    """generated 변경 동작과 경계 조건 테스트 모음."""

    def test_changed_entries_normalizes_staged_rename_records(self):
        """`changed_entries`의 staged rename record 정규화 검증."""

        rename_and_modify = (
            b"R100\0versioned_docs/version-13.x/old.md\0"
            b"versioned_docs/version-13.x/new.md\0"
            b"M\0versioned_sidebars/version-13.x-sidebars.json\0"
        )
        runner, _calls = _runner_for(b"", rename_and_modify, b"")

        changes = validate_generated_changes.changed_entries(
            Path("/repo"),
            process_runner=runner,
            environment={"PATH": "/usr/bin"},
        )

        self.assertEqual(
            changes,
            {
                "versioned_docs/version-13.x/old.md": {"D"},
                "versioned_docs/version-13.x/new.md": {"A"},
                "versioned_sidebars/version-13.x-sidebars.json": {"M"},
            },
        )

    def test_changed_entries_normalizes_copy_records_to_the_new_path(self):
        """`changed_entries`의 copy record 후 신규 경로 정규화 검증."""

        copy = (
            b"C087\0versioned_docs/version-13.x/source.md\0"
            b"versioned_docs/version-13.x/copy.md\0"
        )
        runner, _calls = _runner_for(b"", copy, b"")

        changes = validate_generated_changes.changed_entries(
            Path("/repo"),
            process_runner=runner,
            environment={},
        )

        self.assertEqual(
            changes,
            {"versioned_docs/version-13.x/copy.md": {"A"}},
        )

    def test_changed_entries_rejects_malformed_git_output(self):
        """`changed_entries`의 malformed Git 출력 거부 검증."""

        invalid_outputs = (
            b"R100\0versioned_docs/version-13.x/old.md\0",
            b"M\0../README.md\0",
            (
                b"R999\0versioned_docs/version-13.x/old.md\0"
                b"versioned_docs/version-13.x/new.md\0"
            ),
        )

        for output in invalid_outputs:
            with self.subTest(output=output):
                runner, _calls = _runner_for(output)
                with self.assertRaises(
                    validate_generated_changes._ValidationFailure
                ) as raised:
                    validate_generated_changes.changed_entries(
                        Path("/repo"),
                        process_runner=runner,
                        environment={},
                    )

                self.assertEqual(
                    raised.exception.code,
                    IssueCode.RUNNER_OPERATION_FAILED,
                )

    def test_git_calls_use_one_deadline_and_a_sanitized_environment(self):
        """`git_calls_use_one_deadline_and_a_sanitized_environment` 시나리오 검증."""

        runner, calls = _runner_for(b"", b"", b"")
        clock = Mock(side_effect=[90.0, 91.0, 92.0])

        validate_generated_changes.changed_entries(
            Path("/repo"),
            process_runner=runner,
            workflow_deadline=100.0,
            clock=clock,
            environment={
                "PATH": "/usr/bin",
                "LANG": "C.UTF-8",
                "LC_TEST": "locale",
                "OPENAI_API_KEY": "secret",
                "AZURE_OPENAI_API_KEY": "secret",
                "CODEX_API_KEY": "secret",
                "GH_TOKEN": "secret",
                "SSH_AUTH_SOCK": "/secret/socket",
            },
        )

        self.assertEqual([call[1]["timeout"] for call in calls], [10.0, 9.0, 8.0])
        for command, kwargs in calls:
            self.assertEqual(command[:3], ["git", "-c", "core.fsmonitor=false"])
            self.assertFalse(kwargs["shell"])
            self.assertIs(kwargs["stdin"], subprocess.DEVNULL)
            self.assertFalse(kwargs["check"])
            self.assertTrue(kwargs["capture_output"])
            self.assertEqual(kwargs["env"]["PATH"], "/usr/bin")
            self.assertEqual(kwargs["env"]["LC_TEST"], "locale")
            for secret in (
                "OPENAI_API_KEY",
                "AZURE_OPENAI_API_KEY",
                "CODEX_API_KEY",
                "GH_TOKEN",
                "SSH_AUTH_SOCK",
            ):
                self.assertNotIn(secret, kwargs["env"])

    def test_git_timeout_is_a_workflow_deadline_failure(self):
        """`git_timeout`의 워크플로 기한 실패 판정 검증."""

        def timeout(args, **_kwargs):
            """timeout 처리."""

            raise subprocess.TimeoutExpired(args, 1)

        with self.assertRaises(validate_generated_changes._ValidationFailure) as raised:
            validate_generated_changes.changed_entries(
                Path("/repo"),
                process_runner=timeout,
                workflow_deadline=100.0,
                clock=lambda: 90.0,
                environment={},
            )

        self.assertEqual(
            raised.exception.code,
            IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
        )

    def test_only_translation_outputs_are_allowed(self):
        """`only_translation_outputs_are_allowed` 시나리오 검증."""

        paths = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md",
            "versioned_docs/version-13.x/cache.md",
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md",
            "versioned_sidebars/version-13.x-sidebars.json",
            "i18n/ko/docusaurus-plugin-content-docs/version-13.x.json",
            "i18n/ja/docusaurus-plugin-content-docs/version-master.json",
            "README.md",
            ".github/workflows/deploy.yml",
        }

        self.assertEqual(
            validate_generated_changes.unexpected_paths(paths),
            [".github/workflows/deploy.yml", "README.md"],
        )

    def test_rejects_unsupported_versions_and_unpaired_locale_outputs(self):
        """지원하지 않는 버전 및 unpaired locale 출력 거부 검증."""

        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-999.x/cache.md": {"M"},
            "versioned_docs/version-13.x/orphan.md": {"M"},
        }

        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x", "master"}),
            [
                (
                    "unsupported translation version: "
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-999.x/cache.md"
                ),
                "unpaired translation document: version-13.x/orphan.md",
            ],
        )

    def test_accepts_complete_translation_document_triplet(self):
        """complete 번역 문서 triplet 허용 검증."""

        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
            "versioned_docs/version-13.x/cache.md": {"M"},
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
        }

        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x"}),
            [],
        )

    def test_accepts_nested_translation_document_triplet(self):
        """중첩 번역 문서 triplet 허용 검증."""

        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/guides/queues.md": {
                "A"
            },
            "versioned_docs/version-13.x/guides/queues.md": {"A"},
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/guides/queues.md": {
                "A"
            },
        }

        self.assertEqual(validate_generated_changes.unexpected_paths(changes), [])
        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x"}),
            [],
        )

    def test_rejects_noncanonical_nested_document_segments(self):
        """비정규 중첩 문서 segments 거부 검증."""

        paths = {
            "versioned_docs/version-13.x/guides/../queues.md",
            "versioned_docs/version-13.x/guides\\queues.md",
        }

        self.assertEqual(
            validate_generated_changes.unexpected_paths(paths),
            sorted(paths),
        )

    def test_only_verified_artifacts_can_approve_unchanged_locales(self):
        """`only_verified_artifacts_can_approve_unchanged_locales` 시나리오 검증."""

        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
        }
        key = ("13.x", "cache.md", "ko")

        self.assertEqual(
            validate_generated_changes.validate_changes(
                changes,
                {"13.x"},
                verified_unchanged={key},
            ),
            [("unverified unchanged translation: version-13.x/cache.md (ko)")],
        )
        self.assertEqual(
            validate_generated_changes.validate_changes(
                changes,
                {"13.x"},
                verified_unchanged={key: _artifact()},
            ),
            [],
        )

    def _write_verification_fixture(self, root: Path) -> tuple[Path, Path]:
        """verification fixture 기록."""

        registry = root / "translation-sync/stale-links.json"
        registry.parent.mkdir(parents=True)
        registry.write_bytes(DEFAULT_STALE_LINK_REGISTRY.raw)
        source = root / "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md"
        source.parent.mkdir(parents=True)
        source.write_text("Install the package.\n", encoding="utf-8")
        target = root / "versioned_docs/version-13.x/cache.md"
        target.parent.mkdir(parents=True)
        target.write_text(
            "<!-- Install the package. -->\n패키지를 설치합니다.\n",
            encoding="utf-8",
        )
        return source, target

    def test_proves_unchanged_locale_with_fresh_full_document_inputs(self):
        """`proves_unchanged_locale_with_fresh_full_document_inputs` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target = self._write_verification_fixture(root)
            changes = {
                str(source.relative_to(root)): {"M"},
                "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
            }

            verified = validate_generated_changes.verified_unchanged_locales(
                changes,
                root,
            )
            expected_locale_bytes = target.read_bytes()

        artifact = verified[("13.x", "cache.md", "ko")]
        self.assertIsInstance(artifact, VerifiedLocaleArtifact)
        self.assertEqual(artifact.locale_bytes, expected_locale_bytes)
        self.assertEqual(artifact.version, "13.x")
        self.assertEqual(
            artifact.registry_sha256,
            DEFAULT_STALE_LINK_REGISTRY.sha256,
        )

    def test_final_document_verifier_refusal_never_creates_a_proof(self):
        """`final_document_verifier_refusal_never`의 proof 생성 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _target = self._write_verification_fixture(root)
            changes = {
                str(source.relative_to(root)): {"M"},
                "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
            }
            refused = SimpleNamespace(
                issues=(object(),),
                verification_input_sha256=None,
                artifact=None,
            )
            captured: dict[str, object] = {}

            def refuse(inputs, *, registry_at_start, final_snapshot):
                """refuse 처리."""

                final_input, registry_at_end = final_snapshot()
                captured.update(
                    {
                        "initial": inputs,
                        "final": final_input,
                        "start_registry": registry_at_start,
                        "end_registry": registry_at_end,
                    }
                )
                return refused

            with patch.object(
                validate_generated_changes.document_verification,
                "verify_document",
                side_effect=refuse,
            ) as verifier:
                verified = validate_generated_changes.verified_unchanged_locales(
                    changes,
                    root,
                )

        self.assertEqual(verified, {})
        verifier.assert_called_once()
        initial = captured["initial"]
        final = captured["final"]
        start_registry = captured["start_registry"]
        end_registry = captured["end_registry"]
        self.assertIsNot(initial, final)
        self.assertIsNot(start_registry, end_registry)
        self.assertEqual(
            initial.verification_input_sha256,
            final.verification_input_sha256,
        )
        self.assertEqual(initial.annotation_map_bytes, final.annotation_map_bytes)
        expected_map = validate_generated_changes.document_verification.parse_expected_annotation_map(
            initial.annotation_map_bytes
        )
        self.assertEqual(
            [entry.annotation for entry in expected_map.entries],
            ["<!-- Install the package. -->"],
        )

    def test_changed_final_input_cannot_create_a_proof(self):
        """`changed_final_input_cannot_create_a_proof` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _target = self._write_verification_fixture(root)
            changes = {
                str(source.relative_to(root)): {"M"},
                "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
            }
            reads = [
                ("<!-- Install the package. -->\n패키지를 설치합니다.\n").encode(),
                b"<!-- Install the package. -->\nchanged\n",
            ]

            with patch.object(
                validate_generated_changes,
                "_read_optional_locale",
                side_effect=reads,
            ):
                verified = validate_generated_changes.verified_unchanged_locales(
                    changes,
                    root,
                )

        self.assertEqual(verified, {})

    def test_final_snapshot_filesystem_failure_is_not_downgraded(self):
        """`final_snapshot_filesystem_failure`의 않음 downgraded 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, _target = self._write_verification_fixture(root)
            changes = {
                str(source.relative_to(root)): {"M"},
                "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
            }
            final_failure = validate_generated_changes._ValidationFailure(
                IssueCode.RUNNER_OPERATION_FAILED,
                "English verification source could not be read",
            )

            with (
                patch.object(
                    validate_generated_changes,
                    "_read_source",
                    side_effect=[b"Install the package.\n", final_failure],
                ),
                self.assertRaises(
                    validate_generated_changes._ValidationFailure
                ) as raised,
            ):
                validate_generated_changes.verified_unchanged_locales(
                    changes,
                    root,
                )

        self.assertEqual(
            raised.exception.code,
            IssueCode.RUNNER_OPERATION_FAILED,
        )

    def test_rejects_symlink_output_leaf_and_ancestor(self):
        """symlink 출력 leaf 및 ancestor 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "outside"
            outside.mkdir()
            (outside / "cache.md").write_text("outside\n", encoding="utf-8")

            leaf = root / "versioned_docs/version-13.x/cache.md"
            leaf.parent.mkdir(parents=True)
            leaf.symlink_to(outside / "cache.md")

            ancestor = root / "i18n/en/docusaurus-plugin-content-docs/version-13.x"
            ancestor.parent.mkdir(parents=True)
            ancestor.symlink_to(outside, target_is_directory=True)

            self.assertEqual(
                validate_generated_changes.unsafe_output_paths(
                    {
                        "versioned_docs/version-13.x/cache.md",
                        (
                            "i18n/en/docusaurus-plugin-content-docs/"
                            "version-13.x/cache.md"
                        ),
                    },
                    root,
                ),
                [
                    ("i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md"),
                    "versioned_docs/version-13.x/cache.md",
                ],
            )

    def test_accepts_regular_and_deleted_output_paths(self):
        """regular 및 deleted 출력 경로 허용 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            regular = root / "versioned_docs/version-13.x/cache.md"
            regular.parent.mkdir(parents=True)
            regular.write_text("translated\n", encoding="utf-8")

            self.assertEqual(
                validate_generated_changes.unsafe_output_paths(
                    {
                        "versioned_docs/version-13.x/cache.md",
                        "versioned_docs/version-13.x/deleted.md",
                    },
                    root,
                ),
                [],
            )

    def test_rejects_mismatched_translation_deletion(self):
        """mismatched 번역 deletion 거부 검증."""

        changes = {
            "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md": {"D"},
            "versioned_docs/version-13.x/cache.md": {"D"},
            "i18n/ja/docusaurus-plugin-content-docs/version-13.x/cache.md": {"M"},
        }

        self.assertEqual(
            validate_generated_changes.validate_changes(changes, {"13.x"}),
            ["inconsistent translation status: version-13.x/cache.md"],
        )

    def test_rejects_combined_or_unknown_statuses(self):
        """combined 또는 unknown statuses 거부 검증."""

        for statuses in ({"A", "M"}, {"T"}, set()):
            with self.subTest(statuses=statuses):
                changes = {"versioned_sidebars/version-13.x-sidebars.json": statuses}
                self.assertEqual(
                    validate_generated_changes.validate_changes(changes, {"13.x"}),
                    [
                        (
                            "unsupported translation status: "
                            "versioned_sidebars/version-13.x-sidebars.json"
                        )
                    ],
                )

    def test_sidebar_paths_enforce_their_allowed_statuses(self):
        """공통 sidebar 삭제와 locale override 생성·수정 거부 검증."""

        cases = (
            (
                "versioned_sidebars/version-13.x-sidebars.json",
                {"D"},
                (
                    "shared sidebar deletion is forbidden: "
                    "versioned_sidebars/version-13.x-sidebars.json"
                ),
            ),
            (
                "i18n/ko/docusaurus-plugin-content-docs/version-13.x.json",
                {"A"},
                (
                    "locale sidebar override must only be deleted: "
                    "i18n/ko/docusaurus-plugin-content-docs/version-13.x.json"
                ),
            ),
            (
                "i18n/ja/docusaurus-plugin-content-docs/version-13.x.json",
                {"M"},
                (
                    "locale sidebar override must only be deleted: "
                    "i18n/ja/docusaurus-plugin-content-docs/version-13.x.json"
                ),
            ),
        )

        for path, statuses, expected in cases:
            with self.subTest(path=path, statuses=statuses):
                self.assertEqual(
                    validate_generated_changes.validate_changes(
                        {path: statuses}, {"13.x"}
                    ),
                    [expected],
                )

        self.assertEqual(
            validate_generated_changes.validate_changes(
                {
                    "versioned_sidebars/version-13.x-sidebars.json": {"A"},
                    "i18n/ja/docusaurus-plugin-content-docs/version-13.x.json": {"D"},
                },
                {"13.x"},
            ),
            [],
        )

    def test_changed_entries_rejects_non_utf8_paths(self):
        """UTF-8로 해석할 수 없는 Git 경로 거부 검증."""

        invalid_path = b"M\0versioned_docs/version-13.x/invalid-\xff.md\0"
        runner, _calls = _runner_for(invalid_path, b"", b"")

        with self.assertRaises(validate_generated_changes._ValidationFailure):
            validate_generated_changes.changed_entries(
                Path("/repo"),
                process_runner=runner,
                environment={},
            )

    def test_locale_sidebar_overrides_must_not_exist(self):
        """`locale_sidebar_overrides_must_not_exist` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            override = root / "i18n/ja/docusaurus-plugin-content-docs/version-13.x.json"
            override.parent.mkdir(parents=True)
            override.write_text("{}\n", encoding="utf-8")

            self.assertEqual(
                validate_generated_changes.existing_sidebar_overrides(root),
                ["i18n/ja/docusaurus-plugin-content-docs/version-13.x.json"],
            )

    def _write_versions(self, root: Path, contents: str | None = None) -> None:
        """버전 기록."""

        (root / "versions.json").write_text(
            contents or '["master", "13.x"]\n',
            encoding="utf-8",
        )

    def _main_failure(
        self,
        root: Path,
        *,
        unstaged: bytes = b"",
        environment: dict[str, str] | None = None,
        clock=lambda: 0.0,
    ) -> tuple[int, Path, str]:
        """명령줄 진입점 실행."""

        runner, _calls = _runner_for(unstaged, b"", b"")
        report = (root / "artifacts/failure.json").resolve(strict=False)
        report.parent.mkdir(exist_ok=True)
        runtime_environment = {
            validate_generated_changes.FAILURE_REPORT_ENV: str(report),
            validate_generated_changes.RUN_ID_ENV: "run-123",
            **(environment or {}),
        }
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = validate_generated_changes.main(
                repo_root=root,
                process_runner=runner,
                environment=runtime_environment,
                clock=clock,
            )
        return result, report, stderr.getvalue()

    def _read_canonical_report(self, path: Path) -> dict[str, object]:
        """canonical 보고서 읽기."""

        raw = path.read_bytes()
        value = json.loads(raw)
        self.assertEqual(
            raw,
            (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode(),
        )
        return value

    def test_main_reports_forbidden_paths_with_the_stable_code(self):
        """`main_reports_forbidden_paths_with_the_stable_code` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_versions(root)

            result, report, _stderr = self._main_failure(
                root,
                unstaged=b"M\0README.md\0",
            )

            value = self._read_canonical_report(report)
        self.assertEqual(result, 1)
        self.assertEqual(value["code"], "OUTPUT_PATH_FORBIDDEN")
        self.assertEqual(value["exit_code"], 1)

    def test_main_reports_an_allowed_path_symlink_as_forbidden(self):
        """`main_reports_an_allowed_path_symlink_as_forbidden` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_versions(root)
            outside = root / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            path = "versioned_docs/version-13.x/cache.md"
            output = root / path
            output.parent.mkdir(parents=True)
            output.symlink_to(outside)

            result, report, _stderr = self._main_failure(
                root,
                unstaged=f"M\0{path}\0".encode(),
            )

            value = self._read_canonical_report(report)
        self.assertEqual(result, 1)
        self.assertEqual(value["code"], "OUTPUT_PATH_FORBIDDEN")
        self.assertIn(
            "OUTPUT_STATE_MISMATCH",
            [issue["code"] for issue in value["issues"]],
        )

    def test_main_reports_status_mismatch_with_the_stable_code(self):
        """`main_reports_status_mismatch_with_the_stable_code` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_versions(root)
            path = "versioned_sidebars/version-13.x-sidebars.json"

            result, report, _stderr = self._main_failure(
                root,
                unstaged=f"T\0{path}\0".encode(),
            )

            value = self._read_canonical_report(report)
        self.assertEqual(result, 1)
        self.assertEqual(value["code"], "OUTPUT_STATE_MISMATCH")

    def test_main_reports_each_unverified_english_only_locale(self):
        """`main_reports_each_unverified_english_only_locale` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_versions(root)
            source = (
                root / "i18n/en/docusaurus-plugin-content-docs/version-13.x/cache.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("Install the package.\n", encoding="utf-8")
            registry = root / "translation-sync/stale-links.json"
            registry.parent.mkdir(parents=True)
            registry.write_bytes(DEFAULT_STALE_LINK_REGISTRY.raw)
            path = str(source.relative_to(root))

            result, report, _stderr = self._main_failure(
                root,
                unstaged=f"M\0{path}\0".encode(),
            )

            value = self._read_canonical_report(report)
        self.assertEqual(result, 1)
        self.assertEqual(value["code"], "UNVERIFIED_ENGLISH_ONLY_CHANGE")
        self.assertEqual(
            [issue["code"] for issue in value["issues"]],
            [
                "UNVERIFIED_ENGLISH_ONLY_CHANGE",
                "UNVERIFIED_ENGLISH_ONLY_CHANGE",
            ],
        )

    def test_main_reports_sidebar_override_and_versions_schema(self):
        """`main_reports_sidebar_override_and_versions_schema` 시나리오 검증."""

        scenarios = (
            ("override", "SIDEBAR_OVERRIDE_FORBIDDEN"),
            ("versions", "SIDEBAR_INPUT_INVALID"),
        )
        for scenario, expected in scenarios:
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                if scenario == "versions":
                    self._write_versions(root, "[]\n")
                else:
                    self._write_versions(root)
                    override = (
                        root / "i18n/ja/docusaurus-plugin-content-docs/"
                        "version-13.x.json"
                    )
                    override.parent.mkdir(parents=True)
                    override.write_text("{}\n", encoding="utf-8")

                result, report, _stderr = self._main_failure(root)
                value = self._read_canonical_report(report)

            self.assertEqual(result, 1)
            self.assertEqual(value["code"], expected)

    def test_main_reports_expired_deadline_without_starting_git(self):
        """`main_reports_expired_deadline_without_starting_git` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = (root / "failure.json").resolve(strict=False)
            runner = Mock()
            stderr = io.StringIO()
            environment = {
                validate_generated_changes.FAILURE_REPORT_ENV: str(report),
                validate_generated_changes.RUN_ID_ENV: "run-deadline",
                validate_generated_changes.WORKFLOW_DEADLINE_ENV: "100",
            }

            with redirect_stderr(stderr):
                result = validate_generated_changes.main(
                    repo_root=root,
                    process_runner=runner,
                    environment=environment,
                    clock=lambda: 100.0,
                )

            value = self._read_canonical_report(report)
        self.assertEqual(result, 2)
        self.assertEqual(value["code"], "WORKFLOW_DEADLINE_EXCEEDED")
        runner.assert_not_called()

    def test_main_maps_filesystem_inspection_failure_to_runner_failure(self):
        """`main`의 filesystem inspection 실패 후 runner 실패 매핑 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_versions(root)
            with patch.object(
                validate_generated_changes,
                "unsafe_output_paths",
                side_effect=PermissionError,
            ):
                result, report, _stderr = self._main_failure(root)

            value = self._read_canonical_report(report)
        self.assertEqual(result, 2)
        self.assertEqual(value["code"], "RUNNER_OPERATION_FAILED")

    def test_main_maps_git_failure_to_runner_failure(self):
        """`main_maps_git_failure_to_runner_failure` 시나리오 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = (root / "failure.json").resolve(strict=False)
            stderr = io.StringIO()
            environment = {
                validate_generated_changes.FAILURE_REPORT_ENV: str(report),
                validate_generated_changes.RUN_ID_ENV: "run-git-failure",
            }

            def fail_git(args, **_kwargs):
                """테스트용 Git 대체 동작."""

                return CompletedProcess(args, 128, stdout=b"", stderr=b"secret")

            with redirect_stderr(stderr):
                result = validate_generated_changes.main(
                    repo_root=root,
                    process_runner=fail_git,
                    environment=environment,
                )

            value = self._read_canonical_report(report)
        self.assertEqual(result, 2)
        self.assertEqual(value["code"], "RUNNER_OPERATION_FAILED")
        self.assertNotIn("secret", stderr.getvalue())

    def test_failure_report_is_published_no_replace(self):
        """`failure_report`의 published no replace 판정 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_versions(root)
            report = (root / "artifacts/failure.json").resolve(strict=False)
            report.parent.mkdir()
            report.write_bytes(b"sentinel")
            runner, _calls = _runner_for(b"M\0README.md\0", b"", b"")
            stderr = io.StringIO()
            environment = {
                validate_generated_changes.FAILURE_REPORT_ENV: str(report),
                validate_generated_changes.RUN_ID_ENV: "run-existing",
            }

            with redirect_stderr(stderr):
                result = validate_generated_changes.main(
                    repo_root=root,
                    process_runner=runner,
                    environment=environment,
                )
            report_contents = report.read_bytes()

        self.assertEqual(result, 2)
        self.assertEqual(report_contents, b"sentinel")
        self.assertIn("REPORT_WRITE_FAILED", stderr.getvalue())

    def test_main_rejects_invalid_versions_file_cleanly_without_report(self):
        """`main`의 잘못된 버전 파일 cleanly 제외 보고서 거부 검증."""

        stderr = io.StringIO()
        runner, _calls = _runner_for(b"", b"", b"")

        with tempfile.TemporaryDirectory() as tmp, redirect_stderr(stderr):
            root = Path(tmp)
            self._write_versions(root, "[]\n")
            result = validate_generated_changes.main(
                repo_root=root,
                process_runner=runner,
                environment={},
            )

        self.assertEqual(result, 1)
        self.assertEqual(
            stderr.getvalue(),
            "SIDEBAR_INPUT_INVALID: invalid versions.json: "
            "versions.json must not be empty\n",
        )


if __name__ == "__main__":
    unittest.main()
