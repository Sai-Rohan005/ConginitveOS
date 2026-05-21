# domains/software_engineering/agents/reflection_agent.py

"""
CognitiveOS - Strategic Reflection Agent
---------------------------------------------------------

Responsibilities:
- critique architecture quality
- evaluate production readiness
- analyze scalability
- detect enterprise gaps
- identify missing infrastructure
- improve maintainability
- improve reliability
- trigger strategic retries

IMPORTANT:

This agent NO LONGER handles:
- syntax issues
- import failures
- dependency issues
- runtime patching

Those are deterministic now.
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

api_key = os.getenv(
    "GOOGLE_API_KEY"
)

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

    runtime_repairs: List[
        Dict[str, Any]
    ] = field(default_factory=list)

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
    Strategic reflection and production-readiness evaluator.
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

Runtime Repairs:
{runtime_repairs}
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

            print(
                "\n"
                + "=" * 80
            )

            print(
                "REFLECTION AGENT STARTED"
            )

            print(
                "=" * 80
            )

            runtime_repairs = context.get(
                "runtime_repairs",
                [],
            )

            # =================================================
            # GEMINI CALL
            # =================================================

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

                    "runtime_repairs":
                        str(
                            runtime_repairs
                        ),
                }
            )

            print(
                "\nREFLECTION RESPONSE:\n"
            )

            print(response)

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            overall_quality = response.get(
                "overall_quality",
                "medium",
            )

            architecture_analysis = response.get(
                "architecture_analysis",
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

            production_readiness_analysis = (
                response.get(
                    "production_readiness_analysis",
                    [],
                )
            )

            missing_components = response.get(
                "missing_components",
                [],
            )

            enterprise_gaps = response.get(
                "enterprise_gaps",
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

            # =================================================
            # AUTO DISABLE RETRIES
            # =================================================

            if runtime_repairs:

                retry_required = False

            # =================================================
            # FINAL OUTPUT
            # =================================================

            reflection_output = {

                "success": True,

                "agent":
                    "reflection_agent",

                "overall_quality":
                    overall_quality,

                "architecture_analysis":
                    architecture_analysis,

                "scalability_analysis":
                    scalability_analysis,

                "security_analysis":
                    security_analysis,

                "production_readiness_analysis":
                    production_readiness_analysis,

                "missing_components":
                    missing_components,

                "enterprise_gaps":
                    enterprise_gaps,

                "improvement_suggestions":
                    improvement_suggestions,

                "retry_required":
                    retry_required,

                "retry_strategy":
                    retry_strategy,

                "retry_steps":
                    retry_steps,

                "runtime_repairs":
                    runtime_repairs,

                "reasoning":
                    reasoning,
            }

            print(
                "\nFINAL REFLECTION OUTPUT:\n"
            )

            print(
                reflection_output
            )

            return reflection_output

        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "REFLECTION AGENT FAILED"
            )

            print(
                "=" * 80
            )

            print(str(e))

            print(
                traceback.format_exc()
            )

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
You are the Strategic Reflection Agent for CognitiveOS.

Your role is ONLY to:
- evaluate architecture quality
- evaluate production readiness
- evaluate scalability
- evaluate maintainability
- evaluate enterprise readiness
- detect missing infrastructure
- detect missing observability
- detect security weaknesses
- recommend strategic improvements

IMPORTANT:

You DO NOT handle:
- syntax fixes
- import issues
- dependency installation
- runtime patching
- uvicorn fixes
- FastAPI startup issues

Those are deterministic systems now.

You think like:
- Principal Engineer
- Staff Architect
- Platform Reviewer
- Enterprise Reliability Auditor

You are STRICT and analytical.

Focus ONLY on:

1. architecture quality
2. scalability
3. maintainability
4. production readiness
5. enterprise readiness
6. reliability
7. observability
8. security hardening
9. distributed systems quality

If outputs are weak:
- trigger retries
- recommend strategic improvements
- identify missing enterprise components
- explain architectural weaknesses

Return ONLY valid JSON.

JSON FORMAT:

{{
  "overall_quality":
    "high",

  "architecture_analysis": [

    "Architecture is modular",

    "Service boundaries are clear"
  ],

  "scalability_analysis": [

    "Horizontal scaling supported",

    "Redis caching missing"
  ],

  "security_analysis": [

    "JWT validation implemented",

    "Rate limiting absent"
  ],

  "production_readiness_analysis": [

    "Docker support available",

    "Monitoring stack missing"
  ],

  "missing_components": [

    "Centralized logging",

    "Tracing system",

    "Health check endpoints"
  ],

  "enterprise_gaps": [

    "No CI/CD pipeline",

    "No observability layer"
  ],

  "improvement_suggestions": [

    "Add Prometheus metrics",

    "Add structured logging",

    "Add Redis caching"
  ],

  "retry_required":
    false,

  "retry_strategy": {{

    "reason":
      "Architecture improvements required",

    "priority":
      "medium",

    "max_retry_iterations":
      1
  }},

  "retry_steps": [

    {{
      "step_id": 2,

      "improvement_action":
        "Add observability stack",

      "reason":
        "Production monitoring missing"
    }}

  ],

  "reasoning":
    "System is production capable but lacks enterprise observability and resilience tooling."
}}
"""