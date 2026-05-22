# domains/aiEngineering/agents/rag_agent.py

"""
CognitiveOS - RAG Agent
---------------------------------------------------------

Responsibilities:
- generate RAG systems
- build retrieval pipelines
- generate vector search architectures
- build chunking systems
- generate embedding pipelines
- implement reranking systems
- create scalable retrieval APIs
- build production-grade RAG workflows

This agent behaves like:
- Senior RAG Engineer
- LLM Systems Architect
- Retrieval Engineer
- AI Infrastructure Engineer
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
class RAGAgentState:

    query: str

    task: str

    architecture_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    previous_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# RAG AGENT
# ============================================================


class RAGAgent:

    """
    Production-grade RAG generation agent.
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

Architecture Context:
{architecture_context}

Previous Outputs:
{previous_outputs}
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

                        "architecture_context":
                            str(
                                context.get(
                                    "shared_context",
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
                    }
                )
            )

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            rag_type = result.get(
                "rag_type",
                "hybrid_rag",
            )

            vector_database = result.get(
                "vector_database",
                "Qdrant",
            )

            embedding_model = result.get(
                "embedding_model",
                "",
            )

            llm_provider = result.get(
                "llm_provider",
                "",
            )

            retrieval_strategy = result.get(
                "retrieval_strategy",
                [],
            )

            chunking_strategy = result.get(
                "chunking_strategy",
                {},
            )

            reranking = result.get(
                "reranking",
                {},
            )

            generated_components = result.get(
                "generated_components",
                [],
            )

            api_design = result.get(
                "api_design",
                [],
            )

            scalability_features = result.get(
                "scalability_features",
                [],
            )

            observability = result.get(
                "observability",
                [],
            )

            deployment = result.get(
                "deployment",
                {},
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "rag_agent",

                "rag_type":
                    rag_type,

                "vector_database":
                    vector_database,

                "embedding_model":
                    embedding_model,

                "llm_provider":
                    llm_provider,

                "retrieval_strategy":
                    retrieval_strategy,

                "chunking_strategy":
                    chunking_strategy,

                "reranking":
                    reranking,

                "generated_components":
                    generated_components,

                "api_design":
                    api_design,

                "scalability_features":
                    scalability_features,

                "observability":
                    observability,

                "deployment":
                    deployment,

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
                    "rag_agent",

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
You are the RAG Agent for CognitiveOS.

Your role is to:
- design production-grade RAG systems
- create scalable retrieval architectures
- generate vector search systems
- implement chunking pipelines
- design embedding workflows
- implement reranking systems
- optimize retrieval quality
- design low-latency inference systems

You think like:
- Senior RAG Engineer
- Retrieval Systems Architect
- AI Infrastructure Engineer
- LLM Platform Engineer

Focus on:
- retrieval quality
- scalability
- latency optimization
- hallucination reduction
- observability
- production-readiness
- modularity
- fault tolerance

You MUST:
- design REAL production systems
- avoid toy architectures
- include scalable retrieval strategies
- optimize embedding pipelines
- include observability and monitoring
- include deployment strategies

Return ONLY valid JSON.

JSON FORMAT:

{{
  "rag_type":
    "hybrid_rag",

  "vector_database":
    "Qdrant",

  "embedding_model":
    "text-embedding-3-large",

  "llm_provider":
    "OpenAI GPT-4",

  "retrieval_strategy": [

    "dense retrieval",

    "bm25 retrieval",

    "hybrid search",

    "metadata filtering"
  ],

  "chunking_strategy": {{

    "method":
      "semantic_chunking",

    "chunk_size":
      512,

    "overlap":
      64
  }},

  "reranking": {{

    "enabled":
      true,

    "model":
      "cross-encoder/ms-marco"
  }},

  "generated_components": [

    "document_ingestion_pipeline",

    "embedding_service",

    "retrieval_service",

    "reranking_pipeline",

    "generation_pipeline",

    "conversation_memory",

    "citation_engine"
  ],

  "api_design": [

    {{

      "endpoint":
        "/api/v1/chat",

      "method":
        "POST",

      "purpose":
        "RAG chat inference"
    }},

    {{

      "endpoint":
        "/api/v1/ingest",

      "method":
        "POST",

      "purpose":
        "Document ingestion"
    }}
  ],

  "scalability_features": [

    "async retrieval",

    "embedding batching",

    "horizontal scaling",

    "distributed vector search",

    "response caching"
  ],

  "observability": [

    "LangSmith tracing",

    "Prometheus metrics",

    "structured logging",

    "retrieval analytics"
  ],

  "deployment": {{

    "containerization":
      "Docker",

    "orchestration":
      "Kubernetes",

    "ci_cd":
      "GitHub Actions"
  }},

  "reasoning":
    "Hybrid RAG chosen for high retrieval accuracy and scalability."
}}
"""