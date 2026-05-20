# domains/softwareEngineering/tools/tool_executor.py

"""
CognitiveOS - Advanced Tool Executor
---------------------------------------------------------

Responsibilities:
- execute tools
- manage persistent workspace
- execute projects
- install dependencies
- patch files
- validate runtime execution
- manage autonomous runtime cognition
"""

from __future__ import annotations

import os
import time
import shutil
import traceback
import subprocess

from pathlib import Path

from typing import (
    Dict,
    Any,
    Optional,
    List,
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

        execution_time: Optional[
            float
        ] = None,

        artifacts: Optional[
            List
        ] = None,
    ):

        self.success = success

        self.tool = tool

        self.output = output

        self.error = error

        self.execution_time = (
            execution_time
        )

        self.artifacts = (
            artifacts or []
        )

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

            "execution_time":
                self.execution_time,

            "artifacts":
                self.artifacts,
        }


# ============================================================
# TOOL EXECUTOR
# ============================================================


class ToolExecutor:

    """
    Runtime execution engine.
    """

    def __init__(self):

        # ====================================================
        # ROOT WORKSPACE
        # ====================================================

        self.workspace = Path(
            "workspace"
        )

        self.workspace.mkdir(
            exist_ok=True
        )

        # ====================================================
        # PERSISTENT PROJECT WORKSPACE
        # ====================================================

        self.project_workspace = (

            self.workspace

            / "current_project"
        )

        self.project_workspace.mkdir(

            parents=True,

            exist_ok=True,
        )

        # ====================================================
        # BLOCKED COMMANDS
        # ====================================================

        self.blocked_commands = [

            "rm -rf /",

            "shutdown",

            "reboot",

            "mkfs",

            ":(){ :|:& };:",
        ]

        # ====================================================
        # TOOL REGISTRY
        # ====================================================

        self.tool_registry = {

            # Runtime
            "python":
                self.execute_python,

            "shell":
                self.execute_shell,

            "run_project":
                self.run_project,

            # Filesystem
            "write_file":
                self.write_file,

            "read_file":
                self.read_file,

            "patch_file":
                self.patch_file,

            "list_files":
                self.list_files,

            "tree":
                self.workspace_tree,

            "create_directory":
                self.create_directory,

            "delete_path":
                self.delete_path,

            # Environment
            "pip_install":
                self.install_dependencies,

            # Utility
            "reset_workspace":
                self.reset_workspace,
        }

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:

        print(
            "\n"
            + "=" * 80
        )

        print(
            f"[TOOL EXECUTION] {tool_name}"
        )

        print(
            "=" * 80
        )

        print(parameters)

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

        start_time = time.time()

        try:

            result = await tool(
                **parameters
            )

            execution_time = (
                time.time()
                - start_time
            )

            result.execution_time = (
                execution_time
            )

            return result.to_dict()

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool=tool_name,

                error=str(e),

                execution_time=(
                    time.time()
                    - start_time
                ),
            ).to_dict()

    # ========================================================
    # EXECUTE PYTHON
    # ========================================================

    async def execute_python(
        self,
        code: str,
        filename: str = "temp.py",
        timeout: int = 20,
    ) -> ToolExecutionResult:

        try:

            file_path = (
                self.project_workspace
                / filename
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

                cwd=self.project_workspace,
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

                    "file":
                        str(file_path),
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="python",

                error=str(e),
            )

    # ========================================================
    # EXECUTE SHELL
    # ========================================================

    async def execute_shell(
        self,
        command: str,
        timeout: int = 20,
    ) -> ToolExecutionResult:

        try:

            for blocked in (
                self.blocked_commands
            ):

                if blocked in command:

                    return ToolExecutionResult(

                        success=False,

                        tool="shell",

                        error=(
                            "Blocked command"
                        ),
                    )

            result = subprocess.run(

                command,

                shell=True,

                capture_output=True,

                text=True,

                timeout=timeout,

                cwd=self.project_workspace,
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
    # RUN PROJECT
    # ========================================================

    async def run_project(
        self,
        entry_file: str,
        timeout: int = 30,
    ) -> ToolExecutionResult:

        try:

            entry_path = (
                self.project_workspace
                / entry_file
            )

            if not entry_path.exists():

                return ToolExecutionResult(

                    success=False,

                    tool="run_project",

                    error=(
                        "Entry file not found"
                    ),
                )

            # =================================================
            # AUTO INSTALL REQUIREMENTS
            # =================================================

            requirements_path = (
                self.project_workspace
                / "requirements.txt"
            )

            if requirements_path.exists():

                subprocess.run(

                    [
                        "pip",
                        "install",
                        "-r",
                        str(requirements_path),
                    ],

                    capture_output=True,

                    text=True,

                    cwd=self.project_workspace,
                )

            # =================================================
            # RUN PROJECT
            # =================================================

            result = subprocess.run(

                [
                    "python",
                    str(entry_path),
                ],

                capture_output=True,

                text=True,

                timeout=timeout,

                cwd=self.project_workspace,
            )

            return ToolExecutionResult(

                success=(
                    result.returncode == 0
                ),

                tool="run_project",

                output={

                    "stdout":
                        result.stdout,

                    "stderr":
                        result.stderr,

                    "return_code":
                        result.returncode,
                },
            )

        except subprocess.TimeoutExpired:

            return ToolExecutionResult(

                success=False,

                tool="run_project",

                error=(
                    "Project execution timeout"
                ),
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="run_project",

                error=str(e),
            )

    # ========================================================
    # INSTALL DEPENDENCIES
    # ========================================================

    async def install_dependencies(
        self,
        requirements_file: str = (
            "requirements.txt"
        ),
        timeout: int = 120,
    ) -> ToolExecutionResult:

        try:

            requirements_path = (
                self.project_workspace
                / requirements_file
            )

            if not requirements_path.exists():

                return ToolExecutionResult(

                    success=False,

                    tool="pip_install",

                    error=(
                        "requirements.txt not found"
                    ),
                )

            result = subprocess.run(

                [
                    "pip",
                    "install",
                    "-r",
                    str(requirements_path),
                ],

                capture_output=True,

                text=True,

                timeout=timeout,

                cwd=self.project_workspace,
            )

            return ToolExecutionResult(

                success=(
                    result.returncode == 0
                ),

                tool="pip_install",

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

                tool="pip_install",

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
                self.project_workspace
                / path
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
                self.project_workspace
                / path
            )

            if not full_path.exists():

                return ToolExecutionResult(

                    success=False,

                    tool="read_file",

                    error="File not found",
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
    # PATCH FILE
    # ========================================================

    async def patch_file(
        self,
        path: str,
        old_text: str,
        new_text: str,
    ) -> ToolExecutionResult:

        try:

            full_path = (
                self.project_workspace
                / path
            )

            if not full_path.exists():

                return ToolExecutionResult(

                    success=False,

                    tool="patch_file",

                    error="File not found",
                )

            with open(
                full_path,
                "r",
                encoding="utf-8",
            ) as f:

                content = f.read()

            updated_content = (
                content.replace(
                    old_text,
                    new_text,
                )
            )

            with open(
                full_path,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(
                    updated_content
                )

            return ToolExecutionResult(

                success=True,

                tool="patch_file",

                output={

                    "path":
                        str(full_path),

                    "patched":
                        True,
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="patch_file",

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
                self.project_workspace
                / path
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
    # WORKSPACE TREE
    # ========================================================

    async def workspace_tree(
        self,
    ) -> ToolExecutionResult:

        try:

            tree = []

            for path in (
                self.project_workspace
                .rglob("*")
            ):

                tree.append(

                    {

                        "path":
                            str(path),

                        "is_dir":
                            path.is_dir(),
                    }
                )

            return ToolExecutionResult(

                success=True,

                tool="tree",

                output=tree,
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="tree",

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
                self.project_workspace
                / path
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
                self.project_workspace
                / path
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
    # RESET WORKSPACE
    # ========================================================

    async def reset_workspace(
        self,
    ) -> ToolExecutionResult:

        try:

            if (
                self.project_workspace.exists()
            ):

                shutil.rmtree(
                    self.project_workspace
                )

            self.project_workspace.mkdir(

                parents=True,

                exist_ok=True,
            )

            return ToolExecutionResult(

                success=True,

                tool="reset_workspace",

                output=(
                    "Workspace reset"
                ),
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="reset_workspace",

                error=str(e),
            )

    # ========================================================
    # AVAILABLE TOOLS
    # ========================================================

    def available_tools(self):

        return list(
            self.tool_registry.keys()
        )