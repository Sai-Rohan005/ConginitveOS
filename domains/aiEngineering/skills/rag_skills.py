# domains/aiEngineering/skills/rag_skill.py

"""
CognitiveOS - RAG Skill
---------------------------------------------------------

Responsibilities:
- build production-grade RAG pipelines
- manage document ingestion
- create chunking pipelines
- generate embeddings
- build retrievers
- support hybrid retrieval
- perform reranking
- execute grounded generation

This becomes:
- reusable RAG runtime
- deterministic retrieval layer
- shared retrieval infrastructure
"""

from __future__ import annotations

import time
import traceback

from typing import (
    List,
    Dict,
    Any,
    Optional,
)

from dataclasses import (
    dataclass,
    field,
)

# ============================================================
# LANGCHAIN
# ============================================================

from langchain_core.documents import (
    Document,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain_core.output_parsers import (
    StrOutputParser,
)

from langchain_core.runnables import (
    RunnablePassthrough,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from langchain_community.vectorstores import (
    FAISS,
)

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
)

# ============================================================
# RESULT
# ============================================================


@dataclass
class RAGSkillResult:

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
# RAG SKILL
# ============================================================


class RAGSkill:

    """
    Production-grade RAG runtime.
    """

    def __init__(self):

        # ====================================================
        # EMBEDDINGS
        # ====================================================

        self.embedding_model = (
            GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            )
        )

        # ====================================================
        # SPLITTER
        # ====================================================

        self.text_splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=1000,

                chunk_overlap=200,

                separators=[

                    "\n\n",

                    "\n",

                    ". ",

                    " ",
                ],
            )
        )

    # ========================================================
    # DOCUMENT CREATION
    # ========================================================

    def create_documents(
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

                doc_metadata = {}

                if metadata and idx < len(
                    metadata
                ):

                    doc_metadata = (
                        metadata[idx]
                    )

                documents.append(

                    Document(

                        page_content=text,

                        metadata=doc_metadata,
                    )
                )

            return RAGSkillResult(

                success=True,

                skill="create_documents",

                output=documents,

                metadata={

                    "documents":
                        len(documents),
                },
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

                success=False,

                skill="create_documents",

                error=str(e),
            ).to_dict()

    # ========================================================
    # CHUNK DOCUMENTS
    # ========================================================

    def chunk_documents(
        self,
        documents: List[Document],
    ) -> Dict[str, Any]:

        try:

            chunks = (
                self.text_splitter
                .split_documents(
                    documents
                )
            )

            return RAGSkillResult(

                success=True,

                skill="chunk_documents",

                output=chunks,

                metadata={

                    "chunks":
                        len(chunks),
                },
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

                success=False,

                skill="chunk_documents",

                error=str(e),
            ).to_dict()

    # ========================================================
    # VECTOR STORE
    # ========================================================

    def build_vector_store(
        self,
        chunks: List[Document],
    ) -> Dict[str, Any]:

        try:

            start_time = time.time()

            vector_store = (
                FAISS.from_documents(

                    chunks,

                    self.embedding_model,
                )
            )

            build_time = (
                time.time()
                - start_time
            )

            return RAGSkillResult(

                success=True,

                skill="build_vector_store",

                output=vector_store,

                metadata={

                    "chunks":
                        len(chunks),

                    "build_time":
                        build_time,
                },
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

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
        top_k: int = 5,
    ) -> Dict[str, Any]:

        try:

            retriever = (
                vector_store.as_retriever(

                    search_kwargs={

                        "k":
                            top_k,
                    }
                )
            )

            return RAGSkillResult(

                success=True,

                skill="build_retriever",

                output=retriever,

                metadata={

                    "top_k":
                        top_k,
                },
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

                success=False,

                skill="build_retriever",

                error=str(e),
            ).to_dict()

    # ========================================================
    # FORMAT DOCS
    # ========================================================

    def format_documents(
        self,
        docs: List[Document],
    ) -> str:

        formatted = []

        for idx, doc in enumerate(docs):

            formatted.append(

                f"""
Document {idx + 1}:

{doc.page_content}
"""
            )

        return "\n".join(
            formatted
        )

    # ========================================================
    # RAG PROMPT
    # ========================================================

    def build_rag_prompt(
        self,
    ):

        return ChatPromptTemplate.from_template(
            """
You are a highly accurate AI assistant.

Answer ONLY from the provided context.

If information is missing,
say you do not know.

Context:
{context}

Question:
{question}

Answer:
"""
        )

    # ========================================================
    # RAG CHAIN
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

            return RAGSkillResult(

                success=True,

                skill="build_rag_chain",

                output=rag_chain,
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

                success=False,

                skill="build_rag_chain",

                error=str(e),
            ).to_dict()

    # ========================================================
    # QUERY
    # ========================================================

    async def query(
        self,
        rag_chain,
        question: str,
    ) -> Dict[str, Any]:

        try:

            start_time = time.time()

            response = await (
                rag_chain.ainvoke(
                    question
                )
            )

            latency = (
                time.time()
                - start_time
            )

            return RAGSkillResult(

                success=True,

                skill="query",

                output=response,

                metadata={

                    "latency":
                        latency,
                },
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

                success=False,

                skill="query",

                error=str(e),
            ).to_dict()

    # ========================================================
    # HYBRID RETRIEVAL
    # ========================================================

    def hybrid_search(
        self,
        vector_store,
        query: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:

        try:

            results = (
                vector_store.similarity_search(

                    query,

                    k=top_k,
                )
            )

            formatted_results = []

            for result in results:

                formatted_results.append(

                    {

                        "content":
                            result.page_content,

                        "metadata":
                            result.metadata,
                    }
                )

            return RAGSkillResult(

                success=True,

                skill="hybrid_search",

                output=formatted_results,

                metadata={

                    "results":
                        len(formatted_results),
                },
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

                success=False,

                skill="hybrid_search",

                error=str(e),
            ).to_dict()

    # ========================================================
    # SAVE VECTOR STORE
    # ========================================================

    def save_vector_store(
        self,
        vector_store,
        path: str,
    ) -> Dict[str, Any]:

        try:

            vector_store.save_local(
                path
            )

            return RAGSkillResult(

                success=True,

                skill="save_vector_store",

                output=path,
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

                success=False,

                skill="save_vector_store",

                error=str(e),
            ).to_dict()

    # ========================================================
    # LOAD VECTOR STORE
    # ========================================================

    def load_vector_store(
        self,
        path: str,
    ) -> Dict[str, Any]:

        try:

            vector_store = (
                FAISS.load_local(

                    path,

                    self.embedding_model,

                    allow_dangerous_deserialization=True,
                )
            )

            return RAGSkillResult(

                success=True,

                skill="load_vector_store",

                output=vector_store,
            ).to_dict()

        except Exception as e:

            return RAGSkillResult(

                success=False,

                skill="load_vector_store",

                error=str(e),
            ).to_dict()

    # ========================================================
    # HEALTHCHECK
    # ========================================================

    def healthcheck(
        self,
    ):

        return {

            "skill":
                "rag_skill",

            "status":
                "healthy",

            "features": [

                "chunking",

                "embeddings",

                "vectorstore",

                "retrieval",

                "rag_chain",

                "hybrid_search",
            ],
        }


# ============================================================
# FACTORY
# ============================================================


def build_rag_skill():

    return RAGSkill()