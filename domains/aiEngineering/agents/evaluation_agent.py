# domains/aiEngineering/agents/evaluation_agent.py

"""
CognitiveOS - Evaluation Agent
---------------------------------------------------------

Responsibilities:
- evaluate AI systems
- validate RAG pipelines
- evaluate hallucination risk
- assess inference quality
- evaluate latency and throughput
- validate retrieval quality
- analyze production readiness
- recommend optimizations

This agent behaves like:
- Senior AI Evaluator
- LLM Reliability Engineer
- ML Quality Engineer
- AI Systems Auditor
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
class EvaluationAgentState:

    query: str

    task: str

    architecture_context: Dict[
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
# EVALUATION AGENT
# ============================================================


class EvaluationAgent:

    """
    Production-grade AI evaluation agent.
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

            evaluation_summary = result.get(
                "evaluation_summary",
                "",
            )

            system_quality = result.get(
                "system_quality",
                {},
            )

            hallucination_risk = result.get(
                "hallucination_risk",
                {},
            )

            retrieval_quality = result.get(
                "retrieval_quality",
                {},
            )

            inference_quality = result.get(
                "inference_quality",
                {},
            )

            latency_assessment = result.get(
                "latency_assessment",
                {},
            )

            scalability_assessment = result.get(
                "scalability_assessment",
                {},
            )

            observability_assessment = result.get(
                "observability_assessment",
                {},
            )

            security_assessment = result.get(
                "security_assessment",
                {},
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            evaluation_metrics = result.get(
                "evaluation_metrics",
                {},
            )

            bottlenecks = result.get(
                "bottlenecks",
                [],
            )

            recommended_improvements = result.get(
                "recommended_improvements",
                [],
            )

            critical_issues = result.get(
                "critical_issues",
                [],
            )

            overall_score = result.get(
                "overall_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "evaluation_agent",

                "evaluation_summary":
                    evaluation_summary,

                "system_quality":
                    system_quality,

                "hallucination_risk":
                    hallucination_risk,

                "retrieval_quality":
                    retrieval_quality,

                "inference_quality":
                    inference_quality,

                "latency_assessment":
                    latency_assessment,

                "scalability_assessment":
                    scalability_assessment,

                "observability_assessment":
                    observability_assessment,

                "security_assessment":
                    security_assessment,

                "production_readiness":
                    production_readiness,

                "evaluation_metrics":
                    evaluation_metrics,

                "bottlenecks":
                    bottlenecks,

                "recommended_improvements":
                    recommended_improvements,

                "critical_issues":
                    critical_issues,

                "overall_score":
                    overall_score,

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
                    "evaluation_agent",

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
You are the Evaluation Agent for CognitiveOS.

Your role is to:
- evaluate AI systems
- validate RAG quality
- assess hallucination risk
- evaluate inference quality
- assess scalability
- validate production readiness
- detect bottlenecks
- recommend optimizations

You think like:
- Senior AI Evaluator
- LLM Reliability Engineer
- ML Infrastructure Auditor
- AI Systems Quality Engineer

Focus on:
- retrieval quality
- hallucination reduction
- inference stability
- scalability
- observability
- latency optimization
- production-readiness
- security validation

You MUST:
- evaluate REAL production concerns
- identify bottlenecks
- assess failure risks
- recommend scalable improvements
- validate architecture consistency
- provide quantitative scoring

Return ONLY valid JSON.

JSON FORMAT:

{{
  "evaluation_summary":
    "The AI system is scalable and production-ready with minor optimizations required.",

  "system_quality": {{

    "architecture":
      "high",

    "modularity":
      "high",

    "maintainability":
      "medium"
  }},

  "hallucination_risk": {{

    "risk_level":
      "low",

    "causes": [

      "strong retrieval grounding",

      "reranking enabled"
    ]
  }},

  "retrieval_quality": {{

    "hybrid_search":
      "effective",

    "reranking":
      "high_quality",

    "semantic_accuracy":
      0.91
  }},

  "inference_quality": {{

    "response_quality":
      "high",

    "consistency":
      "stable",

    "context_retention":
      "good"
  }},

  "latency_assessment": {{

    "average_latency_ms":
      850,

    "bottleneck":
      "reranking stage"
  }},

  "scalability_assessment": {{

    "horizontal_scaling":
      true,

    "autoscaling":
      true,

    "distributed_ready":
      true
  }},

  "observability_assessment": {{

    "tracing":
      true,

    "metrics":
      true,

    "structured_logging":
      true
  }},

  "security_assessment": {{

    "prompt_injection_protection":
      "partial",

    "authentication":
      "enabled",

    "rate_limiting":
      "enabled"
  }},

  "production_readiness":
    "mostly_ready",

  "evaluation_metrics": {{

    "retrieval_precision":
      0.92,

    "retrieval_recall":
      0.89,

    "hallucination_score":
      0.08,

    "availability":
      0.99
  }},

  "bottlenecks": [

    "cross-encoder reranking latency",

    "large embedding dimensions"
  ],

  "recommended_improvements": [

    "enable semantic caching",

    "optimize reranker batching",

    "add response streaming"
  ],

  "critical_issues": [

    "missing prompt injection firewall"
  ],

  "overall_score":
    8.9,

  "reasoning":
    "The architecture is scalable and reliable with strong retrieval grounding."
}}
"""