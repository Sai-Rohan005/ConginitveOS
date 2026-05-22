# domains/research/agents/search_agent.py

"""
CognitiveOS - Research Search Agent
---------------------------------------------------------

Responsibilities:
- perform intelligent literature search
- discover research papers
- retrieve technical knowledge
- analyze search relevance
- rank research sources
- detect emerging trends
- synthesize search findings
- support autonomous research workflows

This agent behaves like:
- Research Scientist
- Knowledge Retrieval Engineer
- Literature Review Specialist
- Scientific Discovery Architect
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
class SearchAgentState:

    query: str

    task: str

    research_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    search_context: Dict[
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
# SEARCH AGENT
# ============================================================


class SearchAgent:

    """
    Production-grade autonomous research search agent.
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

Research Context:
{research_context}

Search Context:
{search_context}

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

                        "search_context":
                            str(
                                context.get(
                                    "search_context",
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

            search_strategy = result.get(
                "search_strategy",
                {},
            )

            search_queries = result.get(
                "search_queries",
                [],
            )

            retrieved_sources = result.get(
                "retrieved_sources",
                [],
            )

            literature_domains = result.get(
                "literature_domains",
                [],
            )

            relevance_analysis = result.get(
                "relevance_analysis",
                {},
            )

            source_ranking = result.get(
                "source_ranking",
                {},
            )

            semantic_clustering = result.get(
                "semantic_clustering",
                {},
            )

            trend_analysis = result.get(
                "trend_analysis",
                {},
            )

            novelty_analysis = result.get(
                "novelty_analysis",
                {},
            )

            knowledge_gaps = result.get(
                "knowledge_gaps",
                [],
            )

            citation_analysis = result.get(
                "citation_analysis",
                {},
            )

            research_landscape = result.get(
                "research_landscape",
                {},
            )

            key_papers = result.get(
                "key_papers",
                [],
            )

            generated_insights = result.get(
                "generated_insights",
                [],
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            search_risks = result.get(
                "search_risks",
                [],
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            search_score = result.get(
                "search_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "search_agent",

                "search_strategy":
                    search_strategy,

                "search_queries":
                    search_queries,

                "retrieved_sources":
                    retrieved_sources,

                "literature_domains":
                    literature_domains,

                "relevance_analysis":
                    relevance_analysis,

                "source_ranking":
                    source_ranking,

                "semantic_clustering":
                    semantic_clustering,

                "trend_analysis":
                    trend_analysis,

                "novelty_analysis":
                    novelty_analysis,

                "knowledge_gaps":
                    knowledge_gaps,

                "citation_analysis":
                    citation_analysis,

                "research_landscape":
                    research_landscape,

                "key_papers":
                    key_papers,

                "generated_insights":
                    generated_insights,

                "optimization_recommendations":
                    optimization_recommendations,

                "search_risks":
                    search_risks,

                "production_readiness":
                    production_readiness,

                "search_score":
                    search_score,

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
                    "search_agent",

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
You are the Search Agent
for CognitiveOS.

Your role is to:
- discover relevant research papers
- retrieve scientific knowledge
- rank research quality
- analyze literature trends
- identify knowledge gaps
- synthesize search findings
- optimize semantic retrieval
- improve research discovery

You think like:
- Research Scientist
- Knowledge Retrieval Engineer
- Literature Review Expert
- Scientific Discovery Specialist

Focus on:
- semantic search
- research retrieval
- citation networks
- paper ranking
- trend analysis
- novelty detection
- literature clustering
- research synthesis

You MUST:
- generate REALISTIC research searches
- prioritize scholarly sources
- identify high-impact papers
- improve retrieval relevance
- detect research trends
- analyze scientific quality

Return ONLY valid JSON.

JSON FORMAT:

{{
  "search_strategy": {{

    "search_type":
      "semantic scholarly retrieval",

    "retrieval_mode":
      "multi-source",

    "ranking":
      "citation-aware"
  }},

  "search_queries": [

    "multi-agent reasoning systems",

    "autonomous orchestration frameworks",

    "LLM planning architectures"
  ],

  "retrieved_sources": [

    {{
      "title":
        "Attention Is All You Need",

      "source":
        "arXiv",

      "year":
        2017
    }}
  ],

  "literature_domains": [

    "LLMs",

    "multi-agent systems",

    "reasoning architectures"
  ],

  "relevance_analysis": {{

    "high_relevance":
      18,

    "medium_relevance":
      7
  }},

  "source_ranking": {{

    "top_source":
      "Nature Machine Intelligence",

    "ranking_method":
      "citation weighted"
  }},

  "semantic_clustering": {{

    "clusters":
      5,

    "main_cluster":
      "agent orchestration"
  }},

  "trend_analysis": {{

    "emerging_topics":
      [
        "autonomous cognition",
        "LLM agents"
      ]
  }},

  "novelty_analysis": {{

    "novel_research_areas":
      [
        "deterministic cognition",
        "runtime reasoning"
      ]
  }},

  "knowledge_gaps": [

    "cross-domain orchestration",

    "runtime memory consistency"
  ],

  "citation_analysis": {{

    "highly_cited_papers":
      12,

    "avg_citation_count":
      2400
  }},

  "research_landscape": {{

    "dominant_area":
      "LLM orchestration",

    "research_maturity":
      "rapidly evolving"
  }},

  "key_papers": [

    "Attention Is All You Need",

    "ReAct",

    "Toolformer"
  ],

  "generated_insights": [

    "Agentic AI research is accelerating rapidly",

    "Runtime orchestration is underexplored"
  ],

  "optimization_recommendations": [

    "expand semantic retrieval",

    "prioritize peer-reviewed sources",

    "improve citation diversity"
  ],

  "search_risks": [

    "over-reliance on arXiv",

    "rapidly changing literature"
  ],

  "production_readiness":
    "high",

  "search_score":
    9.4,

  "reasoning":
    "Semantic scholarly retrieval improves research discovery and knowledge synthesis."
}}
"""