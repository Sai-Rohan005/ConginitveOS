# domains/research/agents/summarize_agent.py

"""
CognitiveOS - Research Summarization Agent
---------------------------------------------------------

Responsibilities:
- summarize research papers
- synthesize technical findings
- compress large documents
- generate executive summaries
- identify key insights
- simplify complex concepts
- support literature reviews
- improve knowledge transfer

This agent behaves like:
- Research Scientist
- Scientific Summarization Engineer
- Technical Writer
- Knowledge Synthesis Specialist
"""

from __future__ import annotations

import os
import traceback

from typing import (
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

api_key = os.getenv(
    "GOOGLE_API_KEY"
)

# ============================================================
# STATE
# ============================================================


@dataclass
class SummarizeAgentState:

    query: str

    task: str

    research_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    document_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    previous_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    artifacts: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# SUMMARIZE AGENT
# ============================================================


class SummarizeAgent:

    """
    Production-grade research summarization agent.
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

Research Context:
{research_context}

Document Context:
{document_context}

Previous Outputs:
{previous_outputs}

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

            result = await (

                self.chain.ainvoke(

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

                        "research_context":
                            str(
                                context.get(
                                    "shared_context",
                                    {},
                                )
                            ),

                        "document_context":
                            str(
                                context.get(
                                    "document_context",
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

                        "artifacts":
                            str(
                                context.get(
                                    "artifacts",
                                    {},
                                )
                            ),
                    }
                )
            )

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            summarization_strategy = result.get(
                "summarization_strategy",
                {},
            )

            executive_summary = result.get(
                "executive_summary",
                "",
            )

            abstract_summary = result.get(
                "abstract_summary",
                "",
            )

            technical_summary = result.get(
                "technical_summary",
                "",
            )

            methodology_summary = result.get(
                "methodology_summary",
                "",
            )

            result_summary = result.get(
                "result_summary",
                "",
            )

            key_findings = result.get(
                "key_findings",
                [],
            )

            important_concepts = result.get(
                "important_concepts",
                [],
            )

            research_contributions = result.get(
                "research_contributions",
                [],
            )

            comparative_analysis = result.get(
                "comparative_analysis",
                {},
            )

            novelty_analysis = result.get(
                "novelty_analysis",
                {},
            )

            limitations = result.get(
                "limitations",
                [],
            )

            future_work = result.get(
                "future_work",
                [],
            )

            simplified_explanations = result.get(
                "simplified_explanations",
                [],
            )

            section_summaries = result.get(
                "section_summaries",
                {},
            )

            compression_metrics = result.get(
                "compression_metrics",
                {},
            )

            readability_analysis = result.get(
                "readability_analysis",
                {},
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            summarization_risks = result.get(
                "summarization_risks",
                [],
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            summarization_score = result.get(
                "summarization_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "summarize_agent",

                "summarization_strategy":
                    summarization_strategy,

                "executive_summary":
                    executive_summary,

                "abstract_summary":
                    abstract_summary,

                "technical_summary":
                    technical_summary,

                "methodology_summary":
                    methodology_summary,

                "result_summary":
                    result_summary,

                "key_findings":
                    key_findings,

                "important_concepts":
                    important_concepts,

                "research_contributions":
                    research_contributions,

                "comparative_analysis":
                    comparative_analysis,

                "novelty_analysis":
                    novelty_analysis,

                "limitations":
                    limitations,

                "future_work":
                    future_work,

                "simplified_explanations":
                    simplified_explanations,

                "section_summaries":
                    section_summaries,

                "compression_metrics":
                    compression_metrics,

                "readability_analysis":
                    readability_analysis,

                "optimization_recommendations":
                    optimization_recommendations,

                "summarization_risks":
                    summarization_risks,

                "production_readiness":
                    production_readiness,

                "summarization_score":
                    summarization_score,

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
                    "summarize_agent",

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
You are the Summarization Agent
for CognitiveOS.

Your role is to:
- summarize research documents
- synthesize technical findings
- simplify complex concepts
- compress scientific knowledge
- identify key contributions
- generate executive summaries
- improve readability
- support literature understanding

You think like:
- Research Scientist
- Technical Writer
- Scientific Summarization Expert
- Knowledge Synthesis Engineer

Focus on:
- executive summaries
- technical compression
- methodology extraction
- key findings
- novelty analysis
- readability
- knowledge transfer
- scientific clarity

You MUST:
- generate REALISTIC summaries
- preserve technical accuracy
- simplify difficult concepts
- identify core contributions
- improve readability
- maintain scientific rigor

Return ONLY valid JSON.

JSON FORMAT:

{{
  "summarization_strategy": {{

    "summary_type":
      "technical research summary",

    "compression_level":
      "moderate",

    "target_audience":
      "research engineers"
  }},

  "executive_summary":
    "This paper explores scalable multi-agent reasoning architectures using deterministic orchestration.",

  "abstract_summary":
    "The study evaluates autonomous cognitive workflows powered by LLM-based orchestration.",

  "technical_summary":
    "A deterministic runtime framework coordinates autonomous agents using structured planning.",

  "methodology_summary":
    "The system integrates workflow orchestration, runtime validation, and reflection engines.",

  "result_summary":
    "The framework improved orchestration reliability and reduced runtime failures.",

  "key_findings": [

    "Deterministic planning improves stability",

    "Reflection loops enhance reasoning quality"
  ],

  "important_concepts": [

    "multi-agent systems",

    "runtime cognition",

    "deterministic orchestration"
  ],

  "research_contributions": [

    "Hybrid reasoning runtime",

    "Cross-domain orchestration framework"
  ],

  "comparative_analysis": {{

    "baseline":
      "single-agent pipelines",

    "improvement":
      "better coordination and debugging"
  }},

  "novelty_analysis": {{

    "novelty_level":
      "high",

    "innovations":
      [
        "runtime reflection engine",
        "deterministic debugger"
      ]
  }},

  "limitations": [

    "high compute requirements",

    "limited distributed execution"
  ],

  "future_work": [

    "distributed cognition",

    "cross-domain memory sharing"
  ],

  "simplified_explanations": [

    "The system acts like a team of AI engineers working together autonomously."
  ],

  "section_summaries": {{

    "introduction":
      "Introduces autonomous orchestration challenges.",

    "methodology":
      "Explains workflow cognition runtime."
  }},

  "compression_metrics": {{

    "original_length":
      12000,

    "summary_length":
      1800
  }},

  "readability_analysis": {{

    "clarity":
      "high",

    "technical_density":
      "moderate"
  }},

  "optimization_recommendations": [

    "improve visualization support",

    "reduce repetitive explanations"
  ],

  "summarization_risks": [

    "loss of minor technical details",

    "oversimplification risk"
  ],

  "production_readiness":
    "high",

  "summarization_score":
    9.4,

  "reasoning":
    "Structured summarization improves knowledge transfer and technical understanding."
}}
"""