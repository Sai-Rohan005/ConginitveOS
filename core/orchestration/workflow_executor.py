# core/orchestration/workflow_executor.py

"""
CognitiveOS - Workflow Executor
---------------------------------------------------------

Responsibilities:
- execute workflows
- orchestrate agents
- dynamically load agents
- dynamically inject skills
- manage runtime cognition
- execute retry cycles
- invoke reflection
- validate runtime execution
- aggregate outputs
- manage artifacts
- maintain shared memory
- support deterministic orchestration
- enable scalable cognition runtime
- provide execution telemetry

This becomes the runtime
cognitive execution engine.
"""

from __future__ import annotations

import time
import asyncio
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
# DYNAMIC LOADERS
# ============================================================

from core.agents.agent_loader import (
    get_agent_loader,
)

from core.skills.skill_loader import (
    get_skill_loader,
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
    Runtime cognition execution engine.
    """

    def __init__(
        self,
        tool_executor,
    ):

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
        # LOADERS
        # ====================================================

        self.agent_loader = (
            get_agent_loader()
        )

        self.skill_loader = (
            get_skill_loader()
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

        # ====================================================
        # TELEMETRY
        # ====================================================

        self.telemetry = {

            "executed_steps": 0,

            "failed_steps": 0,

            "retried_steps": 0,

            "parallel_steps": 0,

            "total_runtime": 0.0,
        }

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def execute_workflow(
        self,
        query: str,
        workflow_steps: List[Any],
    ) -> WorkflowExecutionResult:

        start_time = time.time()

        memory = (
            self.memory_manager
            .create_memory(
                query=query
            )
        )

        failed_steps = []

        execution_trace = []

        workflow_state = {

            "started_at":
                start_time,

            "status":
                "running",

            "steps_total":
                len(workflow_steps),
        }

        try:

            # =================================================
            # EXECUTION LOOP
            # =================================================

            remaining_steps = (
                workflow_steps.copy()
            )

            while remaining_steps:

                executable_steps = []

                # =============================================
                # FIND READY STEPS
                # =============================================

                for step in remaining_steps:

                    if self._dependencies_satisfied(

                        step,
                        memory,
                    ):

                        executable_steps.append(
                            step
                        )

                if not executable_steps:

                    raise RuntimeError(

                        "Workflow deadlock detected."
                    )

                # =============================================
                # PARALLEL EXECUTION
                # =============================================

                parallel_tasks = []

                for step in executable_steps:

                    if getattr(
                        step,
                        "parallelizable",
                        False,
                    ):

                        parallel_tasks.append(

                            self._execute_step(
                                step,
                                memory,
                            )
                        )

                    else:

                        result = await (
                            self._execute_step(
                                step,
                                memory,
                            )
                        )
                        print("this is result from step execution", result)

                        execution_trace.append(

                            self._build_execution_trace(
                                step,
                                result,
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

                        self.telemetry[
                            "executed_steps"
                        ] += 1

                    remaining_steps.remove(
                        step
                    )

                # =============================================
                # EXECUTE PARALLEL TASKS
                # =============================================

                if parallel_tasks:

                    self.telemetry[
                        "parallel_steps"
                    ] += len(
                        parallel_tasks
                    )

                    parallel_results = (

                        await asyncio.gather(
                            *parallel_tasks,
                            return_exceptions=True,
                        )
                    )

                    for result in (
                        parallel_results
                    ):

                        if isinstance(
                            result,
                            Exception,
                        ):

                            failed_steps.append(

                                {

                                    "error":
                                        str(result)
                                }
                            )

                            continue

                        execution_trace.append(

                            {

                                "parallel":
                                    True,

                                "success":
                                    result.get(
                                        "success",
                                        False,
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

                        self.telemetry[
                            "retried_steps"
                        ] += 1

                        retry_output = (

                            await self
                            ._execute_step(
                                step,
                                memory,
                            )
                        )

                        execution_trace.append(

                            {

                                "retry":
                                    True,

                                "step_id":
                                    step.step_id,

                                "success":
                                    retry_output.get(
                                        "success",
                                        False,
                                    ),
                            }
                        )

            # =================================================
            # AGGREGATION
            # =================================================

            aggregated_output = {

                "query":
                    query,

                "agent_outputs":
                    memory.agent_outputs,

                "execution_trace":
                    execution_trace,

                "artifacts":
                    memory
                    .artifact_manager
                    .export_artifacts(),

                "telemetry":
                    self.telemetry,
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
            # DEBUG VALIDATION
            # =================================================

            debug_result = (
                self.debugger
                .validate_execution(

                    outputs=
                        memory.agent_outputs
                )
            )

            # =================================================
            # FINAL TELEMETRY
            # =================================================

            total_runtime = (
                time.time() - start_time
            )

            self.telemetry[
                "total_runtime"
            ] = total_runtime

            workflow_state[
                "status"
            ] = "completed"

            # =================================================
            # FINAL OUTPUT
            # =================================================

            final_output = {

                "success":
                    True,

                "query":
                    query,

                "workflow_state":
                    workflow_state,

                "agent_outputs":
                    memory.agent_outputs,

                "execution_trace":
                    execution_trace,

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

                "debug":
                    debug_result,

                "telemetry":
                    self.telemetry,

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

            workflow_state[
                "status"
            ] = "failed"

            return WorkflowExecutionResult(

                success=False,

                final_output={

                    "error":
                        str(e),

                    "traceback":
                        traceback
                        .format_exc(),

                    "workflow_state":
                        workflow_state,
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

        step_start = time.time()

        try:

            # =================================================
            # LOAD EXECUTION CONTEXT
            # =================================================

            execution_context = (

                self.agent_loader
                .build_execution_context(

                    workflow_step=step,

                    global_context={

                        "query":
                            memory.query,

                        "shared_context":
                            memory.shared_context,

                        "agent_outputs":
                            memory.agent_outputs,

                        "artifacts":

                            memory
                            .artifact_manager
                            .get_all_artifacts(),
                    },
                )
            )

            if execution_context.get(
                "success"
            ) is False:

                return execution_context

            # =================================================
            # AGENT
            # =================================================

            agent = execution_context[
                "agent"
            ]

            # =================================================
            # LIFECYCLE HOOK
            # =================================================

            if hasattr(
                agent,
                "before_run",
            ):

                await agent.before_run()

            # =================================================
            # EXECUTION CONTEXT
            # =================================================

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

                "skills":
                    execution_context.get(
                        "skills",
                        {},
                    ),

                "runtime_backend":
                    step.runtime_backend,

                "execution_mode":
                    step.execution_mode,
            }

            # =================================================
            # EXECUTION
            # =================================================

            result = await agent.run(
                context
            )

            # =================================================
            # AFTER RUN HOOK
            # =================================================

            if hasattr(
                agent,
                "after_run",
            ):

                await agent.after_run(
                    result
                )

            # =================================================
            # DEBUG VALIDATION
            # =================================================

            debug_validation = (

                self.debugger
                .validate_agent_output(
                    result
                )
            )

            result[
                "debug_validation"
            ] = debug_validation

            # =================================================
            # RUNTIME PROFILING
            # =================================================

            result[
                "runtime_metrics"
            ] = {

                "execution_time":

                    time.time()
                    - step_start,

                "step_id":
                    step.step_id,

                "agent":
                    step.agent,
            }

            # =================================================
            # STORE OUTPUT
            # =================================================

            self.memory_manager.store_agent_output(

                memory=memory,

                step_id=step.step_id,

                agent=step.agent,

                output=result,
            )

            # =================================================
            # STORE ARTIFACT
            # =================================================

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

                    "agent":
                        step.agent,
                },
            )

            # =================================================
            # COMPLETE STEP
            # =================================================

            self.memory_manager.mark_step_completed(

                memory,

                step.step_id,
            )

            return result

        except Exception as e:

            self.telemetry[
                "failed_steps"
            ] += 1

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
    # EXECUTION TRACE
    # ========================================================

    def _build_execution_trace(
        self,
        step,
        result,
    ) -> Dict[str, Any]:

        return {

            "step_id":
                step.step_id,

            "agent":
                step.agent,

            "task":
                step.task,

            "success":
                result.get(
                    "success",
                    False,
                ),

            "execution_mode":
                step.execution_mode,

            "runtime_backend":
                step.runtime_backend,
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