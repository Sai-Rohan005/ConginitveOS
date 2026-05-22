# domains/aiEngineering/skills/ollama_skill.py

"""
CognitiveOS - Ollama Skill
---------------------------------------------------------

Responsibilities:
- manage local LLM inference
- interact with Ollama runtime
- execute chat completions
- generate embeddings
- manage local models
- support streaming inference
- provide deterministic local AI execution

This becomes:
- local inference layer
- offline AI runtime
- low-cost LLM execution engine
"""

from __future__ import annotations

import json
import time
import traceback
import requests

from typing import (
    Dict,
    Any,
    Optional,
    List,
)

from dataclasses import (
    dataclass,
    field,
)

# ============================================================
# RESULT
# ============================================================


@dataclass
class OllamaSkillResult:

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
# OLLAMA SKILL
# ============================================================


class OllamaSkill:

    """
    Production-grade Ollama runtime skill.
    """

    def __init__(
        self,
        base_url: str = (
            "http://localhost:11434"
        ),
        timeout: int = 300,
    ):

        self.base_url = (
            base_url.rstrip("/")
        )

        self.timeout = timeout

    # ========================================================
    # HEALTHCHECK
    # ========================================================

    def healthcheck(
        self,
    ) -> Dict[str, Any]:

        try:

            response = requests.get(

                f"{self.base_url}/api/tags",

                timeout=10,
            )

            return OllamaSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="healthcheck",

                output=response.json(),
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="healthcheck",

                error=str(e),
            ).to_dict()

    # ========================================================
    # LIST MODELS
    # ========================================================

    def list_models(
        self,
    ) -> Dict[str, Any]:

        try:

            response = requests.get(

                f"{self.base_url}/api/tags",

                timeout=20,
            )

            data = response.json()

            models = data.get(
                "models",
                [],
            )

            return OllamaSkillResult(

                success=True,

                skill="list_models",

                output=models,

                metadata={

                    "count":
                        len(models),
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="list_models",

                error=str(e),
            ).to_dict()

    # ========================================================
    # PULL MODEL
    # ========================================================

    def pull_model(
        self,
        model: str,
    ) -> Dict[str, Any]:

        try:

            response = requests.post(

                f"{self.base_url}/api/pull",

                json={

                    "name":
                        model,
                },

                timeout=self.timeout,
            )

            return OllamaSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="pull_model",

                output=response.json(),

                metadata={

                    "model":
                        model,
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="pull_model",

                error=str(e),
            ).to_dict()

    # ========================================================
    # DELETE MODEL
    # ========================================================

    def delete_model(
        self,
        model: str,
    ) -> Dict[str, Any]:

        try:

            response = requests.delete(

                f"{self.base_url}/api/delete",

                json={

                    "name":
                        model,
                },

                timeout=30,
            )

            return OllamaSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="delete_model",

                output=response.json(),

                metadata={

                    "model":
                        model,
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="delete_model",

                error=str(e),
            ).to_dict()

    # ========================================================
    # GENERATE
    # ========================================================

    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.2,
        stream: bool = False,
    ) -> Dict[str, Any]:

        try:

            payload = {

                "model":
                    model,

                "prompt":
                    prompt,

                "stream":
                    stream,

                "options": {

                    "temperature":
                        temperature,
                },
            }

            if system:

                payload["system"] = (
                    system
                )

            start_time = time.time()

            response = requests.post(

                f"{self.base_url}/api/generate",

                json=payload,

                timeout=self.timeout,
            )

            latency = (
                time.time()
                - start_time
            )

            data = response.json()

            return OllamaSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="generate",

                output=data,

                metadata={

                    "model":
                        model,

                    "latency":
                        latency,
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="generate",

                error=str(e),
            ).to_dict()

    # ========================================================
    # CHAT
    # ========================================================

    def chat(
        self,
        model: str,
        messages: List[
            Dict[str, str]
        ],
        temperature: float = 0.2,
        stream: bool = False,
    ) -> Dict[str, Any]:

        try:

            payload = {

                "model":
                    model,

                "messages":
                    messages,

                "stream":
                    stream,

                "options": {

                    "temperature":
                        temperature,
                },
            }

            start_time = time.time()

            response = requests.post(

                f"{self.base_url}/api/chat",

                json=payload,

                timeout=self.timeout,
            )

            latency = (
                time.time()
                - start_time
            )

            data = response.json()

            return OllamaSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="chat",

                output=data,

                metadata={

                    "model":
                        model,

                    "latency":
                        latency,
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="chat",

                error=str(e),
            ).to_dict()

    # ========================================================
    # EMBEDDINGS
    # ========================================================

    def embeddings(
        self,
        model: str,
        prompt: str,
    ) -> Dict[str, Any]:

        try:

            response = requests.post(

                f"{self.base_url}/api/embeddings",

                json={

                    "model":
                        model,

                    "prompt":
                        prompt,
                },

                timeout=self.timeout,
            )

            data = response.json()

            embedding = data.get(
                "embedding",
                [],
            )

            return OllamaSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="embeddings",

                output=embedding,

                metadata={

                    "embedding_size":
                        len(embedding),

                    "model":
                        model,
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="embeddings",

                error=str(e),
            ).to_dict()

    # ========================================================
    # SIMPLE RAG QUERY
    # ========================================================

    def rag_query(
        self,
        model: str,
        query: str,
        context: str,
    ) -> Dict[str, Any]:

        try:

            prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{query}

Answer using ONLY the provided context.
"""

            result = self.generate(

                model=model,

                prompt=prompt,
            )

            return OllamaSkillResult(

                success=result["success"],

                skill="rag_query",

                output=result,

                metadata={

                    "model":
                        model,
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="rag_query",

                error=str(e),
            ).to_dict()

    # ========================================================
    # MODEL INFO
    # ========================================================

    def model_info(
        self,
        model: str,
    ) -> Dict[str, Any]:

        try:

            response = requests.post(

                f"{self.base_url}/api/show",

                json={

                    "name":
                        model,
                },

                timeout=30,
            )

            return OllamaSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="model_info",

                output=response.json(),

                metadata={

                    "model":
                        model,
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="model_info",

                error=str(e),
            ).to_dict()

    # ========================================================
    # BENCHMARK
    # ========================================================

    def benchmark(
        self,
        model: str,
        prompt: str = (
            "Explain distributed systems."
        ),
    ) -> Dict[str, Any]:

        try:

            start = time.time()

            result = self.generate(

                model=model,

                prompt=prompt,
            )

            total_time = (
                time.time()
                - start
            )

            return OllamaSkillResult(

                success=result["success"],

                skill="benchmark",

                output=result,

                metadata={

                    "model":
                        model,

                    "execution_time":
                        total_time,
                },
            ).to_dict()

        except Exception as e:

            return OllamaSkillResult(

                success=False,

                skill="benchmark",

                error=str(e),
            ).to_dict()

    # ========================================================
    # EXPORT CONFIG
    # ========================================================

    def export_config(
        self,
    ) -> Dict[str, Any]:

        return {

            "skill":
                "ollama_skill",

            "base_url":
                self.base_url,

            "timeout":
                self.timeout,

            "features": [

                "chat",

                "generate",

                "embeddings",

                "rag",

                "benchmarking",

                "model_management",
            ],
        }


# ============================================================
# FACTORY
# ============================================================


def build_ollama_skill():

    return OllamaSkill()