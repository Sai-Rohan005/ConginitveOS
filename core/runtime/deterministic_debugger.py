# domains/softwareEngineering/runtime/deterministic_debugger.py

from __future__ import annotations

import re
import subprocess

from pathlib import Path

from typing import (
    Dict,
    Any,
)


class DeterministicDebugger:

    """
    Deterministic runtime recovery engine.

    This runs BEFORE Gemini debugging.
    """

    def __init__(self):

        self.import_patterns = [

            r"No module named '(.*?)'",

            r'ModuleNotFoundError: No module named "(.*?)"',

            r"ModuleNotFoundError: No module named '(.*?)'",
        ]

    # ========================================================
    # MAIN DEBUG
    # ========================================================


    def validate_agent_output(self, output: dict) -> dict:
        return {
            "valid": isinstance(output, dict),
            "has_success_flag": "success" in output,
            "keys": list(output.keys()) if isinstance(output, dict) else [],
            "warnings": []
        }


    async def debug_runtime_failure(

        self,

        stderr: str,
    ) -> Dict[str, Any]:

        stderr = stderr or ""

        # ====================================================
        # IMPORT ERRORS
        # ====================================================

        missing_module = (
            self._extract_missing_module(
                stderr
            )
        )

        if missing_module:

            install_result = (
                self._install_dependency(
                    missing_module
                )
            )

            return {

                "resolved":
                    install_result,

                "strategy":
                    "auto_dependency_install",

                "module":
                    missing_module,
            }

        # ====================================================
        # ADDRESS ALREADY IN USE
        # ====================================================

        if (
            "Address already in use"
            in stderr
        ):

            return {

                "resolved":
                    True,

                "strategy":
                    "port_conflict_detected",

                "recommendation":
                    "Use different port",
            }

        # ====================================================
        # UVICORN FAILURE
        # ====================================================

        if (
            "uvicorn"
            in stderr.lower()
        ):

            return {

                "resolved":
                    False,

                "strategy":
                    "uvicorn_failure",

                "requires_patch_engine":
                    True,
            }

        # ====================================================
        # SYNTAX ERROR
        # ====================================================

        if "SyntaxError" in stderr:

            return {

                "resolved":
                    False,

                "strategy":
                    "syntax_error",

                "requires_patch_engine":
                    True,
            }

        # ====================================================
        # INDENTATION ERROR
        # ====================================================

        if "IndentationError" in stderr:

            return {

                "resolved":
                    False,

                "strategy":
                    "indentation_error",

                "requires_patch_engine":
                    True,
            }

        # ====================================================
        # JWT ISSUES
        # ====================================================

        if (
            "jwt"
            in stderr.lower()
        ):

            return {

                "resolved":
                    False,

                "strategy":
                    "jwt_runtime_issue",

                "requires_patch_engine":
                    True,
            }

        # ====================================================
        # FASTAPI APP FAILURE
        # ====================================================

        if (
            "FastAPI"
            in stderr
        ):

            return {

                "resolved":
                    False,

                "strategy":
                    "fastapi_runtime_issue",

                "requires_patch_engine":
                    True,
            }

        # ====================================================
        # FALLBACK
        # ====================================================

        return {

            "resolved":
                False,

            "strategy":
                "unknown_failure",

            "requires_llm":
                True,
        }

    # ========================================================
    # EXTRACT MODULE
    # ========================================================

    def _extract_missing_module(
        self,
        stderr: str,
    ):

        for pattern in (
            self.import_patterns
        ):

            match = re.search(
                pattern,
                stderr,
            )

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

                [

                    "pip",

                    "install",

                    package,
                ],

                check=True,

                capture_output=True,

                text=True,
            )

            return True

        except Exception:

            return False