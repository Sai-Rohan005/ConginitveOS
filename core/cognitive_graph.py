# core/cognitive_graph.py

"""
CognitiveOS - Global Cognitive Graph
---------------------------------------------------------

Responsibilities:
- global orchestration
- domain routing
- deterministic planning
- deterministic supervision
- workflow execution
- cognition management
- runtime state management
- unified multi-domain execution

This becomes the MASTER orchestration layer
for CognitiveOS.
"""

from __future__ import annotations

import time
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
# CORE ORCHESTRATION
# ============================================================

from core.orchestration.deterministic_planner import (
    DeterministicPlanner,
)

from core.orchestration.deterministic_supervisor import (
    DeterministicSupervisor,
)

from core.orchestration.workflow_executor import (
    WorkflowExecutor,
)

# ============================================================
# CORE TOOLS
# ============================================================

from core.tools.tool_executor import (
    ToolExecutor,
)

# ============================================================
# COGNITION ENGINES
# ============================================================

from core.cognition.reflection_engine import (
    ReflectionEngine,
)

from core.cognition.scoring_engine import (
    ScoringEngine,
)

from core.cognition.quality_engine import (
    QualityEngine,
)

# ============================================================
# DOMAINS
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

    reflection_output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    quality_output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    score_output: Dict[
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
    Master orchestration graph.
    """

    def __init__(self):

        # ====================================================
        # CORE ENGINES
        # ====================================================

        self.planner = (
            DeterministicPlanner()
        )

        self.supervisor = (
            DeterministicSupervisor()
        )

        self.tool_executor = (
            ToolExecutor()
        )

        self.reflection_engine = (
            ReflectionEngine()
        )

        self.scoring_engine = (
            ScoringEngine()
        )

        self.quality_engine = (
            QualityEngine()
        )

        # ====================================================
        # DOMAIN REGISTRY
        # ====================================================

        self.domain_registry = {

            "softwareEngineering":
                SoftwareEngineeringDomain(),
        }

        # ====================================================
        # AGENT REGISTRY
        # ====================================================

        self.agent_registry = (
            self._build_agent_registry()
        )

        # ====================================================
        # WORKFLOW EXECUTOR
        # ====================================================

        self.workflow_executor = (
            WorkflowExecutor(
                tool_executor=self.tool_executor,
            )
        )

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

        start_time = time.time()

        try:

            print(
                "\n"
                + "=" * 100
            )

            print(
                "COGNITIVEOS EXECUTION STARTED"
            )

            print(
                "=" * 100
            )

            print(
                f"\nQUERY:\n{query}\n"
            )

            # =================================================
            # STEP 1 — DOMAIN ROUTING
            # =================================================

            domain = (
                self._route_domain(
                    query
                )
            )

            runtime_state.active_domain = (
                domain
            )

            print(
                f"[ROUTER] DOMAIN => {domain}"
            )

            # =================================================
            # STEP 2 — DETERMINISTIC PLANNING
            # =================================================

            planner_result = (
                self.planner.plan(
                    query
                )
            )

            runtime_state.planner_output = (
                self.planner.export_plan(
                    planner_result
                )
            )

            print(
                "\n[PLANNER] PLAN GENERATED"
            )

            # =================================================
            # STEP 3 — DETERMINISTIC SUPERVISION
            # =================================================

            supervisor_result = (
                self.supervisor.supervise(

                    workflow_steps=
                        planner_result
                        .workflow_steps,

                    query=query,
                )
            )

            runtime_state.supervisor_output = (

                self.supervisor
                .export_supervision(
                    supervisor_result
                )
            )

            print(
                "\n[SUPERVISOR] WORKFLOW SUPERVISED"
            )

            # =================================================
            # STEP 4 — WORKFLOW EXECUTION
            # =================================================

            execution_result = await (

                self.workflow_executor
                .execute_workflow(

                    query=query,

                    workflow_steps=
                        planner_result
                        .workflow_steps,
                )
            )

            runtime_state.execution_result = {

                "success":
                    execution_result.success,

                "final_output":
                    execution_result
                    .final_output,
            }

            runtime_state.memory_snapshot = (

                execution_result
                .memory_snapshot
            )

            print(
                "\n[EXECUTOR] WORKFLOW EXECUTED"
            )

            # =================================================
            # STEP 5 — QUALITY ANALYSIS
            # =================================================

            quality_result = (
                self.quality_engine
                .evaluate(

                    execution_result
                    .final_output
                )
            )

            runtime_state.quality_output = {

                "overall_score":
                    quality_result
                    .overall_score,

                "production_ready":
                    quality_result
                    .production_ready,

                "issues": getattr(quality_result, "issues", []),
            }

            print(
                "\n[QUALITY] QUALITY ANALYZED"
            )

            # =================================================
            # STEP 6 — SCORING
            # =================================================

            score_result = (
                self.scoring_engine
                .score(

                    execution_result
                    .final_output
                )
            )

            runtime_state.score_output = {

                "overall_score":
                    score_result
                    .overall_score,

                "dimension_scores": getattr(score_result, "dimension_scores", {}),
            }

            print(
                "\n[SCORING] EXECUTION SCORED"
            )

            # =================================================
            # STEP 7 — REFLECTION
            # =================================================

            reflection_result = (

                self.reflection_engine
                .reflect(

                    execution_result=
                        execution_result
                        .final_output,

                    quality_result=
                        runtime_state
                        .quality_output,

                    artifacts=
                        execution_result
                        .memory_snapshot
                        .get(
                            "artifacts",
                            [],
                        ),
                )
            )

            runtime_state.reflection_output = {

                "summary":
                    reflection_result
                    .summary,

                "retry_required":
                    reflection_result
                    .retry_required,

                "improvements": getattr(reflection_result, "recommendations", []),
            }

            print(
                "\n[REFLECTION] REFLECTION COMPLETE"
            )

            # =================================================
            # STEP 8 — FINAL OUTPUT
            # =================================================

            runtime_state.final_output = (

                self._build_final_output(
                    runtime_state
                )
            )

            execution_time = round(

                time.time()
                - start_time,

                2,
            )

            runtime_state.metadata = {

                "success":
                    True,

                "active_domain":
                    domain,

                "execution_time":
                    execution_time,

                "workflow_steps":
                    len(
                        planner_result
                        .workflow_steps
                    ),

                "quality_score":
                    quality_result
                    .overall_score,

                "production_ready":
                    quality_result
                    .production_ready,
            }

            print(
                "\n"
                + "=" * 100
            )

            print(
                "COGNITIVEOS EXECUTION COMPLETED"
            )

            print(
                "=" * 100
            )

            return runtime_state

        # ====================================================
        # GLOBAL FAILURE
        # ====================================================

        except Exception as e:

            runtime_state.final_output = f"""
# CognitiveOS Global Failure

Execution failed.

Error:
{str(e)}

Traceback:
{traceback.format_exc()}
"""

            runtime_state.metadata = {

                "success": False,

                "error":
                    str(e),
            }

            print(
                "\n"
                + "=" * 100
            )

            print(
                "COGNITIVEOS EXECUTION FAILED"
            )

            print(
                "=" * 100
            )

            print(
                traceback.format_exc()
            )

            return runtime_state

    # ========================================================
    # AGENT REGISTRY
    # ========================================================

    def _build_agent_registry(
        self,
    ) -> Dict[str, Any]:

        registry = {}

        # ====================================================
        # LOAD DOMAIN AGENTS
        # ====================================================

        for domain_name, domain in (
            self.domain_registry.items()
        ):

            if hasattr(
                domain,
                "get_agents"
            ):

                registry.update(
                    domain.get_agents()
                )

        return registry

    # ========================================================
    # DOMAIN ROUTER
    # ========================================================

    def _route_domain(
        self,
        query: str,
    ) -> str:

        query_lower = query.lower()

        # ====================================================
        # SOFTWARE ENGINEERING
        # ====================================================

        software_keywords = [

            "fastapi",

            "backend",

            "frontend",

            "jwt",

            "api",

            "docker",

            "microservice",

            "database",

            "websocket",

            "code",

            "python",

            "architecture",

            "system",
        ]

        # ====================================================
        # AI ENGINEERING
        # ====================================================

        ai_keywords = [

            "llm",

            "rag",

            "embedding",

            "vector",

            "langchain",

            "transformer",

            "fine tuning",
        ]

        # ====================================================
        # CYBERSECURITY
        # ====================================================

        security_keywords = [

            "xss",

            "csrf",

            "vulnerability",

            "security",

            "exploit",

            "jwt attack",
        ]

        # ====================================================
        # DEVOPS
        # ====================================================

        devops_keywords = [

            "kubernetes",

            "terraform",

            "ci/cd",

            "deployment",

            "monitoring",
        ]

        # ====================================================
        # DOMAIN SCORING
        # ====================================================

        scores = {

            "softwareEngineering": 0,

            "aiEngineering": 0,

            "cybersecurity": 0,

            "devops": 0,
        }

        for keyword in software_keywords:

            if keyword in query_lower:

                scores[
                    "softwareEngineering"
                ] += 1

        for keyword in ai_keywords:

            if keyword in query_lower:

                scores[
                    "aiEngineering"
                ] += 1

        for keyword in security_keywords:

            if keyword in query_lower:

                scores[
                    "cybersecurity"
                ] += 1

        for keyword in devops_keywords:

            if keyword in query_lower:

                scores[
                    "devops"
                ] += 1

        selected = max(

            scores,

            key=scores.get
        )

        # ====================================================
        # DEFAULT DOMAIN
        # ====================================================

        if scores[selected] == 0:

            return (
                "softwareEngineering"
            )

        return selected

    # ========================================================
    # FINAL OUTPUT BUILDER
    # ========================================================

    def _build_final_output(
        self,
        runtime_state:
            CognitiveRuntimeState,
    ) -> str:

        quality = (
            runtime_state
            .quality_output
            .get(
                "overall_score",
                0,
            )
        )

        score = (
            runtime_state
            .score_output
            .get(
                "overall_score",
                0,
            )
        )

        reflection = (
            runtime_state
            .reflection_output
            .get(
                "summary",
                "",
            )
        )

        return f"""
# CognitiveOS Execution Result

## Active Domain
{runtime_state.active_domain}

## Quality Score
{quality}

## Cognitive Score
{score}

## Reflection Summary
{reflection}

## Metadata
{runtime_state.metadata}
"""
