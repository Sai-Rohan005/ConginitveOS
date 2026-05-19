from __future__ import annotations

import os
import json

from typing import (
    List,
    Optional,
    Dict,
    Any,
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
# EXECUTION STEP
# ============================================================

@dataclass
class ExecutionStep:

    step_id: int

    agent: str

    objective: str

    dependencies: List[int] = field(
        default_factory=list
    )

    estimated_output: str = ""

    parallelizable: bool = False


# ============================================================
# PLANNER STATE
# ============================================================

@dataclass
class PlannerAgentState:

    query: str

    constraints: List[str] = field(
        default_factory=list
    )

    execution_plan: List[
        ExecutionStep
    ] = field(default_factory=list)

    complexity: str = "medium"

    estimated_agents: List[str] = field(
        default_factory=list
    )

    output: Optional[
        Dict[str, Any]
    ] = None


# ============================================================
# PLANNER AGENT
# ============================================================

class PlannerAgent:

    """
    CognitiveOS Planner Agent

    Responsibilities:
    - task decomposition
    - execution planning
    - dependency analysis
    - workflow generation
    - agent assignment
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

Constraints:
{constraints}
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
        state: PlannerAgentState,
    ) -> PlannerAgentState:

        try:

            response = await self.chain.ainvoke(
                {

                    "query":
                        state.query,

                    "constraints":
                        state.constraints,
                }
            )

            execution_plan = response.get(
                "execution_plan",
                []
            )

            parsed_steps = []

            for idx, step in enumerate(
                execution_plan
            ):

                try:

                    parsed_steps.append(

                        ExecutionStep(

                            step_id=step.get(
                                "step_id",
                                idx + 1,
                            ),

                            agent=step.get(
                                "agent",
                                "code_agent",
                            ),

                            objective=step.get(
                                "objective",
                                "",
                            ),

                            dependencies=step.get(
                                "dependencies",
                                [],
                            ),

                            estimated_output=step.get(
                                "estimated_output",
                                "",
                            ),

                            parallelizable=step.get(
                                "parallelizable",
                                False,
                            ),
                        )
                    )

                except Exception:
                    continue

            # ================================================
            # UPDATE STATE
            # ================================================

            state.execution_plan = (
                parsed_steps
            )

            state.complexity = response.get(
                "complexity",
                "medium",
            )

            state.estimated_agents = (
                response.get(
                    "estimated_agents",
                    [],
                )
            )

            state.output = response

            return state

        except Exception as e:

            state.output = {

                "success": False,

                "error": str(e),
            }

            return state

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    def _system_prompt(self):

        return """
You are the Planner Agent for CognitiveOS.

Your role is to:
- analyze software engineering tasks
- decompose tasks into executable steps
- assign specialized agents
- determine dependencies
- create workflow execution plans

Available Agents:
1. architecture_agent
2. code_agent
3. debug_agent
4. reflection_agent
5. aggregator_agent

You MUST think like a senior engineering manager.

Return ONLY valid JSON.

JSON FORMAT:

{{
  "complexity": "medium",

  "estimated_agents": [
    "architecture_agent",
    "code_agent"
  ],

  "execution_plan": [

    {
      "step_id": 1,

      "agent": "architecture_agent",

      "objective":
        "Design scalable backend architecture",

      "dependencies": [],

      "estimated_output":
        "System architecture document",

      "parallelizable": false
    }

  ]
}}
"""