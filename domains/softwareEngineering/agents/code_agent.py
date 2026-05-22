# domains/software_engineering/agents/code_agent.py

"""
CognitiveOS - Deterministic + Self-Healing Code Agent
---------------------------------------------------------

Responsibilities:
- generate production-grade systems
- generate executable codebases
- create scalable backend systems
- generate APIs/services/models
- validate runtime execution
- self-heal runtime failures
- reduce unnecessary Gemini calls
- collaborate through artifacts
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

# ============================================================
# IMPORT RUNTIME SYSTEMS
# ============================================================

from core.runtime.import_extractor import (
    ImportExtractor,
)

from core.runtime.patch_engine import (
    PatchEngine,
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
    Self-healing autonomous code generation agent.
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

        # ====================================================
        # PROJECT STRUCTURE
        # ====================================================

        self.default_directories = [

            "app",
            "app/routes",
            "app/services",
            "app/models",
            "app/core",
            "app/middleware",
            "app/utils",
            "tests",
        ]

        # ====================================================
        # IMPORT EXTRACTOR
        # ====================================================

        self.import_extractor = (
            ImportExtractor()
        )

        # ====================================================
        # PATCH ENGINE
        # ====================================================

        self.patch_engine = (
            PatchEngine()
        )

        # ====================================================
        # MAX RUNTIME REPAIRS
        # ====================================================

        self.max_runtime_repairs = 2

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    def _system_prompt(self) -> str:

        return """
You are CognitiveOS CodeAgent.

You are an autonomous software engineering agent.

Responsibilities:
- generate production-grade systems
- generate executable Python projects
- create scalable backend architectures
- generate APIs, services, models, and utilities
- write modular clean code
- minimize hallucinations
- validate execution correctness
- repair runtime failures when possible
- always return structured JSON

Rules:
- generate complete executable files
- avoid placeholders unless necessary
- prefer FastAPI for APIs
- use clean architecture principles
- separate routes/services/models
- ensure imports are valid
- avoid pseudocode
- generate production-ready implementations

Return JSON only.
"""

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

            tool_executor = context.get(
                "tool_executor"
            )

            if not tool_executor:

                return {

                    "success": False,

                    "error":
                        "tool_executor missing from context",
                }

            # =================================================
            # ARTIFACT COLLABORATION
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
            # GEMINI CALL
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
            # EXTRACT RESPONSE TEXT
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
                "\nPARSED RESPONSE:\n"
            )

            print(response)

            # =================================================
            # EXTRACT DATA
            # =================================================

            implementation_type = response.get(

                "implementation_type",

                "backend_service",
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

            for directory in (
                self.default_directories
            ):

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
            # REQUIREMENTS
            # =================================================

            requirements = (

                self.import_extractor
                .generate_requirements(
                    generated_files
                )
            )

            await tool_executor.execute_tool(

                "write_file",

                {

                    "path":
                        "requirements.txt",

                    "content":
                        "\n".join(
                            requirements
                        ),
                },
            )

            # =================================================
            # DOCKERFILE
            # =================================================

            await tool_executor.execute_tool(

                "write_file",

                {

                    "path":
                        "Dockerfile",

                    "content":
                        self._generate_dockerfile(),
                },
            )

            # =================================================
            # DOCKER COMPOSE
            # =================================================

            await tool_executor.execute_tool(

                "write_file",

                {

                    "path":
                        "docker-compose.yml",

                    "content":
                        self._generate_docker_compose(),
                },
            )

            # =================================================
            # README
            # =================================================

            await tool_executor.execute_tool(

                "write_file",

                {

                    "path":
                        "README.md",

                    "content":
                        self._generate_readme(

                            query=context.get(
                                "query",
                                ""
                            ),

                            requirements=requirements,

                            api_implementations=(
                                api_implementations
                            ),
                        ),
                },
            )

            return {

                "success": True,

                "agent":
                    "code_agent",

                "implementation_type":
                    implementation_type,

                "generated_files":
                    generated_files,

                "written_files":
                    written_files,

                "requirements":
                    requirements,

                "api_implementations":
                    api_implementations,

                "database_models":
                    database_models,

                "deployment_configs":
                    deployment_configs,

                "reasoning":
                    reasoning,
            }

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
    # DOCKERFILE
    # ========================================================

    def _generate_dockerfile(
        self,
    ):

        return """
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "app/main.py"]
"""

    # ========================================================
    # DOCKER COMPOSE
    # ========================================================

    def _generate_docker_compose(
        self,
    ):

        return """
version: '3.9'

services:

  backend:

    build: .

    ports:
      - "8000:8000"

    volumes:
      - .:/app
"""

    # ========================================================
    # README
    # ========================================================

    def _generate_readme(

        self,

        query,

        requirements,

        api_implementations,
    ):

        return f"""
# CognitiveOS Generated Backend

## Query

{query}

## Requirements

{requirements}

## APIs

{api_implementations}

## Run Project

bash
pip install -r requirements.txt
python app/main.py"""