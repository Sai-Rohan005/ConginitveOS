# domains/software_engineering/memory/artifacts.py

"""
CognitiveOS - Advanced Artifact System
---------------------------------------------------------

Responsibilities:
- store generated artifacts
- preserve execution history
- maintain runtime intelligence
- support inter-agent collaboration
- preserve runtime repairs
- preserve patch history
- preserve validation history
- maintain workspace cognition

Artifacts become the LONG-TERM cognition layer.
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

    RUNTIME_REPAIR = "runtime_repair"

    PATCH = "patch"

    VALIDATION = "validation"

    WORKSPACE_SNAPSHOT = (
        "workspace_snapshot"
    )

    DEPENDENCY_INSTALL = (
        "dependency_install"
    )

    RETRY = "retry"

    EXECUTION_SESSION = (
        "execution_session"
    )

    METRICS = "metrics"


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
# PATCH ARTIFACT
# ============================================================


@dataclass
class PatchArtifact(Artifact):

    target_file: Optional[
        str
    ] = None

    patch_strategy: Optional[
        str
    ] = None

    success: bool = False


# ============================================================
# VALIDATION ARTIFACT
# ============================================================


@dataclass
class ValidationArtifact(Artifact):

    validation_type: Optional[
        str
    ] = None

    passed: bool = False

    validation_errors: List[
        str
    ] = field(default_factory=list)


# ============================================================
# DEPENDENCY ARTIFACT
# ============================================================


@dataclass
class DependencyArtifact(Artifact):

    dependency_name: Optional[
        str
    ] = None

    install_success: bool = False


# ============================================================
# ARTIFACT MANAGER
# ============================================================


class ArtifactManager:

    """
    Centralized artifact cognition system.
    """

    def __init__(self):

        self.artifacts: List[
            Artifact
        ] = []

    # ========================================================
    # BASE CREATION
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

            artifact_type=
                artifact_type,

            created_by=
                created_by,

            content=
                content,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=
                metadata or {},
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # CODE ARTIFACT
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

            artifact_type=
                ArtifactType.CODE,

            created_by=
                created_by,

            content=
                code,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=
                metadata or {},

            file_path=
                file_path,

            language=
                language,
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # EXECUTION ARTIFACT
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

            artifact_type=
                ArtifactType.EXECUTION_LOG,

            created_by=
                created_by,

            content={

                "stdout":
                    stdout,

                "stderr":
                    stderr,
            },

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=
                metadata or {},

            stdout=
                stdout,

            stderr=
                stderr,

            return_code=
                return_code,
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # PATCH ARTIFACT
    # ========================================================

    def create_patch_artifact(

        self,

        created_by: str,

        target_file: str,

        patch_strategy: str,

        success: bool,

        content: Any,

        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> PatchArtifact:

        artifact = PatchArtifact(

            artifact_id=str(
                uuid.uuid4()
            ),

            artifact_type=
                ArtifactType.PATCH,

            created_by=
                created_by,

            content=
                content,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=
                metadata or {},

            target_file=
                target_file,

            patch_strategy=
                patch_strategy,

            success=
                success,
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # VALIDATION ARTIFACT
    # ========================================================

    def create_validation_artifact(

        self,

        created_by: str,

        validation_type: str,

        passed: bool,

        validation_errors: List[
            str
        ],

        content: Any,

        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> ValidationArtifact:

        artifact = ValidationArtifact(

            artifact_id=str(
                uuid.uuid4()
            ),

            artifact_type=
                ArtifactType.VALIDATION,

            created_by=
                created_by,

            content=
                content,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=
                metadata or {},

            validation_type=
                validation_type,

            passed=
                passed,

            validation_errors=
                validation_errors,
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # DEPENDENCY ARTIFACT
    # ========================================================

    def create_dependency_artifact(

        self,

        created_by: str,

        dependency_name: str,

        install_success: bool,

        content: Any,

        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> DependencyArtifact:

        artifact = DependencyArtifact(

            artifact_id=str(
                uuid.uuid4()
            ),

            artifact_type=
                ArtifactType.DEPENDENCY_INSTALL,

            created_by=
                created_by,

            content=
                content,

            timestamp=(
                datetime.utcnow().isoformat()
            ),

            metadata=
                metadata or {},

            dependency_name=
                dependency_name,

            install_success=
                install_success,
        )

        self.artifacts.append(
            artifact
        )

        return artifact

    # ========================================================
    # GETTERS
    # ========================================================

    def get_all_artifacts(
        self,
    ) -> List[Artifact]:

        return self.artifacts

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
    # EXPORT
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