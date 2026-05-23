# domains/research/agents/citation_agent.py

"""
CognitiveOS - Citation Agent
---------------------------------------------------------

Responsibilities:
- generate scholarly citations
- validate citation correctness
- detect citation inconsistencies
- recommend academic references
- format multi-style citations
- improve research traceability
- support literature review systems
- ensure academic integrity

This agent behaves like:
- Research Engineer
- Academic Citation Specialist
- Scientific Writing Assistant
- Knowledge Validation Engineer
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
class CitationAgentState:

    query: str

    task: str

    research_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    paper_context: Dict[
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
# CITATION AGENT
# ============================================================


class CitationAgent:

    """
    Production-grade citation intelligence agent.
    """

    def __init__(self):

        self.model = os.getenv(

            "GOOGLE_MODEL",

            "gemini-1.5-flash",
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

Research Context:
{research_context}

Paper Context:
{paper_context}

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

                        "paper_context":
                            str(
                                context.get(
                                    "paper_context",
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

            citation_strategy = result.get(
                "citation_strategy",
                {},
            )

            citation_styles = result.get(
                "citation_styles",
                [],
            )

            generated_citations = result.get(
                "generated_citations",
                [],
            )

            bibliography_structure = result.get(
                "bibliography_structure",
                {},
            )

            reference_validation = result.get(
                "reference_validation",
                {},
            )

            citation_consistency = result.get(
                "citation_consistency",
                {},
            )

            duplicate_detection = result.get(
                "duplicate_detection",
                {},
            )

            source_quality_analysis = result.get(
                "source_quality_analysis",
                {},
            )

            doi_analysis = result.get(
                "doi_analysis",
                {},
            )

            academic_integrity = result.get(
                "academic_integrity",
                {},
            )

            literature_connections = result.get(
                "literature_connections",
                [],
            )

            citation_graph = result.get(
                "citation_graph",
                {},
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            research_risks = result.get(
                "research_risks",
                [],
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            citation_score = result.get(
                "citation_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "citation_agent",

                "citation_strategy":
                    citation_strategy,

                "citation_styles":
                    citation_styles,

                "generated_citations":
                    generated_citations,

                "bibliography_structure":
                    bibliography_structure,

                "reference_validation":
                    reference_validation,

                "citation_consistency":
                    citation_consistency,

                "duplicate_detection":
                    duplicate_detection,

                "source_quality_analysis":
                    source_quality_analysis,

                "doi_analysis":
                    doi_analysis,

                "academic_integrity":
                    academic_integrity,

                "literature_connections":
                    literature_connections,

                "citation_graph":
                    citation_graph,

                "optimization_recommendations":
                    optimization_recommendations,

                "research_risks":
                    research_risks,

                "production_readiness":
                    production_readiness,

                "citation_score":
                    citation_score,

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
                    "citation_agent",

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
You are the Citation Agent
for CognitiveOS.

Your role is to:
- generate academic citations
- validate references
- ensure citation consistency
- improve literature quality
- support bibliography generation
- detect duplicate references
- analyze source credibility
- maintain academic integrity

You think like:
- Research Engineer
- Citation Specialist
- Academic Reviewer
- Scientific Documentation Expert

Focus on:
- APA citations
- IEEE citations
- MLA citations
- BibTeX
- DOI validation
- bibliography consistency
- scholarly references
- citation networks
- literature quality

You MUST:
- generate REALISTIC citations
- validate citation consistency
- improve academic integrity
- detect malformed references
- identify duplicate sources
- improve research traceability

Return ONLY valid JSON.

JSON FORMAT:

{{
  "citation_strategy": {{

    "primary_style":
      "IEEE",

    "secondary_style":
      "APA",

    "bibliography_type":
      "scholarly"
  }},

  "citation_styles": [

    "IEEE",

    "APA",

    "BibTeX"
  ],

  "generated_citations": [

    {{
      "title":
        "Attention Is All You Need",

      "authors":
        [
          "Ashish Vaswani",
          "Noam Shazeer"
        ],

      "year":
        2017,

      "doi":
        "10.48550/arXiv.1706.03762"
    }}
  ],

  "bibliography_structure": {{

    "ordered":
      true,

    "grouped_by_topic":
      true
  }},

  "reference_validation": {{

    "valid_references":
      24,

    "invalid_references":
      1
  }},

  "citation_consistency": {{

    "consistent":
      true,

    "missing_fields":
      false
  }},

  "duplicate_detection": {{

    "duplicates_found":
      0
  }},

  "source_quality_analysis": {{

    "peer_reviewed":
      18,

    "preprints":
      4
  }},

  "doi_analysis": {{

    "valid_dois":
      22,

    "missing_dois":
      2
  }},

  "academic_integrity": {{

    "plagiarism_risk":
      "low",

    "citation_completeness":
      "high"
  }},

  "literature_connections": [

    "Transformer models",

    "Attention mechanisms",

    "LLM scaling laws"
  ],

  "citation_graph": {{

    "connected_papers":
      32,

    "core_papers":
      6
  }},

  "optimization_recommendations": [

    "add DOI references",

    "replace low-quality blogs",

    "improve citation diversity"
  ],

  "research_risks": [

    "over-reliance on preprints",

    "limited citation diversity"
  ],

  "production_readiness":
    "high",

  "citation_score":
    9.2,

  "reasoning":
    "Validated scholarly citations improve research quality and academic traceability."
}}
"""