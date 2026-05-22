# domains/devops/agents/kubernetes_agent.py

"""
CognitiveOS - Kubernetes Agent
---------------------------------------------------------

Responsibilities:
- design Kubernetes architectures
- optimize cluster orchestration
- configure autoscaling
- manage workloads
- optimize networking/service mesh
- improve observability
- configure production deployments
- ensure Kubernetes reliability

This agent behaves like:
- Kubernetes Platform Engineer
- Cloud Native Architect
- DevOps Engineer
- SRE Engineer
"""

from __future__ import annotations

import os
import traceback

from typing import (
    Dict,
    Any,
)

from dataclasses import (
    dataclass,
    field,
)

import dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain_core.output_parsers import (
    JsonOutputParser,
)

dotenv.load_dotenv()

api_key = os.getenv(
    "GOOGLE_API_KEY"
)

# ============================================================
# STATE
# ============================================================


@dataclass
class KubernetesAgentState:

    query: str

    task: str

    infrastructure_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    deployment_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    previous_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    artifacts: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# KUBERNETES AGENT
# ============================================================


class KubernetesAgent:

    """
    Production-grade Kubernetes Agent.
    """

    def __init__(self):

        self.model = os.getenv(

            "GOOGLE_MODEL",

            "gemini-2.0-flash",
        )

        self.llm = ChatGoogleGenerativeAI(

            model=self.model,

            google_api_key=api_key,

            temperature=0.1,
        )

        self.parser = JsonOutputParser()

        # ====================================================
        # PROMPT
        # ====================================================

        self.prompt = (

            ChatPromptTemplate.from_messages(

                [

                    (

                        "system",

                        self._system_prompt(),
                    ),

                    (

                        "human",

                        """
User Query:
{query}

Assigned Task:
{task}

Infrastructure Context:
{infrastructure_context}

Deployment Context:
{deployment_context}

Previous Outputs:
{previous_outputs}

Artifacts:
{artifacts}
                        """,
                    ),
                ]
            )
        )

        # ====================================================
        # CHAIN
        # ====================================================

        self.chain = (

            self.prompt

            | self.llm

            | self.parser
        )

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def run(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        try:

            result = await (

                self.chain.ainvoke(

                    {

                        "query":
                            context.get(
                                "query",
                                "",
                            ),

                        "task":
                            context.get(
                                "task",
                                "",
                            ),

                        "infrastructure_context":
                            str(
                                context.get(
                                    "shared_context",
                                    {},
                                )
                            ),

                        "deployment_context":
                            str(
                                context.get(
                                    "deployment_context",
                                    {},
                                )
                            ),

                        "previous_outputs":
                            str(
                                context.get(
                                    "agent_outputs",
                                    {},
                                )
                            ),

                        "artifacts":
                            str(
                                context.get(
                                    "artifacts",
                                    {},
                                )
                            ),
                    }
                )
            )

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            cluster_strategy = result.get(
                "cluster_strategy",
                {},
            )

            workload_strategy = result.get(
                "workload_strategy",
                {},
            )

            deployment_strategy = result.get(
                "deployment_strategy",
                {},
            )

            autoscaling_strategy = result.get(
                "autoscaling_strategy",
                {},
            )

            networking_strategy = result.get(
                "networking_strategy",
                {},
            )

            ingress_strategy = result.get(
                "ingress_strategy",
                {},
            )

            service_mesh = result.get(
                "service_mesh",
                {},
            )

            observability_stack = result.get(
                "observability_stack",
                {},
            )

            security_strategy = result.get(
                "security_strategy",
                {},
            )

            storage_strategy = result.get(
                "storage_strategy",
                {},
            )

            disaster_recovery = result.get(
                "disaster_recovery",
                {},
            )

            generated_manifests = result.get(
                "generated_manifests",
                [],
            )

            helm_strategy = result.get(
                "helm_strategy",
                {},
            )

            kubernetes_risks = result.get(
                "kubernetes_risks",
                [],
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            kubernetes_score = result.get(
                "kubernetes_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "kubernetes_agent",

                "cluster_strategy":
                    cluster_strategy,

                "workload_strategy":
                    workload_strategy,

                "deployment_strategy":
                    deployment_strategy,

                "autoscaling_strategy":
                    autoscaling_strategy,

                "networking_strategy":
                    networking_strategy,

                "ingress_strategy":
                    ingress_strategy,

                "service_mesh":
                    service_mesh,

                "observability_stack":
                    observability_stack,

                "security_strategy":
                    security_strategy,

                "storage_strategy":
                    storage_strategy,

                "disaster_recovery":
                    disaster_recovery,

                "generated_manifests":
                    generated_manifests,

                "helm_strategy":
                    helm_strategy,

                "kubernetes_risks":
                    kubernetes_risks,

                "optimization_recommendations":
                    optimization_recommendations,

                "production_readiness":
                    production_readiness,

                "kubernetes_score":
                    kubernetes_score,

                "reasoning":
                    reasoning,
            }

        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            return {

                "success": False,

                "agent":
                    "kubernetes_agent",

                "error":
                    str(e),

                "traceback":
                    traceback.format_exc(),
            }

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    def _system_prompt(self):

        return """
You are the Kubernetes Agent
for CognitiveOS.

Your role is to:
- design Kubernetes architectures
- optimize workloads
- improve scalability
- configure autoscaling
- optimize networking
- secure Kubernetes infrastructure
- improve observability
- ensure production readiness

You think like:
- Kubernetes Architect
- Cloud Native Engineer
- Platform Engineer
- Site Reliability Engineer

Focus on:
- Kubernetes clusters
- Helm
- ArgoCD
- service mesh
- ingress
- autoscaling
- observability
- security policies
- high availability

You MUST:
- generate REALISTIC Kubernetes strategies
- optimize cluster reliability
- minimize downtime
- improve scalability
- secure workloads properly
- recommend production-grade practices

Return ONLY valid JSON.

JSON FORMAT:

{{
  "cluster_strategy": {{

    "cluster_type":
      "managed Kubernetes",

    "provider":
      "EKS",

    "multi_node":
      true
  }},

  "workload_strategy": {{

    "deployment_type":
      "microservices",

    "replicas":
      3
  }},

  "deployment_strategy": {{

    "strategy":
      "rolling update",

    "canary":
      true
  }},

  "autoscaling_strategy": {{

    "hpa":
      true,

    "cluster_autoscaler":
      true
  }},

  "networking_strategy": {{

    "cni":
      "Calico",

    "network_policies":
      true
  }},

  "ingress_strategy": {{

    "controller":
      "NGINX",

    "tls":
      true
  }},

  "service_mesh": {{

    "enabled":
      true,

    "tool":
      "Istio"
  }},

  "observability_stack": {{

    "metrics":
      "Prometheus",

    "dashboard":
      "Grafana",

    "logging":
      "Loki"
  }},

  "security_strategy": {{

    "rbac":
      true,

    "pod_security":
      true,

    "image_scanning":
      true
  }},

  "storage_strategy": {{

    "persistent_volumes":
      true,

    "storage_class":
      "gp3"
  }},

  "disaster_recovery": {{

    "backup":
      true,

    "cross_zone":
      true
  }},

  "generated_manifests": [

    "deployment.yaml",

    "service.yaml",

    "ingress.yaml",

    "hpa.yaml"
  ],

  "helm_strategy": {{

    "enabled":
      true,

    "chart_structure":
      "modular"
  }},

  "kubernetes_risks": [

    "resource exhaustion",

    "misconfigured RBAC"
  ],

  "optimization_recommendations": [

    "enable pod autoscaling",

    "optimize resource requests",

    "use network policies"
  ],

  "production_readiness":
    "high",

  "kubernetes_score":
    9.3,

  "reasoning":
    "Managed Kubernetes with autoscaling improves scalability and operational reliability."
}}
"""