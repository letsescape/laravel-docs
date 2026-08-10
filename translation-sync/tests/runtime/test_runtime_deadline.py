"""공통 워크플로 기한과 하위 시간 예산 계약 검증."""

import math
import unittest

from sync.runtime.deadline import DeadlineExceeded, WorkflowDeadline
from sync.runtime.failure import IssueCode


class _Clock:
    """테스트에서 단조 시계 진행을 직접 제어하는 가짜 시계.

    Attributes:
        now: 현재 시각으로 반환할 초 단위 값.
    """

    def __init__(self, now: float = 100.0) -> None:
        """가짜 단조 시계 생성.

        Args:
            now: 초기 현재 시각으로 사용할 초 단위 값.
        """

        self.now = now

    def __call__(self) -> float:
        """현재 가짜 단조 시계 값 반환."""

        return self.now


class WorkflowDeadlineTests(unittest.TestCase):
    """워크플로 전체와 하위 단계가 공유하는 기한 계약 검증."""

    def test_start_uses_one_absolute_monotonic_deadline(self) -> None:
        """워크플로 전체에서 하나의 절대 단조 시계 종료 시각을 유지하는지 검증."""

        clock = _Clock()
        deadline = WorkflowDeadline.start(60, clock=clock)

        self.assertEqual(deadline.expires_at, 160.0)
        self.assertEqual(deadline.remaining_seconds(), 60.0)

        clock.now = 115.5
        self.assertEqual(deadline.phase_remaining(), 44.5)
        self.assertEqual(deadline.expires_at, 160.0)

    def test_child_timeout_never_exceeds_the_remaining_common_budget(self) -> None:
        """하위 작업 제한 시간이 공통 잔여 예산을 넘지 않는지 검증."""

        clock = _Clock()
        deadline = WorkflowDeadline.start(30, clock=clock)

        self.assertEqual(deadline.child_timeout(100), 30.0)
        self.assertEqual(deadline.child_timeout(12), 12.0)
        self.assertEqual(deadline.child_timeout(), 30.0)

        clock.now = 125.0
        self.assertEqual(deadline.child_timeout(12), 5.0)

    def test_capped_deadline_uses_the_earlier_run_and_workflow_limit(self) -> None:
        """실행 제한과 상위 기한 중 이른 값을 실행별 기한으로 사용하는지 검증."""

        clock = _Clock()
        workflow = WorkflowDeadline.start(100, clock=clock)
        clock.now = 110.0

        translation_run = workflow.cap_from_now(
            30,
            exceeded_code=IssueCode.RUN_DEADLINE_EXCEEDED,
        )

        self.assertEqual(translation_run.expires_at, 140.0)
        self.assertEqual(translation_run.remaining_seconds(), 30.0)
        self.assertEqual(workflow.expires_at, 200.0)

        later_workflow = WorkflowDeadline.start(10, clock=clock)
        capped = later_workflow.cap_from_now(
            30,
            exceeded_code=IssueCode.RUN_DEADLINE_EXCEEDED,
        )
        self.assertEqual(capped.expires_at, 120.0)

    def test_provider_retry_requires_wait_and_full_request_timeout_to_fit(self) -> None:
        """재시도 대기와 전체 요청 제한 시간이 잔여 예산에 들어가는지 검증."""

        clock = _Clock()
        deadline = WorkflowDeadline.start(40, clock=clock).cap_from_now(
            35,
            exceeded_code=IssueCode.RUN_DEADLINE_EXCEEDED,
        )

        budget = deadline.provider_retry_budget(
            request_timeout_seconds=20,
            retry_delay_seconds=5,
        )

        self.assertEqual(budget.retry_delay_seconds, 5.0)
        self.assertEqual(budget.request_timeout_seconds, 20.0)
        self.assertEqual(budget.remaining_after_retry_seconds, 30.0)

        clock.now = 111.0
        with self.assertRaises(DeadlineExceeded) as caught:
            deadline.provider_retry_budget(
                request_timeout_seconds=20,
                retry_delay_seconds=5,
            )

        self.assertEqual(caught.exception.code, IssueCode.RUN_DEADLINE_EXCEEDED)

    def test_expired_deadline_rejects_new_phase_and_child(self) -> None:
        """만료된 기한에서 새 단계와 하위 작업 시작 거부."""

        clock = _Clock()
        deadline = WorkflowDeadline.start(10, clock=clock)
        clock.now = 110.0

        for action in (deadline.phase_remaining, deadline.child_timeout):
            with self.subTest(action=action.__name__):
                with self.assertRaises(DeadlineExceeded) as caught:
                    action()
                self.assertEqual(
                    caught.exception.code,
                    IssueCode.WORKFLOW_DEADLINE_EXCEEDED,
                )

        self.assertEqual(deadline.remaining_seconds(), 0.0)

    def test_invalid_durations_are_rejected_before_a_deadline_is_created(self) -> None:
        """기한 생성 전 유효하지 않은 기간 거부."""

        clock = _Clock()
        for value in (0, -1, math.inf, math.nan, True, "10"):
            with self.subTest(value=value):
                with self.assertRaises((TypeError, ValueError)):
                    WorkflowDeadline.start(value, clock=clock)  # type: ignore[arg-type]

        deadline = WorkflowDeadline.start(10, clock=clock)
        for value in (0, -1, math.inf, math.nan, True, "10"):
            with self.subTest(child_timeout=value):
                with self.assertRaises((TypeError, ValueError)):
                    deadline.child_timeout(value)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
