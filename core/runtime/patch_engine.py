# domains/software_engineering/runtime/patch_engine.py

"""
CognitiveOS - Patch Engine
---------------------------------------------------------

Responsibilities:
- apply deterministic code patches
- repair runtime failures
- fix imports
- fix syntax issues
- patch environment issues
- auto-repair common backend failures

This removes unnecessary Gemini calls.

Architecture:

Runtime Failure
    ↓
PatchEngine
    ↓
Auto Repair
    ↓
Retry
    ↓
ONLY if unresolved:
    ↓
Gemini escalation
"""

from __future__ import annotations

import re

from pathlib import Path

from typing import (
    Dict,
    Any,
    Optional,
)


# ============================================================
# PATCH ENGINE
# ============================================================


class PatchEngine:

    """
    Deterministic runtime patching engine.
    """

    def __init__(self):

        # ====================================================
        # PATCH RULES
        # ====================================================

        self.patch_rules = {

            "jwt":
                self._patch_jwt_import,

            "fastapi":
                self._patch_fastapi_import,

            "uvicorn":
                self._patch_uvicorn_import,

            "pydantic":
                self._patch_pydantic_import,
        }

    # ========================================================
    # MAIN PATCH ENTRY
    # ========================================================

    async def patch_runtime_failure(

        self,

        file_path: str,

        stderr: str,
    ) -> Dict[str, Any]:

        try:

            stderr = stderr or ""

            # =================================================
            # MODULE NOT FOUND
            # =================================================

            if (

                "ModuleNotFoundError"
                in stderr

                or

                "No module named"
                in stderr
            ):

                return await (
                    self._patch_missing_import(
                        file_path,
                        stderr,
                    )
                )

            # =================================================
            # FASTAPI APP FIX
            # =================================================

            if (
                "app = FastAPI"
                in stderr
            ):

                return await (
                    self._ensure_fastapi_app(
                        file_path
                    )
                )

            # =================================================
            # UVICORN FIX
            # =================================================

            if (
                "uvicorn"
                in stderr.lower()
            ):

                return await (
                    self._patch_uvicorn_runner(
                        file_path
                    )
                )

            # =================================================
            # SYNTAX FIX
            # =================================================

            if (
                "SyntaxError"
                in stderr
            ):

                return await (
                    self._basic_syntax_repair(
                        file_path
                    )
                )

            # =================================================
            # FALLBACK
            # =================================================

            return {

                "success":
                    False,

                "patched":
                    False,

                "reason":
                    "No deterministic patch found",
            }

        except Exception as e:

            return {

                "success":
                    False,

                "patched":
                    False,

                "error":
                    str(e),
            }

    # ========================================================
    # PATCH MISSING IMPORT
    # ========================================================

    async def _patch_missing_import(

        self,

        file_path: str,

        stderr: str,
    ):

        missing_module = (
            self._extract_missing_module(
                stderr
            )
        )

        if not missing_module:

            return {

                "success":
                    False,

                "patched":
                    False,
            }

        patch_handler = (
            self.patch_rules.get(
                missing_module
            )
        )

        if not patch_handler:

            return {

                "success":
                    False,

                "patched":
                    False,

                "module":
                    missing_module,
            }

        return await patch_handler(
            file_path
        )

    # ========================================================
    # EXTRACT MODULE
    # ========================================================

    def _extract_missing_module(
        self,
        stderr: str,
    ) -> Optional[str]:

        patterns = [

            r"No module named '(.*?)'",

            r'ModuleNotFoundError: No module named "(.*?)"',

            r"ModuleNotFoundError: No module named '(.*?)'",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                stderr,
            )

            if match:

                module_name = (
                    match.group(1)
                )

                return (
                    module_name
                    .split(".")[0]
                )

        return None

    # ========================================================
    # READ FILE
    # ========================================================

    def _read_file(
        self,
        file_path: str,
    ) -> str:

        path = Path(file_path)

        if not path.exists():

            return ""

        return path.read_text(
            encoding="utf-8"
        )

    # ========================================================
    # WRITE FILE
    # ========================================================

    def _write_file(

        self,

        file_path: str,

        content: str,
    ):

        path = Path(file_path)

        path.parent.mkdir(

            parents=True,

            exist_ok=True,
        )

        path.write_text(

            content,

            encoding="utf-8",
        )

    # ========================================================
    # PATCH JWT
    # ========================================================

    async def _patch_jwt_import(
        self,
        file_path: str,
    ):

        content = self._read_file(
            file_path
        )

        if (
            "import jwt"
            not in content
        ):

            content = (
                "import jwt\n"
                + content
            )

        self._write_file(
            file_path,
            content,
        )

        return {

            "success":
                True,

            "patched":
                True,

            "strategy":
                "jwt_import_patch",
        }

    # ========================================================
    # PATCH FASTAPI
    # ========================================================

    async def _patch_fastapi_import(
        self,
        file_path: str,
    ):

        content = self._read_file(
            file_path
        )

        if (
            "from fastapi import FastAPI"
            not in content
        ):

            content = (
                "from fastapi import FastAPI\n"
                + content
            )

        self._write_file(
            file_path,
            content,
        )

        return {

            "success":
                True,

            "patched":
                True,

            "strategy":
                "fastapi_import_patch",
        }

    # ========================================================
    # PATCH UVICORN
    # ========================================================

    async def _patch_uvicorn_import(
        self,
        file_path: str,
    ):

        content = self._read_file(
            file_path
        )

        if (
            "import uvicorn"
            not in content
        ):

            content = (
                "import uvicorn\n"
                + content
            )

        self._write_file(
            file_path,
            content,
        )

        return {

            "success":
                True,

            "patched":
                True,

            "strategy":
                "uvicorn_import_patch",
        }

    # ========================================================
    # PATCH PYDANTIC
    # ========================================================

    async def _patch_pydantic_import(
        self,
        file_path: str,
    ):

        content = self._read_file(
            file_path
        )

        if (
            "from pydantic import BaseModel"
            not in content
        ):

            content = (
                "from pydantic import BaseModel\n"
                + content
            )

        self._write_file(
            file_path,
            content,
        )

        return {

            "success":
                True,

            "patched":
                True,

            "strategy":
                "pydantic_import_patch",
        }

    # ========================================================
    # ENSURE FASTAPI APP
    # ========================================================

    async def _ensure_fastapi_app(
        self,
        file_path: str,
    ):

        content = self._read_file(
            file_path
        )

        if (
            "app = FastAPI()"
            not in content
        ):

            if (
                "FastAPI"
                not in content
            ):

                content = (
                    "from fastapi import FastAPI\n\n"
                    + content
                )

            content += "\n\napp = FastAPI()\n"

        self._write_file(
            file_path,
            content,
        )

        return {

            "success":
                True,

            "patched":
                True,

            "strategy":
                "fastapi_app_patch",
        }

    # ========================================================
    # UVICORN RUNNER PATCH
    # ========================================================

    async def _patch_uvicorn_runner(
        self,
        file_path: str,
    ):

        content = self._read_file(
            file_path
        )

        if (
            'uvicorn.run('
            not in content
        ):

            runner = """

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
"""

            content += runner

        self._write_file(
            file_path,
            content,
        )

        return {

            "success":
                True,

            "patched":
                True,

            "strategy":
                "uvicorn_runner_patch",
        }

    # ========================================================
    # BASIC SYNTAX REPAIR
    # ========================================================

    async def _basic_syntax_repair(
        self,
        file_path: str,
    ):

        content = self._read_file(
            file_path
        )

        # ====================================================
        # REMOVE DOUBLE COMMAS
        # ====================================================

        content = re.sub(
            r",\s*,",
            ",",
            content,
        )

        # ====================================================
        # FIX DOUBLE COLONS
        # ====================================================

        content = re.sub(
            r"::",
            ":",
            content,
        )

        # ====================================================
        # FIX BAD INDENTATION
        # ====================================================

        lines = content.splitlines()

        cleaned_lines = []

        for line in lines:

            cleaned_lines.append(
                line.rstrip()
            )

        content = "\n".join(
            cleaned_lines
        )

        self._write_file(
            file_path,
            content,
        )

        return {

            "success":
                True,

            "patched":
                True,

            "strategy":
                "basic_syntax_repair",
        }