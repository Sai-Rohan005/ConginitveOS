# core/skills/skill_registry.py

"""
CognitiveOS - Skill Registry
---------------------------------------------------------

Responsibilities:
- dynamically register skills
- instantiate reusable skills
- centralize runtime capabilities
- support multi-domain execution
- reduce duplicated logic
- enable deterministic execution

Architecture:

Agents
    ↓
Skill Registry
    ↓
Skill Instances
    ↓
Core Runtime
"""

from __future__ import annotations

from typing import (
    Dict,
    Type,
    Any,
    Optional,
)

# ============================================================
# AI ENGINEERING SKILLS
# ============================================================

from domains.aiEngineering.skills.langchain_skill import (
    LangChainSkill,
)

from domains.aiEngineering.skills.rag_skills import (
    RAGSkill,
)

from domains.aiEngineering.skills.ollama_skill import (
    OllamaSkill,
)

from domains.aiEngineering.skills.vllm_skill import (
    VLLMSkill,
)

# ============================================================
# SKILL REGISTRY
# ============================================================


class SkillRegistry:

    """
    Centralized dynamic skill registry.
    """

    def __init__(self):

        self.registry: Dict[
            str,
            Type
        ] = {}

        self._register_default_skills()

    # ========================================================
    # REGISTER DEFAULT SKILLS
    # ========================================================

    def _register_default_skills(
        self,
    ):

        # ====================================================
        # AI ENGINEERING
        # ====================================================

        self.register_skill(
            "langchain_skill",
            LangChainSkill,
        )

        self.register_skill(
            "rag_skill",
            RAGSkill,
        )

        self.register_skill(
            "ollama_skill",
            OllamaSkill,
        )

        self.register_skill(
            "vllm_skill",
            VLLMSkill,
        )

        # ====================================================
        # DATASCIENCE PLACEHOLDERS
        # ====================================================

        self.register_skill(
            "pandas_skill",
            dict,
        )

        self.register_skill(
            "numpy_skill",
            dict,
        )

        self.register_skill(
            "visualization_skill",
            dict,
        )

        self.register_skill(
            "ml_training_skill",
            dict,
        )

        self.register_skill(
            "feature_engineering_skill",
            dict,
        )

        # ====================================================
        # CYBERSECURITY PLACEHOLDERS
        # ====================================================

        self.register_skill(
            "network_security_skill",
            dict,
        )

        self.register_skill(
            "jwt_security_skill",
            dict,
        )

        self.register_skill(
            "owasp_skill",
            dict,
        )

        self.register_skill(
            "api_security_skill",
            dict,
        )

        self.register_skill(
            "threat_modeling_skill",
            dict,
        )

    # ========================================================
    # REGISTER SKILL
    # ========================================================

    def register_skill(
        self,
        name: str,
        skill_class: Type,
    ):

        self.registry[name] = (
            skill_class
        )

    # ========================================================
    # GET SKILL CLASS
    # ========================================================

    def get_skill_class(
        self,
        name: str,
    ) -> Optional[Type]:

        return self.registry.get(
            name
        )

    # ========================================================
    # CREATE SKILL
    # ========================================================

    def create_skill(
        self,
        name: str,
    ) -> Any:

        skill_class = (
            self.get_skill_class(
                name
            )
        )

        if not skill_class:

            raise ValueError(
                f"Skill not found: {name}"
            )

        try:

            # ================================================
            # PLACEHOLDER SKILLS
            # ================================================

            if skill_class == dict:

                return {

                    "skill":
                        name,

                    "status":
                        "placeholder_skill",
                }

            return skill_class()

        except Exception as e:

            raise RuntimeError(

                f"Failed to create "
                f"skill '{name}': {str(e)}"
            )

    # ========================================================
    # SKILL EXISTS
    # ========================================================

    def skill_exists(
        self,
        name: str,
    ) -> bool:

        return name in self.registry

    # ========================================================
    # LIST SKILLS
    # ========================================================

    def list_skills(
        self,
    ) -> Dict[str, str]:

        return {

            name:
                cls.__name__

            for name, cls in (
                self.registry.items()
            )
        }

    # ========================================================
    # REMOVE SKILL
    # ========================================================

    def remove_skill(
        self,
        name: str,
    ):

        if name in self.registry:

            del self.registry[name]

    # ========================================================
    # CLEAR REGISTRY
    # ========================================================

    def clear_registry(
        self,
    ):

        self.registry.clear()

    # ========================================================
    # DOMAIN SKILLS
    # ========================================================

    def get_domain_skills(
        self,
        domain: str,
    ) -> Dict[str, Any]:

        domain_mapping = {

            "aiEngineering": [

                "langchain_skill",

                "rag_skill",

                "ollama_skill",

                "vllm_skill",
            ],

            "dataScience": [

                "pandas_skill",

                "numpy_skill",

                "visualization_skill",

                "ml_training_skill",

                "feature_engineering_skill",
            ],

            "cybersecurity": [

                "network_security_skill",

                "jwt_security_skill",

                "owasp_skill",

                "api_security_skill",

                "threat_modeling_skill",
            ],
        }

        skills = domain_mapping.get(
            domain,
            [],
        )

        return {

            skill_name:

                self.registry.get(
                    skill_name
                )

            for skill_name in skills
        }

    # ========================================================
    # EXPORT REGISTRY
    # ========================================================

    def export_registry(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_skills":
                len(self.registry),

            "skills": {

                name:
                    cls.__name__

                for name, cls in (
                    self.registry.items()
                )
            },
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

            "registered_skills":
                len(self.registry),

            "domains": [

                "aiEngineering",

                "dataScience",

                "cybersecurity",
            ],
        }


# ============================================================
# GLOBAL REGISTRY
# ============================================================

GLOBAL_SKILL_REGISTRY = (
    SkillRegistry()
)

# ============================================================
# FACTORY
# ============================================================


def get_skill_registry():

    return GLOBAL_SKILL_REGISTRY