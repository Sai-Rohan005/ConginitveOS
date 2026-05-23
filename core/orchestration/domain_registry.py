# core/orchestration/domain_registry.py

"""
CognitiveOS - Domain Registry
---------------------------------------------------------

Responsibilities:
- register domain supervisors
- manage domain metadata
- provide centralized domain access
- support multi-domain cognition
- enable scalable orchestration
- provide domain capabilities
- support plugin architecture
- enable autonomous routing

Architecture:

Master Orchestrator
        ↓
Domain Registry
        ↓
Domain Router
        ↓
Domain Supervisor
"""

from __future__ import annotations

import traceback

from typing import (
    Dict,
    Any,
    Optional,
    Type,
)

# ============================================================
# DOMAIN SUPERVISORS
# ============================================================

from domains.aiEngineering.ai_engineering_domain import (
    AIEngineeringDomain,
)

from domains.cybersecurity.supervisor.cybersecurity_supervisor import (
    CyberSecuritySupervisor,
)

from domains.datascience.supervisor.datascience_supervisor import (
    DataScienceSupervisor,
)

from domains.devops.supervisor.devops_supervisor import (
    DevOpsSupervisor,
)

from domains.research.supervisor.research_supervisor import (
    ResearchSupervisor,
)

# ============================================================
# DOMAIN REGISTRY
# ============================================================


class DomainRegistry:

    """
    Centralized domain registry
    for CognitiveOS.
    """

    def __init__(self):

        # ====================================================
        # REGISTRY
        # ====================================================

        self.registry: Dict[
            str,
            Type
        ] = {}

        # ====================================================
        # METADATA
        # ====================================================

        self.domain_metadata: Dict[
            str,
            Dict[str, Any]
        ] = {}

        # ====================================================
        # REGISTER DEFAULT DOMAINS
        # ====================================================

        self._register_default_domains()

    # ========================================================
    # REGISTER DEFAULT DOMAINS
    # ========================================================

    def _register_default_domains(
        self,
    ):

        # ====================================================
        # AI ENGINEERING
        # ====================================================

        self.register_domain(

            domain_name="aiEngineering",

            supervisor_class=
                AIEngineeringDomain,

            metadata={

                "description":
                    "LLM, RAG, "
                    "training, inference",

                "keywords": [

                    "llm",

                    "rag",

                    "transformer",

                    "training",

                    "vector db",

                    "inference",

                    "evaluation",

                    "embedding",
                ],

                "priority":
                    10,
            },
        )

        # ====================================================
        # CYBERSECURITY
        # ====================================================

        self.register_domain(

            domain_name="cybersecurity",

            supervisor_class=
                CyberSecuritySupervisor,

            metadata={

                "description":
                    "Security analysis "
                    "and penetration testing",

                "keywords": [

                    "vulnerability",

                    "pentest",

                    "exploit",

                    "security",

                    "authentication",

                    "authorization",

                    "malware",

                    "attack",
                ],

                "priority":
                    9,
            },
        )

        # ====================================================
        # DATA SCIENCE
        # ====================================================

        self.register_domain(

            domain_name="dataScience",

            supervisor_class=
                DataScienceSupervisor,

            metadata={

                "description":
                    "EDA, training, "
                    "visualization",

                "keywords": [

                    "data analysis",

                    "eda",

                    "visualization",

                    "feature engineering",

                    "training",

                    "dataset",

                    "statistics",

                    "machine learning",
                ],

                "priority":
                    8,
            },
        )

        # ====================================================
        # DEVOPS
        # ====================================================

        self.register_domain(

            domain_name="devops",

            supervisor_class=
                DevOpsSupervisor,

            metadata={

                "description":
                    "Infrastructure, "
                    "CI/CD, Kubernetes",

                "keywords": [

                    "docker",

                    "kubernetes",

                    "terraform",

                    "helm",

                    "deployment",

                    "cicd",

                    "monitoring",

                    "cloud",

                    "aws",

                    "gcp",

                    "azure",
                ],

                "priority":
                    9,
            },
        )

        # ====================================================
        # RESEARCH
        # ====================================================

        self.register_domain(

            domain_name="research",

            supervisor_class=
                ResearchSupervisor,

            metadata={

                "description":
                    "Research, papers, "
                    "summarization",

                "keywords": [

                    "research",

                    "paper",

                    "citation",

                    "literature",

                    "survey",

                    "report",

                    "summary",

                    "analysis",
                ],

                "priority":
                    7,
            },
        )

    # ========================================================
    # REGISTER DOMAIN
    # ========================================================

    def register_domain(
        self,
        domain_name: str,
        supervisor_class: Type,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        self.registry[
            domain_name
        ] = supervisor_class

        self.domain_metadata[
            domain_name
        ] = metadata or {}

    # ========================================================
    # DOMAIN EXISTS
    # ========================================================

    def domain_exists(
        self,
        domain_name: str,
    ) -> bool:

        return domain_name in (
            self.registry
        )

    # ========================================================
    # GET SUPERVISOR CLASS
    # ========================================================

    def get_supervisor_class(
        self,
        domain_name: str,
    ) -> Optional[Type]:

        return self.registry.get(
            domain_name
        )

    # ========================================================
    # CREATE SUPERVISOR
    # ========================================================

    def create_supervisor(
        self,
        domain_name: str,
    ) -> Any:

        try:

            supervisor_class = (

                self
                .get_supervisor_class(
                    domain_name
                )
            )

            if not supervisor_class:

                raise ValueError(

                    f"Domain not found: "
                    f"{domain_name}"
                )

            return supervisor_class()

        except Exception as e:

            raise RuntimeError(

                f"Failed to create "
                f"supervisor for "
                f"domain '{domain_name}': "
                f"{str(e)}"
            )

    # ========================================================
    # GET DOMAIN METADATA
    # ========================================================

    def get_domain_metadata(
        self,
        domain_name: str,
    ) -> Dict[str, Any]:

        return self.domain_metadata.get(
            domain_name,
            {},
        )

    # ========================================================
    # GET DOMAIN KEYWORDS
    # ========================================================

    def get_domain_keywords(
        self,
        domain_name: str,
    ):

        metadata = (
            self.get_domain_metadata(
                domain_name
            )
        )

        return metadata.get(
            "keywords",
            [],
        )

    # ========================================================
    # LIST DOMAINS
    # ========================================================

    def list_domains(
        self,
    ) -> Dict[str, str]:

        return {

            domain:
                cls.__name__

            for domain, cls in (
                self.registry.items()
            )
        }

    # ========================================================
    # EXPORT REGISTRY
    # ========================================================

    def export_registry(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_domains":
                len(self.registry),

            "domains": {

                domain: {

                    "supervisor":
                        cls.__name__,

                    "metadata":
                        self.domain_metadata.get(
                            domain,
                            {},
                        ),
                }

                for domain, cls in (
                    self.registry.items()
                )
            },
        }

    # ========================================================
    # REMOVE DOMAIN
    # ========================================================

    def remove_domain(
        self,
        domain_name: str,
    ):

        if domain_name in (
            self.registry
        ):

            del self.registry[
                domain_name
            ]

        if domain_name in (
            self.domain_metadata
        ):

            del self.domain_metadata[
                domain_name
            ]

    # ========================================================
    # CLEAR REGISTRY
    # ========================================================

    def clear_registry(
        self,
    ):

        self.registry.clear()

        self.domain_metadata.clear()

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
                len(self.registry),

            "domains":
                list(
                    self.registry.keys()
                ),
        }

    # ========================================================
    # DEBUG EXPORT
    # ========================================================

    def debug_export(
        self,
    ) -> Dict[str, Any]:

        return {

            "registry":
                self.export_registry(),

            "metadata":
                self.domain_metadata,
        }


# ============================================================
# GLOBAL REGISTRY
# ============================================================

GLOBAL_DOMAIN_REGISTRY = (
    DomainRegistry()
)

# ============================================================
# FACTORY
# ============================================================


def get_domain_registry():

    return GLOBAL_DOMAIN_REGISTRY