"""
CognitiveOS - Domain Router (LLM-Based)
---------------------------------------------------------

Replaced deterministic keyword routing with LLM-driven semantic routing.
"""

from __future__ import annotations

import json
import os
import traceback
from typing import Dict, Any, List, Tuple

import dotenv
from langchain.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from core.orchestration.domain_registry import get_domain_registry
dotenv.load_dotenv()

api_key = os.getenv(
    "GOOGLE_API_KEY"
)

class DomainRouter:
    """
    LLM-powered domain routing engine.
    """

    def __init__(self):

        self.domain_registry = get_domain_registry()

        # ====================================================
        # ROUTER CONFIG
        # ====================================================

        self.minimum_confidence = 0.15
        self.enable_multi_domain = True
        self.default_domain = "research"

        # ⚠️ You must inject your LLM client here
        # expected interface: self.llm.generate(prompt: str) -> str
        self.model = os.getenv(

            "GOOGLE_MODEL",

            "gemini-2.0-flash",
        )

        self.llm = ChatGoogleGenerativeAI(

            model=self.model,

            google_api_key=api_key,

            temperature=0.1,
        )

    # ========================================================
    # LLM CORE ROUTER
    # ========================================================

    def _llm_route(self, query: str) -> Dict[str, Any]:
        """
        Uses LLM to decide best domain(s).
        """

        domains = self.domain_registry.list_domains()

        domain_descriptions = {
            d: self.domain_registry.get_domain_metadata(d).get("description", "")
            for d in domains
        }

        prompt = f"""
You are an intelligent domain routing system.

Your job:
Select the BEST domain(s) for the user query.

AVAILABLE DOMAINS:
{json.dumps(domain_descriptions, indent=2)}

RULES:
- Choose 1 primary domain
- Optionally choose secondary domains if relevant
- Return ONLY valid JSON
- Confidence must be 0.0 - 1.0

OUTPUT FORMAT:
{{
  "selected_domain": "string",
  "confidence": float,
  "secondary_domains": ["string"]
}}

USER QUERY:
{query}
"""

        # ====================================================
        # LLM CALL
        # ====================================================

        if not self.llm:
            # safe fallback if LLM not attached
            return {
                "selected_domain": self.default_domain,
                "confidence": 0.1,
                "secondary_domains": [],
            }

        response = self.llm.invoke([HumanMessage(content=prompt)]).content

        try:
            return json.loads(response)
        except Exception:
            # fallback parse failure
            return {
                "selected_domain": self.default_domain,
                "confidence": 0.1,
                "secondary_domains": [],
            }

    # ========================================================
    # MAIN ROUTE (SINGLE DOMAIN)
    # ========================================================

    def route(self, query: str) -> Dict[str, Any]:
        try:
            llm_result = self._llm_route(query)

            selected_domain = llm_result.get("selected_domain", self.default_domain)
            confidence = llm_result.get("confidence", 0.2)
            secondary_domains = llm_result.get("secondary_domains", [])

            supervisor = self.domain_registry.create_supervisor(selected_domain)

            return {
                "success": True,
                "query": query,
                "selected_domain": selected_domain,
                "confidence": confidence,
                "secondary_domains": secondary_domains,
                "supervisor": supervisor,
                "routing_strategy": "llm_semantic_routing",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }

    # ========================================================
    # MULTI DOMAIN ROUTE (LLM DRIVEN)
    # ========================================================

    def multi_domain_route(self, query: str) -> Dict[str, Any]:
        try:
            llm_result = self._llm_route(query)

            primary = llm_result.get("selected_domain", self.default_domain)
            secondary = llm_result.get("secondary_domains", [])

            # combine + deduplicate
            domains = [primary] + [d for d in secondary if d != primary]

            selected_domains = []

            for domain in domains:
                selected_domains.append({
                    "domain": domain,
                    "score": 1.0,
                    "supervisor": self.domain_registry.create_supervisor(domain),
                })

            return {
                "success": True,
                "query": query,
                "domains": selected_domains,
                "strategy": "llm_multi_domain_routing",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }

    # ========================================================
    # DOMAIN SUGGESTIONS (LLM-OPTIONAL ENHANCEMENT)
    # ========================================================

    def suggest_domains(self, query: str) -> List[Dict[str, Any]]:
        try:
            llm_result = self._llm_route(query)

            suggestions = []

            primary = llm_result.get("selected_domain")
            if primary:
                meta = self.domain_registry.get_domain_metadata(primary)
                suggestions.append({
                    "domain": primary,
                    "score": llm_result.get("confidence", 0.5),
                    "description": meta.get("description", ""),
                })

            for d in llm_result.get("secondary_domains", []):
                meta = self.domain_registry.get_domain_metadata(d)
                suggestions.append({
                    "domain": d,
                    "score": 0.7,
                    "description": meta.get("description", ""),
                })

            return suggestions

        except Exception:
            return []

    # ========================================================
    # EXPORT STATE
    # ========================================================

    def export_state(self) -> Dict[str, Any]:
        return {
            "routing_strategy": "llm_semantic",
            "minimum_confidence": self.minimum_confidence,
            "enable_multi_domain": self.enable_multi_domain,
            "default_domain": self.default_domain,
            "domains": self.domain_registry.export_registry(),
        }

    # ========================================================
    # HEALTHCHECK
    # ========================================================

    def healthcheck(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "routing_mode": "llm" if self.llm else "fallback",
            "registered_domains": len(self.domain_registry.list_domains()),
            "multi_domain_enabled": self.enable_multi_domain,
        }


# ============================================================
# GLOBAL ROUTER
# ============================================================

GLOBAL_DOMAIN_ROUTER = DomainRouter()


def get_domain_router():
    return GLOBAL_DOMAIN_ROUTER