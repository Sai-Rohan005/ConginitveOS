# domains/software_engineering/software_engineering_domain.py

"""
CognitiveOS - Software Engineering Domain
---------------------------------------------------------

Responsibilities:
- execute complete software engineering workflow
- invoke planner
- invoke supervisor
- invoke executor
- manage domain-level cognition
- return final execution results

Pipeline:

User Query
    ↓
Planner
    ↓
Supervisor
    ↓
Workflow Executor
    ↓
Final Response
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
# IMPORT PLANNER
# ============================================================

from domains.software_engineering.planner.planner_agent import (

    PlannerAgent,

    PlannerAgentState,
)

# ============================================================
# IMPORT SUPERVISOR
# ============================================================

from domains.software_engineering.supervisor.software_supervisor import (

    SoftwareSupervisor,

    SoftwareSupervisorState,
)

# ============================================================
# IMPORT EXECUTOR
# ============================================================

from domains.software_engineering.executor.workflow_executor import (

    WorkflowExecutor,
)


# ============================================================
# DOMAIN RESULT
# ============================================================


@dataclass
class SoftwareEngineeringDomainResult:

    success: bool

    query: str

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

    final_output: str = ""

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# SOFTWARE ENGINEERING DOMAIN
# ============================================================


class SoftwareEngineeringDomain:

    """
    Complete CognitiveOS Software Engineering Pipeline.
    """

    def __init__(self):

        # ====================================================
        # CORE COMPONENTS
        # ====================================================

        self.planner = PlannerAgent()

        self.supervisor = (
            SoftwareSupervisor()
        )

        self.executor = (
            WorkflowExecutor()
        )

    # ========================================================
    # MAIN DOMAIN EXECUTION
    # ========================================================

    async def execute(
        self,
        query: str,
    ) -> SoftwareEngineeringDomainResult:

        try:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "SOFTWARE ENGINEERING DOMAIN EXECUTION"
            )

            print(
                "=" * 80
            )

            print(
                f"\nUSER QUERY:\n{query}\n"
            )

            # =================================================
            # STEP 1 — PLANNING
            # =================================================

            print(
                "[1/3] Planner Agent Running..."
            )

            planner_state = (
                PlannerAgentState(
                    query=query
                )
            )

            planner_result = await (
                self.planner.run(
                    planner_state
                )
            )

            print(
                "✓ Planning Complete"
            )

            # =================================================
            # STEP 2 — SUPERVISION
            # =================================================

            print(
                "\n[2/3] Supervisor Running..."
            )

            supervisor_state = (
                SoftwareSupervisorState(

                    query=query,

                    planner_output=(
                        planner_result.output
                    ),
                )
            )

            supervisor_result = await (
                self.supervisor.run(
                    supervisor_state
                )
            )

            print(
                "✓ Workflow Generated"
            )

            # =================================================
            # STEP 3 — EXECUTION
            # =================================================

            print(
                "\n[3/3] Workflow Execution Running..."
            )

            execution_result = await (
                self.executor.execute_workflow(

                    query=query,

                    workflow_steps=(
                        supervisor_result
                        .workflow_steps
                    ),
                )
            )

            print(
                "✓ Workflow Execution Complete"
            )

            print(
                "\n"
                + "=" * 80
            )

            print(
                "DOMAIN EXECUTION COMPLETED"
            )

            print(
                "=" * 80
            )

            # =================================================
            # BUILD METADATA
            # =================================================

            metadata = {

                "domain":
                    "software_engineering",

                "planner_steps":
                    len(
                        planner_result
                        .execution_plan
                    ),

                "workflow_steps":
                    len(
                        supervisor_result
                        .workflow_steps
                    ),

                "execution_success":
                    execution_result
                    .success,

                "completed_steps":
                    execution_result
                    .memory_snapshot.get(
                        "completed_steps",
                        [],
                    ),

                "failed_steps":
                    execution_result
                    .memory_snapshot.get(
                        "failed_steps",
                        [],
                    ),

                "active_agents":
                    execution_result
                    .memory_snapshot.get(
                        "active_agents",
                        [],
                    ),
            }

            # =================================================
            # RETURN DOMAIN RESULT
            # =================================================

            return (
                SoftwareEngineeringDomainResult(

                    success=True,

                    query=query,

                    planner_output=(
                        planner_result.output
                    ),

                    supervisor_output=(
                        supervisor_result.output
                    ),

                    execution_result=(
                        execution_result
                        .memory_snapshot
                    ),

                    final_output=(
                        execution_result
                        .final_output
                    ),

                    metadata=metadata,
                )
            )

        # ====================================================
        # DOMAIN FAILURE
        # ====================================================

        except Exception as e:

            return (
                SoftwareEngineeringDomainResult(

                    success=False,

                    query=query,

                    final_output=f"""
# Software Engineering Domain Failed

An internal execution error occurred.

## Error
{str(e)}

## Traceback
{traceback.format_exc()}
""",

                    metadata={

                        "success":
                            False,

                        "error":
                            str(e),
                    },
                )
            )