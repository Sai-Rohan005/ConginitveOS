# domains/software_engineering/agents/debug_agent.py

"""
CognitiveOS - Advanced Debug Agent
---------------------------------------------------------

Responsibilities:
- analyze REAL runtime failures
- inspect execution artifacts
- validate generated systems
- detect runtime errors
- detect scalability issues
- detect security flaws
- patch implementations
- recommend fixes
- validate workspace state

This agent acts like:
- Senior Reliability Engineer
- Production Debugging Engineer
- Security Reviewer
- Platform Stability Engineer
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
class DebugAgentState:

    query: str

    task: str

    agent_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    artifacts: List[Any] = field(
        default_factory=list
    )

    execution_artifacts: List[
        Any
    ] = field(default_factory=list)

    workspace_tree: List[
        Any
    ] = field(default_factory=list)

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# DEBUG AGENT
# ============================================================


class DebugAgent:

    """
    Runtime-aware debugging agent.
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

Agent Outputs:
{agent_outputs}

Execution Artifacts:
{execution_artifacts}

Workspace Tree:
{workspace_tree}

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
                "DEBUG AGENT STARTED"
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
            # CONTEXT ARTIFACTS
            # =================================================

            context_artifacts = context.get(
                "context_artifacts",
                [],
            )

            # =================================================
            # FILTER EXECUTION ARTIFACTS
            # =================================================

            execution_artifacts = [

                artifact

                for artifact in context_artifacts

                if (
                    getattr(
                        artifact,
                        "artifact_type",
                        "",
                    )
                    == "execution_log"
                )
            ]

            # =================================================
            # GET WORKSPACE TREE
            # =================================================

            workspace_tree_result = await (
                tool_executor.execute_tool(
                    "tree",
                    {},
                )
            )

            workspace_tree = (
                workspace_tree_result.get(
                    "output",
                    [],
                )
            )

            print(
                "\nEXECUTION ARTIFACTS:\n"
            )

            print(
                execution_artifacts
            )

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

                    "agent_outputs":
                        str(
                            context.get(
                                "agent_outputs",
                                {},
                            )
                        ),

                    "execution_artifacts":
                        str(
                            execution_artifacts
                        ),

                    "workspace_tree":
                        str(
                            workspace_tree
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
                "\nRAW DEBUG RESPONSE:\n"
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
                "\nPARSED DEBUG RESPONSE:\n"
            )

            print(response)

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            runtime_errors = response.get(
                "runtime_errors",
                [],
            )

            syntax_errors = response.get(
                "syntax_errors",
                [],
            )

            import_errors = response.get(
                "import_errors",
                [],
            )

            logic_issues = response.get(
                "logic_issues",
                [],
            )

            performance_issues = response.get(
                "performance_issues",
                [],
            )

            security_issues = response.get(
                "security_issues",
                [],
            )

            scalability_issues = response.get(
                "scalability_issues",
                [],
            )

            reliability_issues = response.get(
                "reliability_issues",
                [],
            )

            recommended_fixes = response.get(
                "recommended_fixes",
                [],
            )

            required_patches = response.get(
                "required_patches",
                [],
            )

            retry_required = response.get(
                "retry_required",
                False,
            )

            production_readiness = response.get(
                "production_readiness",
                "partial",
            )

            code_quality_score = response.get(
                "code_quality_score",
                "medium",
            )

            reasoning = response.get(
                "reasoning",
                "",
            )

            # =================================================
            # APPLY PATCHES
            # =================================================

            applied_patches = []

            for patch in required_patches:

                try:

                    patch_result = await (
                        tool_executor.execute_tool(

                            "patch_file",

                            {

                                "path":
                                    patch.get(
                                        "file_path",
                                        "",
                                    ),

                                "old_text":
                                    patch.get(
                                        "old_text",
                                        "",
                                    ),

                                "new_text":
                                    patch.get(
                                        "new_text",
                                        "",
                                    ),
                            },
                        )
                    )

                    applied_patches.append(
                        patch_result
                    )

                except Exception as e:

                    applied_patches.append(

                        {

                            "success":
                                False,

                            "error":
                                str(e),
                        }
                    )

            # =================================================
            # FINAL OUTPUT
            # =================================================

            debug_output = {

                "success": True,

                "agent":
                    "debug_agent",

                "runtime_errors":
                    runtime_errors,

                "syntax_errors":
                    syntax_errors,

                "import_errors":
                    import_errors,

                "logic_issues":
                    logic_issues,

                "performance_issues":
                    performance_issues,

                "security_issues":
                    security_issues,

                "scalability_issues":
                    scalability_issues,

                "reliability_issues":
                    reliability_issues,

                "recommended_fixes":
                    recommended_fixes,

                "required_patches":
                    required_patches,

                "applied_patches":
                    applied_patches,

                "retry_required":
                    retry_required,

                "production_readiness":
                    production_readiness,

                "code_quality_score":
                    code_quality_score,

                "reasoning":
                    reasoning,
            }

            print(
                "\nFINAL DEBUG OUTPUT:\n"
            )

            print(debug_output)

            return debug_output

        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "DEBUG AGENT FAILED"
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
                    "debug_agent",

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
You are the Advanced Debug Agent for CognitiveOS.

Your role is to:
- debug REAL runtime failures
- analyze execution artifacts
- inspect stack traces
- inspect stderr
- inspect runtime outputs
- validate generated projects
- improve reliability
- patch implementations

You think like:
- Senior Reliability Engineer
- Production Debugging Engineer
- Security Auditor
- Platform Stability Engineer

You are STRICT and analytical.

Focus on:

1. runtime failures
2. syntax errors
3. import issues
4. scalability
5. security
6. reliability
7. production readiness
8. maintainability
9. observability

You MUST:
- analyze REAL execution logs
- inspect stderr carefully
- identify root causes
- propose production-grade fixes
- recommend patches
- validate architecture consistency

Return ONLY valid JSON.

JSON FORMAT:

{{
  "runtime_errors": [

    "FastAPI app startup failure"
  ],

  "syntax_errors": [

    "Missing colon in route handler"
  ],

  "import_errors": [

    "uvicorn module missing"
  ],

  "logic_issues": [

    "JWT middleware not applied"
  ],

  "performance_issues": [

    "Blocking database calls"
  ],

  "security_issues": [

    "JWT expiration not validated"
  ],

  "scalability_issues": [

    "No async processing"
  ],

  "reliability_issues": [

    "Missing retry logic"
  ],

  "recommended_fixes": [

    "Add async DB layer",

    "Install missing dependencies"
  ],

  "required_patches": [

    {{

      "file_path":
        "app/main.py",

      "old_text":
        "from fastapi import FastAPI",

      "new_text":
        "from fastapi import FastAPI\\nimport uvicorn"
    }}

  ],

  "retry_required":
    true,

  "production_readiness":
    "mostly_ready",

  "code_quality_score":
    "high",

  "reasoning":
    "System is scalable but runtime dependency handling is incomplete."
}}
"""