# core/tools/file_tools.py

"""
CognitiveOS - File Tools
---------------------------------------------------------

Responsibilities:
- filesystem operations
- file writing
- file reading
- workspace management
- directory creation
- project tree inspection
"""

from __future__ import annotations

import shutil

from pathlib import Path

from typing import (
    Dict,
    Any,
    List,
)

# ============================================================
# FILE TOOLS
# ============================================================


class FileTools:

    """
    Filesystem utility layer.
    """

    def __init__(
        self,
        workspace: Path,
    ):

        self.workspace = workspace

    # ========================================================
    # WRITE FILE
    # ========================================================

    async def write_file(
        self,
        path: str,
        content: str,
    ) -> Dict[str, Any]:

        try:

            full_path = (
                self.workspace
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

            return {

                "success": True,

                "path":
                    str(full_path),

                "size":
                    len(content),
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),
            }

    # ========================================================
    # READ FILE
    # ========================================================

    async def read_file(
        self,
        path: str,
    ) -> Dict[str, Any]:

        try:

            full_path = (
                self.workspace
                / path
            )

            if not full_path.exists():

                return {

                    "success": False,

                    "error":
                        "File not found",
                }

            with open(
                full_path,
                "r",
                encoding="utf-8",
            ) as f:

                content = f.read()

            return {

                "success": True,

                "content":
                    content,
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),
            }

    # ========================================================
    # CREATE DIRECTORY
    # ========================================================

    async def create_directory(
        self,
        path: str,
    ) -> Dict[str, Any]:

        try:

            full_path = (
                self.workspace
                / path
            )

            full_path.mkdir(

                parents=True,

                exist_ok=True,
            )

            return {

                "success": True,

                "path":
                    str(full_path),
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),
            }

    # ========================================================
    # LIST FILES
    # ========================================================

    async def list_files(
        self,
        path: str = "",
    ) -> Dict[str, Any]:

        try:

            full_path = (
                self.workspace
                / path
            )

            files = []

            for item in (
                full_path.rglob("*")
            ):

                files.append(

                    {

                        "path":
                            str(item),

                        "is_dir":
                            item.is_dir(),
                    }
                )

            return {

                "success": True,

                "files": files,
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),
            }

    # ========================================================
    # DELETE PATH
    # ========================================================

    async def delete_path(
        self,
        path: str,
    ) -> Dict[str, Any]:

        try:

            full_path = (
                self.workspace
                / path
            )

            if not full_path.exists():

                return {

                    "success": False,

                    "error":
                        "Path not found",
                }

            if full_path.is_file():

                full_path.unlink()

            else:

                shutil.rmtree(
                    full_path
                )

            return {

                "success": True,
            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e),
            }