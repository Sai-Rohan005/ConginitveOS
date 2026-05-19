# domains/software_engineering/agents/reflection_agent.py

"""
CognitiveOS - Reflection Agent
---------------------------------------------------------

Responsibilities:
- critique outputs
- validate correctness
- identify hallucinations
- detect scalability issues
- detect architectural flaws
- identify missing components
- suggest improvements
- trigger retries
- improve failed execution steps

Cognitive Loop:

generate
    ↓
reflect
    ↓
retry failed steps
    ↓
improve outputs
    ↓
re-reflect
"""

from __future__ import annotations

import os
import traceback

from typing import (
    Dict,
    Any,
    List,
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
api_key = os.getenv("GOOGLE_API_KEY")
# ============================================================
# STATE
# ============================================================


@dataclass
class ReflectionAgentState:

    query: str

    agent_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    artifacts: List[Any] = field(
        default_factory=list
    )

    reflection_notes: List[
        str
    ] = field(default_factory=list)

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# REFLECTION AGENT
# ============================================================


class ReflectionAgent:

    """
    Reflection & Self-Improvement Agent.
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

Agent Outputs:
{agent_outputs}

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

            response = await self.chain.ainvoke(

                {

                    "query":
                        context.get(
                            "query",
                            "",
                        ),

                    "agent_outputs":
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
                                [],
                            )
                        ),
                }
            )

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            overall_quality = response.get(
                "overall_quality",
                "medium",
            )

            correctness_analysis = response.get(
                "correctness_analysis",
                [],
            )

            scalability_analysis = response.get(
                "scalability_analysis",
                [],
            )

            security_analysis = response.get(
                "security_analysis",
                [],
            )

            missing_components = response.get(
                "missing_components",
                [],
            )

            improvement_suggestions = (
                response.get(
                    "improvement_suggestions",
                    [],
                )
            )

            retry_required = response.get(
                "retry_required",
                False,
            )

            retry_strategy = response.get(
                "retry_strategy",
                {},
            )

            retry_steps = response.get(
                "retry_steps",
                [],
            )

            reasoning = response.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "reflection_agent",

                "overall_quality":
                    overall_quality,

                "correctness_analysis":
                    correctness_analysis,

                "scalability_analysis":
                    scalability_analysis,

                "security_analysis":
                    security_analysis,

                "missing_components":
                    missing_components,

                "improvement_suggestions":
                    improvement_suggestions,

                "retry_required":
                    retry_required,

                "retry_strategy":
                    retry_strategy,

                "retry_steps":
                    retry_steps,

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
                    "reflection_agent",

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
You are the Reflection Agent for CognitiveOS.

Your role is to:
- critique outputs
- validate correctness
- detect flaws
- identify weak implementations
- detect missing components
- validate production readiness
- improve failed outputs
- generate retry strategies
- improve system quality iteratively

You think like:
- Principal Engineer
- Senior Reviewer
- Staff Architect
- Technical Auditor

You are STRICT and analytical.

You DO NOT generate final solutions.

You ONLY:
- evaluate
- critique
- improve
- recommend retries
- improve failed outputs

Focus on:

1. correctness
2. scalability
3. reliability
4. maintainability
5. production readiness
6. security
7. runtime stability
8. architecture quality

If outputs are weak:
- trigger retries
- recommend improvements
- specify exactly what failed
- explain how to improve

Return ONLY valid JSON.

JSON FORMAT:

{{
  "overall_quality":
    "medium",

  "correctness_analysis": [

    "Architecture is logically consistent",

    "Database flow is valid"
  ],

  "scalability_analysis": [

    "Horizontal scaling supported",

    "Caching layer missing"
  ],

  "security_analysis": [

    "Authentication middleware absent",

    "Rate limiting not implemented"
  ],

  "missing_components": [

    "Centralized logging",

    "Monitoring system"
  ],

  "improvement_suggestions": [

    "Add JWT middleware",

    "Add structured logging",

    "Add retry mechanism"
  ],

  "retry_required": true,

  "retry_strategy": {

    "reason":
      "Security vulnerabilities detected",

    "priority":
      "high",

    "max_retry_iterations":
      2
  },

  "retry_steps": [

    {
      "step_id": 2,

      "improvement_action":
        "Add JWT authentication middleware",

      "reason":
        "Authentication layer missing"
    },

    {
      "step_id": 3,

      "improvement_action":
        "Implement Redis caching",

      "reason":
        "Performance bottleneck detected"
    }

  ],

  "reasoning":
    "The system architecture is scalable but lacks production-grade security and observability."
}}
"""