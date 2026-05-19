# domains/software_engineering/memory/shared_memory.py

"""
CognitiveOS - Shared Memory
---------------------------------------------------------

Responsibilities:
- maintain workflow state
- store agent outputs
- preserve execution history
- maintain shared context
- support inter-agent communication
- track artifacts
- store reflections
- maintain execution logs

This becomes the cognitive workspace
for the entire workflow runtime.
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

from domains.software_engineering.memory.artifacts import (

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
    # ARTIFACT MANAGER
    # ========================================================

    artifact_manager: ArtifactManager = field(
        default_factory=ArtifactManager
    )

    # ========================================================
    # REFLECTION
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
    Centralized cognitive memory manager.
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

            "agent": agent,

            "output": output,

            "timestamp":
                datetime.utcnow().isoformat(),
        }

    # ========================================================
    # GET AGENT OUTPUT
    # ========================================================

    def get_agent_output(
        self,
        memory: SharedMemory,
        step_id: int,
    ):

        return memory.agent_outputs.get(
            f"step_{step_id}"
        )

    # ========================================================
    # UPDATE SHARED CONTEXT
    # ========================================================

    def update_shared_context(
        self,
        memory: SharedMemory,
        key: str,
        value: Any,
    ):

        memory.shared_context[key] = value

    # ========================================================
    # GET SHARED CONTEXT
    # ========================================================

    def get_shared_context(
        self,
        memory: SharedMemory,
        key: str,
        default=None,
    ):

        return memory.shared_context.get(
            key,
            default,
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
                    metadata,
            )
        )

    # ========================================================
    # STORE CODE ARTIFACT
    # ========================================================

    def store_code_artifact(
        self,
        memory: SharedMemory,
        created_by: str,
        code: str,
        file_path: str,
        language: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return (
            memory.artifact_manager
            .create_code_artifact(

                created_by=
                    created_by,

                code=
                    code,

                file_path=
                    file_path,

                language=
                    language,

                metadata=
                    metadata,
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
                    metadata,
            )
        )

    # ========================================================
    # STORE REFLECTION ARTIFACT
    # ========================================================

    def store_reflection_artifact(
        self,
        memory: SharedMemory,
        created_by: str,
        content: Any,
        retry_required: bool,
        retry_steps: List[
            Dict[str, Any]
        ],
        quality_score: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return (
            memory.artifact_manager
            .create_reflection_artifact(

                created_by=
                    created_by,

                content=
                    content,

                retry_required=
                    retry_required,

                retry_steps=
                    retry_steps,

                quality_score=
                    quality_score,

                metadata=
                    metadata,
            )
        )

    # ========================================================
    # GET ALL ARTIFACTS
    # ========================================================

    def get_artifacts(
        self,
        memory: SharedMemory,
    ):

        return (
            memory.artifact_manager
            .get_all_artifacts()
        )

    # ========================================================
    # GET ARTIFACTS BY TYPE
    # ========================================================

    def get_artifacts_by_type(
        self,
        memory: SharedMemory,
        artifact_type: str,
    ):

        return (
            memory.artifact_manager
            .get_artifacts_by_type(
                artifact_type
            )
        )

    # ========================================================
    # STORE REFLECTION NOTE
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
    # MARK STEP COMPLETED
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

    # ========================================================
    # MARK STEP FAILED
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

    # ========================================================
    # SET CURRENT STEP
    # ========================================================

    def set_current_step(
        self,
        memory: SharedMemory,
        step_id: int,
    ):

        memory.current_step = step_id

    # ========================================================
    # REGISTER ACTIVE AGENT
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

    # ========================================================
    # REMOVE ACTIVE AGENT
    # ========================================================

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
    # STORE FINAL OUTPUT
    # ========================================================

    def set_final_output(
        self,
        memory: SharedMemory,
        output: str,
    ):

        memory.final_output = output

    # ========================================================
    # EXPORT MEMORY SNAPSHOT
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

            "current_step":
                memory.current_step,

            "completed_steps":
                memory.completed_steps,

            "failed_steps":
                memory.failed_steps,

            "active_agents":
                memory.active_agents,

            "agent_outputs":
                memory.agent_outputs,

            "shared_context":
                memory.shared_context,

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

            "metadata":
                memory.metadata,
        }