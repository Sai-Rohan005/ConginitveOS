# domains/aiEngineering/skills/vllm_skill.py

"""
CognitiveOS - vLLM Skill
---------------------------------------------------------

Responsibilities:
- manage vLLM inference runtime
- execute high-throughput inference
- support streaming generation
- optimize GPU inference
- manage batching
- provide OpenAI-compatible APIs
- benchmark inference performance

This becomes:
- production inference runtime
- scalable LLM serving layer
- GPU inference abstraction
"""

from __future__ import annotations

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
class VLLMSkillResult:

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
# VLLM SKILL
# ============================================================


class VLLMSkill:

    """
    Production-grade vLLM runtime skill.
    """

    def __init__(
        self,
        base_url: str = (
            "http://localhost:8000"
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

                f"{self.base_url}/health",

                timeout=10,
            )

            return VLLMSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="healthcheck",

                output=response.text,
            ).to_dict()

        except Exception as e:

            return VLLMSkillResult(

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

                f"{self.base_url}/v1/models",

                timeout=20,
            )

            data = response.json()

            return VLLMSkillResult(

                success=True,

                skill="list_models",

                output=data,
            ).to_dict()

        except Exception as e:

            return VLLMSkillResult(

                success=False,

                skill="list_models",

                error=str(e),
            ).to_dict()

    # ========================================================
    # CHAT COMPLETION
    # ========================================================

    def chat_completion(
        self,
        model: str,
        messages: List[
            Dict[str, str]
        ],
        temperature: float = 0.2,
        max_tokens: int = 1024,
        stream: bool = False,
    ) -> Dict[str, Any]:

        try:

            payload = {

                "model":
                    model,

                "messages":
                    messages,

                "temperature":
                    temperature,

                "max_tokens":
                    max_tokens,

                "stream":
                    stream,
            }

            start_time = time.time()

            response = requests.post(

                f"{self.base_url}/v1/chat/completions",

                json=payload,

                timeout=self.timeout,
            )

            latency = (
                time.time()
                - start_time
            )

            data = response.json()

            return VLLMSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="chat_completion",

                output=data,

                metadata={

                    "latency":
                        latency,

                    "model":
                        model,
                },
            ).to_dict()

        except Exception as e:

            return VLLMSkillResult(

                success=False,

                skill="chat_completion",

                error=str(e),
            ).to_dict()

    # ========================================================
    # TEXT GENERATION
    # ========================================================

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:

        try:

            payload = {

                "model":
                    model,

                "prompt":
                    prompt,

                "temperature":
                    temperature,

                "max_tokens":
                    max_tokens,
            }

            start_time = time.time()

            response = requests.post(

                f"{self.base_url}/v1/completions",

                json=payload,

                timeout=self.timeout,
            )

            latency = (
                time.time()
                - start_time
            )

            data = response.json()

            return VLLMSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="generate",

                output=data,

                metadata={

                    "latency":
                        latency,

                    "model":
                        model,
                },
            ).to_dict()

        except Exception as e:

            return VLLMSkillResult(

                success=False,

                skill="generate",

                error=str(e),
            ).to_dict()

    # ========================================================
    # EMBEDDINGS
    # ========================================================

    def embeddings(
        self,
        model: str,
        text: str,
    ) -> Dict[str, Any]:

        try:

            payload = {

                "model":
                    model,

                "input":
                    text,
            }

            response = requests.post(

                f"{self.base_url}/v1/embeddings",

                json=payload,

                timeout=self.timeout,
            )

            data = response.json()

            return VLLMSkillResult(

                success=(
                    response.status_code == 200
                ),

                skill="embeddings",

                output=data,
            ).to_dict()

        except Exception as e:

            return VLLMSkillResult(

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
You are a grounded AI assistant.

Use ONLY the provided context.

Context:
{context}

Question:
{query}

Answer:
"""

            return self.generate(

                model=model,

                prompt=prompt,
            )

        except Exception as e:

            return VLLMSkillResult(

                success=False,

                skill="rag_query",

                error=str(e),
            ).to_dict()

    # ========================================================
    # BENCHMARK
    # ========================================================

    def benchmark(
        self,
        model: str,
        iterations: int = 3,
    ) -> Dict[str, Any]:

        try:

            latencies = []

            for _ in range(iterations):

                start = time.time()

                self.generate(

                    model=model,

                    prompt=(
                        "Explain distributed "
                        "systems."
                    ),
                )

                latency = (
                    time.time()
                    - start
                )

                latencies.append(
                    latency
                )

            avg_latency = (

                sum(latencies)

                / len(latencies)
            )

            return VLLMSkillResult(

                success=True,

                skill="benchmark",

                output={

                    "latencies":
                        latencies,

                    "average_latency":
                        avg_latency,
                },

                metadata={

                    "iterations":
                        iterations,
                },
            ).to_dict()

        except Exception as e:

            return VLLMSkillResult(

                success=False,

                skill="benchmark",

                error=str(e),
            ).to_dict()

    # ========================================================
    # STREAMING CHAT
    # ========================================================

    def streaming_chat(
        self,
        model: str,
        messages: List[
            Dict[str, str]
        ],
    ):

        try:

            payload = {

                "model":
                    model,

                "messages":
                    messages,

                "stream":
                    True,
            }

            response = requests.post(

                f"{self.base_url}/v1/chat/completions",

                json=payload,

                stream=True,

                timeout=self.timeout,
            )

            for line in (
                response.iter_lines()
            ):

                if line:

                    yield line.decode(
                        "utf-8"
                    )

        except Exception as e:

            yield str(e)

    # ========================================================
    # SERVER INFO
    # ========================================================

    def server_info(
        self,
    ) -> Dict[str, Any]:

        return {

            "skill":
                "vllm_skill",

            "base_url":
                self.base_url,

            "features": [

                "chat_completion",

                "text_generation",

                "embeddings",

                "rag",

                "streaming",

                "benchmarking",
            ],
        }


# ============================================================
# FACTORY
# ============================================================


def build_vllm_skill():

    return VLLMSkill()