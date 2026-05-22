# core/utils/import_extractor.py

"""
CognitiveOS - Production Import Extractor
---------------------------------------------------------

Responsibilities:
- extract Python imports
- resolve package dependencies
- map imports to pip packages
- detect local imports
- generate requirements
- support dependency cognition

Production-grade dependency extraction engine.
"""

from __future__ import annotations

import ast
import sys

from pathlib import Path

from typing import (
    Dict,
    Set,
    List,
    Optional,
)

# ============================================================
# STANDARD LIBRARIES
# ============================================================

STANDARD_LIBS = set(sys.stdlib_module_names)

# ============================================================
# IMPORT -> PACKAGE MAP
# ============================================================

IMPORT_PACKAGE_MAP = {

    # FastAPI
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "pydantic": "pydantic",

    # Database
    "sqlalchemy": "sqlalchemy",
    "psycopg2": "psycopg2-binary",

    # JWT
    "jwt": "python-jose",
    "jose": "python-jose",

    # ML
    "sklearn": "scikit-learn",
    "cv2": "opencv-python",
    "PIL": "pillow",

    # YAML
    "yaml": "pyyaml",

    # Async
    "aiohttp": "aiohttp",

    # Env
    "dotenv": "python-dotenv",

    # Data
    "pandas": "pandas",
    "numpy": "numpy",

    # Web
    "requests": "requests",

    # Langchain
    "langchain": "langchain",
    "langchain_core": "langchain-core",
    "langchain_google_genai":
        "langchain-google-genai",

    # Redis
    "redis": "redis",

    # Testing
    "pytest": "pytest",
}

# ============================================================
# IMPORT EXTRACTOR
# ============================================================


class ImportExtractor:

    """
    Production-grade dependency extraction engine.
    """

    def __init__(self):

        self.import_graph = {}

    # ========================================================
    # EXTRACT IMPORTS FROM CODE
    # ========================================================

    def extract_imports(
        self,
        code: str,
    ) -> Dict[str, List[str]]:

        imports = set()

        local_imports = set()

        try:

            tree = ast.parse(code)

            for node in ast.walk(tree):

                # ============================================
                # IMPORT
                # ============================================

                if isinstance(
                    node,
                    ast.Import,
                ):

                    for alias in node.names:

                        module = (
                            alias.name
                            .split(".")[0]
                        )

                        imports.add(module)

                # ============================================
                # FROM IMPORT
                # ============================================

                elif isinstance(
                    node,
                    ast.ImportFrom,
                ):

                    if node.module:

                        module = (
                            node.module
                            .split(".")[0]
                        )

                        imports.add(module)

                    # relative imports
                    if node.level > 0:

                        local_imports.add(
                            node.module
                            or ""
                        )

        except Exception:

            pass

        return {

            "imports":
                sorted(list(imports)),

            "local_imports":
                sorted(
                    list(local_imports)
                ),
        }

    # ========================================================
    # EXTRACT PIP PACKAGES
    # ========================================================

    def extract_packages(
        self,
        code: str,
    ) -> List[str]:

        extracted = (
            self.extract_imports(code)
        )

        imports = extracted["imports"]

        packages = set()

        for module in imports:

            # skip stdlib
            if module in STANDARD_LIBS:

                continue

            package = (
                IMPORT_PACKAGE_MAP.get(
                    module,
                    module,
                )
            )

            packages.add(package)

        return sorted(list(packages))

    # ========================================================
    # GENERATE REQUIREMENTS
    # ========================================================

    def generate_requirements(
        self,
        project_path: str,
    ) -> List[str]:

        project_dir = Path(
            project_path
        )

        all_packages = set()

        for py_file in (
            project_dir.rglob("*.py")
        ):

            try:

                with open(
                    py_file,
                    "r",
                    encoding="utf-8",
                ) as f:

                    code = f.read()

                packages = (
                    self.extract_packages(
                        code
                    )
                )

                all_packages.update(
                    packages
                )

            except Exception:

                continue

        return sorted(
            list(all_packages)
        )


# ============================================================
# GLOBAL HELPERS
# ============================================================

_extractor = ImportExtractor()


def extract_imports(
    code: str,
) -> List[str]:

    result = (
        _extractor.extract_packages(
            code
        )
    )

    return result


def generate_requirements(
    project_path: str,
) -> List[str]:

    return (
        _extractor
        .generate_requirements(
            project_path
        )
    )