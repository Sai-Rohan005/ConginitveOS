# domains/software_engineering/supervisor/software_supervisor.py

"""
CognitiveOS - Deterministic Software Supervisor
---------------------------------------------------------

Responsibilities:
- convert planner goals into execution workflows
- assign agents deterministically
- define dependencies
- orchestrate runtime cognition

NO LLM CALLS.
NO GEMINI.

This is pure orchestration logic.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    List,
    Dict,
    Any,
    Optional,
)

# ============================================================
# EXECUTION STEP
# ============================================================


@dataclass
class WorkflowStep:

    step_id: int
    agent: str
    task: str

    dependencies: List[int] = field(default_factory=list)

    parallelizable: bool = False

    expected_output: str = ""

    # ✅ ADD THIS
    required_skills: List[str] = field(default_factory=list)

    # (VERY IMPORTANT for future failures)
    runtime_backend: str = "python"
    execution_mode: str = "sync"
    deterministic_execution: bool = True



# ============================================================
# SUPERVISOR STATE
# ============================================================


@dataclass
class SoftwareSupervisorState:

    query: str

    planner_output: Dict[
        str,
        Any,
    ]

    workflow_steps: List[
        WorkflowStep
    ] = field(default_factory=list)

    orchestration_strategy: str = ""

    requires_reflection: bool = True

    estimated_execution_order: List[
        int
    ] = field(default_factory=list)

    output: Optional[
        Dict[str, Any]
    ] = None


# ============================================================
# SOFTWARE SUPERVISOR
# ============================================================


class SoftwareSupervisor:

    """
    Deterministic orchestration engine.
    """

    def __init__(self):

        pass

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def run(
        self,
        state: SoftwareSupervisorState,
    ) -> SoftwareSupervisorState:

        try:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "DETERMINISTIC SUPERVISOR STARTED"
            )

            print(
                "=" * 80
            )

            planner_output = (
                state.planner_output
            )

            query = (
                state.query.lower()
            )

            workflow_steps = []

            step_id = 1

            # =================================================
            # ALWAYS START WITH ARCHITECTURE
            # =================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent=
                        "architecture_agent",

                    task=
                        "Design scalable system architecture",

                    dependencies=[],

                    parallelizable=False,

                    expected_output=
                        "Production architecture design",
                )
            )

            architecture_step = step_id

            step_id += 1

            # =================================================
            # CODE GENERATION
            # =================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent=
                        "code_agent",

                    task=
                        self._determine_code_task(
                            query
                        ),

                    dependencies=[
                        architecture_step
                    ],

                    parallelizable=False,

                    expected_output=
                        "Production-ready implementation",
                )
            )

            code_step = step_id

            step_id += 1

            # =================================================
            # DEBUG STEP
            # =================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent=
                        "debug_agent",

                    task=
                        "Validate runtime stability and production readiness",

                    dependencies=[
                        code_step
                    ],

                    parallelizable=False,

                    expected_output=
                        "Runtime validation report",
                )
            )

            debug_step = step_id

            step_id += 1

            # =================================================
            # AGGREGATION STEP
            # =================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent=
                        "aggregator_agent",

                    task=
                        "Aggregate all outputs into final response",

                    dependencies=[
                        debug_step
                    ],

                    parallelizable=False,

                    expected_output=
                        "Final aggregated response",
                )
            )

            # =================================================
            # UPDATE STATE
            # =================================================

            state.workflow_steps = (
                workflow_steps
            )

            state.orchestration_strategy = (
                "Deterministic sequential orchestration"
            )

            state.requires_reflection = True

            state.estimated_execution_order = [

                step.step_id

                for step in workflow_steps
            ]

            state.output = {

                "success": True,

                "workflow_steps":
                    [

                        step.__dict__

                        for step in workflow_steps
                    ],
            }

            print(
                "\nFINAL WORKFLOW:\n"
            )

            for step in workflow_steps:

                print(step)

            return state

        except Exception as e:

            state.output = {

                "success": False,

                "error": str(e),
            }

            return state

    # ========================================================
    # DETERMINE CODE TASK
    # ========================================================

    def _determine_code_task(
        self,
        query: str,
    ) -> str:

        query = query.lower()

        # ====================================================
        # FASTAPI
        # ====================================================

        if "fastapi" in query:

            return (
                "Build scalable FastAPI backend system"
            )

        # ====================================================
        # DJANGO
        # ====================================================

        if "django" in query:

            return (
                "Build scalable Django backend system"
            )

        # ====================================================
        # WEBSOCKET
        # ====================================================

        if "websocket" in query:

            return (
                "Implement realtime websocket system"
            )

        # ====================================================
        # AUTH
        # ====================================================

        if "jwt" in query:

            return (
                "Implement JWT authentication backend"
            )

        # ====================================================
        # DEFAULT
        # ====================================================

        return (
            "Implement production-ready software system"
        )