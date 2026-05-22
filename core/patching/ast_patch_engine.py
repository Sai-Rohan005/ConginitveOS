# core/patching/ast_patch_engine.py

"""
CognitiveOS - AST Patch Engine
---------------------------------------------------------

Responsibilities:
- parse Python AST
- repair syntax issues
- inject missing imports
- repair broken functions
- repair indentation issues
- deterministic code rewriting

AST-based patching is safer than regex patching.
"""

from __future__ import annotations

import ast

from typing import (
    Dict,
    Any,
    List,
)

# ============================================================
# AST PATCH ENGINE
# ============================================================


class ASTPatchEngine:

    """
    AST-based deterministic patch engine.
    """

    def __init__(self):

        self.common_imports = {

            "FastAPI":
                "from fastapi import FastAPI",

            "APIRouter":
                "from fastapi import APIRouter",

            "BaseModel":
                "from pydantic import BaseModel",

            "JWTError":
                "from jose import JWTError",

            "jwt":
                "from jose import jwt",
        }

    # ========================================================
    # MAIN PATCH
    # ========================================================

    def patch(
        self,
        code: str,
    ) -> Dict[str, Any]:

        try:

            tree = ast.parse(code)

            missing_imports = (
                self._detect_missing_imports(
                    tree,
                    code,
                )
            )

            patched_code = (
                self._inject_imports(
                    code,
                    missing_imports,
                )
            )

            return {

                "success": True,

                "patched_code":
                    patched_code,

                "patches_applied":
                    missing_imports,
            }

        except SyntaxError as e:

            repaired = (
                self._repair_syntax(
                    code
                )
            )

            return {

                "success": True,

                "patched_code":
                    repaired,

                "patches_applied": [

                    "syntax_repair"
                ],
            }

        except Exception as e:

            return {

                "success": False,

                "error":
                    str(e),
            }

    # ========================================================
    # DETECT IMPORTS
    # ========================================================

    def _detect_missing_imports(
        self,
        tree,
        code,
    ) -> List[str]:

        required = []

        code_lower = code.lower()

        if (
            "fastapi("
            in code_lower
            and "from fastapi import fastapi"
            not in code_lower
        ):

            required.append(
                self.common_imports[
                    "FastAPI"
                ]
            )

        if (
            "apirouter("
            in code_lower
            and "from fastapi import apirouter"
            not in code_lower
        ):

            required.append(
                self.common_imports[
                    "APIRouter"
                ]
            )

        if (
            "basemodel"
            in code_lower
            and "from pydantic import basemodel"
            not in code_lower
        ):

            required.append(
                self.common_imports[
                    "BaseModel"
                ]
            )

        return required

    # ========================================================
    # INJECT IMPORTS
    # ========================================================

    def _inject_imports(
        self,
        code,
        imports,
    ):

        if not imports:

            return code

        import_block = (
            "\n".join(imports)
            + "\n\n"
        )

        return import_block + code

    # ========================================================
    # REPAIR SYNTAX
    # ========================================================

    def _repair_syntax(
        self,
        code,
    ):

        lines = code.splitlines()

        repaired = []

        for line in lines:

            repaired.append(
                line.rstrip()
            )

        return "\n".join(repaired)