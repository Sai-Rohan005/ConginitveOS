# domains/aiEngineering/agents/vector_db_agent.py

"""
CognitiveOS - Vector Database Agent
---------------------------------------------------------

Responsibilities:
- design vector database systems
- generate embedding storage pipelines
- optimize similarity search
- design hybrid retrieval systems
- configure indexing strategies
- optimize retrieval latency
- generate scalable vector architectures
- support multimodal retrieval

This agent behaves like:
- Vector Database Engineer
- Retrieval Infrastructure Engineer
- AI Systems Architect
- Search Infrastructure Engineer
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
class VectorDBAgentState:

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
# VECTOR DATABASE AGENT
# ============================================================


class VectorDBAgent:

    """
    Production-grade vector database agent.
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

            vector_database = result.get(
                "vector_database",
                "Qdrant",
            )

            indexing_strategy = result.get(
                "indexing_strategy",
                {},
            )

            embedding_strategy = result.get(
                "embedding_strategy",
                {},
            )

            storage_architecture = result.get(
                "storage_architecture",
                {},
            )

            retrieval_pipeline = result.get(
                "retrieval_pipeline",
                [],
            )

            filtering_strategy = result.get(
                "filtering_strategy",
                [],
            )

            hybrid_search = result.get(
                "hybrid_search",
                {},
            )

            sharding_strategy = result.get(
                "sharding_strategy",
                {},
            )

            scalability_features = result.get(
                "scalability_features",
                [],
            )

            observability = result.get(
                "observability",
                [],
            )

            api_design = result.get(
                "api_design",
                [],
            )

            deployment_strategy = result.get(
                "deployment_strategy",
                {},
            )

            performance_optimizations = result.get(
                "performance_optimizations",
                [],
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "vector_db_agent",

                "vector_database":
                    vector_database,

                "indexing_strategy":
                    indexing_strategy,

                "embedding_strategy":
                    embedding_strategy,

                "storage_architecture":
                    storage_architecture,

                "retrieval_pipeline":
                    retrieval_pipeline,

                "filtering_strategy":
                    filtering_strategy,

                "hybrid_search":
                    hybrid_search,

                "sharding_strategy":
                    sharding_strategy,

                "scalability_features":
                    scalability_features,

                "observability":
                    observability,

                "api_design":
                    api_design,

                "deployment_strategy":
                    deployment_strategy,

                "performance_optimizations":
                    performance_optimizations,

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
                    "vector_db_agent",

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
You are the Vector Database Agent for CognitiveOS.

Your role is to:
- design scalable vector database systems
- optimize similarity search
- build hybrid retrieval systems
- optimize embedding storage
- improve retrieval latency
- design distributed vector infrastructure
- optimize indexing and sharding
- support multimodal embeddings

You think like:
- Vector Search Engineer
- AI Infrastructure Engineer
- Distributed Systems Engineer
- Search Platform Architect

Focus on:
- retrieval latency
- scalability
- indexing efficiency
- memory optimization
- distributed retrieval
- fault tolerance
- production-readiness
- observability

You MUST:
- design REAL vector architectures
- avoid toy systems
- optimize for large-scale retrieval
- include hybrid retrieval
- include observability and scaling
- optimize indexing and search

Return ONLY valid JSON.

JSON FORMAT:

{{
  "vector_database":
    "Qdrant",

  "indexing_strategy": {{

    "algorithm":
      "HNSW",

    "distance_metric":
      "cosine",

    "quantization":
      "scalar_quantization"
  }},

  "embedding_strategy": {{

    "embedding_model":
      "text-embedding-3-large",

    "dimension":
      3072,

    "batching":
      true
  }},

  "storage_architecture": {{

    "replication":
      3,

    "distributed":
      true,

    "storage":
      "NVMe SSD"
  }},

  "retrieval_pipeline": [

    "semantic retrieval",

    "metadata filtering",

    "hybrid search",

    "reranking"
  ],

  "filtering_strategy": [

    "metadata filters",

    "tenant isolation",

    "time-range filtering"
  ],

  "hybrid_search": {{

    "enabled":
      true,

    "bm25":
      true,

    "dense_search":
      true
  }},

  "sharding_strategy": {{

    "strategy":
      "collection_sharding",

    "auto_scaling":
      true
  }},

  "scalability_features": [

    "horizontal scaling",

    "distributed indexing",

    "query caching",

    "asynchronous ingestion"
  ],

  "observability": [

    "Prometheus metrics",

    "OpenTelemetry tracing",

    "retrieval analytics",

    "latency monitoring"
  ],

  "api_design": [

    {{

      "endpoint":
        "/api/v1/search",

      "method":
        "POST",

      "purpose":
        "Semantic vector retrieval"
    }},

    {{

      "endpoint":
        "/api/v1/upsert",

      "method":
        "POST",

      "purpose":
        "Vector ingestion"
    }}
  ],

  "deployment_strategy": {{

    "containerization":
      "Docker",

    "orchestration":
      "Kubernetes",

    "autoscaling":
      true
  }},

  "performance_optimizations": [

    "vector quantization",

    "embedding batching",

    "async ingestion",

    "memory-mapped indexing"
  ],

  "reasoning":
    "Qdrant with HNSW selected for scalable low-latency retrieval."
}}
"""