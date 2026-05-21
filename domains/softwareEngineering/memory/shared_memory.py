# domains/software_engineering/memory/shared_memory.py

"""
CognitiveOS - Advanced Shared Memory
---------------------------------------------------------

Responsibilities:
- maintain workflow cognition
- preserve execution history
- enable inter-agent collaboration
- store artifacts
- track runtime repairs
- track patch history
- maintain execution metrics
- support autonomous retries
- maintain workspace intelligence

This becomes the REAL cognitive workspace.
"""

from __future__ import annotations

import uuid

from datetime import datetime

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    Dict,
    Any,
    List,
    Optional,
)

# ============================================================
# IMPORT ARTIFACT SYSTEM
# ============================================================

from domains.softwareEngineering.memory.artifacts import (

    Artifact,

    ArtifactManager,
)

# ============================================================
# EXECUTION LOG
# ============================================================


@dataclass
class ExecutionLog:

    step_id: int

    agent: str

    status: str

    timestamp: str

    details: Dict[str, Any] = field(
        default_factory=dict
    )


# ============================================================
# SHARED MEMORY
# ============================================================


@dataclass
class SharedMemory:

    # ========================================================
    # CORE WORKFLOW
    # ========================================================

    workflow_id: str

    query: str

    created_at: str

    # ========================================================
    # EXECUTION STATE
    # ========================================================

    current_step: Optional[int] = None

    completed_steps: List[int] = field(
        default_factory=list
    )

    failed_steps: List[int] = field(
        default_factory=list
    )

    active_agents: List[str] = field(
        default_factory=list
    )

    retry_count: int = 0

    max_retries: int = 3

    # ========================================================
    # AGENT OUTPUTS
    # ========================================================

    agent_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    # ========================================================
    # SHARED CONTEXT
    # ========================================================

    shared_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    # ========================================================
    # ARTIFACTS
    # ========================================================

    artifact_manager: ArtifactManager = field(
        default_factory=ArtifactManager
    )

    # ========================================================
    # REFLECTIONS
    # ========================================================

    reflection_notes: List[
        str
    ] = field(default_factory=list)

    # ========================================================
    # EXECUTION LOGS
    # ========================================================

    execution_logs: List[
        ExecutionLog
    ] = field(default_factory=list)

    # ========================================================
    # RUNTIME REPAIRS
    # ========================================================

    runtime_repairs: List[
        Dict[str, Any]
    ] = field(default_factory=list)

    # ========================================================
    # PATCH HISTORY
    # ========================================================

    patch_history: List[
        Dict[str, Any]
    ] = field(default_factory=list)

    # ========================================================
    # DEPENDENCY INSTALLS
    # ========================================================

    installed_dependencies: List[
        str
    ] = field(default_factory=list)

    # ========================================================
    # EXECUTION METRICS
    # ========================================================

    metrics: Dict[
        str,
        Any,
    ] = field(
        default_factory=lambda: {

            "steps_executed": 0,

            "successful_steps": 0,

            "failed_steps": 0,

            "runtime_repairs": 0,

            "patches_applied": 0,

            "execution_time_seconds": 0,
        }
    )

    # ========================================================
    # WORKSPACE STATE
    # ========================================================

    workspace_snapshot: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    final_output: Optional[str] = None

    # ========================================================
    # METADATA
    # ========================================================

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# MEMORY MANAGER
# ============================================================


class SharedMemoryManager:

    """
    Advanced cognitive memory manager.
    """

    # ========================================================
    # CREATE MEMORY
    # ========================================================

    def create_memory(
        self,
        query: str,
    ) -> SharedMemory:

        return SharedMemory(

            workflow_id=str(
                uuid.uuid4()
            ),

            query=query,

            created_at=(
                datetime.utcnow().isoformat()
            ),
        )

    # ========================================================
    # STORE AGENT OUTPUT
    # ========================================================

    def store_agent_output(

        self,

        memory: SharedMemory,

        step_id: int,

        agent: str,

        output: Any,
    ):

        memory.agent_outputs[
            f"step_{step_id}"
        ] = {

            "agent":
                agent,

            "output":
                output,

            "timestamp":
                datetime.utcnow().isoformat(),
        }

        memory.metrics[
            "steps_executed"
        ] += 1

    # ========================================================
    # STORE RUNTIME REPAIR
    # ========================================================

    def store_runtime_repair(

        self,

        memory: SharedMemory,

        repair: Dict[str, Any],
    ):

        memory.runtime_repairs.append(
            repair
        )

        memory.metrics[
            "runtime_repairs"
        ] += 1

    # ========================================================
    # STORE PATCH
    # ========================================================

    def store_patch(

        self,

        memory: SharedMemory,

        patch_data: Dict[str, Any],
    ):

        memory.patch_history.append(
            patch_data
        )

        memory.metrics[
            "patches_applied"
        ] += 1

    # ========================================================
    # STORE INSTALLED DEPENDENCY
    # ========================================================

    def store_dependency_install(

        self,

        memory: SharedMemory,

        dependency: str,
    ):

        if (
            dependency
            not in memory.installed_dependencies
        ):

            memory.installed_dependencies.append(
                dependency
            )

    # ========================================================
    # UPDATE WORKSPACE SNAPSHOT
    # ========================================================

    def update_workspace_snapshot(

        self,

        memory: SharedMemory,

        snapshot: Dict[str, Any],
    ):

        memory.workspace_snapshot = (
            snapshot
        )

    # ========================================================
    # STORE ARTIFACT
    # ========================================================

    def store_artifact(

        self,

        memory: SharedMemory,

        artifact_type: str,

        created_by: str,

        content: Any,

        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return (
            memory.artifact_manager
            .create_artifact(

                artifact_type=
                    artifact_type,

                created_by=
                    created_by,

                content=
                    content,

                metadata=
                    metadata or {},
            )
        )

    # ========================================================
    # STORE EXECUTION ARTIFACT
    # ========================================================

    def store_execution_artifact(

        self,

        memory: SharedMemory,

        created_by: str,

        stdout: str,

        stderr: str,

        return_code: int,

        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return (
            memory.artifact_manager
            .create_execution_artifact(

                created_by=
                    created_by,

                stdout=
                    stdout,

                stderr=
                    stderr,

                return_code=
                    return_code,

                metadata=
                    metadata or {},
            )
        )

    # ========================================================
    # STORE REFLECTION
    # ========================================================

    def store_reflection(

        self,

        memory: SharedMemory,

        reflection: str,
    ):

        memory.reflection_notes.append(
            reflection
        )

    # ========================================================
    # STORE EXECUTION LOG
    # ========================================================

    def store_execution_log(

        self,

        memory: SharedMemory,

        step_id: int,

        agent: str,

        status: str,

        details: Optional[
            Dict[str, Any]
        ] = None,
    ):

        log = ExecutionLog(

            step_id=step_id,

            agent=agent,

            status=status,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            details=details or {},
        )

        memory.execution_logs.append(
            log
        )

    # ========================================================
    # STEP COMPLETION
    # ========================================================

    def mark_step_completed(

        self,

        memory: SharedMemory,

        step_id: int,
    ):

        if (
            step_id
            not in memory.completed_steps
        ):

            memory.completed_steps.append(
                step_id
            )

        memory.metrics[
            "successful_steps"
        ] += 1

    # ========================================================
    # STEP FAILURE
    # ========================================================

    def mark_step_failed(

        self,

        memory: SharedMemory,

        step_id: int,
    ):

        if (
            step_id
            not in memory.failed_steps
        ):

            memory.failed_steps.append(
                step_id
            )

        memory.metrics[
            "failed_steps"
        ] += 1

    # ========================================================
    # ACTIVE AGENTS
    # ========================================================

    def register_active_agent(

        self,

        memory: SharedMemory,

        agent_name: str,
    ):

        if (
            agent_name
            not in memory.active_agents
        ):

            memory.active_agents.append(
                agent_name
            )

    def remove_active_agent(

        self,

        memory: SharedMemory,

        agent_name: str,
    ):

        if (
            agent_name
            in memory.active_agents
        ):

            memory.active_agents.remove(
                agent_name
            )

    # ========================================================
    # CURRENT STEP
    # ========================================================

    def set_current_step(

        self,

        memory: SharedMemory,

        step_id: int,
    ):

        memory.current_step = step_id

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    def set_final_output(

        self,

        memory: SharedMemory,

        output: str,
    ):

        memory.final_output = output

    # ========================================================
    # EXPORT SNAPSHOT
    # ========================================================

    def export_memory_snapshot(

        self,

        memory: SharedMemory,
    ) -> Dict[str, Any]:

        return {

            "workflow_id":
                memory.workflow_id,

            "query":
                memory.query,

            "created_at":
                memory.created_at,

            "completed_steps":
                memory.completed_steps,

            "failed_steps":
                memory.failed_steps,

            "active_agents":
                memory.active_agents,

            "retry_count":
                memory.retry_count,

            "agent_outputs":
                memory.agent_outputs,

            "shared_context":
                memory.shared_context,

            "runtime_repairs":
                memory.runtime_repairs,

            "patch_history":
                memory.patch_history,

            "installed_dependencies":
                memory.installed_dependencies,

            "workspace_snapshot":
                memory.workspace_snapshot,

            "metrics":
                memory.metrics,

            "artifacts":
                (
                    memory
                    .artifact_manager
                    .export_artifacts()
                ),

            "reflection_notes":
                memory.reflection_notes,

            "execution_logs": [

                {

                    "step_id":
                        log.step_id,

                    "agent":
                        log.agent,

                    "status":
                        log.status,

                    "timestamp":
                        log.timestamp,

                    "details":
                        log.details,
                }

                for log in memory.execution_logs
            ],

            "final_output":
                memory.final_output,
        }