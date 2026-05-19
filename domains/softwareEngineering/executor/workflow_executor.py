# domains/software_engineering/executor/workflow_executor.py

"""
CognitiveOS - Workflow Executor
---------------------------------------------------------

Responsibilities:
- execute workflow steps
- invoke agents
- provide tools to agents
- maintain shared memory
- run adaptive retry loops
- invoke reflection cycles
- aggregate outputs
- store artifacts
- maintain runtime cognition

Cognitive Loop:

generate
    ↓
execute
    ↓
reflect
    ↓
retry failed steps
    ↓
improve outputs
    ↓
re-reflect
    ↓
finalize
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

from domains.software_engineering.agents.architecture_agent import (
    ArchitectureAgent,
)

from domains.software_engineering.agents.code_agent import (
    CodeAgent,
)

from domains.software_engineering.agents.debug_agent import (
    DebugAgent,
)

from domains.software_engineering.agents.reflection_agent import (
    ReflectionAgent,
)

from domains.software_engineering.agents.aggregator_agent import (
    AggregatorAgent,
)

# ============================================================
# IMPORT TOOL EXECUTOR
# ============================================================

from domains.software_engineering.tools.tool_executor import (
    ToolExecutor,
)

# ============================================================
# IMPORT MEMORY
# ============================================================

from domains.software_engineering.memory.shared_memory import (

    SharedMemory,

    SharedMemoryManager,
)

# ============================================================
# IMPORT SUPERVISOR TYPES
# ============================================================

from domains.software_engineering.supervisor.software_supervisor import (
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
        memory_snapshot: Dict[str, Any],
    ):

        self.success = success

        self.final_output = final_output

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
            self.memory_manager.create_memory(
                query=query
            )
        )

        try:

            # =================================================
            # STORE WORKFLOW
            # =================================================

            memory.shared_context[
                "workflow_steps"
            ] = workflow_steps

            # =================================================
            # INITIAL EXECUTION
            # =================================================

            for step in workflow_steps:

                if not self._dependencies_satisfied(
                    step,
                    memory,
                ):

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

            for iteration in range(
                self.max_reflection_iterations
            ):

                reflection_result = await (
                    self._run_reflection(
                        memory
                    )
                )

                if not reflection_result:
                    break

                retry_required = (
                    reflection_result.get(
                        "retry_required",
                        False,
                    )
                )

                if not retry_required:
                    break

                retry_steps = (
                    reflection_result.get(
                        "retry_steps",
                        [],
                    )
                )

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
            # EXPORT MEMORY SNAPSHOT
            # =================================================

            snapshot = (
                self.memory_manager
                .export_memory_snapshot(
                    memory
                )
            )

            return WorkflowExecutionResult(

                success=True,

                final_output=final_output,

                memory_snapshot=snapshot,
            )

        # ====================================================
        # GLOBAL FAILURE
        # ====================================================

        except Exception as e:

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

            self.memory_manager.mark_step_failed(
                memory,
                step.step_id,
            )

            return

        try:

            # =================================================
            # REGISTER ACTIVE AGENT
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
            }

            # =================================================
            # EXECUTE AGENT
            # =================================================

            result = await agent.run(
                context
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
            # STORE ARTIFACT
            # =================================================

            self.memory_manager.store_artifact(

                memory=memory,

                artifact_type="agent_output",

                created_by=agent_name,

                content=result,

                metadata={

                    "step_id":
                        step.step_id,

                    "task":
                        step.task,
                },
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

                step_id=step.step_id,

                agent=agent_name,

                status="completed",

                details={

                    "task":
                        step.task,
                },
            )

            # =================================================
            # REMOVE ACTIVE AGENT
            # =================================================

            self.memory_manager.remove_active_agent(

                memory,

                agent_name,
            )

        except Exception as e:

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
                    memory.artifacts,
            }

            reflection_result = await (
                reflection_agent.run(
                    reflection_input
                )
            )

            self.memory_manager.store_reflection(

                memory,

                str(reflection_result),
            )

            return reflection_result

        except Exception:

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

        for retry in retry_steps:

            step_id = retry.get(
                "step_id"
            )

            improvement_action = retry.get(
                "improvement_action",
                "",
            )

            step = step_lookup.get(
                step_id
            )

            if not step:
                continue

            # ================================================
            # STORE RETRY CONTEXT
            # ================================================

            memory.shared_context[
                "retry_context"
            ] = {

                "step_id":
                    step_id,

                "improvement_action":
                    improvement_action,
            }

            # ================================================
            # EXECUTION LOG
            # ================================================

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

            # ================================================
            # RE-EXECUTE STEP
            # ================================================

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
                    memory.artifacts,
            }

            result = await (
                aggregator.run(
                    aggregation_input
                )
            )

            return str(result)

        except Exception:

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