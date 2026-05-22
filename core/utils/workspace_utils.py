# core/utils/workspace_utils.py

"""
CognitiveOS - Workspace Utilities
---------------------------------------------------------

Responsibilities:
- workspace management
- project structure generation
- file indexing
- project cleanup
- workspace cognition
- runtime helpers

Production-grade workspace utilities.
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
# WORKSPACE UTILS
# ============================================================


class WorkspaceUtils:

    """
    Production workspace manager.
    """

    def __init__(
        self,
        workspace_root: str = (
            "workspace/current_project"
        ),
    ):

        self.workspace = Path(
            workspace_root
        )

        self.workspace.mkdir(

            parents=True,

            exist_ok=True,
        )

    # ========================================================
    # ENSURE STRUCTURE
    # ========================================================

    def ensure_project_structure(
        self,
    ):

        directories = [

            "app",

            "app/routes",

            "app/services",

            "app/models",

            "app/core",

            "app/utils",

            "tests",

            "docs",
        ]

        for directory in directories:

            (
                self.workspace
                / directory
            ).mkdir(

                parents=True,

                exist_ok=True,
            )

    # ========================================================
    # RESET WORKSPACE
    # ========================================================

    def reset_workspace(
        self,
    ):

        if self.workspace.exists():

            shutil.rmtree(
                self.workspace
            )

        self.workspace.mkdir(

            parents=True,

            exist_ok=True,
        )

    # ========================================================
    # WORKSPACE TREE
    # ========================================================

    def workspace_tree(
        self,
    ) -> List[Dict[str, Any]]:

        tree = []

        for path in (
            self.workspace.rglob("*")
        ):

            tree.append(

                {

                    "path":
                        str(path),

                    "is_dir":
                        path.is_dir(),

                    "size":
                        (
                            path.stat().st_size

                            if path.is_file()

                            else 0
                        ),
                }
            )

        return tree

    # ========================================================
    # FIND FILES
    # ========================================================

    def find_files(
        self,
        extension: str = ".py",
    ) -> List[str]:

        files = []

        for file in (
            self.workspace.rglob(
                f"*{extension}"
            )
        ):

            files.append(str(file))

        return files

    # ========================================================
    # READ PROJECT
    # ========================================================

    def read_project(
        self,
    ) -> Dict[str, str]:

        project = {}

        for file in (
            self.workspace.rglob("*")
        ):

            if file.is_file():

                try:

                    with open(
                        file,
                        "r",
                        encoding="utf-8",
                    ) as f:

                        project[
                            str(file)
                        ] = f.read()

                except Exception:

                    continue

        return project

    # ========================================================
    # PROJECT METADATA
    # ========================================================

    def project_metadata(
        self,
    ) -> Dict[str, Any]:

        files = list(
            self.workspace.rglob("*")
        )

        total_files = len(

            [

                f

                for f in files

                if f.is_file()
            ]
        )

        total_dirs = len(

            [

                d

                for d in files

                if d.is_dir()
            ]
        )

        total_size = sum(

            f.stat().st_size

            for f in files

            if f.is_file()
        )

        return {

            "workspace":
                str(self.workspace),

            "total_files":
                total_files,

            "total_directories":
                total_dirs,

            "total_size_bytes":
                total_size,
        }