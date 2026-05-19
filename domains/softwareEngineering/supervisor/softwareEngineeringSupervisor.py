# domains/software_engineering/supervisor/software_supervisor.py

"""
CognitiveOS - Software Engineering Supervisor
---------------------------------------------------------

Responsibilities:
- convert planner goals into execution workflows
- assign specialized agents
- determine execution ordering
- manage orchestration strategy
- prepare runtime execution graph

This is orchestration intelligence.
"""

from __future__ import annotations

import os
import traceback
import dotenv

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    List,
    Dict,
    Any,
    Optional,
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

dotenv.load_dotenv()

api_key = os.getenv(
    "GOOGLE_API_KEY"
)

# ============================================================
# EXECUTION STEP
# ============================================================


@dataclass
class WorkflowStep:

    step_id: int

    agent: str

    task: str

    dependencies: List[int] = field(
        default_factory=list
    )

    parallelizable: bool = False

    expected_output: str = ""


# ============================================================
# SUPERVISOR STATE
# ============================================================


@dataclass
class SoftwareSupervisorState:

    query: str

    planner_output: Dict[
        str,
        Any,
    ]

    workflow_steps: List[
        WorkflowStep
    ] = field(default_factory=list)

    orchestration_strategy: str = ""

    requires_reflection: bool = True

    estimated_execution_order: List[
        int
    ] = field(default_factory=list)

    output: Optional[
        Dict[str, Any]
    ] = None


# ============================================================
# SOFTWARE SUPERVISOR
# ============================================================


class SoftwareSupervisor:

    """
    CognitiveOS Software Supervisor
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

Planner Output:
{planner_output}
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
        state: SoftwareSupervisorState,
    ) -> SoftwareSupervisorState:

        try:

            # ====================================================
            # RAW LLM CALL
            # ====================================================

            raw_response = await (
                self.prompt
                | self.llm
            ).ainvoke(

                {

                    "query":
                        state.query,

                    "planner_output":
                        str(
                            state.planner_output
                        ),
                }
            )

            # ====================================================
            # EXTRACT RESPONSE TEXT
            # ====================================================

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

            # ====================================================
            # RAW RESPONSE DEBUG
            # ====================================================

            print(
                "\n"
                + "=" * 80
            )

            print(
                "SUPERVISOR RAW RESPONSE"
            )

            print(
                "=" * 80
            )

            print(
                response_text
            )

            # ====================================================
            # CLEAN JSON
            # ====================================================

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

            print(
                "\nCLEANED RESPONSE:\n"
            )

            print(
                response_text
            )

            # ====================================================
            # PARSE JSON
            # ====================================================

            response = self.parser.parse(
                response_text
            )

            print(
                "\nPARSED RESPONSE:\n"
            )

            print(
                response
            )

            # ====================================================
            # SAFE DEFAULTS
            # ====================================================

            workflow = response.get(
                "workflow_steps",
                []
            )

            orchestration_strategy = (
                response.get(
                    "orchestration_strategy",
                    "Sequential execution",
                )
            )

            requires_reflection = (
                response.get(
                    "requires_reflection",
                    True,
                )
            )

            execution_order = response.get(
                "execution_order",
                [],
            )

            parsed_steps = []

            # ====================================================
            # PARSE WORKFLOW STEPS
            # ====================================================

            if isinstance(
                workflow,
                list,
            ):

                for idx, step in enumerate(
                    workflow
                ):

                    try:

                        workflow_step = (
                            WorkflowStep(

                                step_id=step.get(
                                    "step_id",
                                    idx + 1,
                                ),

                                agent=step.get(
                                    "agent",
                                    "code_agent",
                                ),

                                task=step.get(
                                    "task",
                                    "",
                                ),

                                dependencies=step.get(
                                    "dependencies",
                                    [],
                                ),

                                parallelizable=step.get(
                                    "parallelizable",
                                    False,
                                ),

                                expected_output=step.get(
                                    "expected_output",
                                    "",
                                ),
                            )
                        )

                        parsed_steps.append(
                            workflow_step
                        )

                        print(
                            "\nPARSED STEP:\n"
                        )

                        print(
                            workflow_step
                        )

                    except Exception as e:

                        print(
                            "\nSTEP PARSE FAILED\n"
                        )

                        print(
                            str(e)
                        )

                        continue

            # ====================================================
            # FINAL DEBUG
            # ====================================================

            print(
                "\n"
                + "=" * 80
            )

            print(
                "FINAL PARSED WORKFLOW"
            )

            print(
                "=" * 80
            )

            for step in parsed_steps:

                print(step)

            # ====================================================
            # UPDATE STATE
            # ====================================================

            state.workflow_steps = (
                parsed_steps
            )

            state.orchestration_strategy = (
                orchestration_strategy
            )

            state.requires_reflection = (
                requires_reflection
            )

            state.estimated_execution_order = (
                execution_order
            )

            state.output = response

            return state

        # ========================================================
        # ERROR HANDLING
        # ========================================================

        except Exception as e:

            print(
                "\n"
                + "=" * 80
            )

            print(
                "SUPERVISOR FAILED"
            )

            print(
                "=" * 80
            )

            print(
                str(e)
            )

            print(
                traceback.format_exc()
            )

            state.output = {

                "success": False,

                "error":
                    str(e),

                "traceback":
                    traceback.format_exc(),
            }

            return state

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    def _system_prompt(self):

        return """
You are the Software Engineering Supervisor for CognitiveOS.

Your role is to:
- orchestrate execution workflows
- assign specialized agents
- determine execution order
- define dependencies
- coordinate software engineering cognition

You DO NOT solve the task yourself.

You ONLY:
- build execution workflows
- coordinate agent execution strategy

Available Agents:

1. architecture_agent
2. code_agent
3. debug_agent
4. reflection_agent
5. aggregator_agent

You must think like:
- Engineering Manager
- Technical Lead
- AI Orchestrator

Return ONLY valid JSON.

JSON FORMAT:

{{
  "orchestration_strategy":
    "Sequential architecture-first execution",

  "requires_reflection": true,

  "execution_order": [1, 2, 3, 4],

  "workflow_steps": [

    {{
      "step_id": 1,

      "agent": "architecture_agent",

      "task":
        "Design scalable backend architecture",

      "dependencies": [],

      "parallelizable": false,

      "expected_output":
        "Architecture specification"
    }},

    {{
      "step_id": 2,

      "agent": "code_agent",

      "task":
        "Implement websocket backend",

      "dependencies": [1],

      "parallelizable": false,

      "expected_output":
        "Production-ready backend code"
    }},

    {{
      "step_id": 3,

      "agent": "debug_agent",

      "task":
        "Validate backend implementation",

      "dependencies": [2],

      "parallelizable": false,

      "expected_output":
        "Debugging and validation report"
    }}

  ]
}}
"""