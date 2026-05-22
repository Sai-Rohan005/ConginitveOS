# core/cognition/quality_engine.py

"""
CognitiveOS - Quality Engine
---------------------------------------------------------

Responsibilities:
- evaluate execution quality
- calculate deterministic quality scores
- assess production readiness
- evaluate maintainability
- evaluate scalability
- evaluate security posture
- determine reflection necessity
- provide runtime quality intelligence

This becomes the deterministic
quality assessment engine for CognitiveOS.
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
# QUALITY RESULT
# ============================================================


@dataclass
class QualityResult:

    overall_score: int

    production_ready: bool

    reflection_required: bool

    category_scores: Dict[
        str,
        int,
    ] = field(default_factory=dict)

    strengths: List[str] = field(
        default_factory=list
    )

    weaknesses: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    reasoning: str = ""


# ============================================================
# QUALITY ENGINE
# ============================================================


class QualityEngine:

    """
    Deterministic quality evaluation engine.
    """

    def __init__(self):

        # ====================================================
        # QUALITY THRESHOLDS
        # ====================================================

        self.production_threshold = 75

        self.reflection_threshold = 60

        # ====================================================
        # CATEGORY WEIGHTS
        # ====================================================

        self.weights = {

            "runtime": 30,

            "security": 20,

            "maintainability": 15,

            "scalability": 15,

            "testing": 10,

            "architecture": 10,
        }

    # ========================================================
    # MAIN EVALUATION
    # ========================================================

    def evaluate(
        self,
        execution_result: Dict[
            str,
            Any,
        ],
        artifacts: List[Any] = None,
    ) -> QualityResult:

        artifacts = artifacts or []

        # ====================================================
        # CATEGORY SCORES
        # ====================================================

        runtime_score = (
            self._evaluate_runtime(
                execution_result
            )
        )

        security_score = (
            self._evaluate_security(
                execution_result
            )
        )

        maintainability_score = (
            self._evaluate_maintainability(
                execution_result
            )
        )

        scalability_score = (
            self._evaluate_scalability(
                execution_result
            )
        )

        testing_score = (
            self._evaluate_testing(
                execution_result
            )
        )

        architecture_score = (
            self._evaluate_architecture(
                execution_result
            )
        )

        category_scores = {

            "runtime":
                runtime_score,

            "security":
                security_score,

            "maintainability":
                maintainability_score,

            "scalability":
                scalability_score,

            "testing":
                testing_score,

            "architecture":
                architecture_score,
        }

        # ====================================================
        # CALCULATE WEIGHTED SCORE
        # ====================================================

        overall_score = (
            self._calculate_weighted_score(
                category_scores
            )
        )

        # ====================================================
        # PRODUCTION READINESS
        # ====================================================

        production_ready = (
            overall_score
            >= self.production_threshold
        )

        # ====================================================
        # REFLECTION REQUIREMENT
        # ====================================================

        reflection_required = (
            overall_score
            < self.reflection_threshold
        )

        # ====================================================
        # ANALYSIS
        # ====================================================

        strengths = (
            self._identify_strengths(
                category_scores
            )
        )

        weaknesses = (
            self._identify_weaknesses(
                category_scores
            )
        )

        recommendations = (
            self._generate_recommendations(
                category_scores
            )
        )

        reasoning = (
            self._generate_reasoning(
                overall_score,
                production_ready,
                reflection_required,
            )
        )

        return QualityResult(

            overall_score=
                overall_score,

            production_ready=
                production_ready,

            reflection_required=
                reflection_required,

            category_scores=
                category_scores,

            strengths=
                strengths,

            weaknesses=
                weaknesses,

            recommendations=
                recommendations,

            reasoning=
                reasoning,
        )

    # ========================================================
    # RUNTIME QUALITY
    # ========================================================

    def _evaluate_runtime(
        self,
        result: Dict[str, Any],
    ) -> int:

        score = 0

        execution = result.get(
            "execution_validation",
            {}
        )

        if execution.get(
            "success",
            False,
        ):

            score += 70

        stderr = execution.get(
            "stderr",
            ""
        )

        if not stderr:

            score += 30

        elif "warning" in stderr.lower():

            score += 15

        return min(score, 100)

    # ========================================================
    # SECURITY QUALITY
    # ========================================================

    def _evaluate_security(
        self,
        result: Dict[str, Any],
    ) -> int:

        score = 50

        generated_files = result.get(
            "generated_files",
            []
        )

        combined_code = "\n".join(

            file.get("code", "")

            for file in generated_files
        )

        security_keywords = [

            "jwt",

            "oauth",

            "bcrypt",

            "rate_limit",

            "cors",

            "helmet",

            "authentication",
        ]

        for keyword in security_keywords:

            if keyword.lower() in (
                combined_code.lower()
            ):

                score += 7

        return min(score, 100)

    # ========================================================
    # MAINTAINABILITY
    # ========================================================

    def _evaluate_maintainability(
        self,
        result: Dict[str, Any],
    ) -> int:

        score = 40

        generated_files = result.get(
            "generated_files",
            []
        )

        if len(generated_files) >= 5:

            score += 20

        modular_paths = [

            "services",

            "routes",

            "models",

            "core",

            "utils",
        ]

        for file in generated_files:

            path = file.get(
                "file_path",
                ""
            )

            for module in modular_paths:

                if module in path:

                    score += 8

        return min(score, 100)

    # ========================================================
    # SCALABILITY
    # ========================================================

    def _evaluate_scalability(
        self,
        result: Dict[str, Any],
    ) -> int:

        score = 40

        tech_stack = result.get(
            "tech_stack",
            []
        )

        scalable_tech = [

            "fastapi",

            "redis",

            "docker",

            "kubernetes",

            "postgresql",

            "asyncio",

            "celery",
        ]

        for tech in scalable_tech:

            if any(

                tech.lower()
                in item.lower()

                for item in tech_stack
            ):

                score += 8

        return min(score, 100)

    # ========================================================
    # TESTING
    # ========================================================

    def _evaluate_testing(
        self,
        result: Dict[str, Any],
    ) -> int:

        score = 20

        generated_files = result.get(
            "generated_files",
            []
        )

        for file in generated_files:

            path = file.get(
                "file_path",
                ""
            )

            if "test" in path.lower():

                score += 40

        if score == 20:

            return 30

        return min(score, 100)

    # ========================================================
    # ARCHITECTURE
    # ========================================================

    def _evaluate_architecture(
        self,
        result: Dict[str, Any],
    ) -> int:

        score = 40

        generated_files = result.get(
            "generated_files",
            []
        )

        architecture_patterns = [

            "middleware",

            "service",

            "repository",

            "dependency",

            "router",

            "controller",
        ]

        combined_code = "\n".join(

            file.get("code", "")

            for file in generated_files
        )

        for pattern in architecture_patterns:

            if pattern.lower() in (
                combined_code.lower()
            ):

                score += 10

        return min(score, 100)

    # ========================================================
    # WEIGHTED SCORE
    # ========================================================

    def _calculate_weighted_score(
        self,
        scores: Dict[str, int],
    ) -> int:

        total = 0

        for category, weight in (
            self.weights.items()
        ):

            total += (
                scores.get(category, 0)
                * weight
            )

        return int(total / 100)

    # ========================================================
    # STRENGTHS
    # ========================================================

    def _identify_strengths(
        self,
        scores: Dict[str, int],
    ) -> List[str]:

        strengths = []

        for category, score in (
            scores.items()
        ):

            if score >= 80:

                strengths.append(
                    f"Strong {category} quality"
                )

        return strengths

    # ========================================================
    # WEAKNESSES
    # ========================================================

    def _identify_weaknesses(
        self,
        scores: Dict[str, int],
    ) -> List[str]:

        weaknesses = []

        for category, score in (
            scores.items()
        ):

            if score < 50:

                weaknesses.append(
                    f"Weak {category} quality"
                )

        return weaknesses

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    def _generate_recommendations(
        self,
        scores: Dict[str, int],
    ) -> List[str]:

        recommendations = []

        if scores.get(
            "security",
            0
        ) < 70:

            recommendations.append(
                "Improve authentication and security hardening"
            )

        if scores.get(
            "testing",
            0
        ) < 70:

            recommendations.append(
                "Add integration and unit tests"
            )

        if scores.get(
            "scalability",
            0
        ) < 70:

            recommendations.append(
                "Improve scalability architecture"
            )

        if scores.get(
            "runtime",
            0
        ) < 70:

            recommendations.append(
                "Fix runtime execution failures"
            )

        return recommendations

    # ========================================================
    # REASONING
    # ========================================================

    def _generate_reasoning(
        self,
        overall_score: int,
        production_ready: bool,
        reflection_required: bool,
    ) -> str:

        reasoning = (
            f"System achieved overall quality "
            f"score of {overall_score}/100. "
        )

        if production_ready:

            reasoning += (
                "System is production ready. "
            )

        else:

            reasoning += (
                "System requires improvement "
                "before production deployment. "
            )

        if reflection_required:

            reasoning += (
                "Reflection cycle recommended "
                "for quality improvement."
            )

        return reasoning