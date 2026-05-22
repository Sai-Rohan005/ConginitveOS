# domains/softwareEngineering/runtime/retry_policy.py

from __future__ import annotations

from typing import Dict


class RetryPolicy:

    """
    Intelligent retry policy system.

    Responsibilities:
    - classify runtime failures
    - decide retry eligibility
    - determine retry strategy
    - prevent infinite retry loops
    """

    def __init__(self):

        self.max_retries = 3

        # =====================================================
        # NON-RETRYABLE ERRORS
        # =====================================================

        self.non_retryable_errors = [

            "ModuleNotFoundError",
            "ImportError",
            "SyntaxError",
            "IndentationError",
            "NameError",
            "AttributeError",
            "TypeError",
        ]

        # =====================================================
        # RETRYABLE ERRORS
        # =====================================================

        self.retryable_errors = [

            "TimeoutError",
            "ConnectionError",
            "ConnectionRefusedError",
            "Temporary failure",
            "Rate limit",
            "429",
            "500",
            "502",
            "503",
            "504",
        ]

    # =========================================================
    # SHOULD RETRY
    # =========================================================

    def should_retry(
        self,
        stderr: str,
        retry_count: int,
    ) -> bool:

        if retry_count >= self.max_retries:

            print(
                "\nMAX RETRIES REACHED"
            )

            return False

        stderr_lower = stderr.lower()

        # =====================================================
        # NON-RETRYABLE
        # =====================================================

        for error in self.non_retryable_errors:

            if error.lower() in stderr_lower:

                print(
                    f"\nNON-RETRYABLE ERROR DETECTED: {error}"
                )

                return False

        # =====================================================
        # RETRYABLE
        # =====================================================

        for error in self.retryable_errors:

            if error.lower() in stderr_lower:

                print(
                    f"\nRETRYABLE ERROR DETECTED: {error}"
                )

                return True

        # =====================================================
        # UNKNOWN ERRORS
        # =====================================================

        # Default strategy:
        # allow one retry for unknown failures

        if retry_count < 1:

            print(
                "\nUNKNOWN ERROR — ALLOWING SAFE RETRY"
            )

            return True

        return False

    # =========================================================
    # RETRY STRATEGY
    # =========================================================

    def get_retry_strategy(
        self,
        stderr: str,
    ) -> Dict:

        stderr_lower = stderr.lower()

        # =====================================================
        # NETWORK FAILURES
        # =====================================================

        if any(

            keyword.lower() in stderr_lower

            for keyword in [

                "connection",
                "timeout",
                "rate limit",
                "429",
            ]
        ):

            return {

                "strategy":
                    "exponential_backoff",

                "delay_seconds":
                    5,

                "max_attempts":
                    3,
            }

        # =====================================================
        # SERVER FAILURES
        # =====================================================

        if any(

            keyword in stderr_lower

            for keyword in [

                "500",
                "502",
                "503",
                "504",
            ]
        ):

            return {

                "strategy":
                    "fixed_delay",

                "delay_seconds":
                    3,

                "max_attempts":
                    2,
            }

        # =====================================================
        # DEFAULT
        # =====================================================

        return {

            "strategy":
                "single_retry",

            "delay_seconds":
                1,

            "max_attempts":
                1,
        }