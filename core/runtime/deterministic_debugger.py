# domains/softwareEngineering/runtime/deterministic_debugger.py

from __future__ import annotations

import re
import subprocess

from typing import Dict, Any, Optional, Union


class DeterministicDebugger:
    """
    Deterministic runtime recovery engine.

    Runs BEFORE LLM-based debugging.
    Handles:
    - execution validation
    - runtime failure classification
    - dependency recovery
    """

    def __init__(self):

        self.import_patterns = [
            r"No module named '(.*?)'",
            r'ModuleNotFoundError: No module named "(.*?)"',
            r"ModuleNotFoundError: No module named '(.*?)'",
        ]

    # ========================================================
    # AGENT OUTPUT VALIDATION
    # ========================================================

    def validate_agent_output(
        self,
        output: dict,
    ) -> dict:

        return {
            "valid": isinstance(output, dict),
            "has_success_flag": isinstance(output, dict)
                and "success" in output,
            "keys": list(output.keys())
                if isinstance(output, dict)
                else [],
            "warnings": [],
        }

    # ========================================================
    # EXECUTION VALIDATION (FIXED + COMPATIBLE)
    # ========================================================

    def validate_execution(
        self,
        outputs: Optional[Union[dict, list]] = None,
        execution_results: Optional[Union[dict, list]] = None,
        **kwargs,
    ) -> dict:
        """
        FIXED:
        - supports outputs= (used by workflow_executor)
        - supports execution_results= (legacy usage)
        - supports future keyword arguments safely
        """

        data = (
            outputs
            if outputs is not None
            else execution_results
        )

        if data is None:

            return {
                "valid": False,
                "steps_executed": 0,
                "validation_errors": [
                    "No execution data provided"
                ],
                "received_kwargs": list(kwargs.keys()),
            }

        validation_errors = []

        # ----------------------------------------------------
        # TYPE SAFETY
        # ----------------------------------------------------

        if not isinstance(data, (dict, list)):

            validation_errors.append(
                "Execution data must be dict or list"
            )

        # ----------------------------------------------------
        # STEP COUNTING
        # ----------------------------------------------------

        try:
            steps_executed = len(data)
        except Exception:
            steps_executed = 1

        # ----------------------------------------------------
        # DETECT FAILED STEPS (IF STRUCTURED)
        # ----------------------------------------------------

        failed_steps = []

        if isinstance(data, dict):

            for key, value in data.items():

                if (
                    isinstance(value, dict)
                    and value.get("success") is False
                ):
                    failed_steps.append(key)

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        return {
            "valid": len(validation_errors) == 0
                and len(failed_steps) == 0,

            "steps_executed": steps_executed,

            "failed_steps": failed_steps,

            "validation_errors": validation_errors,

            "received_kwargs": list(kwargs.keys()),
        }

    # ========================================================
    # RUNTIME FAILURE DEBUGGER
    # ========================================================

    async def debug_runtime_failure(
        self,
        stderr: str,
    ) -> Dict[str, Any]:

        stderr = stderr or ""

        # ----------------------------------------------------
        # IMPORT ERRORS
        # ----------------------------------------------------

        missing_module = self._extract_missing_module(stderr)

        if missing_module:

            install_result = self._install_dependency(
                missing_module
            )

            return {
                "resolved": install_result,
                "strategy": "auto_dependency_install",
                "module": missing_module,
            }

        # ----------------------------------------------------
        # PORT IN USE
        # ----------------------------------------------------

        if "Address already in use" in stderr:

            return {
                "resolved": True,
                "strategy": "port_conflict_detected",
                "recommendation": "Use different port",
            }

        # ----------------------------------------------------
        # UVICORN ERROR
        # ----------------------------------------------------

        if "uvicorn" in stderr.lower():

            return {
                "resolved": False,
                "strategy": "uvicorn_failure",
                "requires_patch_engine": True,
            }

        # ----------------------------------------------------
        # SYNTAX ERROR
        # ----------------------------------------------------

        if "SyntaxError" in stderr:

            return {
                "resolved": False,
                "strategy": "syntax_error",
                "requires_patch_engine": True,
            }

        # ----------------------------------------------------
        # INDENTATION ERROR
        # ----------------------------------------------------

        if "IndentationError" in stderr:

            return {
                "resolved": False,
                "strategy": "indentation_error",
                "requires_patch_engine": True,
            }

        # ----------------------------------------------------
        # JWT ERROR
        # ----------------------------------------------------

        if "jwt" in stderr.lower():

            return {
                "resolved": False,
                "strategy": "jwt_runtime_issue",
                "requires_patch_engine": True,
            }

        # ----------------------------------------------------
        # FASTAPI ERROR
        # ----------------------------------------------------

        if "fastapi" in stderr.lower():

            return {
                "resolved": False,
                "strategy": "fastapi_runtime_issue",
                "requires_patch_engine": True,
            }

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        return {
            "resolved": False,
            "strategy": "unknown_failure",
            "requires_llm": True,
        }

    # ========================================================
    # MODULE EXTRACTION
    # ========================================================

    def _extract_missing_module(
        self,
        stderr: str,
    ) -> Optional[str]:

        for pattern in self.import_patterns:

            match = re.search(pattern, stderr)

            if match:

                module = match.group(1)

                return module.split(".")[0]

        return None

    # ========================================================
    # INSTALL DEPENDENCY
    # ========================================================

    def _install_dependency(
        self,
        package: str,
    ) -> bool:

        try:

            subprocess.run(
                ["pip", "install", package],
                check=True,
                capture_output=True,
                text=True,
            )

            return True

        except Exception:

            return False