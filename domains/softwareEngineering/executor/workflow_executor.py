# domains/software_engineering/executor/workflow_executor.py

"""
CognitiveOS - Advanced Autonomous Workflow Executor
---------------------------------------------------------

Responsibilities:
- execute workflow steps
- orchestrate agents
- maintain shared memory
- maintain artifacts
- runtime validation
- deterministic debugging
- patch-based self healing
- adaptive retry loops
- artifact-driven cognition
- aggregate outputs

Cognitive Loop:

generate
    ↓
execute
    ↓
validate
    ↓
repair
    ↓
retry
    ↓
reflect
    ↓
aggregate
"""

from __future__ import annotations

import traceback
import time

from typing import (
    Dict,
    Any,
    List,
)

# ============================================================
# AGENTS
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
# TOOLS
# ============================================================

from domains.softwareEngineering.tools.tool_executor import (
    ToolExecutor,
)

# ============================================================
# MEMORY
# ============================================================

from domains.softwareEngineering.memory.shared_memory import (

    SharedMemory,

    SharedMemoryManager,
)

# ============================================================
# ARTIFACTS
# ============================================================

from domains.softwareEngineering.memory.artifacts import (
    ArtifactType,
)

# ============================================================
# SUPERVISOR TYPES
# ============================================================

from domains.softwareEngineering.supervisor.software_supervisor import (
    WorkflowStep,
)

# ============================================================
# RUNTIME SYSTEMS
# ============================================================

from domains.softwareEngineering.runtime.runtime_validator import (
    RuntimeValidator,
)

from domains.softwareEngineering.runtime.deterministic_debugger import (
    DeterministicDebugger,
)

from domains.softwareEngineering.runtime.retry_policy import (
    RetryPolicy,
)

from domains.softwareEngineering.runtime.patch_engine import (
    PatchEngine,
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
        # MEMORY
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
        # RUNTIME SYSTEMS
        # ====================================================

        self.runtime_validator = (
            RuntimeValidator()
        )

        self.runtime_debugger = (
            DeterministicDebugger()
        )

        self.retry_policy = (
            RetryPolicy()
        )

        self.patch_engine = (
            PatchEngine()
        )

        # ====================================================
        # EXECUTION SETTINGS
        # ====================================================

        self.max_reflection_iterations = 1

        self.max_retries = 2

        # ====================================================
        # CACHE
        # ====================================================

        self.agent_cache = {}

        # ====================================================
        # AGENTS
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
            # SHARED CONTEXT
            # =================================================

            memory.shared_context[
                "workflow_steps"
            ] = workflow_steps

            memory.shared_context[
                "execution_mode"
            ] = "balanced"

            memory.shared_context[
                "execution_status"
            ] = "executing"

            memory.shared_context[
                "metrics"
            ] = {

                "total_steps":
                    len(workflow_steps),

                "successful_steps":
                    0,

                "failed_steps":
                    0,

                "runtime_repairs":
                    0,

                "gemini_calls":
                    0,
            }

            # =================================================
            # EXECUTION LOOP
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
                    f"AGENT: {step.agent}"
                )

                print(
                    f"TASK: {step.task}"
                )

                print(
                    "-" * 80
                )

                if not self._dependencies_satisfied(

                    step,

                    memory,
                ):

                    print(
                        "\nDEPENDENCIES FAILED"
                    )

                    memory.shared_context[
                        "metrics"
                    ][
                        "failed_steps"
                    ] += 1

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
            # REFLECTION
            # =================================================

            if memory.failed_steps:

                print(
                    "\n"
                    + "=" * 80
                )

                print(
                    "RUNNING REFLECTION"
                )

                print(
                    "=" * 80
                )

                await self._run_reflection(
                    memory
                )

            # =================================================
            # AGGREGATION
            # =================================================

            final_output = await (
                self._aggregate_outputs(
                    memory
                )
            )

            self.memory_manager.set_final_output(

                memory,

                final_output,
            )

            memory.shared_context[
                "execution_status"
            ] = "completed"

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
    # EXECUTE STEP
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

            return

        try:

            cache_key = (
                f"{memory.query}_{step.task}"
            )

            if cache_key in self.agent_cache:

                print(
                    "\nUSING CACHED OUTPUT"
                )

                result = self.agent_cache[
                    cache_key
                ]

            else:

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

                    "context_artifacts":
                        memory
                        .artifact_manager
                        .get_all_artifacts(),

                    "runtime_repairs":
                        memory
                        .artifact_manager
                        .get_artifacts_by_type(
                            ArtifactType.RUNTIME_REPAIR
                        ),
                }

                start_time = time.time()

                result = await agent.run(
                    context
                )

                execution_time = (
                    time.time()
                    - start_time
                )

                self.agent_cache[
                    cache_key
                ] = result

                if step.agent in [

                    "architecture_agent",

                    "code_agent",

                    "debug_agent",

                    "reflection_agent",
                ]:

                    memory.shared_context[
                        "metrics"
                    ][
                        "gemini_calls"
                    ] += 1

                print(
                    f"\nEXECUTION TIME: {execution_time:.2f}s"
                )

            print(
                "\nAGENT RESULT:\n"
            )

            print(result)

            # =================================================
            # STORE RUNTIME REPAIRS
            # =================================================

            runtime_repairs = result.get(
                "runtime_repairs",
                [],
            )

            for repair in runtime_repairs:

                self.memory_manager.store_artifact(

                    memory=memory,

                    artifact_type=(
                        ArtifactType.RUNTIME_REPAIR
                    ),

                    created_by="patch_engine",

                    content=repair,

                    metadata={

                        "step_id":
                            step.step_id,

                        "agent":
                            agent_name,
                    },
                )

                memory.shared_context[
                    "metrics"
                ][
                    "runtime_repairs"
                ] += 1

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

            if agent_name == "architecture_agent":

                artifact_type = (
                    ArtifactType.ARCHITECTURE
                )

            elif agent_name == "debug_agent":

                artifact_type = (
                    ArtifactType.DEBUG_REPORT
                )

            elif agent_name == "reflection_agent":

                artifact_type = (
                    ArtifactType.REFLECTION
                )

            self.memory_manager.store_artifact(

                memory=memory,

                artifact_type=
                    artifact_type,

                created_by=
                    agent_name,

                content=result,

                metadata={

                    "step_id":
                        step.step_id,

                    "task":
                        step.task,
                },
            )

            # =================================================
            # VALIDATE PYTHON FILES
            # =================================================

            generated_files = result.get(
                "generated_files",
                []
            )

            for generated_file in generated_files:

                file_path = (
                    generated_file.get(
                        "file_path",
                        ""
                    )
                )

                if not file_path.endswith(
                    ".py"
                ):

                    continue

                validation = await (
                    self.runtime_validator
                    .validate_python_file(
                        f"workspace/current_project/{file_path}"
                    )
                )

                print(
                    "\nVALIDATION RESULT:\n"
                )

                print(validation)

                if not validation.get(
                    "success"
                ):

                    await self._handle_runtime_failure(

                        stderr=
                            validation.get(
                                "error",
                                ""
                            ),

                        step=step,

                        memory=memory,
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

                stderr = (
                    execution_validation.get(
                        "stderr",
                        ""
                    )
                )

                return_code = (
                    execution_validation.get(
                        "return_code",
                        0,
                    )
                )

                if stderr or return_code != 0:

                    await self._handle_runtime_failure(

                        stderr=stderr,

                        step=step,

                        memory=memory,
                    )

            # =================================================
            # SUCCESS
            # =================================================

            self.memory_manager.mark_step_completed(

                memory,

                step.step_id,
            )

            memory.shared_context[
                "metrics"
            ][
                "successful_steps"
            ] += 1

        except Exception as e:

            print(
                "\nSTEP EXECUTION FAILED\n"
            )

            print(str(e))

            print(
                traceback.format_exc()
            )

            memory.shared_context[
                "metrics"
            ][
                "failed_steps"
            ] += 1

            self.memory_manager.mark_step_failed(

                memory,

                step.step_id,
            )

    # ========================================================
    # HANDLE RUNTIME FAILURE
    # ========================================================

    async def _handle_runtime_failure(
        self,
        stderr: str,
        step: WorkflowStep,
        memory: SharedMemory,
    ):

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

        # ====================================================
        # PATCH ENGINE
        # ====================================================

        patch_result = await (
            self.patch_engine
            .patch_runtime_failure(

                file_path=(
                    "workspace/current_project/app/main.py"
                ),

                stderr=stderr,
            )
        )

        print(
            "\nPATCH ENGINE RESULT:\n"
        )

        print(
            patch_result
        )

        if patch_result.get(
            "patched",
            False,
        ):

            self.memory_manager.store_artifact(

                memory=memory,

                artifact_type=(
                    ArtifactType.RUNTIME_REPAIR
                ),

                created_by="patch_engine",

                content=patch_result,
            )

            print(
                "\nPATCH ENGINE SUCCESSFULLY REPAIRED FAILURE"
            )

            return

        # ====================================================
        # DETERMINISTIC DEBUGGING
        # ====================================================

        deterministic_result = await (
            self.runtime_debugger
            .debug_runtime_failure(
                stderr
            )
        )

        print(
            "\nDETERMINISTIC DEBUG RESULT:\n"
        )

        print(deterministic_result)

        if deterministic_result.get(
            "resolved"
        ):

            print(
                "\nAUTO-RECOVERY SUCCESSFUL"
            )

            memory.shared_context[
                "metrics"
            ][
                "runtime_repairs"
            ] += 1

            return

        # ====================================================
        # RETRY POLICY
        # ====================================================

        should_retry = (
            self.retry_policy
            .should_retry(
                stderr=stderr,
                retry_count=1,
            )
        )

        if not should_retry:

            print(
                "\nNO RETRY REQUIRED"
            )

            return

        # ====================================================
        # ESCALATE TO DEBUG AGENT
        # ====================================================

        print(
            "\nESCALATING TO DEBUG AGENT"
        )

        memory.shared_context[
            "latest_runtime_failure"
        ] = stderr

        debug_step = WorkflowStep(

            step_id=999,

            agent="debug_agent",

            task=(
                "Fix runtime failures "
                "and improve production stability"
            ),

            dependencies=[],

            parallelizable=False,

            expected_output=(
                "Patched implementation"
            ),
        )

        await self._execute_step(

            debug_step,

            memory,
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

            return

        try:

            reflection_input = {

                "query":
                    memory.query,

                "agent_outputs":
                    memory.agent_outputs,

                "artifacts":
                    memory
                    .artifact_manager
                    .get_all_artifacts(),

                "runtime_repairs":
                    memory
                    .artifact_manager
                    .get_artifacts_by_type(
                        ArtifactType.RUNTIME_REPAIR
                    ),
            }

            result = await (
                reflection_agent.run(
                    reflection_input
                )
            )

            print(
                "\nREFLECTION RESULT:\n"
            )

            print(result)

            self.memory_manager.store_reflection(

                memory,

                str(result),
            )

        except Exception as e:

            print(
                "\nREFLECTION FAILED\n"
            )

            print(str(e))

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

                "artifacts":
                    memory
                    .artifact_manager
                    .get_all_artifacts(),

                "runtime_repairs":
                    memory
                    .artifact_manager
                    .get_artifacts_by_type(
                        ArtifactType.RUNTIME_REPAIR
                    ),

                "metrics":
                    memory.shared_context.get(
                        "metrics",
                        {},
                    ),
            }

            result = await (
                aggregator.run(
                    aggregation_input
                )
            )

            print(
                "\nFINAL OUTPUT:\n"
            )

            print(result)

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