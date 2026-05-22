# domains/devops/agents/monitoring_agent.py

"""
CognitiveOS - Monitoring Agent
---------------------------------------------------------

Responsibilities:
- design observability systems
- configure monitoring stacks
- optimize alerting pipelines
- improve reliability engineering
- detect infrastructure bottlenecks
- analyze telemetry
- optimize incident response
- enable production-grade observability

This agent behaves like:
- Site Reliability Engineer
- Observability Engineer
- Platform Monitoring Engineer
- DevOps Reliability Architect
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
class MonitoringAgentState:

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
# MONITORING AGENT
# ============================================================


class MonitoringAgent:

    """
    Production-grade Monitoring & Observability Agent.
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

            observability_strategy = result.get(
                "observability_strategy",
                {},
            )

            monitoring_stack = result.get(
                "monitoring_stack",
                {},
            )

            metrics_strategy = result.get(
                "metrics_strategy",
                {},
            )

            logging_strategy = result.get(
                "logging_strategy",
                {},
            )

            tracing_strategy = result.get(
                "tracing_strategy",
                {},
            )

            alerting_strategy = result.get(
                "alerting_strategy",
                {},
            )

            dashboard_strategy = result.get(
                "dashboard_strategy",
                {},
            )

            sla_strategy = result.get(
                "sla_strategy",
                {},
            )

            incident_response = result.get(
                "incident_response",
                {},
            )

            anomaly_detection = result.get(
                "anomaly_detection",
                {},
            )

            reliability_analysis = result.get(
                "reliability_analysis",
                {},
            )

            performance_bottlenecks = result.get(
                "performance_bottlenecks",
                [],
            )

            generated_configs = result.get(
                "generated_configs",
                [],
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            monitoring_risks = result.get(
                "monitoring_risks",
                [],
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            observability_score = result.get(
                "observability_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "monitoring_agent",

                "observability_strategy":
                    observability_strategy,

                "monitoring_stack":
                    monitoring_stack,

                "metrics_strategy":
                    metrics_strategy,

                "logging_strategy":
                    logging_strategy,

                "tracing_strategy":
                    tracing_strategy,

                "alerting_strategy":
                    alerting_strategy,

                "dashboard_strategy":
                    dashboard_strategy,

                "sla_strategy":
                    sla_strategy,

                "incident_response":
                    incident_response,

                "anomaly_detection":
                    anomaly_detection,

                "reliability_analysis":
                    reliability_analysis,

                "performance_bottlenecks":
                    performance_bottlenecks,

                "generated_configs":
                    generated_configs,

                "optimization_recommendations":
                    optimization_recommendations,

                "monitoring_risks":
                    monitoring_risks,

                "production_readiness":
                    production_readiness,

                "observability_score":
                    observability_score,

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
                    "monitoring_agent",

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
You are the Monitoring Agent
for CognitiveOS.

Your role is to:
- design observability systems
- optimize monitoring pipelines
- improve reliability engineering
- configure alerting systems
- analyze telemetry
- optimize incident response
- improve production visibility
- detect anomalies and bottlenecks

You think like:
- Site Reliability Engineer
- Observability Engineer
- Platform Monitoring Architect
- Reliability Specialist

Focus on:
- Prometheus
- Grafana
- ELK Stack
- Loki
- OpenTelemetry
- Jaeger
- alerting
- tracing
- metrics
- dashboards
- SLA/SLO reliability

You MUST:
- generate REALISTIC monitoring strategies
- optimize production visibility
- minimize alert fatigue
- improve incident response
- maximize observability coverage
- improve reliability engineering

Return ONLY valid JSON.

JSON FORMAT:

{{
  "observability_strategy": {{

    "architecture":
      "centralized observability",

    "telemetry":
      "OpenTelemetry",

    "coverage":
      "full-stack"
  }},

  "monitoring_stack": {{

    "metrics":
      "Prometheus",

    "dashboard":
      "Grafana",

    "logging":
      "Loki",

    "tracing":
      "Jaeger"
  }},

  "metrics_strategy": {{

    "application_metrics":
      true,

    "infrastructure_metrics":
      true,

    "custom_metrics":
      true
  }},

  "logging_strategy": {{

    "centralized_logging":
      true,

    "log_retention":
      "30 days"
  }},

  "tracing_strategy": {{

    "distributed_tracing":
      true,

    "sampling":
      "adaptive"
  }},

  "alerting_strategy": {{

    "tool":
      "Alertmanager",

    "severity_levels":
      [
        "critical",
        "warning",
        "info"
      ]
  }},

  "dashboard_strategy": {{

    "real_time":
      true,

    "executive_dashboards":
      true
  }},

  "sla_strategy": {{

    "availability_target":
      "99.9%",

    "latency_target":
      "<200ms"
  }},

  "incident_response": {{

    "on_call":
      true,

    "pagerduty":
      true
  }},

  "anomaly_detection": {{

    "enabled":
      true,

    "method":
      "statistical baseline"
  }},

  "reliability_analysis": {{

    "mttr":
      "15 minutes",

    "uptime":
      "99.95%"
  }},

  "performance_bottlenecks": [

    "database latency",

    "high memory utilization"
  ],

  "generated_configs": [

    "prometheus.yml",

    "grafana-dashboard.json",

    "alert_rules.yml"
  ],

  "optimization_recommendations": [

    "reduce noisy alerts",

    "optimize metric cardinality",

    "enable adaptive sampling"
  ],

  "monitoring_risks": [

    "alert fatigue",

    "high telemetry cost"
  ],

  "production_readiness":
    "high",

  "observability_score":
    9.4,

  "reasoning":
    "Centralized observability improves incident response and production reliability."
}}
"""