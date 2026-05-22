# domains/softwareEngineering/runtime/runtime_validator.py

from __future__ import annotations

import ast
import py_compile
import traceback
import subprocess

from pathlib import Path
from typing import Dict, Any


class RuntimeValidator:

    """
    Runtime validation engine.

    Responsibilities:
    - syntax validation
    - AST validation
    - import validation
    - execution validation
    - deterministic diagnostics
    """

    async def validate_python_file(
        self,
        file_path: str,
    ) -> Dict[str, Any]:

        result = {
            "success": True,
            "file_path": file_path,
            "validation_steps": [],
            "error": "",
            "traceback": "",
        }

        try:

            path = Path(file_path)

            # =================================================
            # FILE EXISTS
            # =================================================

            if not path.exists():

                result["success"] = False

                result["error"] = (
                    f"File does not exist: {file_path}"
                )

                return result

            # =================================================
            # READ SOURCE
            # =================================================

            source = path.read_text(
                encoding="utf-8"
            )

            # =================================================
            # EMPTY FILE CHECK
            # =================================================

            if not source.strip():

                result["success"] = False

                result["error"] = (
                    "Python file is empty"
                )

                return result

            # =================================================
            # AST VALIDATION
            # =================================================

            try:

                ast.parse(source)

                result["validation_steps"].append(
                    "ast_parse_success"
                )

            except SyntaxError as e:

                result["success"] = False

                result["error"] = (
                    f"SyntaxError: {str(e)}"
                )

                result["traceback"] = (
                    traceback.format_exc()
                )

                return result

            # =================================================
            # BYTECODE COMPILATION
            # =================================================

            try:

                py_compile.compile(
                    file_path,
                    doraise=True,
                )

                result["validation_steps"].append(
                    "bytecode_compile_success"
                )

            except py_compile.PyCompileError as e:

                result["success"] = False

                result["error"] = str(e)

                result["traceback"] = (
                    traceback.format_exc()
                )

                return result

            # =================================================
            # IMPORT VALIDATION
            # =================================================

            try:

                compile(
                    source,
                    file_path,
                    "exec",
                )

                result["validation_steps"].append(
                    "compile_success"
                )

            except Exception as e:

                result["success"] = False

                result["error"] = str(e)

                result["traceback"] = (
                    traceback.format_exc()
                )

                return result

            # =================================================
            # OPTIONAL SAFE EXECUTION
            # =================================================

            execution_result = await self._safe_execute(
                file_path
            )

            result["execution_validation"] = (
                execution_result
            )

            if not execution_result.get(
                "success"
            ):

                result["success"] = False

                result["error"] = (
                    execution_result.get(
                        "stderr",
                        ""
                    )
                )

                return result

            # =================================================
            # SUCCESS
            # =================================================

            result["validation_steps"].append(
                "runtime_execution_success"
            )

            return result

        except Exception as e:

            result["success"] = False

            result["error"] = str(e)

            result["traceback"] = (
                traceback.format_exc()
            )

            return result

    # =========================================================
    # SAFE EXECUTION
    # =========================================================

    async def _safe_execute(
        self,
        file_path: str,
    ) -> Dict[str, Any]:

        try:

            process = subprocess.run(

                [
                    "python",
                    file_path,
                ],

                capture_output=True,

                text=True,

                timeout=15,
            )

            return {

                "success":
                    process.returncode == 0,

                "stdout":
                    process.stdout,

                "stderr":
                    process.stderr,

                "return_code":
                    process.returncode,
            }

        except subprocess.TimeoutExpired:

            return {

                "success": False,

                "stderr":
                    "Execution timed out",

                "return_code": -1,
            }

        except Exception as e:

            return {

                "success": False,

                "stderr": str(e),

                "return_code": -1,
            }