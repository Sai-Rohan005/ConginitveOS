# core/cognitive_graph.py

"""
CognitiveOS - Cognitive Graph
---------------------------------------------------------

Responsibilities:
- route queries to domains
- manage global orchestration
- invoke domain pipelines
- maintain runtime cognition state
- provide unified execution interface

This becomes the GLOBAL orchestration layer
for CognitiveOS.
"""

from __future__ import annotations

import traceback

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    Dict,
    Any,
    Optional,
)

# ============================================================
# IMPORT DOMAINS
# ============================================================

from domains.softwareEngineering.software_engineering_domain import (
    SoftwareEngineeringDomain,
)

# ============================================================
# RUNTIME STATE
# ============================================================


@dataclass
class CognitiveRuntimeState:

    query: str

    active_domain: str = ""

    planner_output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    supervisor_output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    execution_result: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    memory_snapshot: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    final_output: str = ""

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# COGNITIVE GRAPH
# ============================================================


class CognitiveGraph:

    """
    Global orchestration graph for CognitiveOS.
    """

    def __init__(self):

        # ====================================================
        # DOMAIN REGISTRY
        # ====================================================

        self.domain_registry = {

            "software_engineering":
                SoftwareEngineeringDomain(),
        }

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def execute(
        self,
        query: str,
    ) -> CognitiveRuntimeState:

        runtime_state = (
            CognitiveRuntimeState(
                query=query
            )
        )

        try:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "COGNITIVEOS EXECUTION STARTED"
            )

            print(
                "=" * 80
            )

            print(
                f"\nUSER QUERY:\n{query}\n"
            )

            # =================================================
            # STEP 1 — DOMAIN ROUTING
            # =================================================

            domain = self._route_domain(
                query
            )

            runtime_state.active_domain = (
                domain
            )

            print(
                f"[ROUTER] Selected Domain: {domain}"
            )

            # =================================================
            # STEP 2 — DOMAIN EXECUTION
            # =================================================

            domain_handler = (
                self.domain_registry.get(
                    domain
                )
            )

            if not domain_handler:

                raise ValueError(
                    f"Unknown domain: {domain}"
                )

            domain_result = await (
                domain_handler.execute(
                    query
                )
            )

            # =================================================
            # STEP 3 — UPDATE RUNTIME STATE
            # =================================================

            runtime_state.planner_output = (
                domain_result.planner_output
            )

            runtime_state.supervisor_output = (
                domain_result.supervisor_output
            )

            runtime_state.execution_result = (
                domain_result.execution_result
            )

            runtime_state.memory_snapshot = (
                domain_result.execution_result
            )

            runtime_state.final_output = (
                domain_result.final_output
            )

            runtime_state.metadata = {

                "success":
                    domain_result.success,

                "active_domain":
                    domain,

                **domain_result.metadata,
            }

            print(
                "\n"
                + "=" * 80
            )

            print(
                "COGNITIVEOS EXECUTION COMPLETED"
            )

            print(
                "=" * 80
            )

            return runtime_state

        # ====================================================
        # GLOBAL FAILURE
        # ====================================================

        except Exception as e:

            runtime_state.final_output = f"""
# CognitiveOS Execution Failed

An internal orchestration error occurred.

## Error
{str(e)}

## Traceback
{traceback.format_exc()}
"""

            runtime_state.metadata = {

                "success":
                    False,

                "error":
                    str(e),
            }

            print(
                "\n"
                + "=" * 80
            )

            print(
                "COGNITIVEOS EXECUTION FAILED"
            )

            print(
                "=" * 80
            )

            print(
                traceback.format_exc()
            )

            return runtime_state

    # ========================================================
    # DOMAIN ROUTER
    # ========================================================

    def _route_domain(
        self,
        query: str,
    ) -> str:

        """
        Initial simple rule-based routing.

        Later this becomes:
        - semantic routing
        - LLM routing
        - embedding routing
        - hybrid routing
        """

        query_lower = query.lower()

        software_keywords = [

            "build",

            "api",

            "backend",

            "frontend",

            "system",

            "architecture",

            "database",

            "fastapi",

            "react",

            "docker",

            "kubernetes",

            "microservices",

            "code",

            "debug",

            "python",

            "websocket",

            "software",
        ]

        for keyword in software_keywords:

            if keyword in query_lower:

                return (
                    "software_engineering"
                )

        # ====================================================
        # DEFAULT DOMAIN
        # ====================================================

        return (
            "software_engineering"
        )