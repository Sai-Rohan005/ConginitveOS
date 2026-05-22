# core/orchestration/retry_engine.py

"""
CognitiveOS - Retry Engine
---------------------------------------------------------

Responsibilities:
- manage retry loops
- adaptive retry execution
- retry reasoning
- retry prioritization
- failure recovery
- retry state tracking
- autonomous execution repair

This becomes the adaptive
self-healing retry layer.
"""

from __future__ import annotations

from typing import (
    Dict,
    Any,
    List,
)

from dataclasses import (
    dataclass,
    field,
)

# ============================================================
# RETRY RESULT
# ============================================================


@dataclass
class RetryResult:

    retry_required: bool

    retry_steps: List[
        Dict[str, Any]
    ] = field(default_factory=list)

    retry_strategy: str = ""

    max_retries_reached: bool = False

    reasoning: str = ""

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# RETRY ENGINE
# ============================================================


class RetryEngine:

    """
    Deterministic retry orchestration engine.
    """

    def __init__(self):

        self.max_retry_attempts = 3

    # ========================================================
    # MAIN RETRY ANALYSIS
    # ========================================================

    def analyze_retry(
        self,
        failed_steps: List[
            Dict[str, Any]
        ],
        retry_count: int,
    ) -> RetryResult:

        if retry_count >= (
            self.max_retry_attempts
        ):

            return RetryResult(

                retry_required=False,

                max_retries_reached=True,

                retry_strategy=
                    "retry_limit_reached",

                reasoning=(
                    "Maximum retry attempts reached."
                ),
            )

        retry_steps = []

        for failed_step in failed_steps:

            retry_steps.append(

                {

                    "step_id":
                        failed_step.get(
                            "step_id"
                        ),

                    "agent":
                        failed_step.get(
                            "agent"
                        ),

                    "improvement_action":
                        self._determine_fix(
                            failed_step
                        ),
                }
            )

        strategy = (
            self._determine_strategy(
                retry_steps
            )
        )

        return RetryResult(

            retry_required=
                len(retry_steps) > 0,

            retry_steps=
                retry_steps,

            retry_strategy=
                strategy,

            reasoning=(
                f"{len(retry_steps)} "
                f"steps require retry."
            ),

            metadata={

                "retry_count":
                    retry_count,
            },
        )

    # ========================================================
    # DETERMINE FIX
    # ========================================================

    def _determine_fix(
        self,
        failed_step: Dict[
            str,
            Any,
        ],
    ) -> str:

        error = str(

            failed_step.get(
                "error",
                ""
            )
        ).lower()

        if (
            "modulenotfounderror"
            in error
        ):

            return (
                "install_missing_dependencies"
            )

        if (
            "syntaxerror"
            in error
        ):

            return (
                "patch_syntax_errors"
            )

        if (
            "attributeerror"
            in error
        ):

            return (
                "patch_attribute_usage"
            )

        if (
            "connection"
            in error
        ):

            return (
                "repair_network_logic"
            )

        return (
            "generic_runtime_repair"
        )

    # ========================================================
    # RETRY STRATEGY
    # ========================================================

    def _determine_strategy(
        self,
        retry_steps,
    ) -> str:

        if len(retry_steps) == 1:

            return (
                "targeted_retry"
            )

        return (
            "multi_step_recovery"
        )