# domains/software_engineering/memory/artifacts.py

"""
CognitiveOS - Artifact System
---------------------------------------------------------

Responsibilities:
- store generated artifacts
- maintain execution outputs
- preserve code generations
- store logs
- store stack traces
- maintain runtime assets
- support inter-agent collaboration

Artifacts become the LONG-TERM
working memory of CognitiveOS.
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
    Optional,
    List,
)


# ============================================================
# ARTIFACT TYPES
# ============================================================


class ArtifactType:

    CODE = "code"

    ARCHITECTURE = "architecture"

    EXECUTION_LOG = "execution_log"

    ERROR_TRACE = "error_trace"

    API_SPEC = "api_spec"

    CONFIG = "config"

    DOCUMENTATION = "documentation"

    REFLECTION = "reflection"

    DEBUG_REPORT = "debug_report"

    TEST_RESULT = "test_result"

    DEPLOYMENT = "deployment"

    GENERATED_FILE = "generated_file"


# ============================================================
# BASE ARTIFACT
# ============================================================


@dataclass
class Artifact:

    artifact_id: str

    artifact_type: str

    created_by: str

    content: Any

    timestamp: str

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# CODE ARTIFACT
# ============================================================


@dataclass
class CodeArtifact(Artifact):

    file_path: Optional[
        str
    ] = None

    language: Optional[
        str
    ] = None


# ============================================================
# EXECUTION ARTIFACT
# ============================================================


@dataclass
class ExecutionArtifact(Artifact):

    stdout: Optional[
        str
    ] = None

    stderr: Optional[
        str
    ] = None

    return_code: Optional[
        int
    ] = None


# ============================================================
# DEBUG ARTIFACT
# ============================================================


@dataclass
class DebugArtifact(Artifact):

    issue_type: Optional[
        str
    ] = None

    severity: Optional[
        str
    ] = None

    recommended_fix: Optional[
        str
    ] = None


# ============================================================
# REFLECTION ARTIFACT
# ============================================================


@dataclass
class ReflectionArtifact(Artifact):

    retry_required: bool = False

    retry_steps: List[
        Dict[str, Any]
    ] = field(default_factory=list)

    quality_score: str = "medium"


# ============================================================
# ARTIFACT MANAGER
# ============================================================


class ArtifactManager:

    """
    Central artifact management system.
    """

    def __init__(self):

        self.artifacts: List[
            Artifact
        ] = []

    # ========================================================
    # CREATE BASE ARTIFACT
    # ========================================================

    def create_artifact(
        self,
        artifact_type: str,
        created_by: str,
        content: Any,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Artifact:

        artifact = Artifact(

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

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # CREATE CODE ARTIFACT
    # ========================================================

    def create_code_artifact(
        self,
        created_by: str,
        code: str,
        file_path: str,
        language: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> CodeArtifact:

        artifact = CodeArtifact(

            artifact_id=str(
                uuid.uuid4()
            ),

            artifact_type=(
                ArtifactType.CODE
            ),

            created_by=created_by,

            content=code,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=metadata or {},

            file_path=file_path,

            language=language,
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # CREATE EXECUTION ARTIFACT
    # ========================================================

    def create_execution_artifact(
        self,
        created_by: str,
        stdout: str,
        stderr: str,
        return_code: int,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> ExecutionArtifact:

        artifact = ExecutionArtifact(

            artifact_id=str(
                uuid.uuid4()
            ),

            artifact_type=(
                ArtifactType.EXECUTION_LOG
            ),

            created_by=created_by,

            content={

                "stdout":
                    stdout,

                "stderr":
                    stderr,
            },

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=metadata or {},

            stdout=stdout,

            stderr=stderr,

            return_code=return_code,
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # CREATE DEBUG ARTIFACT
    # ========================================================

    def create_debug_artifact(
        self,
        created_by: str,
        issue_type: str,
        severity: str,
        recommended_fix: str,
        content: Any,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> DebugArtifact:

        artifact = DebugArtifact(

            artifact_id=str(
                uuid.uuid4()
            ),

            artifact_type=(
                ArtifactType.DEBUG_REPORT
            ),

            created_by=created_by,

            content=content,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=metadata or {},

            issue_type=issue_type,

            severity=severity,

            recommended_fix=(
                recommended_fix
            ),
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # CREATE REFLECTION ARTIFACT
    # ========================================================

    def create_reflection_artifact(
        self,
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
    ) -> ReflectionArtifact:

        artifact = ReflectionArtifact(

            artifact_id=str(
                uuid.uuid4()
            ),

            artifact_type=(
                ArtifactType.REFLECTION
            ),

            created_by=created_by,

            content=content,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=metadata or {},

            retry_required=(
                retry_required
            ),

            retry_steps=(
                retry_steps
            ),

            quality_score=(
                quality_score
            ),
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # GET ALL ARTIFACTS
    # ========================================================

    def get_all_artifacts(
        self,
    ) -> List[Artifact]:

        return self.artifacts

    # ========================================================
    # GET BY TYPE
    # ========================================================

    def get_artifacts_by_type(
        self,
        artifact_type: str,
    ) -> List[Artifact]:

        return [

            artifact

            for artifact in self.artifacts

            if (
                artifact.artifact_type
                == artifact_type
            )
        ]

    # ========================================================
    # GET BY CREATOR
    # ========================================================

    def get_artifacts_by_creator(
        self,
        created_by: str,
    ) -> List[Artifact]:

        return [

            artifact

            for artifact in self.artifacts

            if (
                artifact.created_by
                == created_by
            )
        ]

    # ========================================================
    # EXPORT ARTIFACTS
    # ========================================================

    def export_artifacts(
        self,
    ) -> List[Dict[str, Any]]:

        exported = []

        for artifact in self.artifacts:

            exported.append(

                {

                    "artifact_id":
                        artifact.artifact_id,

                    "artifact_type":
                        artifact.artifact_type,

                    "created_by":
                        artifact.created_by,

                    "content":
                        artifact.content,

                    "timestamp":
                        artifact.timestamp,

                    "metadata":
                        artifact.metadata,
                }
            )

        return exported