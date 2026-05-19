# domains/software_engineering/agents/architecture_agent.py

"""
CognitiveOS - Architecture Agent
---------------------------------------------------------

Responsibilities:
- design scalable systems
- define service architecture
- define APIs
- design databases
- recommend infrastructure
- define communication patterns
- generate architecture reasoning

This agent thinks like:
- Senior Software Architect
- Distributed Systems Engineer
- Platform Engineer
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

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain_core.output_parsers import (
    JsonOutputParser,
)


# ============================================================
# AGENT STATE
# ============================================================


@dataclass
class ArchitectureAgentState:

    query: str

    task: str

    shared_context: Dict[
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
# ARCHITECTURE AGENT
# ============================================================


class ArchitectureAgent:

    """
    Software Architecture Agent.
    """

    def __init__(self):

        self.model = os.getenv(
            "GOOGLE_MODEL",
            "gemini-2.0-flash",
        )

        self.llm = ChatGoogleGenerativeAI(

            model=self.model,

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

Previous Outputs:
{previous_outputs}

Shared Context:
{shared_context}
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

                    "task":
                        context.get(
                            "task",
                            "",
                        ),

                    "previous_outputs":
                        str(
                            context.get(
                                "previous_outputs",
                                {},
                            )
                        ),

                    "shared_context":
                        str(
                            context.get(
                                "shared_context",
                                {},
                            )
                        ),
                }
            )

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            architecture_type = response.get(
                "architecture_type",
                "microservices",
            )

            services = response.get(
                "services",
                [],
            )

            database_design = response.get(
                "database_design",
                {},
            )

            api_design = response.get(
                "api_design",
                [],
            )

            infrastructure = response.get(
                "infrastructure",
                {},
            )

            scalability_considerations = (
                response.get(
                    "scalability_considerations",
                    [],
                )
            )

            reasoning = response.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "architecture_agent",

                "architecture_type":
                    architecture_type,

                "services":
                    services,

                "database_design":
                    database_design,

                "api_design":
                    api_design,

                "infrastructure":
                    infrastructure,

                "scalability_considerations":
                    scalability_considerations,

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
                    "architecture_agent",

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
You are the Architecture Agent for CognitiveOS.

Your role is to design:
- scalable software architectures
- APIs
- database schemas
- infrastructure
- distributed systems
- backend services
- deployment architecture

You think like:
- Senior Software Architect
- Distributed Systems Engineer
- Cloud Architect

Focus on:
- scalability
- maintainability
- reliability
- performance
- modularity
- production-readiness

Return ONLY valid JSON.

JSON FORMAT:

{
  "architecture_type":
    "microservices",

  "services": [

    {
      "name":
        "auth_service",

      "responsibility":
        "Authentication and authorization",

      "communication":
        "REST"
    }

  ],

  "database_design": {

    "primary_database":
      "PostgreSQL",

    "caching":
      "Redis",

    "storage":
      "S3"
  },

  "api_design": [

    {
      "endpoint":
        "/api/v1/chat",

      "method":
        "POST",

      "purpose":
        "Send chat messages"
    }

  ],

  "infrastructure": {

    "containerization":
      "Docker",

    "orchestration":
      "Kubernetes",

    "ci_cd":
      "GitHub Actions"
  },

  "scalability_considerations": [

    "horizontal scaling",

    "load balancing",

    "database indexing"
  ],

  "reasoning":
    "Microservices chosen for scalability and modularity."
}
"""