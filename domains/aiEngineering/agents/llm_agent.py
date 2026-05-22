# domains/aiEngineering/agents/llm_agent.py

"""
CognitiveOS - LLM Agent
---------------------------------------------------------

Responsibilities:
- design LLM systems
- generate RAG architectures
- generate autonomous AI agents
- build LangGraph workflows
- design prompt orchestration systems
- optimize context pipelines
- generate memory systems
- build scalable AI applications

This agent behaves like:
- Senior LLM Engineer
- AI Systems Architect
- Agentic AI Engineer
- Prompt Systems Engineer
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
class LLMAgentState:

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

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# LLM AGENT
# ============================================================


class LLMAgent:

    """
    Production-grade LLM systems agent.
    """

    def __init__(self):

        self.model = os.getenv(

            "GOOGLE_MODEL",

            "gemini-2.0-flash",
        )

        self.llm = ChatGoogleGenerativeAI(

            model=self.model,

            google_api_key=api_key,

            temperature=0.2,
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
                    }
                )
            )

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            llm_architecture = result.get(
                "llm_architecture",
                "multi_agent",
            )

            orchestration_framework = result.get(
                "orchestration_framework",
                "LangGraph",
            )

            llm_provider = result.get(
                "llm_provider",
                "OpenAI",
            )

            model_strategy = result.get(
                "model_strategy",
                {},
            )

            prompt_strategy = result.get(
                "prompt_strategy",
                {},
            )

            memory_system = result.get(
                "memory_system",
                {},
            )

            retrieval_strategy = result.get(
                "retrieval_strategy",
                {},
            )

            agent_architecture = result.get(
                "agent_architecture",
                [],
            )

            workflow_pipeline = result.get(
                "workflow_pipeline",
                [],
            )

            observability = result.get(
                "observability",
                [],
            )

            safety_mechanisms = result.get(
                "safety_mechanisms",
                [],
            )

            scalability_features = result.get(
                "scalability_features",
                [],
            )

            deployment_strategy = result.get(
                "deployment_strategy",
                {},
            )

            generated_components = result.get(
                "generated_components",
                [],
            )

            api_design = result.get(
                "api_design",
                [],
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "llm_agent",

                "llm_architecture":
                    llm_architecture,

                "orchestration_framework":
                    orchestration_framework,

                "llm_provider":
                    llm_provider,

                "model_strategy":
                    model_strategy,

                "prompt_strategy":
                    prompt_strategy,

                "memory_system":
                    memory_system,

                "retrieval_strategy":
                    retrieval_strategy,

                "agent_architecture":
                    agent_architecture,

                "workflow_pipeline":
                    workflow_pipeline,

                "observability":
                    observability,

                "safety_mechanisms":
                    safety_mechanisms,

                "scalability_features":
                    scalability_features,

                "deployment_strategy":
                    deployment_strategy,

                "generated_components":
                    generated_components,

                "api_design":
                    api_design,

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
                    "llm_agent",

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
You are the LLM Agent for CognitiveOS.

Your role is to:
- design production-grade LLM systems
- build autonomous AI agents
- create LangGraph workflows
- design prompt orchestration systems
- build memory architectures
- optimize context pipelines
- design scalable AI applications
- build multi-agent systems

You think like:
- Senior LLM Engineer
- AI Systems Architect
- Autonomous Systems Engineer
- Prompt Infrastructure Engineer

Focus on:
- scalability
- context efficiency
- hallucination reduction
- memory systems
- orchestration quality
- observability
- production-readiness
- latency optimization

You MUST:
- design REAL production systems
- avoid toy architectures
- optimize prompt pipelines
- include observability and monitoring
- include safety and guardrails
- support multi-agent orchestration

Return ONLY valid JSON.

JSON FORMAT:

{{
  "llm_architecture":
    "multi_agent_rag",

  "orchestration_framework":
    "LangGraph",

  "llm_provider":
    "OpenAI GPT-4",

  "model_strategy": {{

    "primary_model":
      "gpt-4o",

    "fallback_model":
      "claude-3.5-sonnet",

    "routing_strategy":
      "cost_latency_aware"
  }},

  "prompt_strategy": {{

    "prompt_management":
      "centralized",

    "few_shot":
      true,

    "dynamic_context":
      true
  }},

  "memory_system": {{

    "short_term":
      "conversation_buffer",

    "long_term":
      "vector_memory",

    "episodic_memory":
      true
  }},

  "retrieval_strategy": {{

    "rag":
      true,

    "hybrid_search":
      true,

    "reranking":
      true
  }},

  "agent_architecture": [

    "planner_agent",

    "retrieval_agent",

    "execution_agent",

    "reflection_agent",

    "critic_agent"
  ],

  "workflow_pipeline": [

    "query_analysis",

    "retrieval",

    "reranking",

    "reasoning",

    "response_generation",

    "reflection"
  ],

  "observability": [

    "LangSmith tracing",

    "OpenTelemetry",

    "structured logging",

    "token analytics"
  ],

  "safety_mechanisms": [

    "prompt injection detection",

    "content filtering",

    "output validation",

    "rate limiting"
  ],

  "scalability_features": [

    "async inference",

    "response caching",

    "multi-model routing",

    "horizontal scaling"
  ],

  "deployment_strategy": {{

    "containerization":
      "Docker",

    "orchestration":
      "Kubernetes",

    "autoscaling":
      true
  }},

  "generated_components": [

    "agent_router",

    "memory_manager",

    "prompt_manager",

    "retrieval_pipeline",

    "reflection_engine"
  ],

  "api_design": [

    {{

      "endpoint":
        "/api/v1/chat",

      "method":
        "POST",

      "purpose":
        "LLM conversational endpoint"
    }},

    {{

      "endpoint":
        "/api/v1/agents/run",

      "method":
        "POST",

      "purpose":
        "Multi-agent execution"
    }}
  ],

  "reasoning":
    "Multi-agent LangGraph architecture selected for scalable autonomous reasoning."
}}
"""