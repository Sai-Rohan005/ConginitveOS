# domains/devops/agents/infra_agent.py

"""
CognitiveOS - Infrastructure Agent
---------------------------------------------------------

Responsibilities:
- design cloud infrastructure
- optimize scalability
- configure IaC architectures
- manage Kubernetes infrastructure
- optimize networking
- analyze reliability
- improve fault tolerance
- enable production-grade infrastructure

This agent behaves like:
- Cloud Architect
- Infrastructure Engineer
- Platform Engineer
- Site Reliability Engineer
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
class InfraAgentState:

    query: str

    task: str

    architecture_context: Dict[
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
# INFRA AGENT
# ============================================================


class InfraAgent:

    """
    Production-grade Infrastructure Agent.
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

Architecture Context:
{architecture_context}

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

                        "architecture_context":
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

            infrastructure_strategy = result.get(
                "infrastructure_strategy",
                {},
            )

            cloud_architecture = result.get(
                "cloud_architecture",
                {},
            )

            kubernetes_architecture = result.get(
                "kubernetes_architecture",
                {},
            )

            networking_strategy = result.get(
                "networking_strategy",
                {},
            )

            storage_strategy = result.get(
                "storage_strategy",
                {},
            )

            database_strategy = result.get(
                "database_strategy",
                {},
            )

            scalability_strategy = result.get(
                "scalability_strategy",
                {},
            )

            disaster_recovery = result.get(
                "disaster_recovery",
                {},
            )

            high_availability = result.get(
                "high_availability",
                {},
            )

            infrastructure_security = result.get(
                "infrastructure_security",
                [],
            )

            observability_stack = result.get(
                "observability_stack",
                {},
            )

            iac_strategy = result.get(
                "iac_strategy",
                {},
            )

            cost_optimization = result.get(
                "cost_optimization",
                [],
            )

            generated_configs = result.get(
                "generated_configs",
                [],
            )

            infrastructure_risks = result.get(
                "infrastructure_risks",
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

            infrastructure_score = result.get(
                "infrastructure_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "infra_agent",

                "infrastructure_strategy":
                    infrastructure_strategy,

                "cloud_architecture":
                    cloud_architecture,

                "kubernetes_architecture":
                    kubernetes_architecture,

                "networking_strategy":
                    networking_strategy,

                "storage_strategy":
                    storage_strategy,

                "database_strategy":
                    database_strategy,

                "scalability_strategy":
                    scalability_strategy,

                "disaster_recovery":
                    disaster_recovery,

                "high_availability":
                    high_availability,

                "infrastructure_security":
                    infrastructure_security,

                "observability_stack":
                    observability_stack,

                "iac_strategy":
                    iac_strategy,

                "cost_optimization":
                    cost_optimization,

                "generated_configs":
                    generated_configs,

                "infrastructure_risks":
                    infrastructure_risks,

                "optimization_recommendations":
                    optimization_recommendations,

                "production_readiness":
                    production_readiness,

                "infrastructure_score":
                    infrastructure_score,

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
                    "infra_agent",

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
You are the Infrastructure Agent
for CognitiveOS.

Your role is to:
- design cloud infrastructure
- optimize reliability
- configure scalable systems
- manage Kubernetes architecture
- improve fault tolerance
- enable observability
- optimize networking
- ensure production readiness

You think like:
- Cloud Architect
- Infrastructure Engineer
- Platform Engineer
- SRE Architect

Focus on:
- AWS/GCP/Azure
- Kubernetes
- Terraform
- autoscaling
- networking
- observability
- high availability
- disaster recovery
- cost optimization

You MUST:
- generate REALISTIC infrastructure plans
- optimize scalability
- minimize downtime
- improve reliability
- enable production observability
- secure infrastructure properly

Return ONLY valid JSON.

JSON FORMAT:

{{
  "infrastructure_strategy": {{

    "deployment_model":
      "cloud-native",

    "environment":
      "kubernetes",

    "scalability":
      "horizontal"
  }},

  "cloud_architecture": {{

    "provider":
      "AWS",

    "multi_az":
      true,

    "multi_region":
      false
  }},

  "kubernetes_architecture": {{

    "managed_cluster":
      true,

    "autoscaling":
      true,

    "service_mesh":
      "Istio"
  }},

  "networking_strategy": {{

    "ingress":
      "NGINX",

    "load_balancer":
      "ALB",

    "private_subnets":
      true
  }},

  "storage_strategy": {{

    "object_storage":
      "S3",

    "persistent_volumes":
      true
  }},

  "database_strategy": {{

    "database":
      "PostgreSQL",

    "replication":
      true,

    "backup":
      true
  }},

  "scalability_strategy": {{

    "horizontal_scaling":
      true,

    "hpa":
      true
  }},

  "disaster_recovery": {{

    "backup_enabled":
      true,

    "rto":
      "15 minutes",

    "rpo":
      "5 minutes"
  }},

  "high_availability": {{

    "enabled":
      true,

    "redundancy":
      "multi-node"
  }},

  "infrastructure_security": [

    "network policies",

    "IAM least privilege",

    "private networking"
  ],

  "observability_stack": {{

    "metrics":
      "Prometheus",

    "logging":
      "ELK",

    "tracing":
      "Jaeger"
  }},

  "iac_strategy": {{

    "tool":
      "Terraform",

    "modular":
      true
  }},

  "cost_optimization": [

    "spot instances",

    "autoscaling",

    "resource quotas"
  ],

  "generated_configs": [

    "terraform/main.tf",

    "k8s/deployment.yaml",

    "helm/values.yaml"
  ],

  "infrastructure_risks": [

    "single-region dependency",

    "database bottleneck"
  ],

  "optimization_recommendations": [

    "enable node autoscaling",

    "optimize resource requests",

    "use managed databases"
  ],

  "production_readiness":
    "high",

  "infrastructure_score":
    9.2,

  "reasoning":
    "Cloud-native Kubernetes infrastructure improves scalability and fault tolerance."
}}
"""