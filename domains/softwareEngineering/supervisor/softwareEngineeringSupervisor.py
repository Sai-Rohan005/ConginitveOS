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

This is NOT the executor.
This is orchestration intelligence.
"""

from __future__ import annotations

import os
import traceback

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

    Responsibilities:
    - orchestration planning
    - agent assignment
    - workflow generation
    - execution coordination
    """

    def __init__(self):

        self.model = os.getenv(
            "GOOGLE_MODEL",
            "gemini-2.0-flash",
        )

        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
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
        state: SoftwareSupervisorState,
    ) -> SoftwareSupervisorState:

        try:

            response = await self.chain.ainvoke(
                {

                    "query":
                        state.query,

                    "planner_output":
                        str(
                            state.planner_output
                        ),
                }
            )

            # ================================================
            # SAFE DEFAULTS
            # ================================================

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

            # ================================================
            # PARSE WORKFLOW STEPS
            # ================================================

            if isinstance(
                workflow,
                list,
            ):

                for idx, step in enumerate(
                    workflow
                ):

                    try:

                        parsed_steps.append(

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

                    except Exception:
                        continue

            # ================================================
            # UPDATE STATE
            # ================================================

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

        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            state.output = {

                "success": False,

                "error": str(e),

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

    {
      "step_id": 1,

      "agent": "architecture_agent",

      "task":
        "Design scalable backend architecture",

      "dependencies": [],

      "parallelizable": false,

      "expected_output":
        "Architecture specification"
    },

    {
      "step_id": 2,

      "agent": "code_agent",

      "task":
        "Implement websocket backend",

      "dependencies": [1],

      "parallelizable": false,

      "expected_output":
        "Production-ready backend code"
    }

  ]
}}
"""