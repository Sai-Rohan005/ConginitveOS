# core/orchestration/domain_router.py

"""
CognitiveOS - Domain Router
---------------------------------------------------------

Responsibilities:
- detect appropriate domain
- route queries intelligently
- perform keyword + semantic routing
- support multi-domain orchestration
- enable fallback routing
- minimize routing ambiguity
- provide routing confidence
- support autonomous cognition

Architecture:

Master Orchestrator
        ↓
Domain Router
        ↓
Domain Registry
        ↓
Domain Supervisor
"""

from __future__ import annotations

import traceback

from typing import (
    Dict,
    Any,
    List,
    Tuple,
)

# ============================================================
# DOMAIN REGISTRY
# ============================================================

from core.orchestration.domain_registry import (
    get_domain_registry,
)

# ============================================================
# DOMAIN ROUTER
# ============================================================


class DomainRouter:

    """
    Intelligent domain routing engine.
    """

    def __init__(self):

        self.domain_registry = (
            get_domain_registry()
        )

        # ====================================================
        # ROUTER CONFIG
        # ====================================================

        self.minimum_confidence = 0.15

        self.enable_multi_domain = True

        self.default_domain = (
            "research"
        )

    # ========================================================
    # MAIN ROUTING
    # ========================================================

    def route(
        self,
        query: str,
    ) -> Dict[str, Any]:

        try:

            query_lower = (
                query.lower()
            )

            # ================================================
            # SCORE DOMAINS
            # ================================================

            domain_scores = (
                self._score_domains(
                    query_lower
                )
            )

            # ================================================
            # SORT
            # ================================================

            sorted_domains = sorted(

                domain_scores.items(),

                key=lambda x: x[1],

                reverse=True,
            )

            # ================================================
            # NO MATCH
            # ================================================

            if not sorted_domains:

                return self._fallback_route(
                    query
                )

            # ================================================
            # TOP DOMAIN
            # ================================================

            top_domain = (
                sorted_domains[0]
            )

            selected_domain = (
                top_domain[0]
            )

            confidence = (
                top_domain[1]
            )

            # ================================================
            # LOW CONFIDENCE
            # ================================================

            if (

                confidence
                < self.minimum_confidence

            ):

                return self._fallback_route(
                    query
                )

            # ================================================
            # MULTI DOMAIN
            # ================================================

            secondary_domains = []

            if self.enable_multi_domain:

                secondary_domains = (

                    self._find_secondary_domains(

                        sorted_domains,

                        selected_domain,
                    )
                )

            # ================================================
            # SUPERVISOR
            # ================================================

            supervisor = (

                self.domain_registry
                .create_supervisor(
                    selected_domain
                )
            )

            # ================================================
            # RESULT
            # ================================================

            return {

                "success":
                    True,

                "query":
                    query,

                "selected_domain":
                    selected_domain,

                "confidence":
                    confidence,

                "secondary_domains":
                    secondary_domains,

                "supervisor":
                    supervisor,

                "domain_scores":
                    domain_scores,

                "routing_strategy":
                    "keyword_weighted_routing",
            }

        except Exception as e:

            return {

                "success":
                    False,

                "error":
                    str(e),

                "traceback":
                    traceback.format_exc(),
            }

    # ========================================================
    # SCORE DOMAINS
    # ========================================================

    def _score_domains(
        self,
        query: str,
    ) -> Dict[str, float]:

        scores = {}

        # ====================================================
        # DOMAINS
        # ====================================================

        domains = (

            self.domain_registry
            .list_domains()
        )

        for domain_name in domains:

            keywords = (

                self.domain_registry
                .get_domain_keywords(
                    domain_name
                )
            )

            metadata = (

                self.domain_registry
                .get_domain_metadata(
                    domain_name
                )
            )

            priority = metadata.get(
                "priority",
                1,
            )

            score = 0.0

            # ================================================
            # KEYWORD MATCHING
            # ================================================

            for keyword in keywords:

                keyword_lower = (
                    keyword.lower()
                )

                # EXACT PHRASE
                if keyword_lower in query:

                    score += 1.0

                # TOKEN OVERLAP
                query_tokens = set(
                    query.split()
                )

                keyword_tokens = set(
                    keyword_lower.split()
                )

                overlap = (

                    query_tokens
                    .intersection(
                        keyword_tokens
                    )
                )

                if overlap:

                    token_score = (

                        len(overlap)

                        / max(
                            len(keyword_tokens),
                            1,
                        )
                    )

                    score += (
                        token_score * 0.5
                    )

            # ================================================
            # PRIORITY WEIGHT
            # ================================================

            score *= (
                priority / 10
            )

            scores[
                domain_name
            ] = round(score, 4)

        return scores

    # ========================================================
    # SECONDARY DOMAINS
    # ========================================================

    def _find_secondary_domains(
        self,
        sorted_domains: List[
            Tuple[str, float]
        ],
        selected_domain: str,
    ) -> List[str]:

        secondary_domains = []

        for domain, score in (
            sorted_domains[1:]
        ):

            if score >= 0.5:

                secondary_domains.append(
                    domain
                )

        return secondary_domains

    # ========================================================
    # FALLBACK
    # ========================================================

    def _fallback_route(
        self,
        query: str,
    ) -> Dict[str, Any]:

        supervisor = (

            self.domain_registry
            .create_supervisor(
                self.default_domain
            )
        )

        return {

            "success":
                True,

            "query":
                query,

            "selected_domain":
                self.default_domain,

            "confidence":
                0.1,

            "secondary_domains":
                [],

            "supervisor":
                supervisor,

            "routing_strategy":
                "fallback_routing",
        }

    # ========================================================
    # DOMAIN SUGGESTIONS
    # ========================================================

    def suggest_domains(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:

        query_lower = (
            query.lower()
        )

        scores = (
            self._score_domains(
                query_lower
            )
        )

        sorted_scores = sorted(

            scores.items(),

            key=lambda x: x[1],

            reverse=True,
        )

        suggestions = []

        for domain, score in (
            sorted_scores
        ):

            metadata = (

                self.domain_registry
                .get_domain_metadata(
                    domain
                )
            )

            suggestions.append(

                {

                    "domain":
                        domain,

                    "score":
                        score,

                    "description":

                        metadata.get(
                            "description",
                            "",
                        ),
                }
            )

        return suggestions

    # ========================================================
    # MULTI DOMAIN ROUTE
    # ========================================================

    def multi_domain_route(
        self,
        query: str,
    ) -> Dict[str, Any]:

        scores = self._score_domains(
            query.lower()
        )

        sorted_scores = sorted(

            scores.items(),

            key=lambda x: x[1],

            reverse=True,
        )

        selected_domains = []

        for domain, score in (
            sorted_scores
        ):

            if score >= 0.5:

                selected_domains.append(

                    {

                        "domain":
                            domain,

                        "score":
                            score,

                        "supervisor":

                            self.domain_registry
                            .create_supervisor(
                                domain
                            ),
                    }
                )

        return {

            "success":
                True,

            "query":
                query,

            "domains":
                selected_domains,

            "strategy":
                "multi_domain_parallel_routing",
        }

    # ========================================================
    # EXPORT ROUTER STATE
    # ========================================================

    def export_state(
        self,
    ) -> Dict[str, Any]:

        return {

            "minimum_confidence":
                self.minimum_confidence,

            "enable_multi_domain":
                self.enable_multi_domain,

            "default_domain":
                self.default_domain,

            "domains":

                self.domain_registry
                .export_registry(),
        }

    # ========================================================
    # HEALTHCHECK
    # ========================================================

    def healthcheck(
        self,
    ) -> Dict[str, Any]:

        return {

            "status":
                "healthy",

            "registered_domains":

                len(

                    self.domain_registry
                    .list_domains()
                ),

            "multi_domain_enabled":
                self.enable_multi_domain,
        }


# ============================================================
# GLOBAL ROUTER
# ============================================================

GLOBAL_DOMAIN_ROUTER = (
    DomainRouter()
)

# ============================================================
# FACTORY
# ============================================================


def get_domain_router():

    return GLOBAL_DOMAIN_ROUTER