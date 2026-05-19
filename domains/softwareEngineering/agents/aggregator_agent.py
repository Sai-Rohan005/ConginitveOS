# domains/software_engineering/agents/aggregator_agent.py

"""
CognitiveOS - Aggregator Agent
---------------------------------------------------------

Responsibilities:
- merge outputs from all agents
- remove redundancy
- synthesize reasoning
- generate coherent final responses
- create structured engineering reports
- summarize workflow execution
- produce user-facing output

This agent acts like:
- Technical Lead
- Senior Engineering Manager
- Solution Architect
- Final Report Generator

This is the FINAL response generation layer.
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
dotenv.load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# ============================================================
# STATE
# ============================================================


@dataclass
class AggregatorAgentState:

    query: str

    agent_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    reflection_notes: List[
        str
    ] = field(default_factory=list)

    artifacts: List[Any] = field(
        default_factory=list
    )

    final_response: str = ""


# ============================================================
# AGGREGATOR AGENT
# ============================================================


class AggregatorAgent:

    """
    Final synthesis agent for CognitiveOS.
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

Reflection Notes:
{reflection_notes}

Artifacts:
{artifacts}
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
        )

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def run(
        self,
        context: Dict[str, Any],
    ) -> str:

        try:

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

                    "reflection_notes":
                        str(
                            context.get(
                                "reflection_notes",
                                [],
                            )
                        ),

                    "artifacts":
                        str(
                            context.get(
                                "artifacts",
                                [],
                            )
                        ),
                }
            )

            return str(
                response.content
            )

        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            return f"""
# Aggregation Failed

An error occurred while generating the final response.

Error:
{str(e)}

Traceback:
{traceback.format_exc()}
"""

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    def _system_prompt(self):

        return """
You are the Aggregator Agent for CognitiveOS.

Your role is to:
- merge outputs from multiple agents
- synthesize technical reasoning
- create coherent final responses
- generate engineering-grade reports
- summarize workflow execution
- produce polished user-facing output

You think like:
- Technical Lead
- Senior Engineering Manager
- Principal Engineer
- Solution Architect

You DO NOT:
- dump raw JSON
- repeat redundant outputs
- expose internal orchestration details unnecessarily

You MUST:
- create highly structured responses
- explain architecture clearly
- summarize implementation decisions
- explain scalability considerations
- explain technical tradeoffs
- include reflection insights
- produce production-quality output

The final response should feel like:
- a senior engineer designed it
- a technical architect reviewed it
- a production engineering team prepared it

Structure your response professionally using:

# Overview
# Architecture
# Components
# APIs
# Scalability
# Security
# Deployment
# Reflection Insights
# Final Recommendations

Be concise but highly valuable.
"""