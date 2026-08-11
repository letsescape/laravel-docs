"""워크플로 단계와 하위 작업의 공통 실행 기한 관리.

단조시계 기반의 절대 종료 시각을 공유하여 단계와 하위 작업의 timeout을 제한.
"""

from __future__ import annotations

import math
import time
from collections.abc import Callable
from dataclasses import dataclass, field

from .failure import IssueCode


Clock = Callable[[], float]
_DEADLINE_CODES = frozenset(
    {
        IssueCode.RUN_DEADLINE_EXCEEDED,
        IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
    }
)


class DeadlineExceeded(RuntimeError):
    """안정된 오류 코드를 포함한 공통 실행 기한 초과 오류.

    Attributes:
        code: 초과한 기한을 식별하는 오류 코드.
    """

    def __init__(self, code: IssueCode) -> None:
        """기한 초과 오류 생성.

        Args:
            code: 초과한 기한을 식별하는 오류 코드.
        """

        self.code = code
        super().__init__(code.value)


def _positive_duration(value: float | int, *, name: str) -> float:
    """값을 유한한 양의 초 단위 기간으로 변환.

    Args:
        value: 검증할 초 단위 기간.
        name: 오류 메시지에 사용할 필드명.

    Returns:
        검증을 마친 실수형 기간.

    Raises:
        TypeError: 숫자가 아닌 값 입력.
        ValueError: 유한한 양수가 아닌 값 입력.
    """

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number")
    parsed = float(value)
    if not math.isfinite(parsed) or parsed <= 0:
        raise ValueError(f"{name} must be a positive finite number")
    return parsed


def _non_negative_duration(value: float | int, *, name: str) -> float:
    """값을 유한한 0 이상의 초 단위 기간으로 변환.

    Args:
        value: 검증할 초 단위 기간.
        name: 오류 메시지에 사용할 필드명.

    Returns:
        검증을 마친 실수형 기간.

    Raises:
        TypeError: 숫자가 아닌 값 입력.
        ValueError: 유한한 0 이상의 수가 아닌 값 입력.
    """

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number")
    parsed = float(value)
    if not math.isfinite(parsed) or parsed < 0:
        raise ValueError(f"{name} must be a non-negative finite number")
    return parsed


@dataclass(frozen=True, slots=True)
class ProviderRetryBudget:
    """재시도 대기와 후속 요청에 사용할 수 있는 시간 예산.

    Attributes:
        retry_delay_seconds: 후속 요청 전 재시도 대기 시간.
        request_timeout_seconds: 후속 요청에 적용할 timeout.
        remaining_after_retry_seconds: 재시도 대기 후 남은 공통 시간.
    """

    retry_delay_seconds: float
    request_timeout_seconds: float
    remaining_after_retry_seconds: float


@dataclass(frozen=True, slots=True)
class WorkflowDeadline:
    """모든 단계가 공유하는 절대 종료 시각과 오류 의미.

    Attributes:
        expires_at: 단조시계 기준 절대 종료 시각.
        exceeded_code: 기한 초과 시 사용할 오류 코드.
    """

    expires_at: float
    exceeded_code: IssueCode = IssueCode.WORKFLOW_DEADLINE_EXCEEDED
    _clock: Clock = field(default=time.monotonic, repr=False, compare=False)

    def __post_init__(self) -> None:
        """종료 시각과 초과 오류 코드의 유효성 검증.

        Raises:
            ValueError: 종료 시각이 유한하지 않거나 기한 오류 코드가 아닌 경우.
        """

        if not math.isfinite(self.expires_at):
            raise ValueError("expires_at must be finite")
        code = (
            self.exceeded_code
            if isinstance(self.exceeded_code, IssueCode)
            else IssueCode(self.exceeded_code)
        )
        if code not in _DEADLINE_CODES:
            raise ValueError("exceeded_code must be a deadline issue code")
        object.__setattr__(self, "exceeded_code", code)

    @classmethod
    def start(
        cls,
        timeout_seconds: float | int,
        *,
        clock: Clock = time.monotonic,
    ) -> WorkflowDeadline:
        """현재 단조시계 시각 기준의 새 공통 기한 생성.

        Args:
            timeout_seconds: 현재 시각부터 종료까지 허용할 시간.
            clock: 현재 시각을 초 단위로 제공하는 단조시계.

        Returns:
            워크플로 전체에서 공유할 실행 기한.

        Raises:
            TypeError: timeout이 숫자가 아닌 경우.
            ValueError: timeout이 유한한 양수가 아닌 경우.
        """

        timeout = _positive_duration(timeout_seconds, name="timeout_seconds")
        return cls(expires_at=clock() + timeout, _clock=clock)

    def cap_from_now(
        self,
        timeout_seconds: float | int,
        *,
        exceeded_code: IssueCode,
    ) -> WorkflowDeadline:
        """요청한 제한과 상위 기한 중 이른 시각을 사용하는 하위 기한 생성.

        Args:
            timeout_seconds: 현재 시각부터 하위 작업에 허용할 시간.
            exceeded_code: 하위 기한 초과 시 사용할 오류 코드.

        Returns:
            상위 기한을 초과하지 않는 하위 작업 기한.

        Raises:
            TypeError: timeout이 숫자가 아닌 경우.
            ValueError: timeout 또는 오류 코드가 유효하지 않은 경우.
        """

        timeout = _positive_duration(timeout_seconds, name="timeout_seconds")
        return WorkflowDeadline(
            expires_at=min(self.expires_at, self._clock() + timeout),
            exceeded_code=exceeded_code,
            _clock=self._clock,
        )

    def remaining_seconds(self) -> float:
        """0 이상으로 제한한 기한의 잔여 시간."""

        return max(0.0, self.expires_at - self._clock())

    def phase_remaining(self) -> float:
        """새 단계 시작에 사용할 잔여 시간 확인.

        Returns:
            기한까지 남은 양의 시간.

        Raises:
            DeadlineExceeded: 공통 실행 기한이 만료된 경우.
        """

        remaining = self.expires_at - self._clock()
        if remaining <= 0:
            raise DeadlineExceeded(self.exceeded_code)
        return remaining

    def child_timeout(
        self,
        requested_seconds: float | int | None = None,
    ) -> float:
        """하위 작업 timeout을 공통 잔여 시간 이내로 제한.

        Args:
            requested_seconds: 하위 작업에 요청한 timeout. None일 때 전체 잔여 시간.

        Returns:
            요청값과 공통 잔여 시간 중 작은 timeout.

        Raises:
            DeadlineExceeded: 공통 실행 기한이 만료된 경우.
            TypeError: 요청한 timeout이 숫자가 아닌 경우.
            ValueError: 요청한 timeout이 유한한 양수가 아닌 경우.
        """

        remaining = self.phase_remaining()
        if requested_seconds is None:
            return remaining
        requested = _positive_duration(
            requested_seconds,
            name="requested_seconds",
        )
        return min(requested, remaining)

    def provider_retry_budget(
        self,
        *,
        request_timeout_seconds: float | int,
        retry_delay_seconds: float | int = 0,
    ) -> ProviderRetryBudget:
        """재시도 대기와 한 번의 전체 요청을 위한 시간 예산 계산.

        Args:
            request_timeout_seconds: 후속 요청 전체에 필요한 timeout.
            retry_delay_seconds: 후속 요청 전에 기다릴 시간.

        Returns:
            검증을 마친 재시도 대기와 요청 시간 예산.

        Raises:
            DeadlineExceeded: 대기와 전체 요청이 잔여 시간에 들어가지 않는 경우.
            TypeError: timeout 또는 대기 시간이 숫자가 아닌 경우.
            ValueError: timeout 또는 대기 시간이 허용 범위를 벗어난 경우.
        """

        request_timeout = _positive_duration(
            request_timeout_seconds,
            name="request_timeout_seconds",
        )
        retry_delay = _non_negative_duration(
            retry_delay_seconds,
            name="retry_delay_seconds",
        )
        remaining = self.phase_remaining()
        if retry_delay + request_timeout > remaining:
            raise DeadlineExceeded(self.exceeded_code)
        return ProviderRetryBudget(
            retry_delay_seconds=retry_delay,
            request_timeout_seconds=request_timeout,
            remaining_after_retry_seconds=remaining - retry_delay,
        )
