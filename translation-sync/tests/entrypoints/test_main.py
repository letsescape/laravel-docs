"""주 번역 파이프라인의 동작과 경계 조건 검증."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import call, patch

import main
from sync import config, diff, translate, verify


class MainPipelineTests(unittest.TestCase):
    """주 번역 파이프라인의 동작과 경계 조건 테스트 모음."""

    def _change_with_lines(
        self, path: str, lines: list[tuple[str, str]]
    ) -> diff.SourceChange:
        """줄 목록으로 원문 변경 객체 생성."""

        old_lineno = 1
        new_lineno = 1
        diff_lines: list[diff.DiffLine] = []
        for kind, text in lines:
            if kind == "delete":
                diff_lines.append(diff.DiffLine(kind, text, old_lineno, None))
                old_lineno += 1
            elif kind == "add":
                diff_lines.append(diff.DiffLine(kind, text, None, new_lineno))
                new_lineno += 1
            else:
                diff_lines.append(diff.DiffLine(kind, text, old_lineno, new_lineno))
                old_lineno += 1
                new_lineno += 1
        return diff.SourceChange(
            path=path,
            status="M",
            hunks=(
                diff.DiffHunk(
                    old_start=1,
                    old_count=old_lineno - 1,
                    new_start=1,
                    new_count=new_lineno - 1,
                    lines=tuple(diff_lines),
                ),
            ),
        )

    def test_translation_request_binds_the_current_response_contract(self):
        """번역 요청에 현재 응답 계약 버전을 지정하는지 검증."""

        request = main._translation_request("Source.\n", None)

        self.assertEqual(
            request.response_contract_version,
            main.response_contract.RESPONSE_CONTRACT_VERSION,
        )

    def test_modified_normalized_noop_preserves_exact_locale_bytes(self):
        """정규화 결과가 같은 수정에서 로케일 바이트를 그대로 보존하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                'Image <img src="x"/>.\n',
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            locale_bytes = b'<!-- Image <img src="x">. -->\ntranslated\n\n'
            dest.write_bytes(locale_bytes)
            change = self._change_with_lines(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/example.md"
                ),
                lines=[
                    ("delete", 'Image <img src="x">.'),
                    ("add", 'Image <img src="x"/>.'),
                ],
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=AssertionError("normalized no-op must not call provider"),
            ), patch.object(
                main,
                "_verify_and_admit_document",
                return_value=[],
            ) as admit, patch.object(
                main,
                "atomic_write_bytes",
                side_effect=AssertionError("normalized no-op must not write"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(dest.read_bytes(), locale_bytes)
            self.assertEqual(admit.call_args.args[1], locale_bytes)
            self.assertFalse(admit.call_args.kwargs["write"])

    def test_modified_block_reuses_the_current_pair_restore_map(self):
        """수정된 블록이 현재 원문 쌍의 복원 맵을 재사용하는지 검증."""

        first_uri = "data:image/png;base64,AAAA"
        changed_uri = "data:image/png;base64,BBBB"
        old = (
            f"First ![]({first_uri}).\n\n"
            f"Second old ![]({changed_uri}).\n"
        )
        current = (
            f"First ![]({first_uri}).\n\n"
            f"Second new ![]({changed_uri}).\n"
        )
        change = self._change_with_lines(
            path=(
                "i18n/en/docusaurus-plugin-content-docs/"
                "version-13.x/example.md"
            ),
            lines=[
                ("context", f"First ![]({first_uri})."),
                ("context", ""),
                ("delete", f"Second old ![]({changed_uri})."),
                ("add", f"Second new ![]({changed_uri})."),
            ],
        )
        plan, pair = main._build_modified_plan(change, current)
        placeholder = next(
            key
            for key, value in pair.current.placeholders.items()
            if value == changed_uri
        )
        prepared = main._prepare_block_translation(
            change,
            plan.changes[0],
            config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            ),
            "prompt",
            old,
            placeholders=pair.current.placeholders,
        )

        self.assertIn(placeholder, prepared.request_source)
        self.assertNotIn(changed_uri, prepared.request_source)
        self.assertIs(prepared.placeholders, pair.current.placeholders)

    def test_verified_artifact_bytes_are_the_only_admitted_bytes(self):
        """검증된 산출물 바이트만 최종 출력으로 승인하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dest = root / "versioned_docs/version-13.x/example.md"
            artifact_bytes = b"verified artifact\n"
            artifact = main.document_verification.VerifiedLocaleArtifact(
                schema_version=1,
                locale_bytes=artifact_bytes,
                version="13.x",
                registry_sha256="a" * 64,
                verification_input_sha256="b" * 64,
            )
            result = main.document_verification.VerificationResult(
                issues=(),
                verification_input_sha256="b" * 64,
                artifact=artifact,
            )

            with patch.object(
                main,
                "_document_verification_result",
                return_value=result,
            ):
                issues = main._verify_and_admit_document(
                    dest,
                    "unverified candidate",
                    "English source.",
                    "13.x",
                    {},
                    write=True,
                )

            self.assertEqual(issues, [])
            self.assertEqual(dest.read_bytes(), artifact_bytes)

    def test_canonical_document_cross_module_contract_produces_artifact(self):
        """모듈 간 정규 문서 계약으로 산출물을 생성하는지 검증."""

        source = (
            "## Title {.class #stable}\n\n"
            "First physical line\ncontinues with <img src=\"x\">.\n\n"
            "| Name | Value |\n"
            "| --- | --- |\n"
            "| Widget | enabled |\n"
        )
        locale = (
            "## Title {#stable}\n\n"
            "첫 물리 줄이\n이어지는 <img src=\"x\"/> 설명입니다.\n\n"
            "| 이름 | 값 |\n"
            "| --- | --- |\n"
            "| Widget | 활성 |\n"
        )

        result = main._document_verification_result(
            locale,
            source,
            "13.x",
            {},
            canonicalize=True,
        )

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)
        assert result.artifact is not None
        artifact_text = result.artifact.locale_bytes.decode("utf-8")
        self.assertIn("<!-- ## Title {.class #stable} -->", artifact_text)
        self.assertIn(
            '<!-- First physical line continues with <img src="x">. -->',
            artifact_text,
        )
        self.assertIn(
            "<!-- | Name | Value | | --- | --- | | Widget | enabled | -->",
            artifact_text,
        )

    def test_canonical_artifact_keeps_pre_stale_annotation_bytes(self):
        """정규 산출물이 오래된 링크 처리 전 주석 바이트를 유지하는지 검증."""

        source = "See [Controller](#actions-handled-by-resource-controller).\n"
        locale = (
            "[Controller](#actions-handled-by-resource-controllers)를 "
            "참고하세요.\n"
        )

        result = main._document_verification_result(
            locale,
            source,
            "10.x",
            {},
            canonicalize=True,
        )

        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.artifact)
        assert result.artifact is not None
        artifact_text = result.artifact.locale_bytes.decode("utf-8")
        self.assertIn(
            "<!-- See [Controller](#actions-handled-by-resource-controller). -->",
            artifact_text,
        )
        self.assertIn(
            "[Controller](#actions-handled-by-resource-controllers)",
            artifact_text,
        )

    def test_verification_issue_never_creates_a_locale_file(self):
        """검증 문제 발생 시 로케일 파일을 생성하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dest = root / "versioned_docs/version-13.x/example.md"
            result = main.document_verification.VerificationResult(
                issues=(
                    main.document_verification.VerificationIssue(
                        "PIPELINE_ANNOTATION_MISMATCH",
                        "annotations",
                        "invalid annotation owner",
                    ),
                ),
                verification_input_sha256="b" * 64,
                artifact=None,
            )

            with patch.object(
                main,
                "_document_verification_result",
                return_value=result,
            ):
                issues = main._verify_and_admit_document(
                    dest,
                    "candidate",
                    "English source.",
                    "13.x",
                    {},
                    write=True,
                )

            self.assertIn("PIPELINE_ANNOTATION_MISMATCH", issues[0])
            self.assertFalse(dest.exists())

    def test_change_sort_uses_versions_then_utf8_document_bytes(self):
        """변경 사항을 버전과 UTF-8 문서 바이트 순서로 정렬하는지 검증."""

        changes = [
            diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-12.x/z.md"
                ),
                status="A",
            ),
            diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/b.md"
                ),
                status="A",
            ),
            diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/a.md"
                ),
                status="A",
            ),
        ]

        with patch.object(
            main.sidebar,
            "load_versions",
            return_value=["master", "13.x", "12.x"],
        ):
            ordered = main._sort_changes(changes)

        self.assertEqual(
            [(change.version, change.document) for change in ordered],
            [("13.x", "a.md"), ("13.x", "b.md"), ("12.x", "z.md")],
        )

    def test_global_preflight_rejects_a_later_plan_before_provider_or_write(self):
        """전역 사전 검사가 공급자 호출이나 기록 전에 후속 계획 오류를 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_root = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x"
            )
            source_root.mkdir(parents=True)
            (source_root / "a.md").write_text(
                "A valid paragraph for translation.\n",
                encoding="utf-8",
            )
            (source_root / "b.md").write_text(
                "| A | B |\n|---|---|\n| only one |\n",
                encoding="utf-8",
            )
            changes = [
                diff.SourceChange(
                    path=(
                        "i18n/en/docusaurus-plugin-content-docs/"
                        "version-13.x/a.md"
                    ),
                    status="A",
                ),
                diff.SourceChange(
                    path=(
                        "i18n/en/docusaurus-plugin-content-docs/"
                        "version-13.x/b.md"
                    ),
                    status="A",
                ),
            ]
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )
            stderr = io.StringIO()

            with redirect_stderr(stderr), patch.object(
                main,
                "REPO_ROOT",
                root,
            ), patch.object(
                main.sys,
                "argv",
                ["main.py"],
            ), patch.object(
                main.config,
                "load_config",
                return_value=cfg,
            ), patch.object(
                main,
                "_load_prompts",
                return_value={"ko": "ko", "ja": "ja"},
            ), patch.object(
                main.upstream,
                "main",
                return_value=0,
            ), patch.object(
                main,
                "_select_changes",
                return_value=changes,
            ), patch.object(
                main.translate,
                "translate_request",
                side_effect=AssertionError("provider must not run during preflight"),
            ), patch.object(
                main,
                "_translate_one",
                side_effect=AssertionError("execution must not begin"),
            ), patch.object(
                main,
                "_delete_outputs",
                side_effect=AssertionError("deletion must not begin"),
            ):
                exit_code = main.main()

            self.assertEqual(exit_code, 1)
            self.assertIn("patch preflight failed", stderr.getvalue())
            self.assertFalse((root / "versioned_docs").exists())
            self.assertFalse((root / "i18n/ja").exists())

    def test_request_time_config_error_is_reported_without_traceback(self):
        """요청 시점 설정 오류를 트레이스백 없이 보고하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("Translate this paragraph.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            change = diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/example.md"
                ),
                status="A",
            )
            cfg = config.Config(
                provider="unsupported",
                values={"TRANSLATION_PROVIDER": "unsupported"},
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertIn("translation configuration failed", issues[0])
            self.assertIn("PROVIDER_SELECTION_INVALID", issues[0])
            self.assertFalse(dest.exists())

    def test_translate_one_reports_incomplete_translation_without_writing_output(self):
        """불완전한 번역을 출력 기록 없이 보고하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Translate this new document paragraph.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=translate.IncompleteTranslation("timeout"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertTrue(
                any(issue.startswith("incomplete translation") for issue in issues)
            )
            self.assertFalse(dest.exists())

    def test_added_document_requests_each_prose_owner_and_preserves_front_matter(self):
        """추가된 문서의 각 산문 소유 단위를 번역 요청하고 프런트 매터를 보존하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "---\n"
                "title: Example\n"
                "description: Create plan fixture.\n"
                "---\n\n"
                "# Example\n\n"
                "First source paragraph.\n\n"
                "Second source paragraph.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            responses = iter(
                (
                    "<!-- First source paragraph. -->\n첫 번째 번역 문단.",
                    "<!-- Second source paragraph. -->\n두 번째 번역 문단.",
                )
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=lambda *_args, **_kwargs: next(responses),
            ) as request_mock, patch.object(
                main.response_contract,
                "verify",
                return_value=[],
            ), patch.object(main.verify, "verify", return_value=[]):
                issues = main._translate_added_document(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "---\n"
                "title: Example\n"
                "description: Create plan fixture.\n"
                "---\n\n"
                "<!-- # Example -->\n"
                "# Example\n\n"
                "<!-- First source paragraph. -->\n"
                "첫 번째 번역 문단.\n\n"
                "<!-- Second source paragraph. -->\n"
                "두 번째 번역 문단.\n",
            )
            self.assertEqual(request_mock.call_count, 2)
            requests = [call.args[0].source for call in request_mock.call_args_list]
            self.assertIn("First source paragraph.", requests[0])
            self.assertIn("Second source paragraph.", requests[1])
            self.assertNotIn("description: Create plan fixture.", "\n".join(requests))

    def test_added_document_rejects_invalid_provider_contract_without_writing(self):
        """추가된 문서의 잘못된 공급자 계약을 출력 기록 없이 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Acquire the cache lock before updating the value.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            echoed = "Acquire the cache lock before updating the value.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=echoed,
            ) as provider, patch.object(
                main.verify,
                "verify",
                return_value=[],
            ):
                issues = main._translate_added_document(change, cfg, "prompt", dest)

            self.assertIn("provider original comment mismatch", issues[0])
            self.assertEqual(provider.call_count, 5)
            self.assertFalse(dest.exists())

    def test_added_table_is_admitted_with_one_whole_table_owner(self):
        """추가된 표를 하나의 전체 표 소유자로 승인하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "| Name | Value |\n"
                "| --- | --- |\n"
                "| Widget | enabled |\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            change = diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/example.md"
                ),
                status="A",
            )
            cfg = config.Config(
                provider="cli",
                values={"TRANSLATION_PROVIDER": "cli"},
            )
            response = (
                "<!-- | Name | Value | | --- | --- | | Widget | enabled | -->\n"
                "| 이름 | 값 |\n"
                "| --- | --- |\n"
                "| Widget | 활성 |\n"
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=response,
            ):
                issues = main._translate_added_document(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertEqual(issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), response)
            self.assertEqual(dest.read_text(encoding="utf-8").count("<!--"), 1)

    def test_added_document_rejects_wrong_target_language_without_writing(self):
        """추가된 문서의 잘못된 대상 언어를 출력 기록 없이 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Acquire the cache lock before updating the shared cache value.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            japanese = (
                "<!-- Acquire the cache lock before updating the shared cache value. -->\n"
                "キャッシュロックを取得します。\n"
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=japanese,
            ) as provider:
                issues = main._translate_added_document(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertIn("provider target language mismatch", issues[0])
            self.assertEqual(
                provider.call_count,
                main.MAX_SEGMENT_VERIFICATION_ATTEMPTS,
            )
            self.assertFalse(dest.exists())

    def test_added_license_document_rejects_preserved_legal_english(self):
        """추가된 라이선스 문서에 보존된 법률 영문을 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/license.md"
            )
            source_path.parent.mkdir(parents=True)
            source = "Permission is hereby granted to use this software.\n"
            source_path.write_text(source, encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/license.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/license.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            translated = (
                "<!-- Permission is hereby granted to use this software. -->\n"
                "Permission is hereby granted to use this software.\n"
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=translated,
            ) as provider:
                issues = main._translate_added_document(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertTrue(
                any("provider target language mismatch" in issue for issue in issues)
            )
            self.assertEqual(
                provider.call_count,
                main.MAX_SEGMENT_VERIFICATION_ATTEMPTS,
            )
            self.assertFalse(dest.exists())

    def test_added_document_checks_deadline_after_response_evaluation(self):
        """추가된 문서가 응답 평가 후 실행 기한을 확인하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/guide.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("Source paragraph.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/guide.md"
            change = diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-12.x/guide.md"
                ),
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value="<!-- Source paragraph. -->\n번역 문단.\n",
            ), patch.object(
                main,
                "_contract_issues",
                return_value=[],
            ) as contract_check, patch.object(
                main.translate,
                "require_run_deadline",
                side_effect=translate.RunDeadlineExceeded("deadline expired"),
            ) as deadline_check:
                issues = main._translate_added_document(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                    deadline=10.0,
                )

            contract_check.assert_called_once()
            deadline_check.assert_called_once_with(10.0)
            self.assertEqual(
                issues,
                ["incomplete translation: deadline expired [RUN_DEADLINE_EXCEEDED]"],
            )
            self.assertFalse(dest.exists())

    def test_added_license_document_rejects_untranslated_nonlegal_intro(self):
        """추가된 라이선스 문서의 비법률 서문이 번역되지 않으면 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/license.md"
            )
            source_path.parent.mkdir(parents=True)
            source = "Read this introduction before reviewing the legal terms.\n"
            source_path.write_text(source, encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/license.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/license.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            untranslated = (
                "<!-- Read this introduction before reviewing the legal terms. -->\n"
                "Read this introduction before reviewing the legal terms.\n"
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=untranslated,
            ) as provider:
                issues = main._translate_added_document(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertIn("provider target language mismatch", issues[0])
            self.assertEqual(
                provider.call_count,
                main.MAX_SEGMENT_VERIFICATION_ATTEMPTS,
            )
            self.assertFalse(dest.exists())

    def test_repair_segment_translation_adds_missing_original_comments(self):
        """구간 번역 복구 시 누락된 원문 주석 추가 검증."""

        source = (
            "- [Using Eloquent](https://example.com/eloquent), models can be stored.\n"
            "- [Full-text search](https://example.com/scout/) using the `mongodb` Scout engine.\n"
        )
        translated = (
            "- [Using Eloquent](https://example.com/eloquent): 모델을 저장할 수 있습니다.\n"
            "- [Full-text search](https://example.com/scout/): `mongodb` Scout engine을 사용합니다.\n"
        )

        repaired = main._repair_segment_translation(source, translated, "13.x")

        self.assertEqual(verify.verify(repaired, source=source), [])

    def test_translate_one_updates_only_changed_blocks(self):
        """변경된 블록만 갱신하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\nNew text.\n\nAfter.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "이전 문장은 유지됩니다.\n\n"
                "<!-- Old text. -->\n"
                "예전 번역입니다.\n\n"
                "<!-- After. -->\n"
                "이후 문장도 유지됩니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "Old text."),
                    ("add", "New text."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                return "<!-- New text. -->\n새 번역입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertIn("## English Diff", sent[0])
            self.assertIn("- Old text.", sent[0])
            self.assertIn("+ New text.", sent[0])
            self.assertIn("## English Source", sent[0])
            self.assertIn("New text.", sent[0])
            self.assertNotIn("Before.", sent[0].split("## English Source", 1)[1])
            self.assertNotIn("After.", sent[0].split("## English Source", 1)[1])
            self.assertIn("## Existing Translation Context", sent[0])
            self.assertIn("예전 번역입니다.", sent[0])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "이전 문장은 유지됩니다.\n\n"
                "<!-- New text. -->\n"
                "새 번역입니다.\n\n"
                "<!-- After. -->\n"
                "이후 문장도 유지됩니다.\n",
            )

    def test_translate_one_preserves_following_code_and_anchor_after_replacement(self):
        """블록 교체 후 뒤따르는 코드와 앵커를 보존하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\nNew text.\n\n```php\n$value = true;\n```\n\n"
                '<a name="next"></a>\n#### Next\n',
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- Old text. -->\n"
                "예전 번역입니다.\n\n"
                "```php\n$value = true;\n```\n\n"
                '<a name="next"></a>\n'
                "<!-- #### Next -->\n"
                "#### Next\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "Old text."),
                    ("add", "New text."),
                    ("context", ""),
                    ("context", "```php"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                return "<!-- New text. -->\n새 번역입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- New text. -->\n"
                "새 번역입니다.\n\n"
                "```php\n$value = true;\n```\n\n"
                '<a name="next"></a>\n'
                "<!-- #### Next -->\n"
                "#### Next\n",
            )

    def test_translate_one_inserts_added_blocks_after_context(self):
        """추가된 블록을 앞 문맥 뒤에 삽입하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("Before.\n\nInserted.\n\nAfter.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- After. -->\n"
                "뒤 문장입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("add", "Inserted."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                return "<!-- Inserted. -->\n삽입된 문장입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertIn("+ Inserted.", sent[0])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- Inserted. -->\n"
                "삽입된 문장입니다.\n\n"
                "<!-- After. -->\n"
                "뒤 문장입니다.\n",
            )

    def test_translate_one_inserts_toc_item_with_raw_context(self):
        """원시 문맥을 기준으로 목차 항목을 삽입하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "# Example\n\n"
                "- [Before](#before)\n"
                "- [Callouts](#callouts)\n"
                "- [After](#after)\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- # Example -->\n"
                "# Example\n\n"
                "- [Before](#before)\n"
                "- [After](#after)\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "- [Before](#before)"),
                    ("add", "- [Callouts](#callouts)"),
                    ("context", "- [After](#after)"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                return "- [Callouts](#callouts)\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 0)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- # Example -->\n"
                "# Example\n\n"
                "- [Before](#before)\n"
                "- [Callouts](#callouts)\n"
                "- [After](#after)\n",
            )

    def test_translate_one_updates_only_the_changed_duplicate_bare_link_block(self):
        """중복된 일반 링크 블록 중 변경된 블록만 갱신하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/collections.md"
            )
            source_path.parent.mkdir(parents=True)
            unchanged_list = (
                "[reduce](#method-reduce)\n"
                "[reduceSpread](#method-reduce-spread)\n"
                "[reject](#method-reject)\n"
            )
            changed_list = (
                "[reduce](#method-reduce)\n"
                "[reduceInto](#method-reduce-into)\n"
                "[reduceSpread](#method-reduce-spread)\n"
                "[reject](#method-reject)\n"
            )
            source_path.write_text(
                f"{unchanged_list}\n{changed_list}",
                encoding="utf-8",
            )

            dest = root / "versioned_docs/version-13.x/collections.md"
            dest.parent.mkdir(parents=True)

            def annotated(link_list: str) -> str:
                """여러 줄 원문 주석이 포함된 링크 목록 생성."""

                return f"<!--\n{link_list}-->\n{link_list}"

            def canonical_annotated(link_list: str) -> str:
                """정규 원문 주석이 포함된 링크 목록 생성."""

                body = " ".join(link_list.split())
                return f"<!-- {body} -->\n{link_list}"

            original = f"{annotated(unchanged_list)}\n{annotated(unchanged_list)}"
            expected = (
                f"{canonical_annotated(unchanged_list)}\n"
                f"{canonical_annotated(changed_list)}"
            )
            dest.write_text(original, encoding="utf-8")

            change = self._change_with_lines(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/collections.md"
                ),
                lines=[
                    ("context", "[reduce](#method-reduce)"),
                    ("context", "[reduceSpread](#method-reduce-spread)"),
                    ("context", "[reject](#method-reject)"),
                    ("context", ""),
                    ("context", "[reduce](#method-reduce)"),
                    ("add", "[reduceInto](#method-reduce-into)"),
                    ("context", "[reduceSpread](#method-reduce-spread)"),
                    ("context", "[reject](#method-reject)"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run for bare links"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

                self.assertEqual(issues, [])
                self.assertEqual(dest.read_text(encoding="utf-8"), expected)

                rerun_issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(rerun_issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), expected)

    def test_translate_one_moves_named_sections_without_provider_call(self):
        """이름이 있는 섹션을 공급자 호출 없이 이동하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            beta = '<a name="beta"></a>\n## Beta\n\nBeta body.\n'
            alpha = '<a name="alpha"></a>\n## Alpha\n\nAlpha body.\n'
            source_path.write_text(f"{beta}\n{alpha}", encoding="utf-8")

            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            existing_alpha = (
                '<a name="alpha"></a>\n'
                "<!-- ## Alpha -->\n## Alpha\n\n"
                "<!-- Alpha body. -->\n알파 본문.\n"
            )
            existing_beta = (
                '<a name="beta"></a>\n'
                "<!-- ## Beta -->\n## Beta\n\n"
                "<!-- Beta body. -->\n베타 본문.\n"
            )
            dest.write_text(
                f"{existing_alpha}\n{existing_beta}",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/example.md"
                ),
                lines=[
                    ("add", '<a name="beta"></a>'),
                    ("add", "## Beta"),
                    ("add", ""),
                    ("add", "Beta body."),
                    ("add", ""),
                    ("context", '<a name="alpha"></a>'),
                    ("context", "## Alpha"),
                    ("context", ""),
                    ("context", "Alpha body."),
                    ("delete", ""),
                    ("delete", '<a name="beta"></a>'),
                    ("delete", "## Beta"),
                    ("delete", ""),
                    ("delete", "Beta body."),
                ],
            )
            cfg = config.Config(
                provider="cli",
                values={"TRANSLATION_PROVIDER": "cli"},
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run for a move"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)
                rerun_issues = main._translate_one(change, cfg, "prompt", dest)

            expected = f"{existing_beta}\n{existing_alpha}"
            self.assertEqual(issues, [])
            self.assertEqual(rerun_issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), expected)

    def test_translate_one_inserts_structural_section_before_raw_anchor(self):
        """원시 앵커 앞에 구조 섹션을 삽입하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "```php\n"
                "old();\n"
                "```\n\n"
                '<a name="callouts"></a>\n'
                "## Callouts\n\n"
                "The `callout` function displays a message.\n\n"
                "```php\n"
                "callout(label: 'Environment Configured');\n"
                "```\n\n"
                '<a name="tables"></a>\n'
                "## Tables\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "```php\n"
                "old();\n"
                "```\n\n"
                '<a name="tables"></a>\n'
                "<!-- ## Tables -->\n"
                "## Tables\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "```"),
                    ("context", ""),
                    ("add", '<a name="callouts"></a>'),
                    ("add", "## Callouts"),
                    ("add", ""),
                    ("add", "The `callout` function displays a message."),
                    ("add", ""),
                    ("add", "```php"),
                    ("add", "callout(label: 'Environment Configured');"),
                    ("add", "```"),
                    ("add", ""),
                    ("context", '<a name="tables"></a>'),
                    ("context", "## Tables"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                self.assertIn('<a name="callouts"></a>', content)
                self.assertIn(
                    "```php\ncallout(label: 'Environment Configured');\n```",
                    content,
                )
                return (
                    '<a name="callouts"></a>\n'
                    "<!-- ## Callouts -->\n"
                    "## Callouts\n\n"
                    "<!-- The `callout` function displays a message. -->\n"
                    "`callout` 함수는 메시지를 표시합니다.\n\n"
                    "```php\n"
                    "callout(label: 'Environment Configured');\n"
                    "```\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "```php\n"
                "old();\n"
                "```\n\n"
                '<a name="callouts"></a>\n'
                "<!-- ## Callouts -->\n"
                "## Callouts\n\n"
                "<!-- The `callout` function displays a message. -->\n"
                "`callout` 함수는 메시지를 표시합니다.\n\n"
                "```php\n"
                "callout(label: 'Environment Configured');\n"
                "```\n\n"
                '<a name="tables"></a>\n'
                "<!-- ## Tables -->\n"
                "## Tables\n",
            )

    def test_translate_one_repairs_segment_anchors_and_comments(self):
        """번역 구간의 앵커와 원문 주석 복구 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                '<a name="callouts"></a>\n'
                "## Callouts\n\n"
                "The `callout` function displays a message.\n\n"
                "```php\n"
                "callout(label: 'Environment Configured');\n"
                "```\n\n"
                '<a name="callout-rich-content"></a>\n'
                "#### Rich Content\n\n"
                "You may pass an array of strings and elements.\n\n"
                '<a name="tables"></a>\n'
                "## Tables\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                '<a name="tables"></a>\n'
                "<!-- ## Tables -->\n"
                "## Tables\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("add", '<a name="callouts"></a>'),
                    ("add", "## Callouts"),
                    ("add", ""),
                    ("add", "The `callout` function displays a message."),
                    ("add", ""),
                    ("add", "```php"),
                    ("add", "callout(label: 'Environment Configured');"),
                    ("add", "```"),
                    ("add", ""),
                    ("add", '<a name="callout-rich-content"></a>'),
                    ("add", "#### Rich Content"),
                    ("add", ""),
                    ("add", "You may pass an array of strings and elements."),
                    ("add", ""),
                    ("context", '<a name="tables"></a>'),
                    ("context", "## Tables"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                return (
                    '<a name="callouts"></a>\n'
                    "<!-- ## Callouts -->\n"
                    "## Callouts\n\n"
                    "<!-- The `callout` function displays a message. -->\n"
                    "`callout` 함수는 메시지를 표시합니다.\n\n"
                    "```php\n"
                    "callout(label: 'Environment Configured');\n"
                    "```\n\n"
                    '<a name="callout-rich-content"></a>\n'
                    "<!-- #### Rich Content -->\n"
                    "#### Rich Content\n\n"
                    "<!-- You may pass an array of strings and elements. -->\n"
                    "문자열과 요소의 배열을 전달할 수 있습니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                '<a name="callouts"></a>\n'
                "<!-- ## Callouts -->\n"
                "## Callouts\n\n"
                "<!-- The `callout` function displays a message. -->\n"
                "`callout` 함수는 메시지를 표시합니다.\n\n"
                "```php\n"
                "callout(label: 'Environment Configured');\n"
                "```\n\n"
                '<a name="callout-rich-content"></a>\n'
                "<!-- #### Rich Content -->\n"
                "#### Rich Content\n\n"
                "<!-- You may pass an array of strings and elements. -->\n"
                "문자열과 요소의 배열을 전달할 수 있습니다.\n\n"
                '<a name="tables"></a>\n'
                "<!-- ## Tables -->\n"
                "## Tables\n",
            )

    def test_translate_one_handles_multi_block_insertions_as_one_range(self):
        """여러 블록 삽입을 하나의 범위로 처리하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("A.\n\nB.\n\nD.\n\nE.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- A. -->\n"
                "A 번역.\n\n"
                "<!-- E. -->\n"
                "E 번역.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "A."),
                    ("context", ""),
                    ("add", "B."),
                    ("add", ""),
                    ("add", "D."),
                    ("context", ""),
                    ("context", "E."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                self.assertIn("B.", content)
                self.assertIn("D.", content)
                return (
                    "<!-- B. -->\nB 번역.\n\n"
                    "<!-- D. -->\nD 번역.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- A. -->\n"
                "A 번역.\n\n"
                "<!-- B. -->\n"
                "B 번역.\n\n"
                "<!-- D. -->\n"
                "D 번역.\n\n"
                "<!-- E. -->\n"
                "E 번역.\n",
            )

    def test_translate_one_deletes_removed_blocks_without_provider_call(self):
        """제거된 블록을 공급자 호출 없이 삭제하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("Before.\n\nAfter.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- Removed. -->\n"
                "삭제될 문장입니다.\n\n"
                "<!-- After. -->\n"
                "뒤 문장입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "Removed."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n"
                "앞 문장입니다.\n\n"
                "<!-- After. -->\n"
                "뒤 문장입니다.\n",
            )

    def test_translate_one_coalesces_multiple_edits_in_same_source_block(self):
        """동일 원문 블록의 여러 편집을 병합하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "First.\nNew A.\nMiddle.\nNew B.\nLast.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- First. Old A. Middle. Old B. Last. -->\n"
                "기존 번역입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "First."),
                    ("delete", "Old A."),
                    ("add", "New A."),
                    ("context", "Middle."),
                    ("delete", "Old B."),
                    ("add", "New B."),
                    ("context", "Last."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                return (
                    "<!-- First. New A. Middle. New B. Last. -->\n"
                    "새 번역입니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- First. New A. Middle. New B. Last. -->\n"
                "새 번역입니다.\n",
            )

    def test_translate_one_normalizes_old_anchor_text_before_matching(self):
        """일치 여부 확인 전에 이전 앵커 텍스트를 정규화하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("See {{version}} updated.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("<!-- See 12.x. -->\n기존 번역입니다.\n", encoding="utf-8")
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("delete", "See {{version}}."),
                    ("add", "See {{version}} updated."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                return "<!-- See 12.x updated. -->\n새 번역입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- See 12.x updated. -->\n새 번역입니다.\n",
            )

    def test_translate_one_restores_placeholders_in_plan_state(self):
        """계획 상태의 자리표시자를 복원하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            image = "![Diagram](data:image/png;base64,QUJD)"
            source_path.write_text(
                f"{image}\n\nNew text.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                f"<!-- {image} -->\n{image}\n\n"
                "<!-- Old text. -->\n예전 번역입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", image),
                    ("context", ""),
                    ("delete", "Old text."),
                    ("add", "New text."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                return "<!-- New text. -->\n새 번역입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                f"<!-- {image} -->\n{image}\n\n"
                "<!-- New text. -->\n새 번역입니다.\n",
            )

    def test_annotation_source_normalizes_unquoted_admonition_bodies(self):
        """비인용 경고문 본문에서 annotation 기준과 영어 view 구조 일치 검증."""

        source = "Intro.\n\n> [!NOTE]\nBody text.\n\nAfter.\n"

        annotation = main._annotation_source(source, "12.x", {})

        self.assertIn("> [!NOTE]\n> Body text.", annotation)
        self.assertEqual(
            annotation,
            main.postprocess.postprocess(source, "12.x", {}),
        )

    def test_translate_one_degrades_partial_patch_failure_to_recreation(self):
        """부분 patch 불가 문서를 전체 재생성으로 강등하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("New text.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("Unrelated translation.\n", encoding="utf-8")
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("delete", "Old text."),
                    ("add", "New text."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            response = "<!-- New text. -->\n새 번역입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                return_value=response,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), response)

    def test_added_document_with_verified_locale_is_not_a_state_conflict(self):
        """추가 문서의 locale이 이미 검증을 통과하면 상태 충돌로 보지 않음."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "A paragraph that already has an approved translation.\n",
                encoding="utf-8",
            )
            for dest, body in (
                (
                    root / "versioned_docs/version-12.x/example.md",
                    "이미 승인된 번역이 있는 문단입니다.",
                ),
                (
                    root
                    / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md",
                    "すでに承認された翻訳がある段落です。",
                ),
            ):
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(
                    "<!-- A paragraph that already has an approved translation. -->\n"
                    f"{body}\n",
                    encoding="utf-8",
                )
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._file_state_issues(change)

            self.assertEqual(issues, [])

    def test_added_document_with_wrong_locale_is_a_state_conflict(self):
        """구조가 맞아도 목표 언어가 다르면 승인된 결과로 보지 않음."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "A paragraph that already has an approved translation.\n",
                encoding="utf-8",
            )
            for dest in (
                root / "versioned_docs/version-12.x/example.md",
                root / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md",
            ):
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(
                    "<!-- A paragraph that already has an approved translation. -->\n"
                    "이미 승인된 번역이 있는 문단입니다.\n",
                    encoding="utf-8",
                )
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._file_state_issues(change)

        self.assertEqual(
            issues,
            [
                "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md: "
                "A requires absent ja locale"
            ],
        )

    def test_added_document_with_stale_locale_is_a_state_conflict(self):
        """추가 문서의 locale이 현재 원문과 맞지 않으면 상태 충돌."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("A new paragraph.\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("관련 없는 번역입니다.\n", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._file_state_issues(change)

            self.assertTrue(
                any("requires absent ko locale" in issue for issue in issues)
            )

    def test_recreation_reuses_translations_of_unchanged_blocks(self):
        """재생성 강등이 영어 원문 그대로인 블록의 기존 번역을 재사용."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Keep this paragraph exactly as it already is.\n"
                "\n"
                "New text that must be translated now.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Keep this paragraph exactly as it already is. -->\n"
                "이 문단은 이미 승인된 번역 그대로 유지합니다.\n"
                "\n"
                "<!-- Stale text. -->\n"
                "예전 번역입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("delete", "Stale text."),
                    ("add", "New text that must be translated now."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            requests: list[str] = []

            def translated(request, _cfg, _prompt, **_kwargs) -> str:
                """변경된 블록만 번역."""

                requests.append(request.source)
                return (
                    "<!-- New text that must be translated now. -->\n"
                    "이제 번역해야 하는 새 문장입니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(requests), 1)
            self.assertIn("New text that must be translated now.", requests[0])
            written = dest.read_text(encoding="utf-8")
            self.assertIn("이 문단은 이미 승인된 번역 그대로 유지합니다.", written)
            self.assertIn("이제 번역해야 하는 새 문장입니다.", written)
            self.assertNotIn("예전 번역입니다.", written)

    def test_translate_one_degrades_mixed_plan_state_to_recreation(self):
        """혼합된 계획 상태 문서를 전체 재생성으로 강등하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\nNew text.\n\nAfter.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            existing = (
                "<!-- Before. -->\n앞 문장입니다.\n\n"
                "<!-- Extra. -->\n추가 문장입니다.\n\n"
                "<!-- Old text. -->\n예전 번역입니다.\n\n"
                "<!-- After. -->\n뒤 문장입니다.\n"
            )
            dest.write_text(existing, encoding="utf-8")
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "Old text."),
                    ("add", "New text."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            responses = [
                "<!-- Before. -->\n앞 문장입니다.\n",
                "<!-- New text. -->\n새 번역입니다.\n",
                "<!-- After. -->\n뒤 문장입니다.\n",
            ]

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=responses,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n앞 문장입니다.\n\n"
                "<!-- New text. -->\n새 번역입니다.\n\n"
                "<!-- After. -->\n뒤 문장입니다.\n",
            )

    def test_translate_one_degrades_whole_table_insertion_to_recreation(self):
        """수정 문서의 표 전체 삽입을 재생성 강등으로 처리하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\n"
                "| Name | Value |\n| --- | --- |\n| Widget | enabled |\n\n"
                "After.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            existing = (
                "<!-- Before. -->\n앞 문장입니다.\n\n"
                "<!-- After. -->\n뒤 문장입니다.\n"
            )
            dest.write_text(existing, encoding="utf-8")
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("add", "| Name | Value |"),
                    ("add", "| --- | --- |"),
                    ("add", "| Widget | enabled |"),
                    ("add", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            table_response = (
                "<!-- | Name | Value | | --- | --- | | Widget | enabled | -->\n"
                "| 이름 | 값 |\n"
                "| --- | --- |\n"
                "| Widget | 활성 |\n"
            )
            responses = [
                "<!-- Before. -->\n앞 문장입니다.\n",
                table_response,
                "<!-- After. -->\n뒤 문장입니다.\n",
            ]

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=responses,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n앞 문장입니다.\n\n"
                f"{table_response}\n"
                "<!-- After. -->\n뒤 문장입니다.\n",
            )

    def test_translate_one_verifies_target_state_without_provider(self):
        """공급자 호출 없이 대상 상태를 확인하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\nNew text.\n\nAfter.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            existing = (
                "<!-- Before. -->\n앞 문장입니다.\n\n"
                "<!-- New text. -->\n새 번역입니다.\n\n"
                "<!-- After. -->\n뒤 문장입니다.\n"
            )
            dest.write_text(existing, encoding="utf-8")
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "Old text."),
                    ("add", "New text."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("provider should not run for target state"),
            ), patch.object(
                main,
                "atomic_write_bytes",
                side_effect=AssertionError("target state must not write"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), existing)

    def test_block_translation_does_not_retry_final_verifier_issues(self):
        """블록 번역의 최종 검증 문제를 재시도하지 않는지 검증."""

        change = diff.SourceChange(
            path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
            status="M",
        )
        block_change = main.patch_utils.BlockChange(
            old_lines=("Old text.",),
            new_lines=("New text.",),
            before_context=None,
            after_context=None,
            old_source="Old text.\n",
            new_source="New text.\n",
        )
        cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

        with patch.object(
            main.translate,
            "translate_request",
            return_value="translated\n",
        ) as provider, patch.object(
            main,
            "_contract_issues",
            return_value=[],
        ), patch.object(
            main,
            "_repair_segment_translation",
            return_value="repaired\n",
        ), patch.object(
            main.patch_utils,
            "existing_context",
            return_value="old locale",
        ), patch.object(
            main.verify,
            "verify",
            return_value=["heading mismatch"],
        ):
            result = main._translate_block_change(
                change,
                block_change,
                cfg,
                "prompt",
                "existing locale",
                locale="ko",
            )

        self.assertEqual(result, "repaired\n")
        self.assertEqual(provider.call_count, 1)

    def test_translate_one_skips_an_already_current_prose_and_code_hunk(self):
        """이미 최신인 산문과 코드 변경 묶음을 건너뛰는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            old_source = (
                "Before.\n\n"
                "Use the old key.\n\n"
                "```php\n"
                "$key = 'old';\n"
                "```\n\n"
                "After.\n"
            )
            new_source = (
                "Before.\n\n"
                "Use the new key.\n\n"
                "```php\n"
                "$key = 'new';\n"
                "```\n\n"
                "After.\n"
            )
            source_path.write_text(new_source, encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            existing = (
                "<!-- Before. -->\n이전입니다.\n\n"
                "<!-- Use the new key. -->\n새 키를 사용합니다.\n\n"
                "```php\n"
                "$key = 'new';\n"
                "```\n\n"
                "<!-- After. -->\n이후입니다.\n"
            )
            dest.write_text(existing, encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
                hunks=diff.hunks_between(old_source, new_source),
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.patch_utils,
                "plan_state",
                return_value=main.patch_utils.PlanState.UNGUARDED,
            ), patch.object(
                main.translate,
                "translate_request",
                side_effect=AssertionError("provider should not run for current output"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest, locale="ko")

            self.assertEqual(issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), existing)

    def test_translate_one_repairs_unchanged_legacy_admonition_and_annotation(self):
        """부분 재실행에서 변경 블록 외부의 기존 경고와 주석까지 정규화하는지 검증."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            old_source = (
                "Before.\n\n"
                "> **Note:** Keep this.\n\n"
                "Old text.\n\n"
                "After.\n"
            )
            new_source = old_source.replace("Old text.", "New text.")
            source_path.write_text(new_source, encoding="utf-8")
            dest = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "前の文です。\n\n"
                "<!-- > **Note:** Keep this. -->\n"
                "> **注意:** 保持する必要があります。\n\n"
                "<!-- Old text. -->\n"
                "古い翻訳です。\n\n"
                "<!-- After. -->\n"
                "後の文です。\n",
                encoding="utf-8",
            )
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
                hunks=diff.hunks_between(old_source, new_source),
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._translate_one(change, cfg, "prompt", dest, locale="ja")

            self.assertEqual(issues, [])
            output = dest.read_text(encoding="utf-8")
            self.assertIn("> [!NOTE]\n> 保持する必要があります。", output)
            self.assertNotIn("> **注意:**", output)
            self.assertIn("<!-- New text. -->", output)

    def test_translate_one_expands_line_change_to_containing_paragraph(self):
        """줄 변경 범위를 해당 줄이 속한 문단으로 확장하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "First line.\nNew line.\nThird line.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- First line. Old line. Third line. -->\n"
                "첫 줄입니다. 예전 줄입니다. 세 번째 줄입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "First line."),
                    ("delete", "Old line."),
                    ("add", "New line."),
                    ("context", "Third line."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                return (
                    "<!-- First line. New line. Third line. -->\n"
                    "첫 줄입니다. 새 줄입니다. 세 번째 줄입니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertIn("First line.\nNew line.\nThird line.", sent[0])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- First line. New line. Third line. -->\n"
                "첫 줄입니다. 새 줄입니다. 세 번째 줄입니다.\n",
            )

    def test_translate_one_replaces_paragraph_when_line_is_inserted_inside_it(self):
        """문단 내부에 줄을 삽입할 때 문단 전체를 교체하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "First line.\nInserted line.\nSecond line.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- First line. Second line. -->\n"
                "첫 줄입니다. 두 번째 줄입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "First line."),
                    ("add", "Inserted line."),
                    ("context", "Second line."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                return (
                    "<!-- First line. Inserted line. Second line. -->\n"
                    "첫 줄입니다. 삽입된 줄입니다. 두 번째 줄입니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- First line. Inserted line. Second line. -->\n"
                "첫 줄입니다. 삽입된 줄입니다. 두 번째 줄입니다.\n",
            )

    def test_translate_one_replaces_paragraph_when_line_is_deleted_inside_it(self):
        """문단 내부의 줄을 삭제할 때 문단 전체를 교체하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "First line.\nSecond line.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- First line. Removed line. Second line. -->\n"
                "첫 줄입니다. 삭제될 줄입니다. 두 번째 줄입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                lines=[
                    ("context", "First line."),
                    ("delete", "Removed line."),
                    ("context", "Second line."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                return "<!-- First line. Second line. -->\n첫 줄입니다. 두 번째 줄입니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- First line. Second line. -->\n첫 줄입니다. 두 번째 줄입니다.\n",
            )

    def test_translate_one_replaces_localized_table_row_by_stable_cells(self):
        """안정된 셀을 기준으로 현지화된 표의 행을 교체하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "| Feature | Providers |\n"
                "|---|---|\n"
                "| Text | OpenAI, OpenAI Compatible, Anthropic |\n"
                "| Images | OpenAI |\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "| 기능 | 프로바이더 |\n"
                "|---|---|\n"
                "| 텍스트 | OpenAI, Anthropic |\n"
                "| 이미지 | OpenAI |\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "|---|---|"),
                    ("delete", "| Text | OpenAI, Anthropic |"),
                    ("add", "| Text | OpenAI, OpenAI Compatible, Anthropic |"),
                    ("context", "| Images | OpenAI |"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                self.assertIn("| 텍스트 | OpenAI, Anthropic |", content)
                return (
                    "<!-- | Text | OpenAI, OpenAI Compatible, Anthropic | -->\n"
                    "| 텍스트 | OpenAI, OpenAI Compatible, Anthropic |\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- | Feature | Providers | |---|---| "
                "| Text | OpenAI, OpenAI Compatible, Anthropic | "
                "| Images | OpenAI | -->\n"
                "| 기능 | 프로바이더 |\n"
                "|---|---|\n"
                "| 텍스트 | OpenAI, OpenAI Compatible, Anthropic |\n"
                "| 이미지 | OpenAI |\n",
            )

    def test_translate_one_replaces_localized_table_row_with_japanese_commas(self):
        """일본어 쉼표가 포함된 현지화 표의 행을 교체하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "| Feature | Providers |\n"
                "|---|---|\n"
                "| Text | OpenAI, OpenAI Compatible, Anthropic |\n"
                "| Images | OpenAI |\n",
                encoding="utf-8",
            )
            dest = root / "i18n/ja/docusaurus-plugin-content-docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "| 特徴 | プロバイダ |\n"
                "|---|---|\n"
                "| 文章 | OpenAI、Anthropic |\n"
                "| 画像 | OpenAI |\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "|---|---|"),
                    ("delete", "| Text | OpenAI, Anthropic |"),
                    ("add", "| Text | OpenAI, OpenAI Compatible, Anthropic |"),
                    ("context", "| Images | OpenAI |"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                self.assertIn("| 文章 | OpenAI、Anthropic |", content)
                return (
                    "<!-- | Text | OpenAI, OpenAI Compatible, Anthropic | -->\n"
                    "| 文章 | OpenAI、OpenAI Compatible、Anthropic |\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- | Feature | Providers | |---|---| "
                "| Text | OpenAI, OpenAI Compatible, Anthropic | "
                "| Images | OpenAI | -->\n"
                "| 特徴 | プロバイダ |\n"
                "|---|---|\n"
                "| 文章 | OpenAI、OpenAI Compatible、Anthropic |\n"
                "| 画像 | OpenAI |\n",
            )

    def test_translate_one_replaces_split_paragraph_and_following_warning(self):
        """분리된 문단과 뒤따르는 경고 블록을 함께 교체하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-master/errors.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Debug configuration.\n\n"
                "During local development, you should set `APP_DEBUG` to `true`.\n\n"
                "> [!WARNING]\n"
                "> In production, `APP_DEBUG` should always be `false`.\n\n"
                '<a name="next"></a>\n'
                "## Next\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-master/errors.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Debug configuration. -->\n"
                "디버그 설정입니다.\n\n"
                "<!-- During local development, you should set `APP_DEBUG` to `true`. -->\n"
                "로컬 개발 중에는 `APP_DEBUG`를 `true`로 설정해야 합니다.\n\n"
                "> [!WARNING]\n"
                "> 프로덕션에서는 `APP_DEBUG`가 항상 `false`여야 합니다.\n\n"
                '<a name="next"></a>\n'
                "<!-- ## Next -->\n"
                "## Next\n",
                encoding="utf-8",
            )
            old = (
                "During local development, you should set `APP_DEBUG` to `true`. "
                "**In production, `APP_DEBUG` should always be `false`.**"
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-master/errors.md",
                lines=[
                    ("context", "Debug configuration."),
                    ("context", ""),
                    ("delete", old),
                    ("add", "During local development, you should set `APP_DEBUG` to `true`."),
                    ("add", ""),
                    ("add", "> [!WARNING]"),
                    ("add", "> In production, `APP_DEBUG` should always be `false`."),
                    ("context", ""),
                    ("context", '<a name="next"></a>'),
                    ("context", "## Next"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                return (
                    "<!-- During local development, you should set `APP_DEBUG` to `true`. -->\n"
                    "로컬 개발 중에는 `APP_DEBUG`를 `true`로 설정해야 합니다.\n\n"
                    "> [!WARNING]\n"
                    "> <!-- In production, `APP_DEBUG` should always be `false`. -->\n"
                    "> 프로덕션에서는 `APP_DEBUG`가 항상 `false`여야 합니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Debug configuration. -->\n"
                "디버그 설정입니다.\n\n"
                "<!-- During local development, you should set `APP_DEBUG` to `true`. -->\n"
                "로컬 개발 중에는 `APP_DEBUG`를 `true`로 설정해야 합니다.\n\n"
                "> [!WARNING]\n"
                "> 프로덕션에서는 `APP_DEBUG`가 항상 `false`여야 합니다.\n\n"
                '<a name="next"></a>\n'
                "<!-- ## Next -->\n"
                "## Next\n",
            )

    def test_translate_one_keeps_changed_admonition_body_in_blockquote(self):
        """변경된 경고 본문을 인용문 내부에 유지하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/search.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "The basic workflow for vector search.\n\n"
                "> [!NOTE]\n"
                "> Vector search requires the [Laravel AI SDK](/docs/{{version}}/ai-sdk) "
                "and PostgreSQL with `pgvector`.\n\n"
                '<a name="generating-embeddings"></a>\n'
                "### Generating Embeddings\n",
                encoding="utf-8",
            )
            dest = root / "i18n/ja/docusaurus-plugin-content-docs/version-13.x/search.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- The basic workflow for vector search. -->\n"
                "ベクトル検索の基本的なワークフローです。\n\n"
                "> [!NOTE]\n"
                "> ベクトル検索には、`pgvector` 拡張子と [Laravel AI SDK](/docs/13.x/ai-sdk) "
                "を持つ PostgreSQL データベースが必要です。\n\n"
                '<a name="generating-embeddings"></a>\n'
                "<!-- ### Generating Embeddings -->\n"
                "### Generating Embeddings\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/search.md",
                lines=[
                    ("context", "The basic workflow for vector search."),
                    ("context", ""),
                    ("context", "> [!NOTE]"),
                    (
                        "delete",
                        "> Vector search requires PostgreSQL with `pgvector` and the "
                        "[Laravel AI SDK](/docs/{{version}}/ai-sdk).",
                    ),
                    (
                        "add",
                        "> Vector search requires the [Laravel AI SDK](/docs/{{version}}/ai-sdk) "
                        "and PostgreSQL with `pgvector`.",
                    ),
                    ("context", ""),
                    ("context", '<a name="generating-embeddings"></a>'),
                    ("context", "### Generating Embeddings"),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            def translated(
                _content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                self.assertFalse(split)
                return (
                    "> <!-- Vector search requires the [Laravel AI SDK](/docs/13.x/ai-sdk) "
                    "and PostgreSQL with `pgvector`. -->\n"
                    "> ベクトル検索には、[Laravel AI SDK](/docs/13.x/ai-sdk) と "
                    "`pgvector` を備えた PostgreSQL が必要です。\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- The basic workflow for vector search. -->\n"
                "ベクトル検索の基本的なワークフローです。\n\n"
                "> [!NOTE]\n"
                "> ベクトル検索には、[Laravel AI SDK](/docs/13.x/ai-sdk) と "
                "`pgvector` を備えた PostgreSQL が必要です。\n\n"
                '<a name="generating-embeddings"></a>\n'
                "<!-- ### Generating Embeddings -->\n"
                "### Generating Embeddings\n",
            )

    def test_translate_one_retranslates_an_admonition_marker_change(self):
        """경고 표시가 변경되면 해당 블록을 다시 번역하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\n"
                "> [!WARNING]\n"
                "> Keep the source body.\n\n"
                "After.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n이전입니다.\n\n"
                "> [!NOTE]\n> 기존 본문입니다.\n\n"
                "<!-- After. -->\n이후입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "> [!NOTE]"),
                    ("add", "> [!WARNING]"),
                    ("context", "> Keep the source body."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(
                provider="cli",
                values={"TRANSLATION_PROVIDER": "cli"},
            )

            def translated(request, *_args, **_kwargs):
                """번역 결과 반환."""

                self.assertEqual(
                    request.source,
                    "> [!WARNING]\n> Keep the source body.\n",
                )
                return "> [!WARNING]\n> 원문 본문을 유지합니다.\n"

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=translated,
            ) as provider:
                issues = main._translate_one(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertEqual(issues, [])
            self.assertEqual(provider.call_count, 1)
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- Before. -->\n이전입니다.\n\n"
                "> [!WARNING]\n> 원문 본문을 유지합니다.\n\n"
                "<!-- After. -->\n이후입니다.\n",
            )

    def test_translate_one_replaces_an_annotated_inline_code_list(self):
        """원문 주석이 있는 인라인 코드 목록을 교체하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            old_source = (
                "Before.\n\n"
                "> [!NOTE]\n"
                "> Keep this body.\n\n"
                "Events:\n\n"
                "- `FirstEvent`\n"
                "- `SecondEvent`\n\n"
                "After.\n"
            )
            new_source = old_source.replace(
                "> [!NOTE]",
                "> [!WARNING]",
            ).replace(
                "- `FirstEvent`\n- `SecondEvent`\n",
                "- `FirstEvent`\n- `ThirdEvent`\n- `SecondEvent`\n",
            )
            source_path.write_text(new_source, encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n이전입니다.\n\n"
                "> **Note:** 본문을 유지합니다.\n\n"
                "<!-- Events: -->\n이벤트입니다.\n\n"
                "<!--\n"
                "- `FirstEvent`\n"
                "- `SecondEvent`\n"
                "-->\n"
                "- `FirstEvent`\n"
                "- `SecondEvent`\n\n"
                "<!-- After. -->\n이후입니다.\n",
                encoding="utf-8",
            )
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="M",
                hunks=diff.hunks_between(old_source, new_source),
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=lambda request, *_args, **_kwargs: request.source,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest, locale="ko")

            self.assertEqual(issues, [])
            expected = (
                "<!-- Before. -->\n이전입니다.\n\n"
                "> [!WARNING]\n> Keep this body.\n\n"
                "<!-- Events: -->\n이벤트입니다.\n\n"
                "- `FirstEvent`\n"
                "- `ThirdEvent`\n"
                "- `SecondEvent`\n"
                "\n"
                "<!-- After. -->\n이후입니다.\n"
            )
            self.assertEqual(dest.read_text(encoding="utf-8"), expected)

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=lambda request, *_args, **_kwargs: request.source,
            ):
                repeated_issues = main._translate_one(
                    change,
                    cfg,
                    "prompt",
                    dest,
                    locale="ko",
                )

            self.assertEqual(repeated_issues, [])
            self.assertEqual(dest.read_text(encoding="utf-8"), expected)

    def test_translate_one_retries_link_mismatches_with_feedback(self):
        """링크 불일치 발생 시 feedback 재요청으로 복구하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\n"
                "See [Docs](docs) and [Queues](queues).\n\n"
                "After.\n",
                encoding="utf-8",
            )
            dest = root / "i18n/ja/docusaurus-plugin-content-docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "前の文です。\n\n"
                "<!-- See [Old Docs](old-docs) and [Queues](queues). -->\n"
                "[Old Docs](old-docs) と [Queues](queues) を参照してください。\n\n"
                "<!-- After. -->\n"
                "後の文です。\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    ("delete", "See [Old Docs](old-docs) and [Queues](queues)."),
                    ("add", "See [Docs](docs) and [Queues](queues)."),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                if len(sent) == 1:
                    return (
                        "<!-- See [Docs](docs) and [Queues](queues). -->\n"
                        "[Docs](docs) を参照してください。\n"
                    )
                return (
                    "<!-- See [Docs](docs) and [Queues](queues). -->\n"
                    "[Docs](docs) と [Queues](queues) を参照してください。\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 2)
            self.assertIn("provider link pair mismatch", sent[1])
            self.assertIn("[Docs](docs)", dest.read_text(encoding="utf-8"))

    def test_create_owner_repairs_link_label_and_target_before_contract(self):
        """전체 재번역 응답의 링크를 계약 검사 전에 원문대로 복구."""

        source = "Use [Laravel Sail](/docs/{{version}}/sail).\n"
        translated = (
            "<!-- Use [Laravel Sail](/docs/{{version}}/sail). -->\n"
            "[Laravel Sail 문서](/docs/13.x/sail)를 사용합니다.\n"
        )
        change = diff.SourceChange(
            path=(
                "i18n/en/docusaurus-plugin-content-docs/"
                "version-13.x/redis.md"
            ),
            status="M",
        )
        cfg = config.Config(
            provider="openai",
            values={"TRANSLATION_PROVIDER": "openai"},
        )

        with patch.object(
            main.translate,
            "translate_request",
            return_value=translated,
        ) as provider:
            block, issue = main._translate_create_owner(
                source,
                change,
                cfg,
                "prompt",
                locale="ko",
                deadline=None,
                attempt_counter=None,
            )

        self.assertIsNone(issue)
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(
            block,
            "<!-- Use [Laravel Sail](/docs/{{version}}/sail). -->\n"
            "[Laravel Sail](/docs/{{version}}/sail)를 사용합니다.\n",
        )

    def test_translate_one_retries_inline_code_mismatches_with_feedback(self):
        """인라인 코드 불일치 발생 시 feedback 재요청으로 복구하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text(
                "Before.\n\n"
                "Use `Redis::throttle` with [queues](/docs/13.x/queues).\n\n"
                "After.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n"
                "이전 문장입니다.\n\n"
                "<!-- Use `Redis::funnel` with [queues](/docs/13.x/queues). -->\n"
                "`Redis::funnel`을 [queues](/docs/13.x/queues)와 함께 사용합니다.\n\n"
                "<!-- After. -->\n"
                "이후 문장입니다.\n",
                encoding="utf-8",
            )
            change = self._change_with_lines(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                lines=[
                    ("context", "Before."),
                    ("context", ""),
                    (
                        "delete",
                        "Use `Redis::funnel` with [queues](/docs/13.x/queues).",
                    ),
                    (
                        "add",
                        "Use `Redis::throttle` with [queues](/docs/13.x/queues).",
                    ),
                    ("context", ""),
                    ("context", "After."),
                ],
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})
            sent: list[str] = []

            def translated(
                content: str, _cfg: config.Config, _prompt: str, *, split: bool = True
            ) -> str:
                """번역 결과 반환."""

                sent.append(content)
                self.assertFalse(split)
                if len(sent) == 1:
                    return (
                        "<!-- Use `Redis::throttle` with [queues](/docs/13.x/queues). -->\n"
                        "[queues](/docs/13.x/queues)와 함께 사용합니다.\n"
                    )
                return (
                    "<!-- Use `Redis::throttle` with [queues](/docs/13.x/queues). -->\n"
                    "`Redis::throttle`을 [queues](/docs/13.x/queues)와 함께 사용합니다.\n"
                )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_text",
                side_effect=translated,
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(len(sent), 2)
            self.assertIn("provider inline code mismatch", sent[1])
            self.assertIn("`Redis::throttle`", dest.read_text(encoding="utf-8"))

    def test_inline_code_feedback_includes_required_token_counts(self):
        """인라인 코드 재요청에 원문 token별 필요 개수를 명시."""

        feedback = main._verification_feedback(
            ["provider inline code mismatch"],
            translated="`Redis`와 `GET`을 사용합니다.",
            source="Use the `Redis` facade to call `GET` on `Redis`.",
        )

        self.assertIn("`Redis` × 2", feedback)
        self.assertIn("`GET` × 1", feedback)

    def test_translate_one_requires_hunks_for_existing_documents(self):
        """기존 문서 번역에 원시 diff 묶음이 필요한지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("# One\n\n# Two\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("# 기존 문서\n", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="M",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "split_chunks",
                side_effect=AssertionError("full document fallback should not run"),
            ), patch.object(
                main.translate,
                "translate_text",
                side_effect=AssertionError("full document fallback should not run"),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(
                issues,
                ["missing diff hunks for partial sync [RAW_DIFF_MISSING]"],
            )
            self.assertEqual(dest.read_text(encoding="utf-8"), "# 기존 문서\n")

    def test_translate_one_renders_new_document_headings_without_provider(self):
        """새 문서 제목을 공급자 호출 없이 렌더링하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            source_path.parent.mkdir(parents=True)
            source_path.write_text("# One\n\n# Two\n", encoding="utf-8")
            dest = root / "versioned_docs/version-12.x/example.md"
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="A",
            )
            cfg = config.Config(provider="cli", values={"TRANSLATION_PROVIDER": "cli"})

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=AssertionError(
                    "deterministic heading owners must not call the provider"
                ),
            ):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertEqual(
                dest.read_text(encoding="utf-8"),
                "<!-- # One -->\n# One\n\n<!-- # Two -->\n# Two\n",
            )

    def test_delete_outputs_removes_ko_and_ja_documents_for_deleted_source(self):
        """원문 삭제 시 한국어와 일본어 문서를 제거하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ko_doc = root / "versioned_docs/version-12.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-12.x/example.md"
            )
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            ko_doc.write_text("ko", encoding="utf-8")
            ja_doc.write_text("ja", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
                status="D",
            )

            with patch.object(main, "REPO_ROOT", root):
                main._delete_outputs(change)

            self.assertFalse(ko_doc.exists())
            self.assertFalse(ja_doc.exists())

    def test_validate_file_states_rejects_added_source_with_existing_locale(self):
        """추가된 원문에 기존 로케일 문서가 있으면 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text("new source\n", encoding="utf-8")
            ko_doc.write_text("existing locale\n", encoding="utf-8")
            change = diff.SourceChange(
                path=str(source.relative_to(root)),
                status="A",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._validate_file_states([change])

            self.assertEqual(
                issues,
                [
                    "i18n/en/docusaurus-plugin-content-docs/version-13.x/"
                    "example.md: A requires absent ko locale"
                ],
            )

    def test_validate_file_states_checks_all_modified_inputs_before_writes(self):
        """기록 전에 수정된 모든 입력 파일 상태를 확인하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            source.write_text("updated source\n", encoding="utf-8")
            ko_doc.write_text("ko\n", encoding="utf-8")
            change = self._change_with_lines(
                path=str(source.relative_to(root)),
                lines=[("delete", "old"), ("add", "updated source")],
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._validate_file_states([change])

            self.assertEqual(
                issues,
                [
                    "i18n/en/docusaurus-plugin-content-docs/version-13.x/"
                    "example.md: M requires existing ja locale"
                ],
            )

    def test_validate_file_states_rejects_modified_source_without_raw_hunks(self):
        """원시 diff 묶음이 없는 수정 원문 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            source.write_text("updated source\n", encoding="utf-8")
            ko_doc.write_text("ko\n", encoding="utf-8")
            ja_doc.write_text("ja\n", encoding="utf-8")
            change = diff.SourceChange(
                path=str(source.relative_to(root)),
                status="M",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._validate_file_states([change])

            self.assertEqual(
                issues,
                [
                    "i18n/en/docusaurus-plugin-content-docs/version-13.x/"
                    "example.md: M requires raw diff hunks"
                ],
            )

    def test_validate_file_states_accepts_complete_deleted_triplet(self):
        """완전히 삭제된 원문과 로케일 문서 묶음 허용 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs/version-13.x/example.md"
            )
            ko_doc.parent.mkdir(parents=True)
            ja_doc.parent.mkdir(parents=True)
            ko_doc.write_text("ko\n", encoding="utf-8")
            ja_doc.write_text("ja\n", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="D",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._validate_file_states([change])

            self.assertEqual(issues, [])

    def test_delete_outputs_rejects_symlinked_parent_without_partial_deletion(self):
        """심볼릭 링크 상위 경로 발견 시 일부 출력만 삭제하지 않는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            outside = Path(tmp) / "outside"
            outside.mkdir()
            external_doc = outside / "example.md"
            external_doc.write_text("external\n", encoding="utf-8")
            ko_root = root / "versioned_docs"
            ko_root.mkdir()
            (ko_root / "version-13.x").symlink_to(
                outside,
                target_is_directory=True,
            )
            ja_doc = (
                root
                / "i18n/ja/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            ja_doc.parent.mkdir(parents=True)
            ja_doc.write_text("ja\n", encoding="utf-8")
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="D",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._delete_outputs(change)

            self.assertTrue(external_doc.exists())
            self.assertEqual(external_doc.read_text(encoding="utf-8"), "external\n")
            self.assertEqual(ja_doc.read_text(encoding="utf-8"), "ja\n")
            self.assertEqual(
                issues,
                [
                    "unsafe translation output path: "
                    + str(ko_root / "version-13.x/example.md")
                ],
            )

    def test_delete_outputs_validates_ja_path_before_deleting_ko_output(self):
        """한국어 출력 삭제 전 일본어 출력 경로 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            ko_doc = root / "versioned_docs/version-13.x/example.md"
            ko_doc.parent.mkdir(parents=True)
            ko_doc.write_text("ko\n", encoding="utf-8")
            outside = Path(tmp) / "outside"
            outside.mkdir()
            external_doc = outside / "example.md"
            external_doc.write_text("external\n", encoding="utf-8")
            ja_root = root / "i18n/ja/docusaurus-plugin-content-docs"
            ja_root.mkdir(parents=True)
            (ja_root / "version-13.x").symlink_to(
                outside,
                target_is_directory=True,
            )
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="D",
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._delete_outputs(change)

            self.assertEqual(ko_doc.read_text(encoding="utf-8"), "ko\n")
            self.assertEqual(external_doc.read_text(encoding="utf-8"), "external\n")
            self.assertEqual(
                issues,
                [
                    "unsafe translation output path: "
                    + str(ja_root / "version-13.x/example.md")
                ],
            )

    def test_added_document_rejects_symlinked_final_output(self):
        """추가된 문서의 심볼릭 링크 최종 출력 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("# Example\n", encoding="utf-8")
            outside = Path(tmp) / "outside.md"
            outside.write_text("external\n", encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.symlink_to(outside)
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="A",
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(outside.read_text(encoding="utf-8"), "external\n")
            self.assertTrue(dest.is_symlink())
            self.assertEqual(
                issues,
                [
                    "unsafe translation output path: "
                    + str(dest)
                    + " [OUTPUT_PATH_FORBIDDEN]"
                ],
            )

    def test_added_document_rejects_an_existing_hardlinked_destination(self):
        """추가된 문서의 기존 하드 링크 대상 거부 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text("# Example\n", encoding="utf-8")
            victim = root / "outside.md"
            victim.write_text("external\n", encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.hardlink_to(victim)
            dest.chmod(0o640)
            change = diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/example.md",
                status="A",
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root):
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(
                issues,
                [
                    (
                        "create patch failed: create plan requires an absent "
                        "locale destination [PATCH_LOCATION_AMBIGUOUS]"
                    )
                ],
            )
            self.assertEqual(victim.read_text(encoding="utf-8"), "external\n")
            self.assertEqual(dest.read_text(encoding="utf-8"), "external\n")
            self.assertTrue(dest.samefile(victim))
            self.assertEqual(dest.stat().st_mode & 0o777, 0o640)

    def test_identity_replay_allows_source_echo_after_structural_verification(self):
        """동일성 재실행에서 구조 검증 후 원문 반환을 허용하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_source = "Before.\n\nOld source sentence.\n\nAfter.\n"
            new_source = "Before.\n\nNew source sentence.\n\nAfter.\n"
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text(new_source, encoding="utf-8")
            dest = root / "versioned_docs/version-13.x/example.md"
            dest.parent.mkdir(parents=True)
            dest.write_text(
                "<!-- Before. -->\n이전입니다.\n\n"
                "<!-- Old source sentence. -->\n기존 문장입니다.\n\n"
                "<!-- After. -->\n이후입니다.\n",
                encoding="utf-8",
            )
            change = diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/example.md"
                ),
                status="M",
                hunks=diff.hunks_between(old_source, new_source),
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.preprocess,
                "preprocess_pair",
                wraps=main.preprocess.preprocess_pair,
            ) as preprocess_pair:
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(issues, [])
            self.assertIn("<!-- New source sentence. -->", dest.read_text())
            self.assertEqual(
                preprocess_pair.call_args_list.count(call(old_source, new_source)),
                1,
            )

    def test_malformed_identity_response_is_rejected_before_apply_or_write(self):
        """잘못된 동일성 응답을 적용이나 기록 전에 거부하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = (
                root
                / "i18n/en/docusaurus-plugin-content-docs"
                / "version-13.x/example.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text(
                "A complete English paragraph that requires its canonical "
                "source annotation.\n",
                encoding="utf-8",
            )
            dest = root / "versioned_docs/version-13.x/example.md"
            change = diff.SourceChange(
                path=(
                    "i18n/en/docusaurus-plugin-content-docs/"
                    "version-13.x/example.md"
                ),
                status="A",
            )
            cfg = config.Config(
                provider="identity",
                values={"TRANSLATION_PROVIDER": "identity"},
            )

            with patch.object(main, "REPO_ROOT", root), patch.object(
                main.translate,
                "translate_request",
                side_effect=lambda request, *_args, **_kwargs: request.source,
            ) as provider, patch.object(
                main.patch_utils,
                "apply_plan",
                side_effect=AssertionError("malformed response must not be applied"),
            ) as apply_plan, patch.object(
                main,
                "atomic_write_bytes",
                side_effect=AssertionError("malformed response must not be written"),
            ) as write:
                issues = main._translate_one(change, cfg, "prompt", dest)

            self.assertEqual(provider.call_count, 1)
            apply_plan.assert_not_called()
            write.assert_not_called()
            self.assertFalse(dest.exists())
            self.assertEqual(len(issues), 1)
            self.assertIn("provider response contract failed", issues[0])
            self.assertIn("provider original comment mismatch", issues[0])

    def test_loads_ko_and_ja_prompts_from_separate_files(self):
        """한국어와 일본어 프롬프트를 별도 파일에서 불러오는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sync_root = root / "translation-sync"
            sync_root.mkdir()
            (sync_root / "prompt.md").write_text("KO\n", encoding="utf-8")
            (sync_root / "prompt_jp.md").write_text("JA\n", encoding="utf-8")

            with patch.object(main, "PROMPT_PATH", sync_root / "prompt.md"), patch.object(
                main,
                "JA_PROMPT_PATH",
                sync_root / "prompt_jp.md",
                create=True,
            ):
                prompts = main._load_prompts()

        self.assertEqual(prompts["ko"], "KO")
        self.assertEqual(prompts["ja"], "JA")

    def test_source_structure_mismatch_allows_regeneration(self):
        """기존 locale 구조 불일치는 재생성 강등 대상으로 판정."""

        self.assertTrue(
            main._issues_allow_regeneration(
                ["ko doc.md: SOURCE_STRUCTURE_MISMATCH: document: link label mismatch"]
            )
        )

    def test_list_table_structure_mismatch_allows_regeneration(self):
        """기존 locale의 목록·표 구조 불일치는 재생성 강등 대상으로 판정."""

        self.assertTrue(
            main._issues_allow_regeneration(
                ["LIST_TABLE_STRUCTURE_MISMATCH: list-or-table: list marker mismatch"]
            )
        )

    def test_unrelated_verification_failure_is_not_degradable(self):
        """강등 목록 밖의 검증 실패는 재생성으로 넘기지 않음."""

        self.assertFalse(
            main._issues_allow_regeneration(
                ["ko doc.md: RESIDUAL_PATTERN: unrestored base64 placeholder"]
            )
        )

    def test_select_changes_excludes_untranslated_documents(self):
        """원문 유지 문서는 번역 대상 선택에서 제외하는지 검증."""

        changes = [
            diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/license.md",
                status="M",
            ),
            diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/queues.md",
                status="M",
            ),
        ]

        with patch.object(diff, "changed_sources", return_value=changes):
            selected = main._select_changes()

        self.assertEqual([change.document for change in selected], ["queues.md"])

    def test_select_changes_keeps_untranslated_document_deletion(self):
        """원문 유지 문서라도 삭제는 전파하는지 검증."""

        changes = [
            diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-13.x/license.md",
                status="D",
            ),
        ]

        with patch.object(diff, "changed_sources", return_value=changes):
            selected = main._select_changes()

        self.assertEqual([change.document for change in selected], ["license.md"])

    def test_nested_source_maps_to_matching_ko_and_ja_relative_paths(self):
        """중첩 원문을 대응하는 한국어와 일본어 상대 경로로 매핑하는지 검증."""

        change = diff.SourceChange(
            path=(
                "i18n/en/docusaurus-plugin-content-docs/"
                "version-13.x/guides/queues.md"
            ),
            status="M",
        )

        self.assertEqual(
            main._ko_output(change).relative_to(main.REPO_ROOT).as_posix(),
            "versioned_docs/version-13.x/guides/queues.md",
        )
        self.assertEqual(
            main._ja_output(change).relative_to(main.REPO_ROOT).as_posix(),
            "i18n/ja/docusaurus-plugin-content-docs/"
            "version-13.x/guides/queues.md",
        )
        self.assertTrue(
            main._matches_filters(
                change,
                version="13.x",
                doc="guides/queues.md",
            )
        )
        self.assertFalse(
            main._matches_filters(change, version="13.x", doc="queues.md")
        )

    def test_sidebar_versions_always_include_every_canonical_version(self):
        """사이드바 버전 목록에 모든 정규 버전을 포함하는지 검증."""

        changes = [
            diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-12.x/a.md",
                status="M",
            ),
            diff.SourceChange(
                path="i18n/en/docusaurus-plugin-content-docs/version-master/b.md",
                status="M",
            ),
        ]

        with patch.object(
            main.sidebar,
            "load_versions",
            return_value=["master", "13.x", "12.x"],
        ):
            self.assertEqual(
                main._sidebar_versions(changes, "12.x"),
                ["master", "13.x", "12.x"],
            )

    def test_main_syncs_all_sidebars_when_no_sources_changed(self):
        """원문 변경이 없어도 모든 사이드바를 동기화하는지 검증."""

        calls: list[tuple[list[str], bool]] = []

        def sync_versions(versions, *, write=False, repo_root=None):
            """요청된 버전 목록 동기화."""

            calls.append((versions, write))
            return [main.sidebar.SidebarResult("master", False, [])]

        with patch.object(main.sys, "argv", ["main.py"]), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main.upstream, "main", return_value=0
        ), patch.object(main.diff, "changed_sources", return_value=[]), patch.object(
            main.sidebar,
            "load_versions",
            return_value=["master", "13.x", "12.x"],
        ), patch.object(
            main.sidebar, "sync_versions", side_effect=sync_versions
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(calls, [(["master", "13.x", "12.x"], True)])

    def test_main_scopes_upstream_sync_to_requested_filters(self):
        """업스트림 동기화를 요청된 필터 범위로 제한하는지 검증."""

        with patch.object(
            main.sys,
            "argv",
            ["main.py", "--version", "13.x", "--doc", "collections"],
        ), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main.upstream, "main", return_value=0
        ) as upstream_main, patch.object(
            main.diff, "changed_sources", return_value=[]
        ), patch.object(
            main.sidebar,
            "sync_versions",
            return_value=[main.sidebar.SidebarResult("13.x", False, [])],
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        upstream_main.assert_called_once_with(version="13.x", doc="collections.md")

    def test_main_passes_canonical_nested_document_filter_to_upstream(self):
        """정규 중첩 문서 필터를 업스트림에 전달하는지 검증."""

        with patch.object(
            main.sys,
            "argv",
            ["main.py", "--version", "13.x", "--doc", "guides/queues"],
        ), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main.upstream, "main", return_value=0
        ) as upstream_main, patch.object(
            main.diff, "changed_sources", return_value=[]
        ), patch.object(
            main.sidebar,
            "sync_versions",
            return_value=[main.sidebar.SidebarResult("13.x", False, [])],
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        upstream_main.assert_called_once_with(
            version="13.x",
            doc="guides/queues.md",
        )

    def test_main_rejects_noncanonical_document_filter_before_loading_config(self):
        """설정을 불러오기 전에 비정규 문서 필터를 거부하는지 검증."""

        stderr = io.StringIO()
        with redirect_stderr(stderr), patch.object(
            main.sys,
            "argv",
            ["main.py", "--version", "13.x", "--doc", "guides/../queues.md"],
        ), patch.object(
            main.config,
            "load_config",
            side_effect=AssertionError("configuration must not be loaded"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertIn("configuration failed: invalid document", stderr.getvalue())

    def test_main_requires_version_with_document_filter(self):
        """문서 필터 사용 시 버전 필터를 요구하는지 검증."""

        stderr = io.StringIO()
        with redirect_stderr(stderr), patch.object(
            main.sys,
            "argv",
            ["main.py", "--doc", "queues.md"],
        ), patch.object(
            main.config,
            "load_config",
            side_effect=AssertionError("configuration must not be loaded"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: --doc requires --version\n",
        )

    def test_main_reports_missing_filter_value_without_traceback(self):
        """누락된 필터 값을 트레이스백 없이 보고하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py", "--version"]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: --version requires a value\n",
        )

    def test_main_rejects_unknown_argument_before_upstream_sync(self):
        """업스트림 동기화 전에 알 수 없는 인수를 거부하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py", "--versoin", "13.x"]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: unknown argument: --versoin\n",
        )

    def test_main_rejects_empty_equals_filter_before_upstream_sync(self):
        """업스트림 동기화 전에 등호로 지정한 빈 필터를 거부하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py", "--version="]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: --version requires a value\n",
        )

    def test_main_rejects_obsolete_fail_fast_option(self):
        """폐기된 `--fail-fast` 옵션 거부 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys,
            "argv",
            ["main.py", "--fail-fast"],
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: unknown argument: --fail-fast\n",
        )

    def test_main_fail_fast_stops_after_first_verification_failure(self):
        """첫 번째 검증 실패 후 번역 처리를 중단하는지 검증."""

        change = diff.SourceChange(
            path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
            status="M",
        )
        calls: list[str] = []

        def translate_one(
            change,
            cfg,
            prompt,
            dest,
            *,
            locale=None,
            deadline=None,
            prepared_target=None,
            attempt_counter=None,
        ):
            """단일 로케일 번역 실패 반환."""

            self.assertIn(locale, ("ko", "ja"))
            self.assertIsNone(deadline)
            self.assertIsNotNone(attempt_counter)
            calls.append(str(dest))
            return ["heading mismatch"]

        with patch.object(
            main.sys, "argv", ["main.py"]
        ), patch.object(main.upstream, "main", return_value=0), patch.object(
            main.diff, "changed_sources", return_value=[change]
        ), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main, "_load_prompts", return_value={"ko": "ko prompt", "ja": "ja prompt"}
        ), patch.object(
            main, "_validate_file_states", return_value=[]
        ), patch.object(
            main,
            "_preflight_all_translation_targets",
            return_value=(
                {
                    (change.path, "ko"): object(),
                    (change.path, "ja"): object(),
                },
                [],
            ),
        ), patch.object(
            main, "_translate_one", side_effect=translate_one
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(len(calls), 1)

    def test_main_writes_provider_failure_report_with_attempt_context(self):
        """sync-core provider 실패의 정규 보고서와 시도 문맥 기록 검증."""

        change = diff.SourceChange(
            path="i18n/en/docusaurus-plugin-content-docs/version-12.x/example.md",
            status="M",
        )

        def translate_one(
            change,
            cfg,
            prompt,
            dest,
            *,
            locale=None,
            deadline=None,
            prepared_target=None,
            attempt_counter=None,
        ):
            """provider 응답 계약 실패와 누적 시도 횟수 기록."""

            self.assertIsNotNone(attempt_counter)
            attempt_counter.transport = 3
            attempt_counter.response_evaluation = 2
            return [
                (
                    "provider response contract failed: heading mismatch "
                    "[RESPONSE_CONTRACT_FAILED]"
                )
            ]

        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp).resolve() / "sync-failure.json"
            with patch.dict(
                main.os.environ,
                {
                    main.FAILURE_REPORT_ENV: str(report_path),
                    main.RUN_ID_ENV: "candidate-run-1",
                },
            ), patch.object(
                main.sys, "argv", ["main.py"]
            ), patch.object(
                main.upstream, "main", return_value=0
            ), patch.object(
                main.diff, "changed_sources", return_value=[change]
            ), patch.object(
                main.config,
                "load_config",
                return_value=config.Config(
                    provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
                ),
            ), patch.object(
                main, "_load_prompts", return_value={"ko": "ko prompt", "ja": "ja prompt"}
            ), patch.object(
                main, "_validate_file_states", return_value=[]
            ), patch.object(
                main,
                "_preflight_all_translation_targets",
                return_value=(
                    {
                        (change.path, "ko"): object(),
                        (change.path, "ja"): object(),
                    },
                    [],
                ),
            ), patch.object(
                main, "_translate_one", side_effect=translate_one
            ):
                exit_code = main.main()

            raw = report_path.read_bytes()
            report = json.loads(raw)

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["code"], "RESPONSE_CONTRACT_FAILED")
        self.assertEqual(report["stage"], "translation-provider")
        self.assertEqual(report["version"], "12.x")
        self.assertEqual(report["locale"], "ko")
        self.assertEqual(report["document"], change.path)
        self.assertEqual(
            report["attempts"],
            {"response_evaluation": 2, "transport": 3},
        )
        self.assertEqual(
            raw,
            (
                json.dumps(
                    report,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8"),
        )

    def test_main_stops_when_upstream_sync_fails(self):
        """업스트림 동기화 실패 시 중단하는지 검증."""

        with patch.object(main.sys, "argv", ["main.py"]), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main.upstream, "main", return_value=1
        ), patch.object(
            main.diff,
            "changed_sources",
            side_effect=AssertionError("diff should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)

    def test_main_redacts_unexpected_runner_and_internal_errors(self):
        """예상하지 못한 오류가 traceback 없이 exit 2로 변환되는지 검증."""

        cases = (
            (
                PermissionError("/Users/person/private/source.md"),
                "translation sync failed: runner operation failed\n",
            ),
            (
                RuntimeError("secret internal detail"),
                "translation sync failed: unexpected internal error\n",
            ),
        )
        for error, expected_stderr in cases:
            with self.subTest(error=type(error).__name__):
                stderr = io.StringIO()
                with redirect_stderr(stderr), patch.dict(
                    main.os.environ, {}, clear=True
                ), patch.object(
                    main.sys, "argv", ["main.py"]
                ), patch.object(
                    main.config,
                    "load_config",
                    return_value=config.Config(
                        provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
                    ),
                ), patch.object(
                    main, "_load_prompts", return_value={"ko": "ko", "ja": "ja"}
                ), patch.object(
                    main.upstream, "main", side_effect=error
                ):
                    exit_code = main.main()

                self.assertEqual(exit_code, 2)
                self.assertEqual(stderr.getvalue(), expected_stderr)

    def test_main_reports_invalid_source_diff_without_traceback(self):
        """잘못된 원문 diff를 트레이스백 없이 보고하는지 검증."""

        stderr = io.StringIO()
        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py"]
        ), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main, "_load_prompts", return_value={"ko": "ko", "ja": "ja"}
        ), patch.object(
            main.upstream, "main", return_value=0
        ), patch.object(
            main.diff,
            "changed_sources",
            side_effect=diff.SourceDiffError("unsupported source status 'U'"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "source diff failed: unsupported source status 'U'\n",
        )

    def test_main_reports_invalid_provider_configuration_without_traceback(self):
        """잘못된 공급자 설정을 트레이스백 없이 보고하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py"]
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ), patch.object(
            main.config,
            "load_config",
            side_effect=config.ConfigError(
                "TRANSLATION_CLI_TIMEOUT must be an integer > 0"
            ),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "configuration failed: "
            "TRANSLATION_CLI_TIMEOUT must be an integer > 0\n",
        )

    def test_main_reports_missing_prompt_before_upstream_sync(self):
        """업스트림 동기화 전에 누락된 프롬프트를 보고하는지 검증."""

        stderr = io.StringIO()

        with redirect_stderr(stderr), patch.object(
            main.sys, "argv", ["main.py"]
        ), patch.object(
            main.config,
            "load_config",
            return_value=config.Config(
                provider="cli", values={"TRANSLATION_PROVIDER": "cli"}
            ),
        ), patch.object(
            main,
            "_load_prompts",
            side_effect=main.prompt.PromptError("missing prompt file: prompt.md"),
        ), patch.object(
            main.upstream,
            "main",
            side_effect=AssertionError("upstream should not run"),
        ):
            exit_code = main.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "prompt loading failed: missing prompt file: prompt.md\n",
        )

if __name__ == "__main__":
    unittest.main()
