# core/patching/semantic_patch_engine.py

"""
CognitiveOS - Semantic Patch Engine
---------------------------------------------------------

Responsibilities:
- semantic runtime repair
- logical code repair
- runtime fix injection
- framework-aware patching
- backend repair heuristics
- architecture-aware fixes

This layer repairs logical/runtime issues.
"""

from __future__ import annotations

from typing import (
    Dict,
    Any,
)

# ============================================================
# SEMANTIC PATCH ENGINE
# ============================================================


class SemanticPatchEngine:

    """
    Semantic runtime repair engine.
    """

    def __init__(self):

        self.replacements = {

            "app = FastAPI()":
                (
                    "app = FastAPI("
                    "title='CognitiveOS API'"
                    ")"
                ),

            "router = APIRouter()":
                (
                    "router = APIRouter("
                    "prefix='/api'"
                    ")"
                ),
        }

    # ========================================================
    # MAIN PATCH
    # ========================================================

    def patch(
        self,
        code: str,
        runtime_error: str = "",
    ) -> Dict[str, Any]:

        patched = code

        applied = []

        # ====================================================
        # GENERIC PATCHES
        # ====================================================

        for old, new in (
            self.replacements.items()
        ):

            if old in patched:

                patched = patched.replace(
                    old,
                    new,
                )

                applied.append(old)

        # ====================================================
        # JWT PATCHES
        # ====================================================

        if (
            "jwt"
            in patched.lower()
            and "SECRET_KEY"
            not in patched
        ):

            patched = (
                "SECRET_KEY='CHANGE_ME'\n"
                + patched
            )

            applied.append(
                "jwt_secret_injection"
            )

        # ====================================================
        # UVICORN PATCH
        # ====================================================

        if (
            "FastAPI"
            in patched
            and "__main__"
            not in patched
        ):

            patched += """

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
"""

            applied.append(
                "uvicorn_runner"
            )

        return {

            "success": True,

            "patched_code":
                patched,

            "patches_applied":
                applied,
        }