"""공통 파일 연산의 동작과 경계 조건 검증."""

import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sync.common import files


class AtomicWriteTests(unittest.TestCase):
    """원자적 파일 쓰기의 동작과 경계 조건 테스트 모음."""

    def test_text_write_fsyncs_file_and_parent_directory(self) -> None:
        """텍스트 교체 시 파일과 상위 디렉터리 동기화 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example.md"
            real_fsync = os.fsync
            targets: list[str] = []

            def record(descriptor: int) -> None:
                """동기화 대상 파일 종류 기록."""

                mode = os.fstat(descriptor).st_mode
                targets.append(
                    "directory" if stat.S_ISDIR(mode) else "file"
                )
                real_fsync(descriptor)

            with patch.object(files.os, "fsync", side_effect=record):
                files.atomic_write_text(path, "new\n")

            self.assertEqual(targets, ["file", "directory"])
            self.assertEqual(path.read_text(encoding="utf-8"), "new\n")

    def test_binary_write_replaces_inode_and_preserves_mode(self) -> None:
        """바이너리 교체 시 기존 inode 분리와 파일 권한 보존 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "artifact.bin"
            alias = root / "approved.bin"
            path.write_bytes(b"old")
            path.chmod(0o640)
            os.link(path, alias)

            files.atomic_write_bytes(path, b"new")

            self.assertEqual(path.read_bytes(), b"new")
            self.assertEqual(alias.read_bytes(), b"old")
            self.assertNotEqual(path.stat().st_ino, alias.stat().st_ino)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o640)

    def test_unlink_fsyncs_parent_directory(self) -> None:
        """파일 삭제 시 상위 디렉터리 동기화 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example.md"
            path.write_text("old\n", encoding="utf-8")
            real_fsync = os.fsync
            targets: list[str] = []

            def record(descriptor: int) -> None:
                """동기화 대상 파일 종류 기록."""

                mode = os.fstat(descriptor).st_mode
                targets.append(
                    "directory" if stat.S_ISDIR(mode) else "file"
                )
                real_fsync(descriptor)

            with patch.object(files.os, "fsync", side_effect=record):
                removed = files.unlink_file(path)

            self.assertTrue(removed)
            self.assertEqual(targets, ["directory"])
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
