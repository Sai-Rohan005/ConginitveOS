# domains/software_engineering/runtime/import_extractor.py

"""
CognitiveOS - Import Extractor
---------------------------------------------------------

Responsibilities:
- extract imports from generated code
- map imports to pip packages
- generate deterministic requirements
- avoid unnecessary LLM calls

This replaces:
Gemini-generated requirements.txt
"""

from __future__ import annotations

import re

from typing import (
    List,
    Dict,
    Set,
)


# ============================================================
# IMPORT EXTRACTOR
# ============================================================


class ImportExtractor:

    """
    Deterministic import extraction engine.
    """

    def __init__(self):

        # ====================================================
        # STANDARD LIBRARIES
        # ====================================================

        self.standard_libraries = {

            "os",
            "sys",
            "json",
            "re",
            "math",
            "time",
            "uuid",
            "typing",
            "pathlib",
            "datetime",
            "asyncio",
            "subprocess",
            "logging",
            "traceback",
            "functools",
            "itertools",
            "collections",
            "dataclasses",
            "threading",
            "multiprocessing",
            "shutil",
            "tempfile",
            "sqlite3",
            "http",
            "urllib",
            "base64",
            "hashlib",
            "random",
            "enum",
            "inspect",
        }

        # ====================================================
        # IMPORT → PACKAGE MAP
        # ====================================================

        self.package_map = {

            # FastAPI
            "fastapi":
                "fastapi",

            "uvicorn":
                "uvicorn",

            "pydantic":
                "pydantic",

            "starlette":
                "starlette",

            # Database
            "sqlalchemy":
                "sqlalchemy",

            "asyncpg":
                "asyncpg",

            "psycopg2":
                "psycopg2-binary",

            "motor":
                "motor",

            "pymongo":
                "pymongo",

            # Redis
            "redis":
                "redis",

            # Auth
            "jwt":
                "pyjwt",

            "passlib":
                "passlib[bcrypt]",

            "bcrypt":
                "bcrypt",

            # AI
            "transformers":
                "transformers",

            "torch":
                "torch",

            "langchain":
                "langchain",

            "openai":
                "openai",

            # HTTP
            "requests":
                "requests",

            "httpx":
                "httpx",

            "aiohttp":
                "aiohttp",

            # Environment
            "dotenv":
                "python-dotenv",

            # Validation
            "marshmallow":
                "marshmallow",

            # Background Jobs
            "celery":
                "celery",

            # Testing
            "pytest":
                "pytest",

            # Websocket
            "websockets":
                "websockets",

            # File Upload
            "multipart":
                "python-multipart",

            # ORM
            "alembic":
                "alembic",

            # Security
            "cryptography":
                "cryptography",
        }

    # ========================================================
    # EXTRACT IMPORTS FROM CODE
    # ========================================================

    def extract_imports_from_code(
        self,
        code: str,
    ) -> List[str]:

        imports = set()

        # ====================================================
        # import x
        # ====================================================

        import_pattern = re.findall(

            r"^\s*import\s+([a-zA-Z0-9_\.]+)",

            code,

            re.MULTILINE,
        )

        # ====================================================
        # from x import y
        # ====================================================

        from_pattern = re.findall(

            r"^\s*from\s+([a-zA-Z0-9_\.]+)\s+import",

            code,

            re.MULTILINE,
        )

        all_imports = (
            import_pattern
            + from_pattern
        )

        for imported in all_imports:

            root_import = (
                imported.split(".")[0]
            )

            if (
                root_import
                not in self.standard_libraries
            ):

                imports.add(
                    root_import
                )

        return sorted(
            list(imports)
        )

    # ========================================================
    # MAP IMPORTS TO REQUIREMENTS
    # ========================================================

    def imports_to_requirements(
        self,
        imports: List[str],
    ) -> List[str]:

        requirements = set()

        for imported in imports:

            imported = imported.lower()

            package = self.package_map.get(
                imported
            )

            if package:

                requirements.add(
                    package
                )

            else:

                # ============================================
                # FALLBACK
                # ============================================

                requirements.add(
                    imported
                )

        return sorted(
            list(requirements)
        )

    # ========================================================
    # GENERATE REQUIREMENTS FROM FILES
    # ========================================================

    def generate_requirements(
        self,
        generated_files: List[
            Dict[str, str]
        ],
    ) -> List[str]:

        all_imports = set()

        for file_data in generated_files:

            code = file_data.get(
                "code",
                ""
            )

            imports = (
                self.extract_imports_from_code(
                    code
                )
            )

            all_imports.update(
                imports
            )

        requirements = (
            self.imports_to_requirements(
                list(all_imports)
            )
        )

        # ====================================================
        # ENSURE FASTAPI RUNTIME
        # ====================================================

        if "fastapi" not in requirements:

            requirements.append(
                "fastapi"
            )

        if "uvicorn" not in requirements:

            requirements.append(
                "uvicorn"
            )

        return sorted(
            list(set(requirements))
        )

    # ========================================================
    # GENERATE REQUIREMENTS.TXT CONTENT
    # ========================================================

    def generate_requirements_txt(
        self,
        generated_files: List[
            Dict[str, str]
        ],
    ) -> str:

        requirements = (
            self.generate_requirements(
                generated_files
            )
        )

        return "\n".join(
            requirements
        )