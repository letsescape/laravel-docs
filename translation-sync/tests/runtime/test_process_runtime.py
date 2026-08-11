"""프로세스 실행기 동작과 경계 조건 검증."""

import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from sync.runtime import process as process_runtime


class ProcessTreeRunnerTest(unittest.TestCase):
    """프로세스 트리 실행기 테스트 모음."""

    @staticmethod
    def _process_is_live(pid: int) -> bool:
        """프로세스 생존 여부 확인. reap되지 않은 zombie는 종료로 간주."""

        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        try:
            with open(f"/proc/{pid}/stat", "rb") as stat_file:
                record = stat_file.read()
        except OSError:
            return True
        comm_end = record.rfind(b")")
        if comm_end < 0:
            return True
        fields = record[comm_end + 1 :].split()
        if not fields:
            return True
        return fields[0] not in (b"Z", b"X", b"x")

    @classmethod
    def _wait_for_process_exit(cls, pid: int, timeout: float = 2.0) -> bool:
        """지정한 시간 동안 프로세스 종료 대기."""

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not cls._process_is_live(pid):
                return True
            time.sleep(0.01)
        return not cls._process_is_live(pid)

    def test_run_compatible_input_and_captured_output(self) -> None:
        """``subprocess.run`` 호환 입력과 출력 캡처 검증."""

        args = [
            sys.executable,
            "-c",
            "import sys; sys.stdout.write(sys.stdin.read().upper())",
        ]
        completed = process_runtime.run_process_tree(
            args,
            input="hello",
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "HELLO")
        self.assertEqual(completed.stderr, "")
        self.assertIs(completed.args, args)

    def test_spawn_uses_exact_environment_and_a_new_session(self) -> None:
        """프로세스 생성 시 정확한 환경과 새 세션 사용 검증."""

        environment = {"ONLY": "explicit"}
        child = MagicMock(pid=123, returncode=0)
        child.communicate.return_value = (None, None)

        with patch.object(
            process_runtime.subprocess,
            "Popen",
            return_value=child,
        ) as popen, patch.object(
            process_runtime,
            "_process_group_alive",
            return_value=False,
        ):
            process_runtime.run_process_tree(
                ["command"],
                env=environment,
            )

        self.assertIs(popen.call_args.kwargs["env"], environment)
        self.assertIs(popen.call_args.kwargs["shell"], False)
        self.assertIs(popen.call_args.kwargs["start_new_session"], True)

    def test_shell_execution_is_rejected_before_process_start(self) -> None:
        """셸 실행을 프로세스 시작 전에 거부하는지 검증."""

        with patch.object(process_runtime.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(ValueError, "shell execution is forbidden"):
                process_runtime.run_process_tree(["ignored"], shell=True)

        popen.assert_not_called()

    def test_timeout_kills_process_group_before_raising(self) -> None:
        """기한 초과 예외 전에 프로세스 그룹을 종료하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pid_path = root / "grandchild.pid"
            marker = root / "late-write"
            grandchild = (
                "import pathlib,sys,time; time.sleep(0.8); "
                "pathlib.Path(sys.argv[1]).write_text('late')"
            )
            parent = (
                "import pathlib,subprocess,sys,time; "
                "child=subprocess.Popen([sys.executable,'-c',sys.argv[1],"
                "sys.argv[3]], "
                "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, "
                "stderr=subprocess.DEVNULL); "
                "pathlib.Path(sys.argv[2]).write_text(str(child.pid)); "
                "time.sleep(30)"
            )

            with self.assertRaises(subprocess.TimeoutExpired):
                process_runtime.run_process_tree(
                    [
                        sys.executable,
                        "-c",
                        parent,
                        grandchild,
                        str(pid_path),
                        str(marker),
                    ],
                    timeout=0.3,
                )

            grandchild_pid = int(pid_path.read_text())
            self.assertTrue(self._wait_for_process_exit(grandchild_pid))
            time.sleep(0.9)
            self.assertFalse(marker.exists())

    def test_timeout_does_not_hang_on_a_grandchild_inheriting_stdout(self) -> None:
        """출력을 상속한 손자 프로세스가 있어도 기한 초과 처리가 멈추지 않는지 검증."""

        child = "import time; time.sleep(30)"
        parent = (
            "import subprocess,sys; "
            "subprocess.Popen([sys.executable,'-c',sys.argv[1]])"
        )
        started = time.monotonic()

        with self.assertRaises(subprocess.TimeoutExpired):
            process_runtime.run_process_tree(
                [sys.executable, "-c", parent, child],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=0.3,
            )

        self.assertLess(time.monotonic() - started, 2)

    def test_parent_success_with_surviving_child_is_a_cleaned_leak(self) -> None:
        """부모 프로세스 성공 후에도 살아 있는 하위 프로세스를 누수로 정리하는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pid_path = root / "grandchild.pid"
            marker = root / "late-write"
            grandchild = (
                "import pathlib,sys,time; time.sleep(0.8); "
                "pathlib.Path(sys.argv[1]).write_text('late')"
            )
            parent = (
                "import pathlib,subprocess,sys; "
                "child=subprocess.Popen([sys.executable,'-c',sys.argv[1],"
                "sys.argv[3]], stdin=subprocess.DEVNULL, "
                "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); "
                "pathlib.Path(sys.argv[2]).write_text(str(child.pid))"
            )

            with self.assertRaises(process_runtime.ProcessTreeLeak):
                process_runtime.run_process_tree(
                    [
                        sys.executable,
                        "-c",
                        parent,
                        grandchild,
                        str(pid_path),
                        str(marker),
                    ],
                    timeout=5,
                )

            grandchild_pid = int(pid_path.read_text())
            self.assertTrue(self._wait_for_process_exit(grandchild_pid))
            time.sleep(0.9)
            self.assertFalse(marker.exists())

    @unittest.skipUnless(hasattr(signal, "setitimer"), "requires POSIX timers")
    def test_keyboard_interrupt_cleans_tree_and_is_re_raised(self) -> None:
        """키보드 인터럽트 시 프로세스 트리를 정리하고 예외를 다시 발생시키는지 검증."""

        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "late-write"
            grandchild = (
                "import pathlib,sys,time; time.sleep(0.8); "
                "pathlib.Path(sys.argv[1]).write_text('late')"
            )
            parent = (
                "import subprocess,sys,time; "
                "subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2]], "
                "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, "
                "stderr=subprocess.DEVNULL); time.sleep(30)"
            )
            previous = signal.getsignal(signal.SIGALRM)

            def interrupt(_signum: int, _frame: object) -> None:
                """키보드 인터럽트 발생."""

                raise KeyboardInterrupt

            signal.signal(signal.SIGALRM, interrupt)
            signal.setitimer(signal.ITIMER_REAL, 0.3)
            try:
                with self.assertRaises(KeyboardInterrupt):
                    process_runtime.run_process_tree(
                        [sys.executable, "-c", parent, grandchild, str(marker)],
                    )
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, previous)

            time.sleep(0.9)
            self.assertFalse(marker.exists())

    def test_check_raises_after_the_process_group_is_gone(self) -> None:
        """프로세스 그룹 종료 후 검사 예외를 발생시키는지 검증."""

        with self.assertRaises(subprocess.CalledProcessError) as raised:
            process_runtime.run_process_tree(
                [sys.executable, "-c", "raise SystemExit(7)"],
                capture_output=True,
                timeout=5,
                check=True,
            )

        self.assertEqual(raised.exception.returncode, 7)

    def test_cleanup_failure_replaces_timeout_with_explicit_error(self) -> None:
        """정리 실패가 기한 초과를 명시적 오류로 대체하는지 검증."""

        cleanup = process_runtime.ProcessTreeCleanupError("cleanup failed")
        child = MagicMock()
        child.communicate.side_effect = subprocess.TimeoutExpired(["command"], 1)
        with patch.object(
            process_runtime,
            "_terminate_process_group",
            side_effect=cleanup,
        ), patch.object(
            process_runtime.subprocess,
            "Popen",
            return_value=child,
        ):
            with self.assertRaises(process_runtime.ProcessTreeCleanupError) as raised:
                process_runtime.run_process_tree(
                    [sys.executable, "-c", "pass"],
                    timeout=1,
                )

        self.assertIs(raised.exception, cleanup)

    def test_timeout_preserves_subprocess_run_exception_fields(self) -> None:
        """기한 초과 시 ``subprocess.run`` 예외 필드 보존 검증."""

        args = [
            sys.executable,
            "-c",
            "import sys,time; sys.stdout.write('partial'); "
            "sys.stdout.flush(); time.sleep(30)",
        ]

        with self.assertRaises(subprocess.TimeoutExpired) as raised:
            process_runtime.run_process_tree(
                args,
                capture_output=True,
                text=True,
                timeout=0.1,
            )

        self.assertIs(raised.exception.cmd, args)
        self.assertEqual(raised.exception.output, b"partial")
        self.assertIsNone(raised.exception.stderr)

    def test_cleanup_continues_after_process_group_kill_failure(self) -> None:
        """프로세스 그룹 종료 실패 후에도 정리를 계속하는지 검증."""

        process = MagicMock(pid=123)
        process.poll.side_effect = [None, 0]
        failure = process_runtime.ProcessTreeCleanupError(
            "the process group could not be killed"
        )

        with patch.object(
            process_runtime,
            "_kill_process_group",
            side_effect=failure,
        ):
            with self.assertRaises(process_runtime.ProcessTreeCleanupError):
                process_runtime._terminate_process_group(
                    process,
                    drain_pipes=False,
                )

        process.kill.assert_called_once_with()
        process.wait.assert_called_once()

    def test_cleanup_timeout_is_accumulated_after_group_kill(self) -> None:
        """프로세스 그룹 종료 후 정리 기한 초과를 누적하는지 검증."""

        process = MagicMock(pid=123)
        process.poll.return_value = 0
        process.wait.side_effect = subprocess.TimeoutExpired(["command"], 0)

        with patch.object(
            process_runtime,
            "_kill_process_group",
            return_value=True,
        ) as kill_group, patch.object(
            process_runtime.time,
            "monotonic",
            side_effect=[0.0, 6.0],
        ):
            with self.assertRaises(process_runtime.ProcessTreeCleanupError):
                process_runtime._terminate_process_group(
                    process,
                    drain_pipes=False,
                )

        kill_group.assert_called_once_with(process.pid)
        process.wait.assert_called_once_with(timeout=0.0)

    def test_cleanup_waits_until_the_process_group_disappears(self) -> None:
        """직접 자식 회수 뒤 전체 프로세스 그룹 소멸까지 확인하는지 검증."""

        process = MagicMock(pid=123)
        process.poll.return_value = 0

        with patch.object(
            process_runtime,
            "_kill_process_group",
            return_value=True,
        ), patch.object(
            process_runtime,
            "_process_group_alive",
            side_effect=[True, False],
        ) as group_alive, patch.object(
            process_runtime.time,
            "monotonic",
            return_value=0.0,
        ), patch.object(process_runtime.time, "sleep") as sleep:
            process_runtime._terminate_process_group(
                process,
                drain_pipes=False,
            )

        self.assertEqual(group_alive.call_count, 2)
        sleep.assert_called_once_with(
            process_runtime._CLEANUP_POLL_INTERVAL_SECONDS
        )

    def test_cleanup_rejects_a_process_group_that_does_not_disappear(self) -> None:
        """정리 기한 뒤 남은 프로세스 그룹을 성공으로 보고하지 않는지 검증."""

        process = MagicMock(pid=123)
        process.poll.return_value = 0

        with patch.object(
            process_runtime,
            "_kill_process_group",
            return_value=True,
        ), patch.object(
            process_runtime,
            "_process_group_alive",
            return_value=True,
        ), patch.object(
            process_runtime.time,
            "monotonic",
            side_effect=[0.0, 0.0, 6.0],
        ), self.assertRaisesRegex(
            process_runtime.ProcessTreeCleanupError,
            "cleanup could not be fully verified",
        ):
            process_runtime._terminate_process_group(
                process,
                drain_pipes=False,
            )

    def test_process_group_kill_reports_whether_signal_was_accepted(self) -> None:
        """프로세스 그룹 종료 신호의 수락 여부를 보고하는지 검증."""

        with patch.object(process_runtime.os, "killpg"):
            self.assertTrue(process_runtime._kill_process_group(123))

        with patch.object(
            process_runtime.os,
            "killpg",
            side_effect=ProcessLookupError,
        ):
            self.assertFalse(process_runtime._kill_process_group(123))

    def test_process_group_probe_permission_is_not_treated_as_dead(self) -> None:
        """프로세스 그룹 조회 권한 오류를 종료 상태로 간주하지 않는지 검증."""

        with patch.object(
            process_runtime.os,
            "killpg",
            side_effect=PermissionError,
        ):
            with self.assertRaisesRegex(
                process_runtime.ProcessTreeCleanupError,
                "process group could not be inspected",
            ):
                process_runtime._process_group_alive(123)

    def test_zombie_only_process_group_is_treated_as_exited(self) -> None:
        """zombie만 남은 프로세스 그룹을 정리 완료로 간주하는지 검증."""

        with patch.object(
            process_runtime,
            "_process_group_alive",
            return_value=True,
        ), patch.object(
            process_runtime,
            "_process_group_has_running_members",
            return_value=False,
        ):
            self.assertFalse(
                process_runtime._process_group_members_running(123)
            )

    def test_unknown_member_states_keep_the_group_alive(self) -> None:
        """구성원 상태를 알 수 없으면 fail-closed로 생존을 유지하는지 검증."""

        with patch.object(
            process_runtime,
            "_process_group_alive",
            return_value=True,
        ), patch.object(
            process_runtime,
            "_process_group_has_running_members",
            return_value=None,
        ):
            self.assertTrue(
                process_runtime._process_group_members_running(123)
            )

    def test_cleanup_succeeds_when_only_zombies_remain(self) -> None:
        """zombie만 남은 그룹에서 정리가 명시적 오류 없이 끝나는지 검증."""

        process = MagicMock(pid=123)
        process.poll.return_value = 0

        with patch.object(
            process_runtime,
            "_kill_process_group",
            return_value=True,
        ), patch.object(
            process_runtime,
            "_process_group_alive",
            return_value=True,
        ), patch.object(
            process_runtime,
            "_process_group_has_running_members",
            return_value=False,
        ):
            process_runtime._terminate_process_group(
                process,
                drain_pipes=False,
            )

    def test_proc_scan_reports_running_and_zombie_members(self) -> None:
        """``/proc`` 스캔이 실행 중·zombie 구성원을 구별하는지 검증."""

        with tempfile.TemporaryDirectory() as proc_root:
            zombie = Path(proc_root, "101")
            zombie.mkdir()
            (zombie / "stat").write_bytes(b"101 (worker) Z 1 123 123 0 -1\n")
            with patch.object(process_runtime, "_PROC_ROOT", proc_root):
                self.assertFalse(
                    process_runtime._process_group_has_running_members(123)
                )
            runner = Path(proc_root, "102")
            runner.mkdir()
            (runner / "stat").write_bytes(
                b"102 (wo rk)er) R 1 123 123 0 -1\n"
            )
            with patch.object(process_runtime, "_PROC_ROOT", proc_root):
                self.assertTrue(
                    process_runtime._process_group_has_running_members(123)
                )

    def test_proc_scan_without_group_members_is_inconclusive(self) -> None:
        """그룹 구성원이 관측되지 않으면 판정을 유보하는지 검증."""

        with tempfile.TemporaryDirectory() as proc_root:
            other = Path(proc_root, "104")
            other.mkdir()
            (other / "stat").write_bytes(b"104 (other) R 1 999 999 0 -1\n")
            with patch.object(process_runtime, "_PROC_ROOT", proc_root):
                self.assertIsNone(
                    process_runtime._process_group_has_running_members(123)
                )

    def test_proc_scan_missing_root_is_inconclusive(self) -> None:
        """``/proc``이 없으면 판정을 유보하는지 검증."""

        with tempfile.TemporaryDirectory() as proc_root:
            missing = os.path.join(proc_root, "absent")
            with patch.object(process_runtime, "_PROC_ROOT", missing):
                self.assertIsNone(
                    process_runtime._process_group_has_running_members(123)
                )


if __name__ == "__main__":
    unittest.main()
