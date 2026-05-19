# domains/software_engineering/agents/code_agent.py

"""
CognitiveOS - Code Agent
---------------------------------------------------------

Responsibilities:
- generate production-ready code
- implement backend systems
- implement APIs
- create services/modules
- generate configs
- generate scalable software components
- follow architecture specifications

This agent acts like:
- Senior Software Engineer
- Backend Engineer
- Full Stack Engineer
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
api_key = os.getenv("GOOGLE_API_KEY")

# ============================================================
# STATE
# ============================================================


@dataclass
class CodeAgentState:

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

    generated_files: List[
        Dict[str, str]
    ] = field(default_factory=list)

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# CODE AGENT
# ============================================================


class CodeAgent:

    """
    Production-grade Code Generation Agent.
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

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            implementation_type = response.get(
                "implementation_type",
                "backend_service",
            )

            tech_stack = response.get(
                "tech_stack",
                [],
            )

            generated_files = response.get(
                "generated_files",
                [],
            )

            api_implementations = response.get(
                "api_implementations",
                [],
            )

            database_models = response.get(
                "database_models",
                [],
            )

            deployment_configs = response.get(
                "deployment_configs",
                [],
            )

            reasoning = response.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "code_agent",

                "implementation_type":
                    implementation_type,

                "tech_stack":
                    tech_stack,

                "generated_files":
                    generated_files,

                "api_implementations":
                    api_implementations,

                "database_models":
                    database_models,

                "deployment_configs":
                    deployment_configs,

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
                    "code_agent",

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
You are the Code Agent for CognitiveOS.

Your role is to:
- generate production-ready code
- implement scalable systems
- implement APIs
- create backend services
- generate modular codebases
- follow architecture specifications

You think like:
- Senior Software Engineer
- Backend Engineer
- Full Stack Engineer
- Platform Engineer

Focus on:
- clean architecture
- modularity
- scalability
- maintainability
- production-readiness
- readability
- performance

Code must:
- follow best practices
- be production-grade
- be scalable
- include proper structure
- avoid toy implementations

Return ONLY valid JSON.

JSON FORMAT:

{{
  "implementation_type":
    "backend_service",

  "tech_stack": [

    "FastAPI",

    "PostgreSQL",

    "Redis",

    "Docker"
  ],

  "generated_files": [

    {
      "file_path":
        "app/main.py",

      "purpose":
        "FastAPI application entrypoint",

      "code":
        "from fastapi import FastAPI"
    },

    {
      "file_path":
        "app/routes/chat.py",

      "purpose":
        "Chat API routes",

      "code":
        "router = APIRouter()"
    }

  ],

  "api_implementations": [

    {
      "endpoint":
        "/api/v1/chat",

      "method":
        "POST",

      "description":
        "Send chat message"
    }

  ],

  "database_models": [

    {
      "model":
        "User",

      "purpose":
        "Stores user information"
    }

  ],

  "deployment_configs": [

    {
      "file":
        "Dockerfile",

      "purpose":
        "Containerization"
    }

  ],

  "reasoning":
    "FastAPI chosen for async scalability and modular backend architecture."
}}
"""