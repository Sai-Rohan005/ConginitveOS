# domains/software_engineering/executor/workflow_executor.py

"""
CognitiveOS - Advanced Workflow Executor
---------------------------------------------------------

Responsibilities:
- execute workflow steps
- orchestrate agents
- inject tools
- maintain runtime cognition
- manage shared memory
- maintain artifacts
- run adaptive reflection loops
- retry failed executions
- validate runtime execution
- aggregate outputs

Cognitive Loop:

generate
    ↓
execute
    ↓
validate
    ↓
reflect
    ↓
retry
    ↓
improve
    ↓
aggregate
"""

from __future__ import annotations

import traceback

from typing import (
    Dict,
    Any,
    List,
)

# ============================================================
# IMPORT AGENTS
# ============================================================

from domains.softwareEngineering.agents.architecture_agent import (
    ArchitectureAgent,
)

from domains.softwareEngineering.agents.code_agent import (
    CodeAgent,
)

from domains.softwareEngineering.agents.debug_agent import (
    DebugAgent,
)

from domains.softwareEngineering.agents.reflection_agent import (
    ReflectionAgent,
)

from domains.softwareEngineering.agents.aggregator_agent import (
    AggregatorAgent,
)

# ============================================================
# IMPORT TOOL EXECUTOR
# ============================================================

from domains.softwareEngineering.tools.tool_executor import (
    ToolExecutor,
)

# ============================================================
# IMPORT MEMORY
# ============================================================

from domains.softwareEngineering.memory.shared_memory import (

    SharedMemory,

    SharedMemoryManager,
)

# ============================================================
# IMPORT ARTIFACT TYPES
# ============================================================

from domains.softwareEngineering.memory.artifacts import (
    ArtifactType,
)

# ============================================================
# IMPORT SUPERVISOR TYPES
# ============================================================

from domains.softwareEngineering.supervisor.softwareEngineeringSupervisor import (
    WorkflowStep,
)

# ============================================================
# EXECUTION RESULT
# ============================================================


class WorkflowExecutionResult:

    def __init__(

        self,

        success: bool,

        final_output: str,

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

    def __init__(self):

        # ====================================================
        # MEMORY MANAGER
        # ====================================================

        self.memory_manager = (
            SharedMemoryManager()
        )

        # ====================================================
        # TOOL EXECUTOR
        # ====================================================

        self.tool_executor = (
            ToolExecutor()
        )

        # ====================================================
        # MAX REFLECTION ITERATIONS
        # ====================================================

        self.max_reflection_iterations = 2

        # ====================================================
        # AGENT REGISTRY
        # ====================================================

        self.agent_registry = {

            "architecture_agent":
                ArchitectureAgent(),

            "code_agent":
                CodeAgent(),

            "debug_agent":
                DebugAgent(),

            "reflection_agent":
                ReflectionAgent(),

            "aggregator_agent":
                AggregatorAgent(),
        }

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def execute_workflow(
        self,
        query: str,
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> WorkflowExecutionResult:

        # ====================================================
        # CREATE MEMORY
        # ====================================================

        memory = (
            self.memory_manager
            .create_memory(
                query=query
            )
        )

        try:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "WORKFLOW EXECUTION STARTED"
            )

            print(
                "=" * 80
            )

            # =================================================
            # STORE WORKFLOW
            # =================================================

            memory.shared_context[
                "workflow_steps"
            ] = workflow_steps

            memory.shared_context[
                "execution_status"
            ] = "executing"

            memory.shared_context[
                "retry_history"
            ] = {}

            # =================================================
            # INITIAL EXECUTION
            # =================================================

            for step in workflow_steps:

                print(
                    "\n"
                    + "-" * 80
                )

                print(
                    f"EXECUTING STEP {step.step_id}"
                )

                print(
                    "-" * 80
                )

                if not self._dependencies_satisfied(

                    step,

                    memory,
                ):

                    print(
                        "\nDEPENDENCIES NOT SATISFIED"
                    )

                    self.memory_manager.mark_step_failed(

                        memory,

                        step.step_id,
                    )

                    continue

                await self._execute_step(

                    step,

                    memory,
                )

            # =================================================
            # REFLECTION LOOP
            # =================================================

            memory.shared_context[
                "execution_status"
            ] = "reflecting"

            for iteration in range(

                self.max_reflection_iterations
            ):

                print(
                    "\n"
                    + "=" * 80
                )

                print(
                    f"REFLECTION ITERATION {iteration + 1}"
                )

                print(
                    "=" * 80
                )

                reflection_result = await (
                    self._run_reflection(
                        memory
                    )
                )

                if not reflection_result:

                    print(
                        "\nNO REFLECTION RESULT"
                    )

                    break

                retry_required = (
                    reflection_result.get(
                        "retry_required",
                        False,
                    )
                )

                if not retry_required:

                    print(
                        "\nNO RETRY REQUIRED"
                    )

                    break

                retry_steps = (
                    reflection_result.get(
                        "retry_steps",
                        [],
                    )
                )

                print(
                    "\nRETRY STEPS:\n"
                )

                print(retry_steps)

                memory.shared_context[
                    "execution_status"
                ] = "retrying"

                await self._retry_failed_steps(

                    retry_steps=
                        retry_steps,

                    workflow_steps=
                        workflow_steps,

                    memory=memory,
                )

            # =================================================
            # FINAL AGGREGATION
            # =================================================

            memory.shared_context[
                "execution_status"
            ] = "aggregating"

            final_output = await (
                self._aggregate_outputs(
                    memory
                )
            )

            # =================================================
            # STORE FINAL OUTPUT
            # =================================================

            self.memory_manager.set_final_output(

                memory,

                final_output,
            )

            # =================================================
            # UPDATE STATUS
            # ====================================================

            memory.shared_context[
                "execution_status"
            ] = "completed"

            # =================================================
            # EXPORT SNAPSHOT
            # ====================================================

            snapshot = (

                self.memory_manager
                .export_memory_snapshot(
                    memory
                )
            )

            print(
                "\n"
                + "=" * 80
            )

            print(
                "WORKFLOW EXECUTION COMPLETED"
            )

            print(
                "=" * 80
            )

            return WorkflowExecutionResult(

                success=True,

                final_output=(
                    final_output
                ),

                memory_snapshot=(
                    snapshot
                ),
            )

        # ====================================================
        # GLOBAL FAILURE
        # ====================================================

        except Exception as e:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "WORKFLOW EXECUTION FAILED"
            )

            print(
                "=" * 80
            )

            print(str(e))

            print(
                traceback.format_exc()
            )

            return WorkflowExecutionResult(

                success=False,

                final_output=f"""
Workflow execution failed.

Error:
{str(e)}

Traceback:
{traceback.format_exc()}
""",

                memory_snapshot={}
            )

    # ========================================================
    # EXECUTE SINGLE STEP
    # ========================================================

    async def _execute_step(
        self,
        step: WorkflowStep,
        memory: SharedMemory,
    ):

        agent_name = step.agent

        agent = self.agent_registry.get(
            agent_name
        )

        if not agent:

            print(
                f"\nUNKNOWN AGENT: {agent_name}"
            )

            self.memory_manager.mark_step_failed(

                memory,

                step.step_id,
            )

            return

        try:

            # =================================================
            # ACTIVE AGENT
            # =================================================

            self.memory_manager.register_active_agent(

                memory,

                agent_name,
            )

            self.memory_manager.set_current_step(

                memory,

                step.step_id,
            )

            # =================================================
            # EXECUTION TIMELINE
            # =================================================

            memory.shared_context.setdefault(
                "execution_timeline",
                [],
            )

            memory.shared_context[
                "execution_timeline"
            ].append(

                {

                    "event":
                        "agent_started",

                    "agent":
                        agent_name,

                    "step":
                        step.step_id,
                }
            )

            # =================================================
            # CONTEXT ARTIFACTS
            # =================================================

            context_artifacts = (

                memory
                .artifact_manager
                .get_all_artifacts()
            )

            # =================================================
            # BUILD CONTEXT
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

                "reflection_notes":
                    memory.reflection_notes,

                "tool_executor":
                    self.tool_executor,

                "retry_context":
                    memory.shared_context.get(
                        "retry_context",
                        {},
                    ),

                "context_artifacts":
                    context_artifacts,
            }

            print(
                f"\nEXECUTING AGENT: {agent_name}"
            )

            print(
                f"TASK: {step.task}"
            )

            # =================================================
            # EXECUTE AGENT
            # =================================================

            result = await agent.run(
                context
            )

            print(
                "\nAGENT RESULT:\n"
            )

            print(result)

            # =================================================
            # STORE WORKSPACE SNAPSHOT
            # =================================================

            workspace_snapshot = await (
                self.tool_executor.execute_tool(
                    "tree",
                    {},
                )
            )

            self.memory_manager.store_artifact(

                memory=memory,

                artifact_type=
                    "workspace_snapshot",

                created_by=
                    agent_name,

                content=
                    workspace_snapshot,
            )

            # =================================================
            # STORE OUTPUT
            # =================================================

            self.memory_manager.store_agent_output(

                memory=memory,

                step_id=step.step_id,

                agent=agent_name,

                output=result,
            )

            # =================================================
            # ARTIFACT TYPE
            # =================================================

            artifact_type = (
                ArtifactType.CODE
            )

            if (
                agent_name
                == "architecture_agent"
            ):

                artifact_type = (
                    ArtifactType.ARCHITECTURE
                )

            elif (
                agent_name
                == "debug_agent"
            ):

                artifact_type = (
                    ArtifactType.DEBUG_REPORT
                )

            elif (
                agent_name
                == "reflection_agent"
            ):

                artifact_type = (
                    ArtifactType.REFLECTION
                )

            # =================================================
            # STORE MAIN ARTIFACT
            # =================================================

            self.memory_manager.store_artifact(

                memory=memory,

                artifact_type=
                    artifact_type,

                created_by=
                    agent_name,

                content=
                    result,

                metadata={

                    "step_id":
                        step.step_id,

                    "task":
                        step.task,
                },
            )

            # =================================================
            # EXECUTION VALIDATION
            # =================================================

            execution_validation = (
                result.get(
                    "execution_validation",
                    {}
                )
            )

            if execution_validation:

                stdout = (
                    execution_validation.get(
                        "stdout",
                        "",
                    )
                )

                stderr = (
                    execution_validation.get(
                        "stderr",
                        "",
                    )
                )

                return_code = (
                    execution_validation.get(
                        "return_code",
                        -1,
                    )
                )

                # =============================================
                # STORE EXECUTION ARTIFACT
                # =============================================

                self.memory_manager.store_execution_artifact(

                    memory=memory,

                    created_by=
                        agent_name,

                    stdout=
                        stdout,

                    stderr=
                        stderr,

                    return_code=
                        return_code,
                )

                # =============================================
                # AUTO DEBUGGING
                # =============================================

                if stderr or return_code != 0:

                    print(
                        "\n"
                        + "=" * 80
                    )

                    print(
                        "RUNTIME FAILURE DETECTED"
                    )

                    print(
                        "=" * 80
                    )

                    print(stderr)

                    memory.shared_context[
                        "execution_timeline"
                    ].append(

                        {

                            "event":
                                "runtime_failure",

                            "agent":
                                agent_name,

                            "step":
                                step.step_id,

                            "stderr":
                                stderr,
                        }
                    )

                    # =========================================
                    # DEBUG STEP
                    # =========================================

                    debug_step = WorkflowStep(

                        step_id=999,

                        agent="debug_agent",

                        task=(
                            "Debug runtime failures "
                            "and patch implementation"
                        ),

                        dependencies=[],

                        parallelizable=False,

                        expected_output=(
                            "Patched production-ready system"
                        ),
                    )

                    await self._execute_step(

                        debug_step,

                        memory,
                    )

                    # =========================================
                    # RE-RUN PROJECT
                    # =========================================

                    print(
                        "\nRE-RUNNING PROJECT AFTER PATCH\n"
                    )

                    rerun_result = await (
                        self.tool_executor.execute_tool(

                            "run_project",

                            {

                                "entry_file":
                                    "app/main.py"
                            },
                        )
                    )

                    print(
                        "\nRERUN RESULT:\n"
                    )

                    print(rerun_result)

                    rerun_output = (
                        rerun_result.get(
                            "output",
                            {}
                        )
                    )

                    self.memory_manager.store_execution_artifact(

                        memory=memory,

                        created_by=
                            "runtime_validator",

                        stdout=
                            rerun_output.get(
                                "stdout",
                                "",
                            ),

                        stderr=
                            rerun_output.get(
                                "stderr",
                                "",
                            ),

                        return_code=
                            rerun_output.get(
                                "return_code",
                                -1,
                            ),
                    )

                    memory.shared_context[
                        "execution_timeline"
                    ].append(

                        {

                            "event":
                                "project_rerun",

                            "step":
                                step.step_id,

                            "success":
                                rerun_result.get(
                                    "success",
                                    False,
                                ),
                        }
                    )

            # =================================================
            # MARK COMPLETE
            # =================================================

            self.memory_manager.mark_step_completed(

                memory,

                step.step_id,
            )

            # =================================================
            # EXECUTION LOG
            # =================================================

            self.memory_manager.store_execution_log(

                memory=memory,

                step_id=
                    step.step_id,

                agent=
                    agent_name,

                status=
                    "completed",

                details={

                    "task":
                        step.task,
                },
            )

            # =================================================
            # EXECUTION TIMELINE
            # =================================================

            memory.shared_context[
                "execution_timeline"
            ].append(

                {

                    "event":
                        "agent_completed",

                    "agent":
                        agent_name,

                    "step":
                        step.step_id,
                }
            )

            # =================================================
            # REMOVE ACTIVE AGENT
            # =================================================

            self.memory_manager.remove_active_agent(

                memory,

                agent_name,
            )

        # ====================================================
        # FAILURE HANDLING
        # ====================================================

        except Exception as e:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "AGENT EXECUTION FAILED"
            )

            print(
                "=" * 80
            )

            print(
                f"Agent: {agent_name}"
            )

            print(
                f"Step: {step.step_id}"
            )

            print(str(e))

            print(
                traceback.format_exc()
            )

            memory.shared_context[
                "execution_timeline"
            ].append(

                {

                    "event":
                        "agent_failed",

                    "agent":
                        agent_name,

                    "step":
                        step.step_id,

                    "error":
                        str(e),
                }
            )

            self.memory_manager.mark_step_failed(

                memory,

                step.step_id,
            )

            self.memory_manager.store_execution_log(

                memory=memory,

                step_id=step.step_id,

                agent=agent_name,

                status="failed",

                details={

                    "error":
                        str(e),
                },
            )
    # ========================================================
    # REFLECTION
    # ========================================================

    async def _run_reflection(
        self,
        memory: SharedMemory,
    ):

        reflection_agent = (
            self.agent_registry.get(
                "reflection_agent"
            )
        )

        if not reflection_agent:

            return None

        try:

            reflection_input = {

                "query":
                    memory.query,

                "agent_outputs":
                    memory.agent_outputs,

                "artifacts":
                    (
                        memory
                        .artifact_manager
                        .get_all_artifacts()
                    ),
            }

            reflection_result = await (
                reflection_agent.run(
                    reflection_input
                )
            )

            print(
                "\nREFLECTION RESULT:\n"
            )

            print(reflection_result)

            self.memory_manager.store_reflection(

                memory,

                str(reflection_result),
            )

            self.memory_manager.store_reflection_artifact(

                memory=memory,

                created_by=
                    "reflection_agent",

                content=
                    reflection_result,

                retry_required=
                    reflection_result.get(
                        "retry_required",
                        False,
                    ),

                retry_steps=
                    reflection_result.get(
                        "retry_steps",
                        [],
                    ),

                quality_score=
                    reflection_result.get(
                        "quality_score",
                        "medium",
                    ),
            )

            return reflection_result

        except Exception as e:

            print(
                "\nREFLECTION FAILED\n"
            )

            print(str(e))

            return None

    # ========================================================
    # RETRY LOOP
    # ========================================================

    async def _retry_failed_steps(
        self,
        retry_steps,
        workflow_steps,
        memory,
    ):

        step_lookup = {

            step.step_id: step

            for step in workflow_steps
        }

        retry_history = (
            memory.shared_context.get(
                "retry_history",
                {},
            )
        )

        for retry in retry_steps:

            step_id = retry.get(
                "step_id"
            )

            improvement_action = retry.get(
                "improvement_action",
                "",
            )

            retry_count = retry_history.get(
                step_id,
                0,
            )

            # =================================================
            # PREVENT INFINITE RETRIES
            # =================================================

            if retry_count >= 2:

                print(
                    f"\nSKIPPING STEP {step_id}"
                )

                continue

            retry_history[
                step_id
            ] = retry_count + 1

            step = step_lookup.get(
                step_id
            )

            if not step:
                continue

            # =================================================
            # STORE RETRY CONTEXT
            # =================================================

            memory.shared_context[
                "retry_context"
            ] = {

                "step_id":
                    step_id,

                "improvement_action":
                    improvement_action,
            }

            # =================================================
            # EXECUTION LOG
            # =================================================

            self.memory_manager.store_execution_log(

                memory=memory,

                step_id=step_id,

                agent=step.agent,

                status="retrying",

                details={

                    "improvement_action":
                        improvement_action,
                },
            )

            print(
                f"\nRETRYING STEP {step_id}"
            )

            await self._execute_step(
                step,
                memory,
            )

    # ========================================================
    # AGGREGATION
    # ========================================================

    async def _aggregate_outputs(
        self,
        memory: SharedMemory,
    ) -> str:

        aggregator = (
            self.agent_registry.get(
                "aggregator_agent"
            )
        )

        if not aggregator:

            return str(
                memory.agent_outputs
            )

        try:

            aggregation_input = {

                "query":
                    memory.query,

                "agent_outputs":
                    memory.agent_outputs,

                "reflection_notes":
                    memory.reflection_notes,

                "artifacts":
                    (
                        memory
                        .artifact_manager
                        .get_all_artifacts()
                    ),
            }

            print(
                "\nAGGREGATION INPUT:\n"
            )

            print(
                aggregation_input
            )

            result = await (
                aggregator.run(
                    aggregation_input
                )
            )

            print(
                "\nFINAL AGGREGATED OUTPUT:\n"
            )

            print(result)

            if isinstance(
                result,
                str,
            ):

                return result

            if isinstance(
                result,
                dict,
            ):

                return result.get(
                    "final_output",
                    str(result),
                )

            return str(result)

        except Exception as e:

            print(
                "\nAGGREGATION FAILED\n"
            )

            print(str(e))

            return str(
                memory.agent_outputs
            )

    # ========================================================
    # DEPENDENCY CHECK
    # ========================================================

    def _dependencies_satisfied(
        self,
        step: WorkflowStep,
        memory: SharedMemory,
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