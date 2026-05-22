# core/tools/shell_tools.py

"""
CognitiveOS - Shell Tools
---------------------------------------------------------

Responsibilities:
- shell command execution
- safe terminal execution
- runtime inspection
- deterministic shell operations
"""

from __future__ import annotations

import subprocess

from pathlib import Path

from typing import (
    Dict,
    Any,
)

# ============================================================
# SHELL TOOLS
# ============================================================


class ShellTools:

    """
    Safe shell execution utilities.
    """

    def __init__(
        self,
        workspace: Path,
    ):

        self.workspace = workspace

        self.blocked_commands = [

            "rm -rf /",

            "shutdown",

            "reboot",

            "mkfs",

            ":(){ :|:& };:",
        ]

    # ========================================================
    # EXECUTE SHELL
    # ========================================================

    async def execute_shell(
        self,
        command: str,
        timeout: int = 20,
    ) -> Dict[str, Any]:

        try:

            # ================================================
            # SECURITY CHECK
            # ================================================

            for blocked in (
                self.blocked_commands
            ):

                if blocked in command:

                    return {

                        "success": False,

                        "error":
                            "Blocked command",
                    }

            result = subprocess.run(

                command,

                shell=True,

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