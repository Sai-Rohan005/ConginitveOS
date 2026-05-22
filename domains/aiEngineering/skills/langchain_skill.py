# domains/aiEngineering/skills/langchain_skill.py

"""
CognitiveOS - LangChain Skill
---------------------------------------------------------

Responsibilities:
- build LangChain pipelines
- generate chains
- build RAG systems
- create tools and agents
- generate memory systems
- build prompt pipelines
- create retrieval workflows
- support production orchestration

This module acts as:
- reusable AI skill layer
- deterministic LangChain utility layer
- low-LLM orchestration helper
"""

from __future__ import annotations

import json
import traceback

from typing import (
    Dict,
    Any,
    List,
    Optional,
)

from dataclasses import (
    dataclass,
    field,
)

# ============================================================
# LANGCHAIN IMPORTS
# ============================================================

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain_core.output_parsers import (
    StrOutputParser,
)

from langchain_core.runnables import (
    RunnablePassthrough,
)

from langchain_core.documents import (
    Document,
)

from langchain_core.vectorstores import (
    InMemoryVectorStore,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from langchain_community.document_loaders import (
    TextLoader,
)

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
)

# ============================================================
# SKILL RESULT
# ============================================================


@dataclass
class SkillResult:

    success: bool

    skill: str

    output: Any = None

    error: Optional[str] = None

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    def to_dict(self):

        return {

            "success":
                self.success,

            "skill":
                self.skill,

            "output":
                self.output,

            "error":
                self.error,

            "metadata":
                self.metadata,
        }


# ============================================================
# LANGCHAIN SKILL
# ============================================================


class LangChainSkill:

    """
    Production-grade LangChain utility layer.
    """

    def __init__(self):

        self.embedding_model = (
            GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            )
        )

        self.text_splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=1000,

                chunk_overlap=200,
            )
        )

    # ========================================================
    # DOCUMENT CHUNKING
    # ========================================================

    def chunk_text(
        self,
        text: str,
    ) -> Dict[str, Any]:

        try:

            chunks = self.text_splitter.split_text(
                text
            )

            return SkillResult(

                success=True,

                skill="chunk_text",

                output=chunks,

                metadata={

                    "total_chunks":
                        len(chunks),
                },
            ).to_dict()

        except Exception as e:

            return SkillResult(

                success=False,

                skill="chunk_text",

                error=str(e),
            ).to_dict()

    # ========================================================
    # BUILD DOCUMENTS
    # ========================================================

    def build_documents(
        self,
        texts: List[str],
        metadata: Optional[
            List[Dict[str, Any]]
        ] = None,
    ) -> Dict[str, Any]:

        try:

            documents = []

            for idx, text in enumerate(
                texts
            ):

                meta = {}

                if metadata and idx < len(
                    metadata
                ):

                    meta = metadata[idx]

                documents.append(

                    Document(

                        page_content=text,

                        metadata=meta,
                    )
                )

            return SkillResult(

                success=True,

                skill="build_documents",

                output=documents,

                metadata={

                    "documents":
                        len(documents),
                },
            ).to_dict()

        except Exception as e:

            return SkillResult(

                success=False,

                skill="build_documents",

                error=str(e),
            ).to_dict()

    # ========================================================
    # VECTOR STORE
    # ========================================================

    def build_vector_store(
        self,
        documents: List[Document],
    ) -> Dict[str, Any]:

        try:

            vector_store = (
                InMemoryVectorStore
                .from_documents(

                    documents,

                    self.embedding_model,
                )
            )

            return SkillResult(

                success=True,

                skill="build_vector_store",

                output=vector_store,

                metadata={

                    "documents":
                        len(documents),
                },
            ).to_dict()

        except Exception as e:

            return SkillResult(

                success=False,

                skill="build_vector_store",

                error=str(e),
            ).to_dict()

    # ========================================================
    # RETRIEVER
    # ========================================================

    def build_retriever(
        self,
        vector_store,
        k: int = 4,
    ) -> Dict[str, Any]:

        try:

            retriever = (
                vector_store.as_retriever(

                    search_kwargs={
                        "k": k
                    }
                )
            )

            return SkillResult(

                success=True,

                skill="build_retriever",

                output=retriever,

                metadata={

                    "top_k":
                        k,
                },
            ).to_dict()

        except Exception as e:

            return SkillResult(

                success=False,

                skill="build_retriever",

                error=str(e),
            ).to_dict()

    # ========================================================
    # SIMPLE RAG CHAIN
    # ========================================================

    def build_rag_prompt(
        self,
    ):

        return ChatPromptTemplate.from_template(
            """
You are a helpful AI assistant.

Context:
{context}

Question:
{question}

Answer:
"""
        )

    # ========================================================
    # FORMAT DOCUMENTS
    # ========================================================

    def format_documents(
        self,
        docs: List[Document],
    ) -> str:

        return "\n\n".join(

            [

                doc.page_content

                for doc in docs
            ]
        )

    # ========================================================
    # BUILD RAG CHAIN
    # ========================================================

    def build_rag_chain(
        self,
        llm,
        retriever,
    ) -> Dict[str, Any]:

        try:

            prompt = (
                self.build_rag_prompt()
            )

            rag_chain = (

                {

                    "context":

                        retriever
                        | self.format_documents,

                    "question":
                        RunnablePassthrough(),
                }

                | prompt

                | llm

                | StrOutputParser()
            )

            return SkillResult(

                success=True,

                skill="build_rag_chain",

                output=rag_chain,
            ).to_dict()

        except Exception as e:

            return SkillResult(

                success=False,

                skill="build_rag_chain",

                error=str(e),
            ).to_dict()

    # ========================================================
    # LOAD TEXT FILE
    # ========================================================

    def load_text_file(
        self,
        path: str,
    ) -> Dict[str, Any]:

        try:

            loader = TextLoader(path)

            documents = loader.load()

            return SkillResult(

                success=True,

                skill="load_text_file",

                output=documents,

                metadata={

                    "documents":
                        len(documents),
                },
            ).to_dict()

        except Exception as e:

            return SkillResult(

                success=False,

                skill="load_text_file",

                error=str(e),
            ).to_dict()

    # ========================================================
    # CHAIN SERIALIZATION
    # ========================================================

    def serialize_chain_config(
        self,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:

        try:

            serialized = json.dumps(

                config,

                indent=2,
            )

            return SkillResult(

                success=True,

                skill="serialize_chain_config",

                output=serialized,
            ).to_dict()

        except Exception as e:

            return SkillResult(

                success=False,

                skill="serialize_chain_config",

                error=str(e),
            ).to_dict()

    # ========================================================
    # HEALTHCHECK
    # ========================================================

    def healthcheck(self):

        return {

            "skill":
                "langchain_skill",

            "status":
                "healthy",

            "features": [

                "chunking",

                "retrieval",

                "rag",

                "vectorstore",

                "document_loading",

                "prompt_building",
            ],
        }


# ============================================================
# FACTORY
# ============================================================


def build_langchain_skill():

    return LangChainSkill()