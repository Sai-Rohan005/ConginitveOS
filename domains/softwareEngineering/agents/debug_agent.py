# domains/software_engineering/agents/debug_agent.py

"""
CognitiveOS - Debug Agent
---------------------------------------------------------

Responsibilities:
- identify bugs
- detect logical flaws
- validate implementations
- analyze stack traces
- detect performance bottlenecks
- identify security vulnerabilities
- suggest fixes
- improve reliability

This agent acts like:
- Senior Debugging Engineer
- Production Support Engineer
- Reliability Engineer
- Security Reviewer
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

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# DEBUG AGENT
# ============================================================


class DebugAgent:

    """
    Debugging and validation agent.
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

Assigned Task:
{task}

Agent Outputs:
{agent_outputs}

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

                    "agent_outputs":
                        str(
                            context.get(
                                "agent_outputs",
                                {},
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

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            bug_analysis = response.get(
                "bug_analysis",
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

            reliability_issues = response.get(
                "reliability_issues",
                [],
            )

            recommended_fixes = response.get(
                "recommended_fixes",
                [],
            )

            code_quality_score = response.get(
                "code_quality_score",
                "medium",
            )

            production_readiness = response.get(
                "production_readiness",
                "partial",
            )

            reasoning = response.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "debug_agent",

                "bug_analysis":
                    bug_analysis,

                "logic_issues":
                    logic_issues,

                "performance_issues":
                    performance_issues,

                "security_issues":
                    security_issues,

                "reliability_issues":
                    reliability_issues,

                "recommended_fixes":
                    recommended_fixes,

                "code_quality_score":
                    code_quality_score,

                "production_readiness":
                    production_readiness,

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
You are the Debug Agent for CognitiveOS.

Your role is to:
- identify bugs
- validate implementations
- detect logical flaws
- identify scalability issues
- detect security vulnerabilities
- improve production reliability
- validate architecture consistency

You think like:
- Senior Debugging Engineer
- Reliability Engineer
- Production Support Engineer
- Security Auditor

You are STRICT and analytical.

Focus on:

1. correctness
2. logic validation
3. scalability
4. reliability
5. security
6. maintainability
7. production-readiness
8. performance bottlenecks

You MUST:
- identify flaws clearly
- explain why issues exist
- recommend production-grade fixes
- detect hidden edge cases
- validate architecture consistency

Return ONLY valid JSON.

JSON FORMAT:

{
  "bug_analysis": [

    "Potential websocket connection leak",

    "Missing async exception handling"
  ],

  "logic_issues": [

    "Authentication middleware not applied",

    "Retry logic missing"
  ],

  "performance_issues": [

    "Database queries not indexed",

    "Blocking I/O detected"
  ],

  "security_issues": [

    "JWT validation missing",

    "Rate limiting absent"
  ],

  "reliability_issues": [

    "No circuit breaker pattern",

    "No centralized logging"
  ],

  "recommended_fixes": [

    "Add Redis caching",

    "Implement structured logging",

    "Add retry middleware"
  ],

  "code_quality_score":
    "high",

  "production_readiness":
    "mostly_ready",

  "reasoning":
    "The implementation is scalable but lacks observability and security hardening."
}
"""