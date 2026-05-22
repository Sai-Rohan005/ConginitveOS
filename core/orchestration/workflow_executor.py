# core/orchestration/workflow_executor.py

"""
CognitiveOS - Workflow Executor
---------------------------------------------------------

Responsibilities:
- execute workflows
- orchestrate agents
- manage runtime cognition
- execute retry cycles
- invoke reflection
- validate runtime execution
- aggregate outputs
- manage artifacts
- maintain shared memory

This becomes the runtime
cognitive execution engine.
"""

from __future__ import annotations

import traceback

from typing import (
    Dict,
    Any,
    List,
)

# ============================================================
# CORE IMPORTS
# ============================================================

from core.memory.shared_memory import (
    SharedMemoryManager,
)

from core.memory.artifacts import (
    ArtifactType,
)

from core.orchestration.retry_engine import (
    RetryEngine,
)

from core.cognition.reflection_engine import (
    ReflectionEngine,
)

from core.cognition.scoring_engine import (
    ScoringEngine,
)

from core.cognition.quality_engine import (
    QualityEngine,
)

from core.runtime.deterministic_debugger import (
    DeterministicDebugger,
)

# ============================================================
# EXECUTION RESULT
# ============================================================


class WorkflowExecutionResult:

    def __init__(
        self,
        success: bool,
        final_output: Dict[
            str,
            Any,
        ],
        memory_snapshot: Dict[
            str,
            Any,
        ],
    ):

        self.success = success

        self.final_output = (
            final_output
        )

        self.memory_snapshot = (
            memory_snapshot
        )


# ============================================================
# WORKFLOW EXECUTOR
# ============================================================


class WorkflowExecutor:

    """
    Runtime cognition engine.
    """

    def __init__(
        self,
        agent_registry: Dict[
            str,
            Any,
        ],
        tool_executor,
    ):

        # ====================================================
        # AGENTS
        # ====================================================

        self.agent_registry = (
            agent_registry
        )

        # ====================================================
        # TOOLS
        # ====================================================

        self.tool_executor = (
            tool_executor
        )

        # ====================================================
        # MEMORY
        # ====================================================

        self.memory_manager = (
            SharedMemoryManager()
        )

        # ====================================================
        # COGNITION
        # ====================================================

        self.retry_engine = (
            RetryEngine()
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

        self.debugger = (
            DeterministicDebugger()
        )

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def execute_workflow(
        self,
        query: str,
        workflow_steps: List[Any],
    ) -> WorkflowExecutionResult:

        memory = (
            self.memory_manager
            .create_memory(
                query=query
            )
        )

        failed_steps = []

        try:

            # =================================================
            # EXECUTE WORKFLOW
            # =================================================

            for step in workflow_steps:

                if not (
                    self._dependencies_satisfied(
                        step,
                        memory,
                    )
                ):

                    failed_steps.append(

                        {

                            "step_id":
                                step.step_id,

                            "agent":
                                step.agent,

                            "error":
                                "Dependency failure",
                        }
                    )

                    continue

                result = await (
                    self._execute_step(
                        step,
                        memory,
                    )
                )

                if not result.get(
                    "success",
                    False,
                ):

                    failed_steps.append(

                        {

                            "step_id":
                                step.step_id,

                            "agent":
                                step.agent,

                            "error":
                                result.get(
                                    "error",
                                    "Unknown failure",
                                ),
                        }
                    )

            # =================================================
            # RETRY ANALYSIS
            # =================================================

            retry_result = (
                self.retry_engine
                .analyze_retry(

                    failed_steps=
                        failed_steps,

                    retry_count=0,
                )
            )

            # =================================================
            # RETRY EXECUTION
            # =================================================

            if (
                retry_result.retry_required
            ):

                for retry_step in (
                    retry_result.retry_steps
                ):

                    step = self._find_step(

                        retry_step[
                            "step_id"
                        ],

                        workflow_steps,
                    )

                    if step:

                        await self._execute_step(
                            step,
                            memory,
                        )

            # =================================================
            # AGGREGATE OUTPUTS
            # =================================================

            aggregated_output = {

                "query":
                    query,

                "agent_outputs":
                    memory.agent_outputs,

                "artifacts":
                    memory.artifact_manager
                    .export_artifacts(),
            }

            # =================================================
            # SCORING
            # =================================================

            score_result = (
                self.scoring_engine
                .score(
                    aggregated_output
                )
            )

            # =================================================
            # QUALITY
            # =================================================

            quality_result = (
                self.quality_engine
                .evaluate(
                    aggregated_output
                )
            )

            # =================================================
            # REFLECTION
            # =================================================

            reflection_result = (
                self.reflection_engine
                .reflect(

                    execution_result=
                        aggregated_output,

                    quality_result=
                        {

                            "overall_score":
                                quality_result
                                .overall_score
                        },

                    artifacts=
                        memory
                        .artifact_manager
                        .get_all_artifacts(),
                )
            )

            # =================================================
            # FINAL OUTPUT
            # =================================================

            final_output = {

                "success":
                    True,

                "query":
                    query,

                "agent_outputs":
                    memory.agent_outputs,

                "score":
                    score_result
                    .overall_score,

                "quality":
                    quality_result
                    .overall_score,

                "production_ready":
                    quality_result
                    .production_ready,

                "reflection":
                    reflection_result.summary,

                "artifacts":
                    memory
                    .artifact_manager
                    .export_artifacts(),
            }

            snapshot = (
                self.memory_manager
                .export_memory_snapshot(
                    memory
                )
            )

            return WorkflowExecutionResult(

                success=True,

                final_output=
                    final_output,

                memory_snapshot=
                    snapshot,
            )

        except Exception as e:

            return WorkflowExecutionResult(

                success=False,

                final_output={

                    "error":
                        str(e),

                    "traceback":
                        traceback
                        .format_exc(),
                },

                memory_snapshot={},
            )

    # ========================================================
    # EXECUTE STEP
    # ========================================================

    async def _execute_step(
        self,
        step,
        memory,
    ) -> Dict[str, Any]:

        agent = (
            self.agent_registry.get(
                step.agent
            )
        )

        if not agent:

            return {

                "success":
                    False,

                "error":
                    f"Unknown agent: "
                    f"{step.agent}",
            }

        try:

            context = {

                "query":
                    memory.query,

                "task":
                    step.task,

                "shared_context":
                    memory.shared_context,

                "agent_outputs":
                    memory.agent_outputs,

                "tool_executor":
                    self.tool_executor,

                "context_artifacts":
                    memory
                    .artifact_manager
                    .get_all_artifacts(),
            }

            result = await agent.run(
                context
            )

            # ================================================
            # STORE OUTPUT
            # ================================================

            self.memory_manager.store_agent_output(

                memory=memory,

                step_id=step.step_id,

                agent=step.agent,

                output=result,
            )

            # ================================================
            # STORE ARTIFACT
            # ================================================

            self.memory_manager.store_artifact(

                memory=memory,

                artifact_type=
                    ArtifactType
                    .DOCUMENTATION,

                created_by=
                    step.agent,

                content=result,

                metadata={

                    "step_id":
                        step.step_id,

                    "task":
                        step.task,
                },
            )

            # ================================================
            # COMPLETE STEP
            # ================================================

            self.memory_manager.mark_step_completed(

                memory,

                step.step_id,
            )

            return result

        except Exception as e:

            return {

                "success":
                    False,

                "error":
                    str(e),

                "traceback":
                    traceback
                    .format_exc(),
            }

    # ========================================================
    # DEPENDENCIES
    # ========================================================

    def _dependencies_satisfied(
        self,
        step,
        memory,
    ) -> bool:

        for dependency in (
            step.dependencies
        ):

            if (
                dependency
                not in memory.completed_steps
            ):

                return False

        return True

    # ========================================================
    # FIND STEP
    # ========================================================

    def _find_step(
        self,
        step_id: int,
        workflow_steps: List[Any],
    ):

        for step in workflow_steps:

            if step.step_id == step_id:

                return step

        return None