"""process runtime 동작과 경계 조건 검증."""

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
    """프로세스 tree runner 테스트 객체."""

    @staticmethod
    def _process_is_live(pid: int) -> bool:
        """live 처리."""

        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True

    @classmethod
    def _wait_for_process_exit(cls, pid: int, timeout: float = 2.0) -> bool:
        """for 프로세스 exit 대기."""

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not cls._process_is_live(pid):
                return True
            time.sleep(0.01)
        return not cls._process_is_live(pid)

    def test_run_compatible_input_and_captured_output(self) -> None:
        """`run_compatible_input_and_captured_output` 시나리오 검증."""

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
        """`spawn`의 exact 환경 및 신규 session 사용 검증."""

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
        """`shell_execution`의 프로세스 start 전 rejected 판정 검증."""

        with patch.object(process_runtime.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(ValueError, "shell execution is forbidden"):
                process_runtime.run_process_tree(["ignored"], shell=True)

        popen.assert_not_called()

    def test_timeout_kills_process_group_before_raising(self) -> None:
        """`timeout_kills_process_group_before_raising` 시나리오 검증."""

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
        """`timeout`의 않음 hang on grandchild inheriting stdout 동작 검증."""

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
        """`parent_success_with_surviving_child`의 cleaned leak 판정 검증."""

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
        """`keyboard_interrupt_cleans_tree_and`의 re raised 판정 검증."""

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
                """interrupt 처리."""

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
        """`check_raises_after_the_process_group`의 gone 판정 검증."""

        with self.assertRaises(subprocess.CalledProcessError) as raised:
            process_runtime.run_process_tree(
                [sys.executable, "-c", "raise SystemExit(7)"],
                capture_output=True,
                timeout=5,
                check=True,
            )

        self.assertEqual(raised.exception.returncode, 7)

    def test_cleanup_failure_replaces_timeout_with_explicit_error(self) -> None:
        """`cleanup_failure_replaces_timeout_with_explicit_error` 시나리오 검증."""

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
        """`timeout`의 하위 프로세스 실행 exception fields 보존 검증."""

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
        """`cleanup_continues_after_process_group_kill_failure` 시나리오 검증."""

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
        """`cleanup_timeout`의 group kill 후 accumulated 판정 검증."""

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

    def test_process_group_kill_reports_whether_signal_was_accepted(self) -> None:
        """`process_group_kill_reports_whether_signal_was_accepted` 시나리오 검증."""

        with patch.object(process_runtime.os, "killpg"):
            self.assertTrue(process_runtime._kill_process_group(123))

        with patch.object(
            process_runtime.os,
            "killpg",
            side_effect=ProcessLookupError,
        ):
            self.assertFalse(process_runtime._kill_process_group(123))

    def test_process_group_probe_permission_is_not_treated_as_dead(self) -> None:
        """`process_group_probe_permission`의 않음 treated 로 dead 판정 검증."""

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


if __name__ == "__main__":
    unittest.main()
