# core/cognition/scoring_engine.py

"""
CognitiveOS - Scoring Engine
---------------------------------------------------------

Responsibilities:
- calculate deterministic execution scores
- evaluate runtime quality
- evaluate scalability
- evaluate maintainability
- evaluate security posture
- evaluate architecture quality
- generate weighted production scores
- provide autonomous scoring intelligence

This becomes the deterministic
scoring system for CognitiveOS.
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
# SCORE RESULT
# ============================================================


@dataclass
class ScoreResult:

    production_ready: bool


    category_scores: Dict[
        str,
        float,
    ] = field(default_factory=dict)

    weighted_breakdown: Dict[
        str,
        float,
    ] = field(default_factory=dict)

    reasoning: str = ""

    strengths: List[str] = field(
        default_factory=list
    )

    weaknesses: List[str] = field(
        default_factory=list
    )
    overall_score: float=0.0


# ============================================================
# SCORING ENGINE
# ============================================================


class ScoringEngine:

    """
    Deterministic production scoring engine.
    """

    def __init__(self):

        # ====================================================
        # WEIGHTS
        # ====================================================

        self.weights = {

            "runtime": 0.30,

            "security": 0.20,

            "scalability": 0.15,

            "maintainability": 0.15,

            "architecture": 0.10,

            "testing": 0.10,
        }

        # ====================================================
        # PRODUCTION THRESHOLD
        # ====================================================

        self.production_threshold = 75

    # ========================================================
    # MAIN SCORING
    # ========================================================

    def score(
        self,
        execution_result: Dict[
            str,
            Any,
        ],
    ) -> ScoreResult:

        # ====================================================
        # CATEGORY SCORES
        # ====================================================

        category_scores = {

            "runtime":
                self._score_runtime(
                    execution_result
                ),

            "security":
                self._score_security(
                    execution_result
                ),

            "scalability":
                self._score_scalability(
                    execution_result
                ),

            "maintainability":
                self._score_maintainability(
                    execution_result
                ),

            "architecture":
                self._score_architecture(
                    execution_result
                ),

            "testing":
                self._score_testing(
                    execution_result
                ),
        }

        # ====================================================
        # WEIGHTED BREAKDOWN
        # ====================================================

        weighted_breakdown = {}

        overall_score = 0.0

        for category, score in (
            category_scores.items()
        ):

            weighted = (
                score
                * self.weights[
                    category
                ]
            )

            weighted_breakdown[
                category
            ] = round(
                weighted,
                2,
            )

            overall_score += weighted

        overall_score = round(
            overall_score,
            2,
        )

        # ====================================================
        # PRODUCTION READY
        # ====================================================

        production_ready = (
            overall_score
            >= self.production_threshold
        )

        # ====================================================
        # STRENGTHS
        # ====================================================

        strengths = []

        weaknesses = []

        for category, score in (
            category_scores.items()
        ):

            if score >= 80:

                strengths.append(
                    f"Strong {category}"
                )

            if score < 50:

                weaknesses.append(
                    f"Weak {category}"
                )

        # ====================================================
        # REASONING
        # ====================================================

        reasoning = (
            self._generate_reasoning(
                overall_score,
                production_ready,
                category_scores,
            )
        )

        return ScoreResult(

            overall_score=
                overall_score,

            production_ready=
                production_ready,

            category_scores=
                category_scores,

            weighted_breakdown=
                weighted_breakdown,

            reasoning=
                reasoning,

            strengths=
                strengths,

            weaknesses=
                weaknesses,
        )

    # ========================================================
    # RUNTIME SCORE
    # ========================================================

    def _score_runtime(
        self,
        result: Dict[str, Any],
    ) -> float:

        execution = result.get(
            "execution_validation",
            {}
        )

        success = execution.get(
            "success",
            False,
        )

        stderr = execution.get(
            "stderr",
            "",
        )

        if success and not stderr:

            return 100.0

        if success and stderr:

            return 75.0

        return 30.0

    # ========================================================
    # SECURITY SCORE
    # ========================================================

    def _score_security(
        self,
        result: Dict[str, Any],
    ) -> float:

        score = 40.0

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

            "cors",

            "authentication",

            "authorization",

            "rate_limit",
        ]

        for keyword in security_keywords:

            if keyword.lower() in (
                combined_code.lower()
            ):

                score += 8

        return min(score, 100.0)

    # ========================================================
    # SCALABILITY SCORE
    # ========================================================

    def _score_scalability(
        self,
        result: Dict[str, Any],
    ) -> float:

        score = 40.0

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

            "celery",

            "asyncio",
        ]

        for tech in scalable_tech:

            if any(

                tech.lower()
                in item.lower()

                for item in tech_stack
            ):

                score += 8

        return min(score, 100.0)

    # ========================================================
    # MAINTAINABILITY SCORE
    # ========================================================

    def _score_maintainability(
        self,
        result: Dict[str, Any],
    ) -> float:

        score = 30.0

        generated_files = result.get(
            "generated_files",
            []
        )

        if len(generated_files) >= 5:

            score += 20

        modular_paths = [

            "services",

            "models",

            "routes",

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

        return min(score, 100.0)

    # ========================================================
    # ARCHITECTURE SCORE
    # ========================================================

    def _score_architecture(
        self,
        result: Dict[str, Any],
    ) -> float:

        score = 40.0

        generated_files = result.get(
            "generated_files",
            []
        )

        combined_code = "\n".join(

            file.get("code", "")

            for file in generated_files
        )

        architecture_patterns = [

            "middleware",

            "dependency",

            "router",

            "service",

            "repository",

            "controller",
        ]

        for pattern in architecture_patterns:

            if pattern.lower() in (
                combined_code.lower()
            ):

                score += 10

        return min(score, 100.0)

    # ========================================================
    # TESTING SCORE
    # ========================================================

    def _score_testing(
        self,
        result: Dict[str, Any],
    ) -> float:

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

                return 100.0

        return 25.0

    # ========================================================
    # REASONING
    # ========================================================

    def _generate_reasoning(
        self,
        overall_score: float,
        production_ready: bool,
        category_scores: Dict[
            str,
            float,
        ],
    ) -> str:

        best_category = max(

            category_scores,

            key=category_scores.get
        )

        weakest_category = min(

            category_scores,

            key=category_scores.get
        )

        reasoning = (
            f"Overall deterministic score: "
            f"{overall_score}/100. "
        )

        reasoning += (
            f"Strongest area: "
            f"{best_category}. "
        )

        reasoning += (
            f"Weakest area: "
            f"{weakest_category}. "
        )

        if production_ready:

            reasoning += (
                "System is production ready."
            )

        else:

            reasoning += (
                "System requires improvements "
                "before production deployment."
            )

        return reasoning