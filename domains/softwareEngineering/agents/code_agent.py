# domains/software_engineering/agents/code_agent.py

"""
CognitiveOS - Advanced Code Agent
---------------------------------------------------------

Responsibilities:
- generate production-grade systems
- create real project structures
- generate executable codebases
- write files into workspace
- execute generated systems
- validate runtime execution
- create artifacts
- collaborate using artifacts

This agent acts like:
- Senior Backend Engineer
- Platform Engineer
- Staff Software Engineer
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
    Advanced autonomous code generation agent.
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
                "CODE AGENT STARTED"
            )

            print(
                "=" * 80
            )

            # =================================================
            # TOOL EXECUTOR
            # =================================================

            tool_executor = context.get(
                "tool_executor"
            )

            # =================================================
            # ARTIFACT REASONING
            # =================================================

            context_artifacts = context.get(
                "context_artifacts",
                [],
            )

            architecture_artifacts = [

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
            # LLM EXECUTION
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

                    "architecture_context":
                        str(
                            architecture_artifacts
                        ),

                    "previous_outputs":
                        str(
                            context.get(
                                "agent_outputs",
                                {},
                            )
                        ),

                    "context_artifacts":
                        str(
                            context_artifacts
                        ),
                }
            )

            # =================================================
            # EXTRACT TEXT
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
                "\nRAW CODE RESPONSE:\n"
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
                "\nPARSED CODE RESPONSE:\n"
            )

            print(response)

            # =================================================
            # EXTRACTION
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

            # =================================================
            # CREATE PROJECT STRUCTURE
            # =================================================

            print(
                "\nCREATING PROJECT STRUCTURE...\n"
            )

            directories = [

                "app",

                "app/routes",

                "app/services",

                "app/models",

                "app/core",

                "tests",
            ]

            for directory in directories:

                await tool_executor.execute_tool(

                    "create_directory",

                    {
                        "path": directory
                    },
                )

            # =================================================
            # WRITE GENERATED FILES
            # =================================================

            written_files = []

            for file_data in generated_files:

                try:

                    file_path = file_data.get(
                        "file_path",
                        ""
                    )

                    code = file_data.get(
                        "code",
                        ""
                    )

                    purpose = file_data.get(
                        "purpose",
                        ""
                    )

                    if not file_path:

                        continue

                    print(
                        f"\nWRITING FILE: {file_path}"
                    )

                    write_result = await (
                        tool_executor.execute_tool(

                            "write_file",

                            {

                                "path":
                                    file_path,

                                "content":
                                    code,
                            },
                        )
                    )

                    written_files.append(

                        {

                            "file":
                                file_path,

                            "purpose":
                                purpose,

                            "result":
                                write_result,
                        }
                    )

                except Exception as e:

                    print(
                        f"\nFILE WRITE FAILED: {str(e)}"
                    )

            # =================================================
            # WRITE REQUIREMENTS
            # =================================================

            requirements = "\n".join(

                tech_stack
            )

            await tool_executor.execute_tool(

                "write_file",

                {

                    "path":
                        "requirements.txt",

                    "content":
                        requirements,
                },
            )

            # =================================================
            # WRITE DOCKERFILE
            # =================================================

            dockerfile = """
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app/main.py"]
"""

            await tool_executor.execute_tool(

                "write_file",

                {

                    "path":
                        "Dockerfile",

                    "content":
                        dockerfile,
                },
            )

            # =================================================
            # WRITE README
            # =================================================

            readme = f"""
# CognitiveOS Generated Project

## Tech Stack

{tech_stack}

## APIs

{api_implementations}
"""

            await tool_executor.execute_tool(

                "write_file",

                {

                    "path":
                        "README.md",

                    "content":
                        readme,
                },
            )

            # =================================================
            # EXECUTION VALIDATION
            # =================================================

            print(
                "\nVALIDATING EXECUTION...\n"
            )

            execution_result = await (
                tool_executor.execute_tool(

                    "run_project",

                    {

                        "entry_file":
                            "app/main.py"
                    },
                )
            )

            print(
                "\nEXECUTION RESULT:\n"
            )

            print(execution_result)

            stdout = ""
            stderr = ""
            return_code = -1

            if execution_result.get(
                "output"
            ):

                stdout = (
                    execution_result[
                        "output"
                    ].get(
                        "stdout",
                        "",
                    )
                )

                stderr = (
                    execution_result[
                        "output"
                    ].get(
                        "stderr",
                        "",
                    )
                )

                return_code = (
                    execution_result[
                        "output"
                    ].get(
                        "return_code",
                        -1,
                    )
                )

            # =================================================
            # FINAL OUTPUT
            # =================================================

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

                "written_files":
                    written_files,

                "api_implementations":
                    api_implementations,

                "database_models":
                    database_models,

                "deployment_configs":
                    deployment_configs,

                "execution_validation": {

                    "stdout":
                        stdout,

                    "stderr":
                        stderr,

                    "return_code":
                        return_code,

                    "success":
                        execution_result.get(
                            "success",
                            False,
                        ),
                },

                "reasoning":
                    reasoning,
            }

        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "CODE AGENT FAILED"
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
You are the Advanced Code Agent for CognitiveOS.

Your role is to:
- generate production-grade systems
- create scalable architectures
- generate executable projects
- create modular backends
- implement APIs
- generate real project structures

You think like:
- Staff Software Engineer
- Senior Backend Engineer
- Platform Architect

Focus on:
- scalability
- maintainability
- modularity
- production-readiness
- clean architecture
- runtime execution

You MUST generate REAL executable systems.

The generated codebase should include:
- app structure
- APIs
- services
- models
- configs
- Docker support
- requirements

Return ONLY valid JSON.

JSON FORMAT:

{{
  "implementation_type":
    "backend_service",

  "tech_stack": [

    "fastapi",

    "uvicorn",

    "pydantic",

    "sqlalchemy"
  ],

  "generated_files": [

    {{

      "file_path":
        "app/main.py",

      "purpose":
        "FastAPI application entrypoint",

      "code":
        "from fastapi import FastAPI"
    }},

    {{

      "file_path":
        "app/routes/chat.py",

      "purpose":
        "Chat route",

      "code":
        "from fastapi import APIRouter"
    }}

  ],

  "api_implementations": [

    {{

      "endpoint":
        "/chat",

      "method":
        "POST",

      "description":
        "Chat endpoint"
    }}

  ],

  "database_models": [

    {{

      "model":
        "User",

      "purpose":
        "Stores user information"
    }}

  ],

  "deployment_configs": [

    {{

      "file":
        "Dockerfile",

      "purpose":
        "Containerization"
    }}

  ],

  "reasoning":
    "FastAPI selected for async scalability."
}}
"""