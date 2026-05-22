# core/cognition/reasoning_engine.py

"""
CognitiveOS - Reasoning Engine
---------------------------------------------------------

Responsibilities:
- deterministic reasoning
- execution decision making
- adaptive workflow control
- retry reasoning
- reflection reasoning
- domain-level cognition
- runtime intelligence
- planning support

This becomes the central
reasoning intelligence layer
for CognitiveOS.
"""

from __future__ import annotations

from typing import (
    Dict,
    Any,
    List,
    Optional,
)

from dataclasses import (
    dataclass,
    field,
)

# ============================================================
# REASONING RESULT
# ============================================================


@dataclass
class ReasoningResult:

    success: bool

    decision: str

    confidence: float

    reasoning: str

    next_actions: List[str] = field(
        default_factory=list
    )

    retry_required: bool = False

    reflection_required: bool = False

    escalation_required: bool = False

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# REASONING ENGINE
# ============================================================


class ReasoningEngine:

    """
    Deterministic cognitive reasoning engine.
    """

    def __init__(self):

        # ====================================================
        # CONFIDENCE THRESHOLDS
        # ====================================================

        self.high_confidence = 0.85

        self.medium_confidence = 0.60

        self.low_confidence = 0.40

        # ====================================================
        # MAX RETRIES
        # ====================================================

        self.max_retry_attempts = 3

    # ========================================================
    # MAIN REASONING ENTRYPOINT
    # ========================================================

    def reason(
        self,
        context: Dict[str, Any],
    ) -> ReasoningResult:

        # ====================================================
        # EXTRACT CONTEXT
        # ====================================================

        query = context.get(
            "query",
            ""
        )

        execution_result = context.get(
            "execution_result",
            {}
        )

        quality_result = context.get(
            "quality_result",
            {}
        )

        retry_count = context.get(
            "retry_count",
            0,
        )

        # ====================================================
        # EXECUTION STATUS
        # ====================================================

        runtime_success = (
            execution_result.get(
                "success",
                False,
            )
        )

        quality_score = (
            quality_result.get(
                "overall_score",
                0,
            )
        )

        # ====================================================
        # DECISION TREE
        # ====================================================

        if runtime_success and quality_score >= 80:

            return self._successful_reasoning(
                query=query,
                quality_score=quality_score,
            )

        if (
            runtime_success
            and quality_score < 80
        ):

            return self._improvement_reasoning(
                query=query,
                quality_score=quality_score,
            )

        if (
            not runtime_success
            and retry_count
            < self.max_retry_attempts
        ):

            return self._retry_reasoning(
                query=query,
                retry_count=retry_count,
                execution_result=execution_result,
            )

        return self._failure_reasoning(
            query=query,
            execution_result=execution_result,
        )

    # ========================================================
    # SUCCESS REASONING
    # ========================================================

    def _successful_reasoning(
        self,
        query: str,
        quality_score: int,
    ) -> ReasoningResult:

        return ReasoningResult(

            success=True,

            decision="finalize",

            confidence=0.95,

            reasoning=(
                f"Execution completed successfully "
                f"with high quality score "
                f"({quality_score}/100)."
            ),

            next_actions=[

                "store_artifacts",

                "store_experience",

                "finalize_output",
            ],

            retry_required=False,

            reflection_required=False,
        )

    # ========================================================
    # IMPROVEMENT REASONING
    # ========================================================

    def _improvement_reasoning(
        self,
        query: str,
        quality_score: int,
    ) -> ReasoningResult:

        reflection_required = (
            quality_score < 70
        )

        return ReasoningResult(

            success=True,

            decision="improve_output",

            confidence=0.75,

            reasoning=(
                f"Execution succeeded but quality "
                f"score ({quality_score}/100) "
                f"indicates room for improvement."
            ),

            next_actions=[

                "run_reflection",

                "improve_quality",

                "revalidate_runtime",
            ],

            retry_required=False,

            reflection_required=
                reflection_required,
        )

    # ========================================================
    # RETRY REASONING
    # ========================================================

    def _retry_reasoning(
        self,
        query: str,
        retry_count: int,
        execution_result: Dict[
            str,
            Any,
        ],
    ) -> ReasoningResult:

        stderr = (
            execution_result.get(
                "stderr",
                ""
            )
        )

        strategy = self._determine_retry_strategy(
            stderr
        )

        return ReasoningResult(

            success=False,

            decision="retry_execution",

            confidence=0.80,

            reasoning=(
                f"Execution failed but retry "
                f"is viable. "
                f"Retry attempt "
                f"{retry_count + 1}/"
                f"{self.max_retry_attempts}."
            ),

            next_actions=[

                strategy,

                "patch_runtime",

                "reexecute_project",
            ],

            retry_required=True,

            reflection_required=False,

            metadata={

                "retry_strategy":
                    strategy,
            },
        )

    # ========================================================
    # FAILURE REASONING
    # ========================================================

    def _failure_reasoning(
        self,
        query: str,
        execution_result: Dict[
            str,
            Any,
        ],
    ) -> ReasoningResult:

        return ReasoningResult(

            success=False,

            decision="escalate_failure",

            confidence=0.90,

            reasoning=(
                "Execution repeatedly failed. "
                "Escalation and deeper "
                "reflection required."
            ),

            next_actions=[

                "run_reflection",

                "run_debugging",

                "request_regeneration",
            ],

            retry_required=False,

            reflection_required=True,

            escalation_required=True,
        )

    # ========================================================
    # RETRY STRATEGY
    # ========================================================

    def _determine_retry_strategy(
        self,
        stderr: str,
    ) -> str:

        stderr = stderr.lower()

        # ====================================================
        # IMPORT ERROR
        # ====================================================

        if (
            "modulenotfounderror"
            in stderr
        ):

            return "install_missing_dependencies"

        # ====================================================
        # SYNTAX ERROR
        # ====================================================

        if (
            "syntaxerror"
            in stderr
        ):

            return "patch_syntax_errors"

        # ====================================================
        # ATTRIBUTE ERROR
        # ====================================================

        if (
            "attributeerror"
            in stderr
        ):

            return "patch_object_usage"

        # ====================================================
        # TYPE ERROR
        # ====================================================

        if (
            "typeerror"
            in stderr
        ):

            return "patch_type_mismatch"

        # ====================================================
        # CONNECTION ERROR
        # ====================================================

        if (
            "connection"
            in stderr
        ):

            return "patch_network_logic"

        # ====================================================
        # DEFAULT
        # ====================================================

        return "generic_runtime_repair"

    # ========================================================
    # WORKFLOW REASONING
    # ========================================================

    def determine_workflow_strategy(
        self,
        query: str,
    ) -> Dict[str, Any]:

        query = query.lower()

        # ====================================================
        # BACKEND ENGINEERING
        # ====================================================

        if any(

            keyword in query

            for keyword in [

                "fastapi",

                "backend",

                "api",

                "jwt",

                "database",
            ]
        ):

            return {

                "workflow":
                    "backend_engineering",

                "priority":
                    "high_scalability",

                "agents": [

                    "architecture_agent",

                    "code_agent",

                    "debug_agent",
                ],
            }

        # ====================================================
        # AI ENGINEERING
        # ====================================================

        if any(

            keyword in query

            for keyword in [

                "rag",

                "llm",

                "vector",

                "embedding",

                "langchain",
            ]
        ):

            return {

                "workflow":
                    "ai_engineering",

                "priority":
                    "model_accuracy",

                "agents": [

                    "rag_agent",

                    "vector_db_agent",

                    "evaluation_agent",
                ],
            }

        # ====================================================
        # CYBERSECURITY
        # ====================================================

        if any(

            keyword in query

            for keyword in [

                "security",

                "vulnerability",

                "exploit",

                "pentest",
            ]
        ):

            return {

                "workflow":
                    "cybersecurity",

                "priority":
                    "security_validation",

                "agents": [

                    "security_agent",

                    "audit_agent",

                    "exploit_agent",
                ],
            }

        # ====================================================
        # DEFAULT
        # ====================================================

        return {

            "workflow":
                "general_engineering",

            "priority":
                "balanced",

            "agents": [

                "architecture_agent",

                "code_agent",
            ],
        }

    # ========================================================
    # REFLECTION DECISION
    # ========================================================

    def should_reflect(
        self,
        quality_score: int,
        retry_count: int,
        runtime_success: bool,
    ) -> bool:

        if not runtime_success:

            return True

        if retry_count > 0:

            return True

        if quality_score < 70:

            return True

        return False

    # ========================================================
    # EXECUTION CONFIDENCE
    # ========================================================

    def calculate_confidence(
        self,
        execution_result: Dict[
            str,
            Any,
        ],
        quality_score: int,
    ) -> float:

        confidence = 0.5

        if execution_result.get(
            "success",
            False,
        ):

            confidence += 0.3

        confidence += (
            quality_score / 100
        ) * 0.2

        return round(
            min(confidence, 1.0),
            2,
        )