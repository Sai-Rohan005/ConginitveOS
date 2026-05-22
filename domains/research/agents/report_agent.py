# domains/research/agents/report_agent.py

"""
CognitiveOS - Research Report Agent
---------------------------------------------------------

Responsibilities:
- generate structured research reports
- synthesize findings
- summarize technical literature
- generate executive summaries
- organize scientific content
- improve readability
- create publication-ready reports
- support knowledge synthesis

This agent behaves like:
- Research Scientist
- Technical Writer
- Scientific Documentation Engineer
- Academic Report Specialist
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
class ReportAgentState:

    query: str

    task: str

    research_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    citation_context: Dict[
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
# REPORT AGENT
# ============================================================


class ReportAgent:

    """
    Production-grade research report generation agent.
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

Citation Context:
{citation_context}

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

                        "citation_context":
                            str(
                                context.get(
                                    "citation_context",
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

            report_strategy = result.get(
                "report_strategy",
                {},
            )

            executive_summary = result.get(
                "executive_summary",
                "",
            )

            abstract = result.get(
                "abstract",
                "",
            )

            report_structure = result.get(
                "report_structure",
                {},
            )

            key_findings = result.get(
                "key_findings",
                [],
            )

            methodology_summary = result.get(
                "methodology_summary",
                "",
            )

            technical_analysis = result.get(
                "technical_analysis",
                {},
            )

            literature_review = result.get(
                "literature_review",
                {},
            )

            result_synthesis = result.get(
                "result_synthesis",
                {},
            )

            comparative_analysis = result.get(
                "comparative_analysis",
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

            visualization_recommendations = result.get(
                "visualization_recommendations",
                [],
            )

            publication_strategy = result.get(
                "publication_strategy",
                {},
            )

            generated_sections = result.get(
                "generated_sections",
                [],
            )

            readability_analysis = result.get(
                "readability_analysis",
                {},
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            report_risks = result.get(
                "report_risks",
                [],
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            report_score = result.get(
                "report_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "report_agent",

                "report_strategy":
                    report_strategy,

                "executive_summary":
                    executive_summary,

                "abstract":
                    abstract,

                "report_structure":
                    report_structure,

                "key_findings":
                    key_findings,

                "methodology_summary":
                    methodology_summary,

                "technical_analysis":
                    technical_analysis,

                "literature_review":
                    literature_review,

                "result_synthesis":
                    result_synthesis,

                "comparative_analysis":
                    comparative_analysis,

                "limitations":
                    limitations,

                "future_work":
                    future_work,

                "visualization_recommendations":
                    visualization_recommendations,

                "publication_strategy":
                    publication_strategy,

                "generated_sections":
                    generated_sections,

                "readability_analysis":
                    readability_analysis,

                "optimization_recommendations":
                    optimization_recommendations,

                "report_risks":
                    report_risks,

                "production_readiness":
                    production_readiness,

                "report_score":
                    report_score,

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
                    "report_agent",

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
You are the Report Agent
for CognitiveOS.

Your role is to:
- generate structured research reports
- synthesize findings
- organize technical content
- improve readability
- summarize methodologies
- create publication-ready reports
- support scientific communication
- improve knowledge transfer

You think like:
- Research Scientist
- Technical Writer
- Scientific Reviewer
- Academic Documentation Specialist

Focus on:
- research structure
- executive summaries
- literature synthesis
- technical clarity
- publication readiness
- readability
- scientific rigor
- report organization

You MUST:
- generate REALISTIC research reports
- improve readability
- organize technical findings clearly
- summarize methodologies correctly
- maintain scientific rigor
- optimize publication quality

Return ONLY valid JSON.

JSON FORMAT:

{{
  "report_strategy": {{

    "report_type":
      "technical research report",

    "audience":
      "research engineers",

    "publication_target":
      "conference paper"
  }},

  "executive_summary":
    "This report evaluates scalable transformer architectures for multi-agent reasoning systems.",

  "abstract":
    "The study explores distributed cognitive orchestration using autonomous AI agents.",

  "report_structure": {{

    "sections":
      [
        "Introduction",
        "Methodology",
        "Results",
        "Discussion",
        "Conclusion"
      ],

    "appendix":
      true
  }},

  "key_findings": [

    "Distributed orchestration improves scalability",

    "Deterministic debugging reduces runtime failures"
  ],

  "methodology_summary":
    "A multi-agent orchestration pipeline was evaluated using deterministic runtime validation.",

  "technical_analysis": {{

    "models_evaluated":
      4,

    "datasets":
      3
  }},

  "literature_review": {{

    "papers_reviewed":
      28,

    "major_topics":
      [
        "LLM orchestration",
        "multi-agent systems",
        "reasoning engines"
      ]
  }},

  "result_synthesis": {{

    "performance_gain":
      "18%",

    "runtime_stability":
      "improved"
  }},

  "comparative_analysis": {{

    "baseline":
      "single-agent systems",

    "improvement":
      "higher coordination accuracy"
  }},

  "limitations": [

    "limited benchmark diversity",

    "high GPU requirements"
  ],

  "future_work": [

    "distributed execution",

    "cross-domain reasoning"
  ],

  "visualization_recommendations": [

    "workflow diagrams",

    "performance comparison charts"
  ],

  "publication_strategy": {{

    "venue":
      "AI Systems Conference",

    "review_type":
      "peer-reviewed"
  }},

  "generated_sections": [

    "Introduction draft",

    "Methodology draft",

    "Conclusion draft"
  ],

  "readability_analysis": {{

    "clarity":
      "high",

    "technical_density":
      "moderate"
  }},

  "optimization_recommendations": [

    "improve visual storytelling",

    "reduce repetitive explanations"
  ],

  "report_risks": [

    "insufficient baseline comparison",

    "limited reproducibility details"
  ],

  "production_readiness":
    "high",

  "report_score":
    9.3,

  "reasoning":
    "Structured synthesis improves research communication and publication readiness."
}}
"""