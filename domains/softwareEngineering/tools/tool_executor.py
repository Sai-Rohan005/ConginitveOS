# domains/software_engineering/tools/tool_executor.py

"""
CognitiveOS - Tool Executor
---------------------------------------------------------

Responsibilities:
- execute tools
- provide runtime capabilities
- execute python code
- manage filesystem operations
- run shell commands
- validate generated code
- provide external execution layer

This becomes the REAL capability layer
of CognitiveOS.

Without tools:
agents are just text generators.
"""

from __future__ import annotations

import os
import json
import uuid
import shutil
import traceback
import subprocess

from pathlib import Path

from typing import (
    Dict,
    Any,
    Optional,
)


# ============================================================
# TOOL EXECUTION RESULT
# ============================================================


class ToolExecutionResult:

    def __init__(
        self,
        success: bool,
        tool: str,
        output: Any = None,
        error: Optional[str] = None,
    ):

        self.success = success

        self.tool = tool

        self.output = output

        self.error = error

    def to_dict(self):

        return {

            "success":
                self.success,

            "tool":
                self.tool,

            "output":
                self.output,

            "error":
                self.error,
        }


# ============================================================
# TOOL EXECUTOR
# ============================================================


class ToolExecutor:

    """
    Runtime tool execution layer.
    """

    def __init__(self):

        # ====================================================
        # WORKSPACE
        # ====================================================

        self.workspace = Path(
            "workspace"
        )

        self.workspace.mkdir(
            exist_ok=True
        )

        # ====================================================
        # TOOL REGISTRY
        # ====================================================

        self.tool_registry = {

            "python":
                self.execute_python,

            "shell":
                self.execute_shell,

            "write_file":
                self.write_file,

            "read_file":
                self.read_file,

            "list_files":
                self.list_files,

            "create_directory":
                self.create_directory,

            "delete_path":
                self.delete_path,
        }

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:

        tool = self.tool_registry.get(
            tool_name
        )

        if not tool:

            return ToolExecutionResult(

                success=False,

                tool=tool_name,

                error=(
                    f"Unknown tool: "
                    f"{tool_name}"
                ),
            ).to_dict()

        try:

            result = await tool(
                **parameters
            )

            return result.to_dict()

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool=tool_name,

                error=str(e),
            ).to_dict()

    # ========================================================
    # PYTHON EXECUTION
    # ========================================================

    async def execute_python(
        self,
        code: str,
        timeout: int = 15,
    ) -> ToolExecutionResult:

        try:

            execution_id = str(
                uuid.uuid4()
            )

            file_path = (
                self.workspace
                / f"{execution_id}.py"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(code)

            result = subprocess.run(

                [
                    "python",
                    str(file_path),
                ],

                capture_output=True,

                text=True,

                timeout=timeout,
            )

            return ToolExecutionResult(

                success=(
                    result.returncode == 0
                ),

                tool="python",

                output={

                    "stdout":
                        result.stdout,

                    "stderr":
                        result.stderr,

                    "return_code":
                        result.returncode,
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="python",

                error=str(e),
            )

    # ========================================================
    # SHELL EXECUTION
    # ========================================================

    async def execute_shell(
        self,
        command: str,
        timeout: int = 15,
    ) -> ToolExecutionResult:

        try:

            result = subprocess.run(

                command,

                shell=True,

                capture_output=True,

                text=True,

                timeout=timeout,
            )

            return ToolExecutionResult(

                success=(
                    result.returncode == 0
                ),

                tool="shell",

                output={

                    "stdout":
                        result.stdout,

                    "stderr":
                        result.stderr,

                    "return_code":
                        result.returncode,
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="shell",

                error=str(e),
            )

    # ========================================================
    # WRITE FILE
    # ========================================================

    async def write_file(
        self,
        path: str,
        content: str,
    ) -> ToolExecutionResult:

        try:

            full_path = (
                self.workspace / path
            )

            full_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(
                full_path,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(content)

            return ToolExecutionResult(

                success=True,

                tool="write_file",

                output={

                    "path":
                        str(full_path),

                    "size":
                        len(content),
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="write_file",

                error=str(e),
            )

    # ========================================================
    # READ FILE
    # ========================================================

    async def read_file(
        self,
        path: str,
    ) -> ToolExecutionResult:

        try:

            full_path = (
                self.workspace / path
            )

            if not full_path.exists():

                return ToolExecutionResult(

                    success=False,

                    tool="read_file",

                    error=(
                        "File not found"
                    ),
                )

            with open(
                full_path,
                "r",
                encoding="utf-8",
            ) as f:

                content = f.read()

            return ToolExecutionResult(

                success=True,

                tool="read_file",

                output={

                    "path":
                        str(full_path),

                    "content":
                        content,
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="read_file",

                error=str(e),
            )

    # ========================================================
    # LIST FILES
    # ========================================================

    async def list_files(
        self,
        path: str = "",
    ) -> ToolExecutionResult:

        try:

            full_path = (
                self.workspace / path
            )

            if not full_path.exists():

                return ToolExecutionResult(

                    success=False,

                    tool="list_files",

                    error=(
                        "Directory not found"
                    ),
                )

            files = []

            for item in full_path.iterdir():

                files.append(

                    {

                        "name":
                            item.name,

                        "is_dir":
                            item.is_dir(),

                        "path":
                            str(item),
                    }
                )

            return ToolExecutionResult(

                success=True,

                tool="list_files",

                output=files,
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="list_files",

                error=str(e),
            )

    # ========================================================
    # CREATE DIRECTORY
    # ========================================================

    async def create_directory(
        self,
        path: str,
    ) -> ToolExecutionResult:

        try:

            full_path = (
                self.workspace / path
            )

            full_path.mkdir(

                parents=True,

                exist_ok=True,
            )

            return ToolExecutionResult(

                success=True,

                tool="create_directory",

                output={

                    "path":
                        str(full_path),
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="create_directory",

                error=str(e),
            )

    # ========================================================
    # DELETE PATH
    # ========================================================

    async def delete_path(
        self,
        path: str,
    ) -> ToolExecutionResult:

        try:

            full_path = (
                self.workspace / path
            )

            if not full_path.exists():

                return ToolExecutionResult(

                    success=False,

                    tool="delete_path",

                    error=(
                        "Path not found"
                    ),
                )

            if full_path.is_file():

                full_path.unlink()

            else:

                shutil.rmtree(
                    full_path
                )

            return ToolExecutionResult(

                success=True,

                tool="delete_path",

                output={

                    "deleted":
                        str(full_path),
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="delete_path",

                error=str(e),
            )

    # ========================================================
    # AVAILABLE TOOLS
    # ========================================================

    def available_tools(self):

        return list(
            self.tool_registry.keys()
        )