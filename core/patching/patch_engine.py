"""
CognitiveOS - Runtime Patch Engine
----------------------------------

Responsibilities:
- analyze runtime errors
- auto repair common failures
- patch broken imports
- patch syntax issues
- patch indentation issues
- patch missing variables
"""

from __future__ import annotations

import re
import traceback


class PatchEngine:

    """
    Lightweight autonomous runtime patch engine.
    """

    def __init__(self):

        self.supported_errors = [

            "ModuleNotFoundError",

            "NameError",

            "SyntaxError",

            "IndentationError",

            "AttributeError",
        ]

    # ========================================================
    # MAIN PATCHER
    # ========================================================

    def patch_runtime_error(
        self,
        original_code: str,
        runtime_error: str,
    ) -> str:

        """
        Detect runtime failure
        and attempt automatic repair.
        """

        try:

            # =================================================
            # MODULE NOT FOUND
            # =================================================

            if (
                "ModuleNotFoundError"
                in runtime_error
            ):

                return self._patch_missing_module(
                    original_code,
                    runtime_error,
                )

            # =================================================
            # NAME ERROR
            # =================================================

            if (
                "NameError"
                in runtime_error
            ):

                return self._patch_name_error(
                    original_code,
                    runtime_error,
                )

            # =================================================
            # INDENTATION ERROR
            # =================================================

            if (
                "IndentationError"
                in runtime_error
            ):

                return self._patch_indentation(
                    original_code
                )

            # =================================================
            # SYNTAX ERROR
            # =================================================

            if (
                "SyntaxError"
                in runtime_error
            ):

                return self._patch_syntax_error(
                    original_code
                )

            # =================================================
            # ATTRIBUTE ERROR
            # =================================================

            if (
                "AttributeError"
                in runtime_error
            ):

                return self._patch_attribute_error(
                    original_code,
                    runtime_error,
                )

            return original_code

        except Exception:

            traceback.print_exc()

            return original_code

    # ========================================================
    # MODULE PATCH
    # ========================================================

    def _patch_missing_module(
        self,
        code: str,
        error: str,
    ) -> str:

        """
        Remove failing imports if missing.
        """

        match = re.search(

            r"No module named ['\"](.+?)['\"]",

            error,
        )

        if not match:

            return code

        missing_module = match.group(1)

        patched_lines = []

        for line in code.splitlines():

            if (
                missing_module in line
                and (
                    line.strip().startswith(
                        "import"
                    )
                    or line.strip().startswith(
                        "from"
                    )
                )
            ):

                continue

            patched_lines.append(line)

        return "\n".join(
            patched_lines
        )

    # ========================================================
    # NAME ERROR PATCH
    # ========================================================

    def _patch_name_error(
        self,
        code: str,
        error: str,
    ) -> str:

        """
        Create placeholder variable.
        """

        match = re.search(

            r"name ['\"](.+?)['\"] is not defined",

            error,
        )

        if not match:

            return code

        variable = match.group(1)

        placeholder = (
            f"\n{variable} = None\n"
        )

        return placeholder + code

    # ========================================================
    # INDENTATION PATCH
    # ========================================================

    def _patch_indentation(
        self,
        code: str,
    ) -> str:

        """
        Normalize tabs/spaces.
        """

        return code.replace(
            "\t",
            "    ",
        )

    # ========================================================
    # SYNTAX PATCH
    # ========================================================

    def _patch_syntax_error(
        self,
        code: str,
    ) -> str:

        """
        Very lightweight syntax cleanup.
        """

        fixed_lines = []

        for line in code.splitlines():

            stripped = line.rstrip()

            fixed_lines.append(
                stripped
            )

        return "\n".join(
            fixed_lines
        )

    # ========================================================
    # ATTRIBUTE PATCH
    # ========================================================

    def _patch_attribute_error(
        self,
        code: str,
        error: str,
    ) -> str:

        """
        Placeholder attribute repair.
        """

        return code

    # ========================================================
    # HEALTH
    # ========================================================

    def health_check(self):

        return {

            "status": "healthy",

            "supported_errors":
                self.supported_errors,
        }