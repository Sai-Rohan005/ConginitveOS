# domains/devops/agents/cicd_agent.py

"""
CognitiveOS - CI/CD Agent
---------------------------------------------------------

Responsibilities:
- design CI/CD pipelines
- optimize deployment workflows
- automate infrastructure delivery
- configure GitOps workflows
- improve release engineering
- validate deployment strategies
- optimize rollback mechanisms
- enable production-grade DevOps

This agent behaves like:
- DevOps Engineer
- Release Engineer
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
class CICDAgentState:

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
# CICD AGENT
# ============================================================


class CICDAgent:

    """
    Production-grade CI/CD orchestration agent.
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

            pipeline_strategy = result.get(
                "pipeline_strategy",
                {},
            )

            cicd_platform = result.get(
                "cicd_platform",
                {},
            )

            build_pipeline = result.get(
                "build_pipeline",
                {},
            )

            deployment_pipeline = result.get(
                "deployment_pipeline",
                {},
            )

            testing_strategy = result.get(
                "testing_strategy",
                {},
            )

            rollback_strategy = result.get(
                "rollback_strategy",
                {},
            )

            gitops_strategy = result.get(
                "gitops_strategy",
                {},
            )

            container_strategy = result.get(
                "container_strategy",
                {},
            )

            kubernetes_strategy = result.get(
                "kubernetes_strategy",
                {},
            )

            monitoring_strategy = result.get(
                "monitoring_strategy",
                {},
            )

            security_controls = result.get(
                "security_controls",
                [],
            )

            scalability_analysis = result.get(
                "scalability_analysis",
                {},
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            generated_configs = result.get(
                "generated_configs",
                [],
            )

            deployment_risks = result.get(
                "deployment_risks",
                [],
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            devops_score = result.get(
                "devops_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "cicd_agent",

                "pipeline_strategy":
                    pipeline_strategy,

                "cicd_platform":
                    cicd_platform,

                "build_pipeline":
                    build_pipeline,

                "deployment_pipeline":
                    deployment_pipeline,

                "testing_strategy":
                    testing_strategy,

                "rollback_strategy":
                    rollback_strategy,

                "gitops_strategy":
                    gitops_strategy,

                "container_strategy":
                    container_strategy,

                "kubernetes_strategy":
                    kubernetes_strategy,

                "monitoring_strategy":
                    monitoring_strategy,

                "security_controls":
                    security_controls,

                "scalability_analysis":
                    scalability_analysis,

                "optimization_recommendations":
                    optimization_recommendations,

                "generated_configs":
                    generated_configs,

                "deployment_risks":
                    deployment_risks,

                "production_readiness":
                    production_readiness,

                "devops_score":
                    devops_score,

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
                    "cicd_agent",

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
You are the CI/CD Agent
for CognitiveOS.

Your role is to:
- design CI/CD pipelines
- optimize deployments
- automate releases
- configure GitOps workflows
- improve scalability
- ensure production readiness
- optimize rollback strategies
- secure deployment systems

You think like:
- Senior DevOps Engineer
- Platform Engineer
- Release Architect
- SRE Engineer

Focus on:
- GitHub Actions
- GitLab CI
- Jenkins
- Kubernetes
- Docker
- Helm
- ArgoCD
- Terraform
- rollback safety
- blue-green deployment
- canary deployment

You MUST:
- generate REALISTIC CI/CD strategies
- optimize deployment reliability
- minimize downtime
- maximize scalability
- ensure observability
- improve deployment safety

Return ONLY valid JSON.

JSON FORMAT:

{{
  "pipeline_strategy": {{

    "deployment_type":
      "blue-green",

    "release_strategy":
      "GitOps",

    "automation_level":
      "fully automated"
  }},

  "cicd_platform": {{

    "platform":
      "GitHub Actions",

    "runner":
      "self-hosted"
  }},

  "build_pipeline": {{

    "containerized":
      true,

    "parallel_builds":
      true,

    "cache_enabled":
      true
  }},

  "deployment_pipeline": {{

    "kubernetes":
      true,

    "helm":
      true,

    "argocd":
      true
  }},

  "testing_strategy": {{

    "unit_tests":
      true,

    "integration_tests":
      true,

    "security_scanning":
      true
  }},

  "rollback_strategy": {{

    "automatic_rollback":
      true,

    "health_check_based":
      true
  }},

  "gitops_strategy": {{

    "enabled":
      true,

    "sync_policy":
      "automatic"
  }},

  "container_strategy": {{

    "base_image":
      "python:3.11-slim",

    "multi_stage_build":
      true
  }},

  "kubernetes_strategy": {{

    "autoscaling":
      true,

    "hpa":
      true
  }},

  "monitoring_strategy": {{

    "prometheus":
      true,

    "grafana":
      true
  }},

  "security_controls": [

    "container scanning",

    "secret scanning",

    "SAST"
  ],

  "scalability_analysis": {{

    "horizontal_scaling":
      true,

    "multi_region":
      false
  }},

  "optimization_recommendations": [

    "enable build caching",

    "use canary deployment",

    "reduce container size"
  ],

  "generated_configs": [

    ".github/workflows/deploy.yml",

    "helm/values.yaml",

    "Dockerfile"
  ],

  "deployment_risks": [

    "rollback latency",

    "misconfigured secrets"
  ],

  "production_readiness":
    "high",

  "devops_score":
    9.1,

  "reasoning":
    "GitOps with Kubernetes improves scalability and deployment reliability."
}}
"""