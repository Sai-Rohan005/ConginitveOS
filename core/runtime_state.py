# core/runtime_state.py

"""
CognitiveOS - Runtime State
---------------------------------------------------------

Responsibilities:
- maintain global execution state
- store orchestration outputs
- preserve workflow cognition
- maintain runtime metadata
- track execution lifecycle
- provide unified system state

This becomes the GLOBAL MEMORY LAYER
for CognitiveOS runtime execution.
"""

from __future__ import annotations

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

from datetime import datetime
import uuid


# ============================================================
# EXECUTION EVENT
# ============================================================


@dataclass
class ExecutionEvent:

    event_id: str

    event_type: str

    source: str

    message: str

    timestamp: str

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# ============================================================
# RUNTIME ARTIFACT
# ============================================================


@dataclass
class RuntimeArtifact:

    artifact_id: str

    artifact_type: str

    created_by: str

    content: Any

    timestamp: str

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# ============================================================
# RUNTIME STATE
# ============================================================


@dataclass
class RuntimeState:

    # ========================================================
    # CORE EXECUTION
    # ========================================================

    execution_id: str

    query: str

    created_at: str

    active_domain: Optional[
        str
    ] = None

    # ========================================================
    # PLANNER
    # ========================================================

    planner_output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    # ========================================================
    # SUPERVISOR
    # ========================================================

    supervisor_output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    # ========================================================
    # EXECUTION
    # ========================================================

    execution_result: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    workflow_steps: List[
        Dict[str, Any]
    ] = field(default_factory=list)

    completed_steps: List[
        int
    ] = field(default_factory=list)

    failed_steps: List[
        int
    ] = field(default_factory=list)

    # ========================================================
    # AGENTS
    # ========================================================

    active_agents: List[
        str
    ] = field(default_factory=list)

    agent_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    # ========================================================
    # MEMORY
    # ========================================================

    shared_memory_snapshot: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    # ========================================================
    # REFLECTION
    # ========================================================

    reflection_notes: List[
        str
    ] = field(default_factory=list)

    # ========================================================
    # ARTIFACTS
    # ========================================================

    artifacts: List[
        RuntimeArtifact
    ] = field(default_factory=list)

    # ========================================================
    # EVENTS
    # ========================================================

    execution_events: List[
        ExecutionEvent
    ] = field(default_factory=list)

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    final_output: str = ""

    # ========================================================
    # EXECUTION STATUS
    # ========================================================

    success: bool = False

    execution_status: str = (
        "initialized"
    )

    # ========================================================
    # METADATA
    # ========================================================

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# RUNTIME STATE MANAGER
# ============================================================


class RuntimeStateManager:

    """
    Global runtime state manager.
    """

    # ========================================================
    # CREATE STATE
    # ========================================================

    def create_runtime_state(
        self,
        query: str,
    ) -> RuntimeState:

        return RuntimeState(

            execution_id=str(
                uuid.uuid4()
            ),

            query=query,

            created_at=(
                datetime.utcnow().isoformat()
            ),
        )

    # ========================================================
    # UPDATE DOMAIN
    # ========================================================

    def set_active_domain(
        self,
        state: RuntimeState,
        domain: str,
    ):

        state.active_domain = domain

    # ========================================================
    # STORE PLANNER OUTPUT
    # ========================================================

    def store_planner_output(
        self,
        state: RuntimeState,
        output: Dict[str, Any],
    ):

        state.planner_output = output

    # ========================================================
    # STORE SUPERVISOR OUTPUT
    # ========================================================

    def store_supervisor_output(
        self,
        state: RuntimeState,
        output: Dict[str, Any],
    ):

        state.supervisor_output = output

    # ========================================================
    # STORE EXECUTION RESULT
    # ========================================================

    def store_execution_result(
        self,
        state: RuntimeState,
        result: Dict[str, Any],
    ):

        state.execution_result = result

    # ========================================================
    # STORE AGENT OUTPUT
    # ========================================================

    def store_agent_output(
        self,
        state: RuntimeState,
        agent: str,
        output: Any,
    ):

        state.agent_outputs[
            agent
        ] = output

    # ========================================================
    # ADD EVENT
    # ========================================================

    def add_event(
        self,
        state: RuntimeState,
        event_type: str,
        source: str,
        message: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        event = ExecutionEvent(

            event_id=str(
                uuid.uuid4()
            ),

            event_type=event_type,

            source=source,

            message=message,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=metadata or {},
        )

        state.execution_events.append(
            event
        )

    # ========================================================
    # STORE ARTIFACT
    # ========================================================

    def store_artifact(
        self,
        state: RuntimeState,
        artifact_type: str,
        created_by: str,
        content: Any,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        artifact = RuntimeArtifact(

            artifact_id=str(
                uuid.uuid4()
            ),

            artifact_type=artifact_type,

            created_by=created_by,

            content=content,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=metadata or {},
        )

        state.artifacts.append(
            artifact
        )

    # ========================================================
    # ADD REFLECTION
    # ========================================================

    def add_reflection_note(
        self,
        state: RuntimeState,
        note: str,
    ):

        state.reflection_notes.append(
            note
        )

    # ========================================================
    # SET FINAL OUTPUT
    # ========================================================

    def set_final_output(
        self,
        state: RuntimeState,
        output: str,
    ):

        state.final_output = output

    # ========================================================
    # UPDATE EXECUTION STATUS
    # ========================================================

    def update_execution_status(
        self,
        state: RuntimeState,
        status: str,
    ):

        state.execution_status = status

    # ========================================================
    # MARK SUCCESS
    # ========================================================

    def mark_success(
        self,
        state: RuntimeState,
    ):

        state.success = True

        state.execution_status = (
            "completed"
        )

    # ========================================================
    # MARK FAILURE
    # ========================================================

    def mark_failure(
        self,
        state: RuntimeState,
    ):

        state.success = False

        state.execution_status = (
            "failed"
        )

    # ========================================================
    # EXPORT SNAPSHOT
    # ========================================================

    def export_snapshot(
        self,
        state: RuntimeState,
    ) -> Dict[str, Any]:

        return {

            "execution_id":
                state.execution_id,

            "query":
                state.query,

            "active_domain":
                state.active_domain,

            "execution_status":
                state.execution_status,

            "success":
                state.success,

            "planner_output":
                state.planner_output,

            "supervisor_output":
                state.supervisor_output,

            "execution_result":
                state.execution_result,

            "completed_steps":
                state.completed_steps,

            "failed_steps":
                state.failed_steps,

            "active_agents":
                state.active_agents,

            "agent_outputs":
                state.agent_outputs,

            "reflection_notes":
                state.reflection_notes,

            "final_output":
                state.final_output,

            "metadata":
                state.metadata,
        }