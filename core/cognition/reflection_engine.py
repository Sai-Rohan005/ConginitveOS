# core/cognition/reflection_engine.py

"""
CognitiveOS - Reflection Engine
---------------------------------------------------------

Responsibilities:
- analyze execution outcomes
- identify weak outputs
- determine retry necessity
- generate improvement strategies
- evaluate cognitive quality
- recommend workflow improvements
- detect architectural flaws
- drive autonomous self-improvement

This becomes the meta-cognition
layer of CognitiveOS.
"""

from __future__ import annotations

from typing import (
    Dict,
    Any,
    List,
)

from dataclasses import (
    dataclass,
    field,
)

# ============================================================
# REFLECTION RESULT
# ============================================================


@dataclass
class ReflectionResult:

    success: bool

    retry_required: bool

    quality_score: int

    summary: str

    strengths: List[str] = field(
        default_factory=list
    )

    weaknesses: List[str] = field(
        default_factory=list
    )

    retry_steps: List[
        Dict[str, Any]
    ] = field(default_factory=list)

    recommendations: List[str] = field(
        default_factory=list
    )

    reflection_notes: List[str] = field(
        default_factory=list
    )

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# REFLECTION ENGINE
# ============================================================


class ReflectionEngine:

    """
    Deterministic reflection engine.
    """

    def __init__(self):

        self.retry_threshold = 70

        self.max_retry_steps = 3

    # ========================================================
    # MAIN REFLECTION
    # ========================================================

    def reflect(
        self,
        execution_result: Dict[
            str,
            Any,
        ],
        quality_result: Dict[
            str,
            Any,
        ],
        artifacts: List[Any] = None,
    ) -> ReflectionResult:

        artifacts = artifacts or []

        # ====================================================
        # QUALITY SCORE
        # ====================================================

        quality_score = (
            quality_result.get(
                "overall_score",
                0,
            )
        )

        # ====================================================
        # ANALYZE OUTPUTS
        # ====================================================

        strengths = self._identify_strengths(
            execution_result,
            quality_result,
        )

        weaknesses = self._identify_weaknesses(
            execution_result,
            quality_result,
        )

        # ====================================================
        # RETRY DECISION
        # ====================================================

        retry_required = (
            quality_score
            < self.retry_threshold
        )

        retry_steps = []

        if retry_required:

            retry_steps = (
                self._generate_retry_steps(
                    execution_result,
                    quality_result,
                )
            )

        # ====================================================
        # RECOMMENDATIONS
        # ====================================================

        recommendations = (
            self._generate_recommendations(
                execution_result,
                quality_result,
            )
        )

        # ====================================================
        # REFLECTION NOTES
        # ====================================================

        reflection_notes = (
            self._generate_reflection_notes(
                execution_result,
                quality_result,
            )
        )

        # ====================================================
        # SUMMARY
        # ====================================================

        summary = (
            self._generate_summary(
                quality_score,
                retry_required,
            )
        )

        return ReflectionResult(

            success=True,

            retry_required=
                retry_required,

            quality_score=
                quality_score,

            summary=
                summary,

            strengths=
                strengths,

            weaknesses=
                weaknesses,

            retry_steps=
                retry_steps,

            recommendations=
                recommendations,

            reflection_notes=
                reflection_notes,

            metadata={

                "artifact_count":
                    len(artifacts),
            },
        )

    # ========================================================
    # STRENGTHS
    # ========================================================

    def _identify_strengths(
        self,
        execution_result,
        quality_result,
    ) -> List[str]:

        strengths = []

        execution = execution_result.get(
            "execution_validation",
            {}
        )

        if execution.get(
            "success",
            False,
        ):

            strengths.append(
                "Runtime execution succeeded"
            )

        tech_stack = execution_result.get(
            "tech_stack",
            []
        )

        scalable_tech = [

            "fastapi",

            "docker",

            "redis",

            "postgresql",

            "kubernetes",
        ]

        for tech in scalable_tech:

            if any(

                tech.lower()
                in item.lower()

                for item in tech_stack
            ):

                strengths.append(
                    f"Uses scalable technology: {tech}"
                )

        if (
            quality_result.get(
                "production_ready",
                False
            )
        ):

            strengths.append(
                "Production-ready architecture"
            )

        return strengths

    # ========================================================
    # WEAKNESSES
    # ========================================================

    def _identify_weaknesses(
        self,
        execution_result,
        quality_result,
    ) -> List[str]:

        weaknesses = []

        execution = execution_result.get(
            "execution_validation",
            {}
        )

        stderr = execution.get(
            "stderr",
            ""
        )

        if stderr:

            weaknesses.append(
                "Runtime execution produced errors"
            )

        quality_score = (
            quality_result.get(
                "overall_score",
                0,
            )
        )

        if quality_score < 70:

            weaknesses.append(
                "Overall quality score is low"
            )

        generated_files = execution_result.get(
            "generated_files",
            []
        )

        has_tests = any(

            "test"
            in file.get(
                "file_path",
                ""
            ).lower()

            for file in generated_files
        )

        if not has_tests:

            weaknesses.append(
                "No automated tests generated"
            )

        return weaknesses

    # ========================================================
    # RETRY STEP GENERATION
    # ========================================================

    def _generate_retry_steps(
        self,
        execution_result,
        quality_result,
    ) -> List[Dict[str, Any]]:

        retry_steps = []

        execution = execution_result.get(
            "execution_validation",
            {}
        )

        stderr = execution.get(
            "stderr",
            ""
        )

        # ====================================================
        # IMPORT FAILURES
        # ====================================================

        if (
            "ModuleNotFoundError"
            in stderr
        ):

            retry_steps.append(

                {

                    "step_id": 1,

                    "action":
                        "install_missing_dependencies",

                    "reason":
                        "Missing Python modules detected",
                }
            )

        # ====================================================
        # SYNTAX FAILURES
        # ====================================================

        if (
            "SyntaxError"
            in stderr
        ):

            retry_steps.append(

                {

                    "step_id": 2,

                    "action":
                        "patch_syntax_errors",

                    "reason":
                        "Syntax issues detected",
                }
            )

        # ====================================================
        # TESTING IMPROVEMENT
        # ====================================================

        generated_files = execution_result.get(
            "generated_files",
            []
        )

        has_tests = any(

            "test"
            in file.get(
                "file_path",
                ""
            ).lower()

            for file in generated_files
        )

        if not has_tests:

            retry_steps.append(

                {

                    "step_id": 3,

                    "action":
                        "generate_tests",

                    "reason":
                        "Missing automated tests",
                }
            )

        return retry_steps[
            : self.max_retry_steps
        ]

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    def _generate_recommendations(
        self,
        execution_result,
        quality_result,
    ) -> List[str]:

        recommendations = []

        score = quality_result.get(
            "overall_score",
            0,
        )

        if score < 70:

            recommendations.append(
                "Improve architecture modularity"
            )

            recommendations.append(
                "Strengthen runtime validation"
            )

        execution = execution_result.get(
            "execution_validation",
            {}
        )

        stderr = execution.get(
            "stderr",
            ""
        )

        if stderr:

            recommendations.append(
                "Improve deterministic patching"
            )

        generated_files = execution_result.get(
            "generated_files",
            []
        )

        if len(generated_files) < 5:

            recommendations.append(
                "Increase project modularization"
            )

        return recommendations

    # ========================================================
    # REFLECTION NOTES
    # ========================================================

    def _generate_reflection_notes(
        self,
        execution_result,
        quality_result,
    ) -> List[str]:

        notes = []

        execution = execution_result.get(
            "execution_validation",
            {}
        )

        if execution.get(
            "success",
            False,
        ):

            notes.append(
                "Execution runtime is stable"
            )

        else:

            notes.append(
                "Runtime instability detected"
            )

        score = quality_result.get(
            "overall_score",
            0,
        )

        if score >= 80:

            notes.append(
                "High production readiness"
            )

        elif score >= 60:

            notes.append(
                "Moderate production readiness"
            )

        else:

            notes.append(
                "Low production readiness"
            )

        return notes

    # ========================================================
    # SUMMARY
    # ========================================================

    def _generate_summary(
        self,
        quality_score: int,
        retry_required: bool,
    ) -> str:

        summary = (
            f"Reflection completed with "
            f"quality score "
            f"{quality_score}/100. "
        )

        if retry_required:

            summary += (
                "Retry and improvement "
                "cycles are recommended."
            )

        else:

            summary += (
                "System output is acceptable."
            )

        return summary

    # ========================================================
    # SHOULD RETRY
    # ========================================================

    def should_retry(
        self,
        quality_score: int,
        runtime_success: bool,
    ) -> bool:

        if not runtime_success:

            return True

        if quality_score < self.retry_threshold:

            return True

        return False