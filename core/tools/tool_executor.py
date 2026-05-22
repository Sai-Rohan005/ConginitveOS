# domains/softwareEngineering/tools/tool_executor.py

"""
CognitiveOS - Autonomous Runtime Tool Executor
---------------------------------------------------------

Responsibilities:
- manage workspace
- execute generated projects
- validate runtime execution
- install dependencies
- auto-repair runtime failures
- patch broken files
- manage execution cognition
- support autonomous SWE loops
"""

from __future__ import annotations

import os
import ast
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
# IMPORT HELPERS
# ============================================================

from core.utils.import_extractor import (
    extract_imports,
)

from core.patching.patch_engine import (
    PatchEngine,
)

# ============================================================
# RESULT
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
    Autonomous runtime execution engine.
    """

    def __init__(self):

        self.workspace = Path(
            "workspace"
        )

        self.workspace.mkdir(
            exist_ok=True
        )

        self.project_workspace = (
            self.workspace
            / "current_project"
        )

        self.project_workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.patch_engine = (
            PatchEngine()
        )

        self.blocked_commands = [

            "rm -rf /",

            "shutdown",

            "reboot",

            "mkfs",

            ":(){ :|:& };:",
        ]

        self.tool_registry = {

            "python":
                self.execute_python,

            "shell":
                self.execute_shell,

            "run_project":
                self.run_project,

            "write_file":
                self.write_file,

            "read_file":
                self.read_file,

            "patch_file":
                self.patch_file,

            "validate_python":
                self.validate_python,

            "auto_install":
                self.auto_install_dependencies,

            "workspace_tree":
                self.workspace_tree,

            "reset_workspace":
                self.reset_workspace,
        }

    # ========================================================
    # EXECUTE TOOL
    # ========================================================

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:

        print(
            f"\n[TOOL] {tool_name}"
        )

        tool = self.tool_registry.get(
            tool_name
        )

        if not tool:

            return ToolExecutionResult(

                success=False,

                tool=tool_name,

                error="Unknown tool",
            ).to_dict()

        start = time.time()

        try:

            result = await tool(
                **parameters
            )

            result.execution_time = (
                time.time() - start
            )

            return result.to_dict()

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool=tool_name,

                error=str(e),
            ).to_dict()

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
                    "path": str(full_path)
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
                    "content": content
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="read_file",

                error=str(e),
            )

    # ========================================================
    # VALIDATE PYTHON
    # ========================================================

    async def validate_python(
        self,
        path: str,
    ) -> ToolExecutionResult:

        try:

            full_path = (
                self.project_workspace
                / path
            )

            with open(
                full_path,
                "r",
                encoding="utf-8",
            ) as f:

                source = f.read()

            ast.parse(source)

            return ToolExecutionResult(

                success=True,

                tool="validate_python",

                output={
                    "valid": True
                },
            )

        except SyntaxError as e:

            return ToolExecutionResult(

                success=False,

                tool="validate_python",

                error=str(e),
            )

    # ========================================================
    # AUTO INSTALL
    # ========================================================

    async def auto_install_dependencies(
        self,
        code: str,
    ) -> ToolExecutionResult:

        try:

            imports = extract_imports(
                code
            )

            installed = []

            for package in imports:

                result = subprocess.run(

                    [
                        "pip",
                        "install",
                        package,
                    ],

                    capture_output=True,
                    text=True,
                )

                installed.append({

                    "package":
                        package,

                    "success":
                        result.returncode == 0,
                })

            return ToolExecutionResult(

                success=True,

                tool="auto_install",

                output=installed,
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="auto_install",

                error=str(e),
            )

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

            validate = await (
                self.validate_python(
                    filename
                )
            )

            if not validate.success:

                return validate

            await self.auto_install_dependencies(
                code
            )

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

            success = (
                result.returncode == 0
            )

            stderr = result.stderr

            # =================================================
            # AUTO PATCH
            # =================================================

            if not success:

                repaired_code = (
                    self.patch_engine
                    .patch_runtime_error(
                        original_code=code,
                        runtime_error=stderr,
                    )
                )

                if repaired_code != code:

                    with open(
                        file_path,
                        "w",
                        encoding="utf-8",
                    ) as f:

                        f.write(
                            repaired_code
                        )

                    retry_result = (
                        subprocess.run(
                            [
                                "python",
                                str(file_path),
                            ],
                            capture_output=True,
                            text=True,
                            timeout=timeout,
                            cwd=self.project_workspace,
                        )
                    )

                    return ToolExecutionResult(

                        success=(
                            retry_result.returncode
                            == 0
                        ),

                        tool="python",

                        output={

                            "stdout":
                                retry_result.stdout,

                            "stderr":
                                retry_result.stderr,

                            "patched":
                                True,
                        },
                    )

            return ToolExecutionResult(

                success=success,

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

                    error="Entry file missing",
                )

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

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="run_project",

                error=str(e),
            )

    # ========================================================
    # PATCH FILE
    # ========================================================

    async def patch_file(
        self,
        path: str,
        runtime_error: str,
    ) -> ToolExecutionResult:

        try:

            full_path = (
                self.project_workspace
                / path
            )

            with open(
                full_path,
                "r",
                encoding="utf-8",
            ) as f:

                original = f.read()

            patched = (
                self.patch_engine
                .patch_runtime_error(
                    original_code=original,
                    runtime_error=runtime_error,
                )
            )

            with open(
                full_path,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(patched)

            return ToolExecutionResult(

                success=True,

                tool="patch_file",

                output={
                    "patched": True
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="patch_file",

                error=str(e),
            )

    # ========================================================
    # SHELL
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

                        error="Blocked command",
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
                },
            )

        except Exception as e:

            return ToolExecutionResult(

                success=False,

                tool="shell",

                error=str(e),
            )

    # ========================================================
    # WORKSPACE TREE
    # ========================================================

    async def workspace_tree(
        self,
    ) -> ToolExecutionResult:

        tree = []

        for path in (
            self.project_workspace
            .rglob("*")
        ):

            tree.append(str(path))

        return ToolExecutionResult(

            success=True,

            tool="workspace_tree",

            output=tree,
        )

    # ========================================================
    # RESET
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

                output="Workspace reset",
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