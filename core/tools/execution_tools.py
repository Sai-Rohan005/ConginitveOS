# core/tools/execution_tools.py

"""
CognitiveOS - Execution Tools
---------------------------------------------------------

Responsibilities:
- execute python code
- execute projects
- validate runtime
- install dependencies
- capture stdout/stderr
- runtime sandboxing

Runtime execution intelligence layer.
"""

from __future__ import annotations

import subprocess
import traceback
import time

from pathlib import Path

from typing import (
    Dict,
    Any,
)

# ============================================================
# EXECUTION TOOLS
# ============================================================


class ExecutionTools:

    """
    Runtime execution utilities.
    """

    def __init__(
        self,
        workspace: Path,
    ):

        self.workspace = workspace

    # ========================================================
    # EXECUTE PYTHON
    # ========================================================

    async def execute_python(
        self,
        filename: str,
        timeout: int = 30,
    ) -> Dict[str, Any]:

        try:

            file_path = (
                self.workspace
                / filename
            )

            start = time.time()

            result = subprocess.run(

                [
                    "python",
                    str(file_path),
                ],

                capture_output=True,

                text=True,

                cwd=self.workspace,

                timeout=timeout,
            )

            duration = (
                time.time()
                - start
            )

            return {

                "success":
                    result.returncode == 0,

                "stdout":
                    result.stdout,

                "stderr":
                    result.stderr,

                "return_code":
                    result.returncode,

                "execution_time":
                    duration,
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),

                "traceback":
                    traceback.format_exc(),
            }

    # ========================================================
    # INSTALL REQUIREMENTS
    # ========================================================

    async def install_requirements(
        self,
        requirements_file: str = (
            "requirements.txt"
        ),
        timeout: int = 120,
    ) -> Dict[str, Any]:

        try:

            requirements_path = (
                self.workspace
                / requirements_file
            )

            if not requirements_path.exists():

                return {

                    "success": False,

                    "error":
                        "requirements.txt not found",
                }

            result = subprocess.run(

                [

                    "pip",

                    "install",

                    "-r",

                    str(requirements_path),
                ],

                capture_output=True,

                text=True,

                cwd=self.workspace,

                timeout=timeout,
            )

            return {

                "success":
                    result.returncode == 0,

                "stdout":
                    result.stdout,

                "stderr":
                    result.stderr,

                "return_code":
                    result.returncode,
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),
            }

    # ========================================================
    # RUN UVICORN
    # ========================================================

    async def run_uvicorn(
        self,
        app_path: str = (
            "app.main:app"
        ),
        timeout: int = 20,
    ) -> Dict[str, Any]:

        try:

            result = subprocess.run(

                [

                    "uvicorn",

                    app_path,

                    "--host",

                    "0.0.0.0",

                    "--port",

                    "8000",
                ],

                capture_output=True,

                text=True,

                cwd=self.workspace,

                timeout=timeout,
            )

            return {

                "success":
                    result.returncode == 0,

                "stdout":
                    result.stdout,

                "stderr":
                    result.stderr,
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),
            }