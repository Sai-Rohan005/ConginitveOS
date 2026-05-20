# domains/software_engineering/agents/architecture_agent.py

"""
CognitiveOS - Advanced Architecture Agent
---------------------------------------------------------

Responsibilities:
- design scalable systems
- define distributed architectures
- design APIs
- design databases
- recommend infrastructure
- define communication patterns
- generate architecture reasoning
- collaborate using artifacts
- generate executable project structures

This agent thinks like:
- Staff Software Architect
- Distributed Systems Engineer
- Cloud Architect
- Platform Engineer
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

    context_artifacts: List[
        Any
    ] = field(default_factory=list)

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# ARCHITECTURE AGENT
# ============================================================


class ArchitectureAgent:

    """
    Advanced software architecture agent.
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

Previous Outputs:
{previous_outputs}

Shared Context:
{shared_context}

Context Artifacts:
{context_artifacts}
                        """,
                    ),
                ]
            )
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
                "ARCHITECTURE AGENT STARTED"
            )

            print(
                "=" * 80
            )

            # =================================================
            # CONTEXT ARTIFACTS
            # =================================================

            context_artifacts = context.get(
                "context_artifacts",
                [],
            )

            previous_architectures = [

                artifact

                for artifact in context_artifacts

                if (
                    getattr(
                        artifact,
                        "artifact_type",
                        "",
                    )
                    == "architecture"
                )
            ]

            # =================================================
            # RAW LLM CALL
            # =================================================

            raw_response = await (

                self.prompt

                | self.llm

            ).ainvoke(

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
                                "agent_outputs",
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

                    "context_artifacts":
                        str(
                            previous_architectures
                        ),
                }
            )

            # =================================================
            # EXTRACT RESPONSE
            # =================================================

            response_text = ""

            if hasattr(
                raw_response,
                "content"
            ):

                response_text = (
                    raw_response.content
                )

            else:

                response_text = str(
                    raw_response
                )

            print(
                "\nRAW ARCHITECTURE RESPONSE:\n"
            )

            print(
                response_text
            )

            # =================================================
            # CLEAN JSON
            # =================================================

            response_text = (

                response_text

                .replace(
                    "```json",
                    "",
                )

                .replace(
                    "```",
                    "",
                )

                .strip()
            )

            # =================================================
            # PARSE JSON
            # =================================================

            response = self.parser.parse(
                response_text
            )

            print(
                "\nPARSED ARCHITECTURE RESPONSE:\n"
            )

            print(response)

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            architecture_type = response.get(

                "architecture_type",

                "modular_monolith",
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

            communication_patterns = (
                response.get(
                    "communication_patterns",
                    [],
                )
            )

            project_structure = response.get(
                "project_structure",
                [],
            )

            security_design = response.get(
                "security_design",
                {},
            )

            deployment_strategy = response.get(
                "deployment_strategy",
                {},
            )

            reasoning = response.get(
                "reasoning",
                "",
            )

            # =================================================
            # FINAL OUTPUT
            # =================================================

            architecture_output = {

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

                "communication_patterns":
                    communication_patterns,

                "project_structure":
                    project_structure,

                "security_design":
                    security_design,

                "deployment_strategy":
                    deployment_strategy,

                "reasoning":
                    reasoning,
            }

            print(
                "\nFINAL ARCHITECTURE OUTPUT:\n"
            )

            print(
                architecture_output
            )

            return architecture_output

        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "ARCHITECTURE AGENT FAILED"
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
You are the Advanced Architecture Agent for CognitiveOS.

Your role is to:
- design scalable architectures
- define APIs
- define infrastructure
- define deployment architecture
- define security models
- design distributed systems
- design production-ready systems

You think like:
- Staff Software Architect
- Distributed Systems Engineer
- Cloud Architect
- Platform Engineer

Focus on:
- scalability
- maintainability
- modularity
- reliability
- observability
- production-readiness
- fault tolerance
- clean architecture

You MUST generate REAL production-ready architecture.

Return ONLY valid JSON.

JSON FORMAT:

{{
  "architecture_type":
    "microservices",

  "services": [

    {{

      "name":
        "auth_service",

      "responsibility":
        "JWT authentication",

      "communication":
        "REST"
    }},

    {{

      "name":
        "chat_service",

      "responsibility":
        "Realtime chat handling",

      "communication":
        "WebSocket"
    }}

  ],

  "database_design": {{

    "primary_database":
      "PostgreSQL",

    "caching":
      "Redis",

    "storage":
      "S3"
  }},

  "api_design": [

    {{

      "endpoint":
        "/api/v1/chat",

      "method":
        "POST",

      "purpose":
        "Chat endpoint"
    }}

  ],

  "infrastructure": {{

    "containerization":
      "Docker",

    "orchestration":
      "Kubernetes",

    "ci_cd":
      "GitHub Actions"
  }},

  "communication_patterns": [

    "REST",

    "WebSockets",

    "Async events"
  ],

  "project_structure": [

    "app/",

    "app/routes/",

    "app/services/",

    "app/models/",

    "app/core/",

    "tests/"
  ],

  "security_design": {{

    "authentication":
      "JWT",

    "authorization":
      "RBAC",

    "rate_limiting":
      true
  }},

  "deployment_strategy": {{

    "containerized":
      true,

    "horizontal_scaling":
      true,

    "load_balancer":
      "NGINX"
  }},

  "scalability_considerations": [

    "horizontal scaling",

    "database indexing",

    "async processing",

    "caching"
  ],

  "reasoning":
    "Microservices selected for scalability and modularity."
}}
"""