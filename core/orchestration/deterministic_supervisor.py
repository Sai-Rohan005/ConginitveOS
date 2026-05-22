# core/orchestration/deterministic_supervisor.py

"""
CognitiveOS - Deterministic Supervisor
---------------------------------------------------------

Responsibilities:
- orchestrate workflow execution
- validate workflow dependencies
- manage execution ordering
- coordinate retry strategies
- invoke reflection cycles
- manage runtime cognition
- reduce unnecessary LLM calls
- provide deterministic orchestration

This replaces expensive supervisor
LLM calls with deterministic orchestration.
"""

from __future__ import annotations

from typing import (
    Dict,
    Any,
    List,
    Optional,
)

from dataclasses import (
    dataclass,
    field,
)

# ============================================================
# IMPORTS
# ============================================================

from core.orchestration.deterministic_planner import (
    WorkflowStep,
)

# ============================================================
# SUPERVISOR RESULT
# ============================================================


@dataclass
class SupervisorResult:

    success: bool

    orchestration_strategy: str

    execution_order: List[int]

    reflection_enabled: bool

    retry_enabled: bool

    workflow_steps: List[
        WorkflowStep
    ] = field(default_factory=list)

    dependency_graph: Dict[
        int,
        List[int],
    ] = field(default_factory=dict)

    execution_groups: List[
        List[int]
    ] = field(default_factory=list)

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# DETERMINISTIC SUPERVISOR
# ============================================================


class DeterministicSupervisor:

    """
    Deterministic orchestration supervisor.
    """

    def __init__(self):

        # ====================================================
        # MAX RETRIES
        # ====================================================

        self.max_retry_attempts = 3

        # ====================================================
        # PARALLEL EXECUTION LIMIT
        # ====================================================

        self.parallel_limit = 3

    # ========================================================
    # MAIN SUPERVISION
    # ========================================================

    def supervise(
        self,
        workflow_steps: List[
            WorkflowStep
        ],
        query: str,
    ) -> SupervisorResult:

        # ====================================================
        # VALIDATE WORKFLOW
        # ====================================================

        validated_steps = (
            self._validate_workflow(
                workflow_steps
            )
        )

        # ====================================================
        # BUILD DEPENDENCY GRAPH
        # ====================================================

        dependency_graph = (
            self._build_dependency_graph(
                validated_steps
            )
        )

        # ====================================================
        # EXECUTION ORDER
        # ====================================================

        execution_order = (
            self._determine_execution_order(
                validated_steps
            )
        )

        # ====================================================
        # EXECUTION GROUPS
        # ====================================================

        execution_groups = (
            self._build_execution_groups(
                validated_steps
            )
        )

        # ====================================================
        # STRATEGY
        # ====================================================

        orchestration_strategy = (
            self._determine_strategy(
                validated_steps
            )
        )

        # ====================================================
        # REFLECTION
        # ====================================================

        reflection_enabled = (
            self._requires_reflection(
                query
            )
        )

        return SupervisorResult(

            success=True,

            orchestration_strategy=
                orchestration_strategy,

            execution_order=
                execution_order,

            reflection_enabled=
                reflection_enabled,

            retry_enabled=True,

            workflow_steps=
                validated_steps,

            dependency_graph=
                dependency_graph,

            execution_groups=
                execution_groups,

            metadata={

                "workflow_size":
                    len(validated_steps),

                "parallel_groups":
                    len(execution_groups),

                "max_retry_attempts":
                    self.max_retry_attempts,
            },
        )

    # ========================================================
    # VALIDATE WORKFLOW
    # ========================================================

    def _validate_workflow(
        self,
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> List[WorkflowStep]:

        validated = []

        seen_ids = set()

        for step in workflow_steps:

            # ================================================
            # UNIQUE STEP IDS
            # ================================================

            if step.step_id in seen_ids:

                continue

            seen_ids.add(
                step.step_id
            )

            # ================================================
            # CLEAN DEPENDENCIES
            # ================================================

            cleaned_dependencies = []

            for dependency in (
                step.dependencies
            ):

                if dependency != step.step_id:

                    cleaned_dependencies.append(
                        dependency
                    )

            step.dependencies = (
                cleaned_dependencies
            )

            validated.append(step)

        return validated

    # ========================================================
    # DEPENDENCY GRAPH
    # ========================================================

    def _build_dependency_graph(
        self,
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> Dict[int, List[int]]:

        graph = {}

        for step in workflow_steps:

            graph[
                step.step_id
            ] = step.dependencies

        return graph

    # ========================================================
    # EXECUTION ORDER
    # ========================================================

    def _determine_execution_order(
        self,
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> List[int]:

        ordered = []

        remaining = workflow_steps.copy()

        completed = set()

        while remaining:

            progress = False

            for step in remaining[:]:

                dependencies_satisfied = all(

                    dependency in completed

                    for dependency
                    in step.dependencies
                )

                if dependencies_satisfied:

                    ordered.append(
                        step.step_id
                    )

                    completed.add(
                        step.step_id
                    )

                    remaining.remove(
                        step
                    )

                    progress = True

            # ================================================
            # PREVENT INFINITE LOOP
            # ================================================

            if not progress:

                for step in remaining:

                    ordered.append(
                        step.step_id
                    )

                break

        return ordered

    # ========================================================
    # EXECUTION GROUPS
    # ========================================================

    def _build_execution_groups(
        self,
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> List[List[int]]:

        groups = []

        completed = set()

        remaining = workflow_steps.copy()

        while remaining:

            current_group = []

            removable = []

            for step in remaining:

                dependencies_satisfied = all(

                    dependency in completed

                    for dependency
                    in step.dependencies
                )

                if dependencies_satisfied:

                    current_group.append(
                        step.step_id
                    )

                    removable.append(
                        step
                    )

                if (
                    len(current_group)
                    >= self.parallel_limit
                ):

                    break

            if not current_group:

                break

            groups.append(
                current_group
            )

            for step in removable:

                completed.add(
                    step.step_id
                )

                remaining.remove(
                    step
                )

        return groups

    # ========================================================
    # STRATEGY
    # ========================================================

    def _determine_strategy(
        self,
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> str:

        workflow_size = len(
            workflow_steps
        )

        if workflow_size <= 2:

            return (
                "Lightweight sequential execution"
            )

        if any(

            step.parallelizable

            for step in workflow_steps
        ):

            return (
                "Hybrid parallel orchestration"
            )

        return (
            "Sequential architecture-first "
            "execution with runtime validation"
        )

    # ========================================================
    # REFLECTION DECISION
    # ========================================================

    def _requires_reflection(
        self,
        query: str,
    ) -> bool:

        query = query.lower()

        reflection_keywords = [

            "production",

            "enterprise",

            "scalable",

            "secure",

            "distributed",

            "high availability",

            "real-time",
        ]

        for keyword in reflection_keywords:

            if keyword in query:

                return True

        return False

    # ========================================================
    # FAILED STEP ANALYSIS
    # ========================================================

    def analyze_failed_steps(
        self,
        completed_steps: List[int],
        failed_steps: List[int],
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> Dict[str, Any]:

        retryable_steps = []

        blocked_steps = []

        for step in workflow_steps:

            # ================================================
            # FAILED STEP
            # ================================================

            if step.step_id in failed_steps:

                retryable_steps.append(

                    {

                        "step_id":
                            step.step_id,

                        "agent":
                            step.agent,

                        "task":
                            step.task,

                        "retry_reason":
                            "Execution failure",
                    }
                )

            # ================================================
            # BLOCKED STEP
            # ================================================

            for dependency in (
                step.dependencies
            ):

                if dependency in failed_steps:

                    blocked_steps.append(

                        {

                            "step_id":
                                step.step_id,

                            "blocked_by":
                                dependency,

                            "agent":
                                step.agent,
                        }
                    )

        return {

            "retryable_steps":
                retryable_steps,

            "blocked_steps":
                blocked_steps,

            "retry_required":
                len(retryable_steps)
                > 0,
        }

    # ========================================================
    # EXECUTION SUMMARY
    # ========================================================

    def generate_execution_summary(
        self,
        completed_steps: List[int],
        failed_steps: List[int],
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> Dict[str, Any]:

        total_steps = len(
            workflow_steps
        )

        completed_count = len(
            completed_steps
        )

        failed_count = len(
            failed_steps
        )

        success_rate = 0.0

        if total_steps > 0:

            success_rate = round(

                (
                    completed_count
                    / total_steps
                ) * 100,

                2,
            )

        return {

            "total_steps":
                total_steps,

            "completed_steps":
                completed_count,

            "failed_steps":
                failed_count,

            "success_rate":
                success_rate,

            "workflow_success":
                failed_count == 0,
        }

    # ========================================================
    # EXPORT SUPERVISION
    # ========================================================

    def export_supervision(
        self,
        result: SupervisorResult,
    ) -> Dict[str, Any]:

        return {

            "success":
                result.success,

            "orchestration_strategy":
                result.orchestration_strategy,

            "execution_order":
                result.execution_order,

            "reflection_enabled":
                result.reflection_enabled,

            "retry_enabled":
                result.retry_enabled,

            "dependency_graph":
                result.dependency_graph,

            "execution_groups":
                result.execution_groups,

            "workflow_steps": [

                {

                    "step_id":
                        step.step_id,

                    "agent":
                        step.agent,

                    "task":
                        step.task,

                    "dependencies":
                        step.dependencies,

                    "parallelizable":
                        step.parallelizable,

                    "expected_output":
                        step.expected_output,
                }

                for step
                in result.workflow_steps
            ],

            "metadata":
                result.metadata,
        }