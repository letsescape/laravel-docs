"""호출보다 오래 살아남는 process group 없이 argv 명령 실행.

의도적인 POSIX 전용 runner.
각 직접 하위 프로세스는 새 session에서 시작하고 PID를 정리용 process-group ID로 사용.
관리 대상 명령의 ``setsid``, ``setpgid``, double-fork, reparent, detach 및 runner의 group signal을 막는 자격 증명 변경은 금지.
이 명령 계약을 위반한 하위 프로세스는 격리 보장 대상에서 제외.
"""

from __future__ import annotations

import math
import os
import signal
import subprocess
import time
from collections.abc import Mapping, Sequence
from typing import Any


_CLEANUP_TIMEOUT_SECONDS = 5.0
_CLEANUP_POLL_INTERVAL_SECONDS = 0.01
_INVALID_TIMEOUT = "timeout must be a non-negative finite number"


class ProcessTreeError(RuntimeError):
    """fail-closed process-group runner 실패의 기반 오류."""


class ProcessTreeUnsupported(ProcessTreeError):
    """호스트에서 필수 process-group 격리를 제공할 수 없는 오류."""


class ProcessTreeLeak(ProcessTreeError):
    """process group 구성원이 남은 상태에서 명령이 반환된 오류."""


class ProcessTreeCleanupError(ProcessTreeError):
    """runner가 process-group 정리 완료를 증명할 수 없는 오류."""


def _validate_timeout(timeout: float | None) -> float | None:
    """하위 프로세스 timeout을 유한한 0 이상의 실수로 정규화."""

    if timeout is None:
        return None
    if isinstance(timeout, bool):
        raise TypeError(_INVALID_TIMEOUT)
    try:
        parsed = float(timeout)
    except (TypeError, ValueError, OverflowError):
        raise TypeError(_INVALID_TIMEOUT) from None
    if not math.isfinite(parsed) or parsed < 0:
        raise ValueError(_INVALID_TIMEOUT)
    return parsed


def _validate_argv(
    args: Sequence[str | bytes | os.PathLike[str] | os.PathLike[bytes]],
) -> None:
    """shell 문자열이 아닌 비어 있지 않은 argv 확인."""

    if isinstance(args, (str, bytes, os.PathLike)):
        raise TypeError("args must be a non-empty argv sequence")
    if not tuple(args):
        raise ValueError("args must be a non-empty argv sequence")


def _kill_process_group(process_group: int) -> bool:
    """프로세스 그룹에 강제 종료 시그널 전송."""

    try:
        os.killpg(process_group, signal.SIGKILL)
    except ProcessLookupError:
        return False
    except PermissionError as exc:
        raise ProcessTreeCleanupError(
            "the process group could not be killed"
        ) from exc
    except OSError as exc:
        raise ProcessTreeCleanupError(
            "the process group could not be killed"
        ) from exc
    return True


def _process_group_alive(process_group: int) -> bool:
    """프로세스 그룹 구성원의 생존 여부 확인."""

    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return False
    except PermissionError as exc:
        raise ProcessTreeCleanupError(
            "the process group could not be inspected"
        ) from exc
    except OSError as exc:
        raise ProcessTreeCleanupError(
            "the process group could not be inspected"
        ) from exc
    return True


def _cleanup_error(failures: list[BaseException]) -> ProcessTreeCleanupError:
    """첫 원인을 보존하는 프로세스 정리 실패 생성."""

    error = ProcessTreeCleanupError(
        "process-group cleanup could not be fully verified"
    )
    if failures:
        error.__cause__ = failures[0]
    return error


def _wait_for_process_group_exit(process_group: int, deadline: float) -> None:
    """정리 기한 안에 프로세스 그룹이 사라졌는지 확인.

    Args:
        process_group: 확인할 프로세스 그룹 ID.
        deadline: 정리를 마쳐야 하는 단조 시계 시각.

    Raises:
        ProcessTreeCleanupError: 기한 안에 그룹 소멸을 확인하지 못한 경우.
    """

    while _process_group_alive(process_group):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ProcessTreeCleanupError(
                "the process group remained after termination"
            )
        time.sleep(min(_CLEANUP_POLL_INTERVAL_SECONDS, remaining))


def _terminate_process_group(
    process: subprocess.Popen[Any],
    *,
    drain_pipes: bool,
) -> tuple[Any, Any]:
    """격리 프로세스 그룹 종료와 직접 하위 프로세스 회수."""

    cleanup_deadline = time.monotonic() + _CLEANUP_TIMEOUT_SECONDS
    failures: list[BaseException] = []
    try:
        _kill_process_group(process.pid)
    except ProcessTreeCleanupError as exc:
        failures.append(exc)

    try:
        direct_child_alive = process.poll() is None
    except Exception as exc:
        failures.append(exc)
        direct_child_alive = True
    if direct_child_alive:
        try:
            process.kill()
        except Exception as exc:
            failures.append(exc)

    stdout: Any = None
    stderr: Any = None
    remaining = max(cleanup_deadline - time.monotonic(), 0.0)
    try:
        if drain_pipes:
            stdout, stderr = process.communicate(timeout=remaining)
        else:
            process.wait(timeout=remaining)
    except Exception as exc:
        failures.append(exc)

    try:
        direct_child_alive = process.poll() is None
    except Exception as exc:
        failures.append(exc)
        direct_child_alive = True
    if direct_child_alive:
        failures.append(
            ProcessTreeCleanupError("the direct child was not reaped")
        )
    try:
        _wait_for_process_group_exit(process.pid, cleanup_deadline)
    except ProcessTreeCleanupError as exc:
        failures.append(exc)
    if failures:
        raise _cleanup_error(failures)
    return stdout, stderr


def _validate_run_options(
    *,
    shell: bool,
    input_value: str | bytes | None,
    stdin: Any,
    stdout: Any,
    stderr: Any,
    capture_output: bool,
) -> None:
    """프로세스 그룹 실행에 필요한 호스트와 입출력 옵션 검증.

    Args:
        shell: shell 실행 요청 여부.
        input_value: 표준 입력으로 전달할 값.
        stdin: 표준 입력 stream 설정.
        stdout: 표준 출력 stream 설정.
        stderr: 표준 오류 stream 설정.
        capture_output: 표준 출력과 오류의 동시 캡처 여부.
    """

    if os.name != "posix" or not hasattr(os, "killpg"):
        raise ProcessTreeUnsupported("POSIX process groups are required")
    if shell is not False:
        raise ValueError("shell execution is forbidden")
    if input_value is not None and stdin is not None:
        raise ValueError("stdin and input arguments may not both be used")
    if capture_output and (stdout is not None or stderr is not None):
        raise ValueError(
            "stdout and stderr arguments may not be used with capture_output"
        )


def _communicate_with_cleanup(
    process: subprocess.Popen[Any],
    *,
    input_value: str | bytes | None,
    timeout: float | None,
) -> tuple[Any, Any]:
    """명령과 통신하고 실패 시 프로세스 그룹 정리.

    Args:
        process: 새 세션에서 실행 중인 직접 하위 프로세스.
        input_value: 표준 입력으로 전달할 값.
        timeout: 프로세스 실행 제한 시간.

    Returns:
        표준 출력과 표준 오류 값.
    """

    try:
        return process.communicate(input=input_value, timeout=timeout)
    except BaseException as exc:
        try:
            _terminate_process_group(process, drain_pipes=True)
        except ProcessTreeCleanupError as cleanup_error:
            raise cleanup_error from exc
        raise


def _require_empty_process_group(process: subprocess.Popen[Any]) -> None:
    """직접 하위 프로세스 종료 뒤 프로세스 그룹이 비었는지 확인.

    Args:
        process: 종료된 직접 하위 프로세스.
    """

    try:
        survivors = _process_group_alive(process.pid)
    except BaseException as inspection_error:
        try:
            _terminate_process_group(process, drain_pipes=False)
        except ProcessTreeCleanupError as cleanup_error:
            raise cleanup_error from inspection_error
        raise
    if not survivors:
        return
    _terminate_process_group(process, drain_pipes=False)
    raise ProcessTreeLeak(
        "the command returned while process-group members were still running"
    )


def run_process_tree(
    args: Sequence[str | bytes | os.PathLike[str] | os.PathLike[bytes]],
    *,
    cwd: str | bytes | os.PathLike[str] | os.PathLike[bytes] | None = None,
    env: Mapping[str, str] | Mapping[bytes, bytes] | None = None,
    input: str | bytes | None = None,
    stdin: Any = None,
    stdout: Any = None,
    stderr: Any = None,
    capture_output: bool = False,
    text: bool = False,
    encoding: str | None = None,
    errors: str | None = None,
    timeout: float | None = None,
    check: bool = False,
    shell: bool = False,
) -> subprocess.CompletedProcess[Any]:
    """process group 제거를 완료 조건으로 하는 단일 argv 명령 실행.

    번역 워크플로에서 사용하는 ``subprocess.run`` 인자 부분집합과 의도적으로 동일한 계약.
    shell 실행은 항상 금지.

    Args:
        args: 실행 파일과 인수로 구성된 비어 있지 않은 argv.
        cwd: 하위 프로세스의 작업 디렉터리.
        env: 하위 프로세스에 전달할 환경 변수 mapping.
        input: 표준 입력으로 전달할 문자열 또는 바이트.
        stdin: 표준 입력 stream 설정.
        stdout: 표준 출력 stream 설정.
        stderr: 표준 오류 stream 설정.
        capture_output: 표준 출력과 오류의 동시 캡처 여부.
        text: text mode 사용 여부.
        encoding: text mode 인코딩.
        errors: text mode 디코딩 오류 정책.
        timeout: 프로세스 실행 제한 시간(초).
        check: 0이 아닌 종료 코드 예외 변환 여부.
        shell: shell 실행 금지 확인용 인수. ``False``만 허용.

    Returns:
        하위 프로세스 종료 코드와 캡처 결과.

    Raises:
        ProcessTreeUnsupported: POSIX 프로세스 그룹을 사용할 수 없는 경우.
        ProcessTreeLeak: 직접 하위 프로세스 종료 후 그룹 구성원이 남은 경우.
        ProcessTreeCleanupError: 프로세스 그룹 정리를 증명하지 못한 경우.
        subprocess.TimeoutExpired: 제한 시간을 초과한 경우.
        subprocess.CalledProcessError: ``check``가 참이고 명령이 실패한 경우.
        TypeError: argv 또는 timeout 타입이 계약에 맞지 않는 경우.
        ValueError: argv 또는 실행 옵션이 계약에 맞지 않는 경우.
    """

    _validate_run_options(
        shell=shell,
        input_value=input,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        capture_output=capture_output,
    )

    _validate_argv(args)
    parsed_timeout = _validate_timeout(timeout)
    if input is not None:
        stdin = subprocess.PIPE
    if capture_output:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE

    process = subprocess.Popen(
        args,
        cwd=cwd,
        env=env,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        text=text,
        encoding=encoding,
        errors=errors,
        shell=False,
        close_fds=True,
        start_new_session=True,
    )

    stdout_value, stderr_value = _communicate_with_cleanup(
        process,
        input_value=input,
        timeout=parsed_timeout,
    )
    _require_empty_process_group(process)

    completed = subprocess.CompletedProcess(
        args,
        process.returncode,
        stdout_value,
        stderr_value,
    )
    if check:
        completed.check_returncode()
    return completed


__all__ = [
    "ProcessTreeCleanupError",
    "ProcessTreeError",
    "ProcessTreeLeak",
    "ProcessTreeUnsupported",
    "run_process_tree",
]
