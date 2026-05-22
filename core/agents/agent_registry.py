# core/agents/agent_registry.py

"""
CognitiveOS - Agent Registry
---------------------------------------------------------

Responsibilities:
- dynamically register agents
- instantiate agents
- provide centralized access
- support multi-domain execution
- enable plugin architecture
- reduce hardcoded imports
- support deterministic runtime loading
- enable scalable multi-domain cognition

Architecture:

Workflow Executor
        ↓
Agent Registry
        ↓
Dynamic Agent Loading
        ↓
Agent Instance
"""

from __future__ import annotations

import traceback

from typing import (
    Dict,
    Any,
    Type,
    Optional,
)

# ============================================================
# SOFTWARE ENGINEERING
# ============================================================

from domains.softwareEngineering.agents.architecture_agent import (
    ArchitectureAgent,
)

from domains.softwareEngineering.agents.code_agent import (
    CodeAgent,
)

from domains.softwareEngineering.agents.debug_agent import (
    DebugAgent,
)

from domains.softwareEngineering.agents.reflection_agent import (
    ReflectionAgent,
)

# ============================================================
# AI ENGINEERING
# ============================================================

from domains.aiEngineering.agents.llm_agent import (
    LLMAgent,
)

from domains.aiEngineering.agents.rag_agent import (
    RAGAgent,
)

from domains.aiEngineering.agents.vector_db_agent import (
    VectorDBAgent,
)

from domains.aiEngineering.agents.training_agent import (
    TrainingAgent as AITrainingAgent,
)

from domains.aiEngineering.agents.inference_agent import (
    InferenceAgent,
)

from domains.aiEngineering.agents.evaluation_agent import (
    EvaluationAgent,
)

# ============================================================
# CYBERSECURITY
# ============================================================

from domains.cybersecurity.agents.auth_security_agent import (
    AuthSecurityAgent,
)

from domains.cybersecurity.agents.exploit_analysis_agent import (
    ExploitAnalysisAgent,
)

from domains.cybersecurity.agents.pentest_agent import (
    PentestAgent,
)

from domains.cybersecurity.agents.vuln_agent import (
    VulnerabilityAgent,
)

# ============================================================
# DATA SCIENCE
# ============================================================

from domains.datascience.agents.eda_agent import (
    EDAAgent,
)

from domains.datascience.agents.feature_engineering_agent import (
    FeatureEngineeringAgent,
)

from domains.datascience.agents.training_agent import (
    TrainingAgent as DSTrainingAgent,
)

from domains.datascience.agents.visualization_agent import (
    VisualizationAgent,
)

# ============================================================
# DEVOPS
# ============================================================

from domains.devops.agents.cicd_agent import (
    CICDAgent,
)

from domains.devops.agents.infra_agent import (
    InfraAgent,
)

from domains.devops.agents.kubernetes_agent import (
    KubernetesAgent,
)

from domains.devops.agents.monitoring_agent import (
    MonitoringAgent,
)

# ============================================================
# RESEARCH
# ============================================================

from domains.research.agents.search_agent import (
    SearchAgent,
)

from domains.research.agents.summarize_agent import (
    SummarizeAgent,
)

from domains.research.agents.citation_agent import (
    CitationAgent,
)

from domains.research.agents.report_agent import (
    ReportAgent,
)

# ============================================================
# AGENT REGISTRY
# ============================================================


class AgentRegistry:

    """
    Centralized dynamic agent registry.
    """

    def __init__(self):

        self.registry: Dict[
            str,
            Type
        ] = {}

        self.domain_registry: Dict[
            str,
            list
        ] = {}

        self.agent_metadata: Dict[
            str,
            Dict[str, Any]
        ] = {}

        self._register_default_agents()

    # ========================================================
    # REGISTER DEFAULT AGENTS
    # ========================================================

    def _register_default_agents(
        self,
    ):

        # ====================================================
        # SOFTWARE ENGINEERING
        # ====================================================

        self.register_agent(
            name="architecture_agent",
            agent_class=ArchitectureAgent,
            domain="softwareEngineering",
            metadata={
                "role":
                    "system_design",
            },
        )

        self.register_agent(
            name="code_agent",
            agent_class=CodeAgent,
            domain="softwareEngineering",
            metadata={
                "role":
                    "implementation",
            },
        )

        self.register_agent(
            name="debug_agent",
            agent_class=DebugAgent,
            domain="softwareEngineering",
            metadata={
                "role":
                    "debugging",
            },
        )

        self.register_agent(
            name="reflection_agent",
            agent_class=ReflectionAgent,
            domain="softwareEngineering",
            metadata={
                "role":
                    "reflection",
            },
        )

        # ====================================================
        # AI ENGINEERING
        # ====================================================

        self.register_agent(
            "llm_agent",
            LLMAgent,
            "aiEngineering",
        )

        self.register_agent(
            "rag_agent",
            RAGAgent,
            "aiEngineering",
        )

        self.register_agent(
            "vector_db_agent",
            VectorDBAgent,
            "aiEngineering",
        )

        self.register_agent(
            "ai_training_agent",
            AITrainingAgent,
            "aiEngineering",
        )

        self.register_agent(
            "inference_agent",
            InferenceAgent,
            "aiEngineering",
        )

        self.register_agent(
            "evaluation_agent",
            EvaluationAgent,
            "aiEngineering",
        )

        # ====================================================
        # CYBERSECURITY
        # ====================================================

        self.register_agent(
            "authsecurity_agent",
            AuthSecurityAgent,
            "cybersecurity",
        )

        self.register_agent(
            "exploit_analysis_agent",
            ExploitAnalysisAgent,
            "cybersecurity",
        )

        self.register_agent(
            "pentest_agent",
            PentestAgent,
            "cybersecurity",
        )

        self.register_agent(
            "vuln_agent",
            VulnerabilityAgent,
            "cybersecurity",
        )

        # ====================================================
        # DATA SCIENCE
        # ====================================================

        self.register_agent(
            "eda_agent",
            EDAAgent,
            "dataScience",
        )

        self.register_agent(
            "feature_engineering_agent",
            FeatureEngineeringAgent,
            "dataScience",
        )

        self.register_agent(
            "ds_training_agent",
            DSTrainingAgent,
            "dataScience",
        )

        self.register_agent(
            "visualization_agent",
            VisualizationAgent,
            "dataScience",
        )

        # ====================================================
        # DEVOPS
        # ====================================================

        self.register_agent(
            "cicd_agent",
            CICDAgent,
            "devops",
        )

        self.register_agent(
            "infra_agent",
            InfraAgent,
            "devops",
        )

        self.register_agent(
            "kubernetes_agent",
            KubernetesAgent,
            "devops",
        )

        self.register_agent(
            "monitoring_agent",
            MonitoringAgent,
            "devops",
        )

        # ====================================================
        # RESEARCH
        # ====================================================

        self.register_agent(
            "search_agent",
            SearchAgent,
            "research",
        )

        self.register_agent(
            "summarize_agent",
            SummarizeAgent,
            "research",
        )

        self.register_agent(
            "citation_agent",
            CitationAgent,
            "research",
        )

        self.register_agent(
            "report_agent",
            ReportAgent,
            "research",
        )

    # ========================================================
    # REGISTER AGENT
    # ========================================================

    def register_agent(
        self,
        name: str,
        agent_class: Type,
        domain: str = "general",
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        self.registry[name] = (
            agent_class
        )

        # ====================================================
        # DOMAIN REGISTRY
        # ====================================================

        if domain not in (
            self.domain_registry
        ):

            self.domain_registry[
                domain
            ] = []

        self.domain_registry[
            domain
        ].append(name)

        # ====================================================
        # METADATA
        # ====================================================

        self.agent_metadata[
            name
        ] = metadata or {}

    # ========================================================
    # GET AGENT CLASS
    # ========================================================

    def get_agent_class(
        self,
        name: str,
    ) -> Optional[Type]:

        return self.registry.get(
            name
        )

    # ========================================================
    # CREATE AGENT
    # ========================================================

    def create_agent(
        self,
        name: str,
    ) -> Any:

        try:

            agent_class = (
                self.get_agent_class(
                    name
                )
            )

            if not agent_class:

                raise ValueError(
                    f"Agent not found: {name}"
                )

            agent = agent_class()

            return agent

        except Exception as e:

            raise RuntimeError(

                f"Failed to create "
                f"agent '{name}': "
                f"{str(e)}"
            )

    # ========================================================
    # AGENT EXISTS
    # ========================================================

    def agent_exists(
        self,
        name: str,
    ) -> bool:

        return name in self.registry

    # ========================================================
    # GET DOMAIN AGENTS
    # ========================================================

    def get_domain_agents(
        self,
        domain: str,
    ) -> Dict[str, Any]:

        agents = self.domain_registry.get(
            domain,
            [],
        )

        return {

            agent_name:

                self.registry.get(
                    agent_name
                )

            for agent_name in agents
        }

    # ========================================================
    # LIST AGENTS
    # ========================================================

    def list_agents(
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
    # GET AGENT METADATA
    # ========================================================

    def get_agent_metadata(
        self,
        agent_name: str,
    ) -> Dict[str, Any]:

        return self.agent_metadata.get(
            agent_name,
            {},
        )

    # ========================================================
    # REMOVE AGENT
    # ========================================================

    def remove_agent(
        self,
        name: str,
    ):

        if name in self.registry:

            del self.registry[name]

        if name in self.agent_metadata:

            del self.agent_metadata[
                name
            ]

        for domain in (
            self.domain_registry
        ):

            if name in (
                self.domain_registry[
                    domain
                ]
            ):

                self.domain_registry[
                    domain
                ].remove(name)

    # ========================================================
    # CLEAR REGISTRY
    # ========================================================

    def clear_registry(
        self,
    ):

        self.registry.clear()

        self.domain_registry.clear()

        self.agent_metadata.clear()

    # ========================================================
    # EXPORT REGISTRY
    # ========================================================

    def export_registry(
        self,
    ) -> Dict[str, Any]:

        return {

            "total_agents":
                len(self.registry),

            "domains":
                self.domain_registry,

            "agents": {

                name: {

                    "class":
                        cls.__name__,

                    "metadata":
                        self.agent_metadata.get(
                            name,
                            {},
                        ),
                }

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

            "registered_agents":
                len(self.registry),

            "registered_domains":
                len(
                    self.domain_registry
                ),

            "domains": list(

                self.domain_registry.keys()
            ),
        }


# ============================================================
# GLOBAL REGISTRY
# ============================================================

GLOBAL_AGENT_REGISTRY = (
    AgentRegistry()
)

# ============================================================
# FACTORY
# ============================================================


def get_agent_registry():

    return GLOBAL_AGENT_REGISTRY