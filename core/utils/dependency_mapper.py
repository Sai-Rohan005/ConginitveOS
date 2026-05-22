# core/utils/dependency_mapper.py

"""
CognitiveOS - Dependency Mapper
---------------------------------------------------------

Responsibilities:
- build dependency graph
- map file relationships
- identify circular imports
- determine execution order
- support autonomous patching
- support cognition graph

Production-grade dependency analysis system.
"""

from __future__ import annotations

import ast

from pathlib import Path

from collections import defaultdict

from typing import (
    Dict,
    Set,
    List,
)

# ============================================================
# DEPENDENCY MAPPER
# ============================================================


class DependencyMapper:

    """
    Production dependency graph builder.
    """

    def __init__(self):

        self.graph = defaultdict(set)

    # ========================================================
    # BUILD GRAPH
    # ========================================================

    def build_graph(
        self,
        project_path: str,
    ) -> Dict[str, List[str]]:

        project_dir = Path(
            project_path
        )

        python_files = list(

            project_dir.rglob("*.py")
        )

        for py_file in python_files:

            relative = str(

                py_file.relative_to(
                    project_dir
                )
            )

            imports = (
                self._extract_imports(
                    py_file
                )
            )

            self.graph[
                relative
            ].update(imports)

        return {

            key: sorted(list(value))

            for key, value in (
                self.graph.items()
            )
        }

    # ========================================================
    # EXTRACT IMPORTS
    # ========================================================

    def _extract_imports(
        self,
        file_path: Path,
    ) -> Set[str]:

        imports = set()

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8",
            ) as f:

                code = f.read()

            tree = ast.parse(code)

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    ast.Import,
                ):

                    for alias in node.names:

                        imports.add(
                            alias.name
                        )

                elif isinstance(
                    node,
                    ast.ImportFrom,
                ):

                    if node.module:

                        imports.add(
                            node.module
                        )

        except Exception:

            pass

        return imports

    # ========================================================
    # DETECT CIRCULAR IMPORTS
    # ========================================================

    def detect_cycles(
        self,
    ) -> List[List[str]]:

        visited = set()

        stack = []

        cycles = []

        def dfs(node):

            if node in stack:

                cycle = stack[
                    stack.index(node):
                ]

                cycles.append(cycle)

                return

            if node in visited:

                return

            visited.add(node)

            stack.append(node)

            for neighbor in (
                self.graph.get(
                    node,
                    []
                )
            ):

                dfs(neighbor)

            stack.pop()

        for node in self.graph:

            dfs(node)

        return cycles

    # ========================================================
    # EXECUTION ORDER
    # ========================================================

    def execution_order(
        self,
    ) -> List[str]:

        visited = set()

        order = []

        def dfs(node):

            if node in visited:

                return

            visited.add(node)

            for dep in (
                self.graph.get(
                    node,
                    []
                )
            ):

                dfs(dep)

            order.append(node)

        for node in self.graph:

            dfs(node)

        return order[::-1]