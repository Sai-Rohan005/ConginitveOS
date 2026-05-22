# domains/aiEngineering/agents/inference_agent.py

"""
CognitiveOS - Inference Agent
---------------------------------------------------------

Responsibilities:
- design AI inference systems
- build scalable inference APIs
- optimize LLM serving
- optimize GPU inference
- generate multimodal inference pipelines
- build batching systems
- optimize latency and throughput
- create production-grade deployment systems

This agent behaves like:
- AI Inference Engineer
- LLM Infrastructure Engineer
- GPU Systems Engineer
- ML Platform Engineer
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
class InferenceAgentState:

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
# INFERENCE AGENT
# ============================================================


class InferenceAgent:

    """
    Production-grade inference systems agent.
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

            inference_architecture = result.get(
                "inference_architecture",
                "distributed_inference",
            )

            serving_framework = result.get(
                "serving_framework",
                "vLLM",
            )

            model_runtime = result.get(
                "model_runtime",
                {},
            )

            batching_strategy = result.get(
                "batching_strategy",
                {},
            )

            caching_strategy = result.get(
                "caching_strategy",
                {},
            )

            hardware_optimization = result.get(
                "hardware_optimization",
                {},
            )

            scalability_features = result.get(
                "scalability_features",
                [],
            )

            multimodal_support = result.get(
                "multimodal_support",
                {},
            )

            observability = result.get(
                "observability",
                [],
            )

            deployment_strategy = result.get(
                "deployment_strategy",
                {},
            )

            latency_optimization = result.get(
                "latency_optimization",
                [],
            )

            throughput_optimization = result.get(
                "throughput_optimization",
                [],
            )

            generated_components = result.get(
                "generated_components",
                [],
            )

            api_design = result.get(
                "api_design",
                [],
            )

            security_features = result.get(
                "security_features",
                [],
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "inference_agent",

                "inference_architecture":
                    inference_architecture,

                "serving_framework":
                    serving_framework,

                "model_runtime":
                    model_runtime,

                "batching_strategy":
                    batching_strategy,

                "caching_strategy":
                    caching_strategy,

                "hardware_optimization":
                    hardware_optimization,

                "scalability_features":
                    scalability_features,

                "multimodal_support":
                    multimodal_support,

                "observability":
                    observability,

                "deployment_strategy":
                    deployment_strategy,

                "latency_optimization":
                    latency_optimization,

                "throughput_optimization":
                    throughput_optimization,

                "generated_components":
                    generated_components,

                "api_design":
                    api_design,

                "security_features":
                    security_features,

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
                    "inference_agent",

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
You are the Inference Agent for CognitiveOS.

Your role is to:
- design scalable AI inference systems
- optimize GPU inference
- build low-latency inference APIs
- optimize throughput and batching
- design multimodal serving systems
- build production-grade AI infrastructure
- optimize model deployment
- support distributed inference

You think like:
- AI Infrastructure Engineer
- LLM Serving Engineer
- GPU Systems Engineer
- ML Platform Architect

Focus on:
- latency optimization
- throughput optimization
- GPU efficiency
- autoscaling
- observability
- fault tolerance
- production-readiness
- distributed inference

You MUST:
- design REAL inference systems
- avoid toy architectures
- optimize GPU utilization
- support distributed serving
- include observability and monitoring
- include autoscaling and caching

Return ONLY valid JSON.

JSON FORMAT:

{{
  "inference_architecture":
    "distributed_llm_serving",

  "serving_framework":
    "vLLM",

  "model_runtime": {{

    "primary_runtime":
      "TensorRT-LLM",

    "fallback_runtime":
      "Transformers",

    "quantization":
      "4-bit"
  }},

  "batching_strategy": {{

    "dynamic_batching":
      true,

    "max_batch_size":
      64,

    "queue_timeout_ms":
      50
  }},

  "caching_strategy": {{

    "kv_cache":
      true,

    "response_cache":
      true,

    "semantic_cache":
      true
  }},

  "hardware_optimization": {{

    "gpu":
      "A100",

    "multi_gpu":
      true,

    "gpu_parallelism":
      "tensor_parallelism"
  }},

  "scalability_features": [

    "horizontal autoscaling",

    "multi-node inference",

    "load balancing",

    "distributed batching"
  ],

  "multimodal_support": {{

    "image":
      true,

    "audio":
      true,

    "video":
      false
  }},

  "observability": [

    "Prometheus metrics",

    "GPU telemetry",

    "OpenTelemetry tracing",

    "latency analytics"
  ],

  "deployment_strategy": {{

    "containerization":
      "Docker",

    "orchestration":
      "Kubernetes",

    "autoscaling":
      true
  }},

  "latency_optimization": [

    "tensor parallelism",

    "quantization",

    "continuous batching",

    "GPU pinning"
  ],

  "throughput_optimization": [

    "async inference",

    "request batching",

    "multi-instance serving",

    "cache reuse"
  ],

  "generated_components": [

    "inference_gateway",

    "gpu_scheduler",

    "batch_manager",

    "cache_manager",

    "autoscaling_controller"
  ],

  "api_design": [

    {{

      "endpoint":
        "/api/v1/generate",

      "method":
        "POST",

      "purpose":
        "LLM text generation"
    }},

    {{

      "endpoint":
        "/api/v1/embeddings",

      "method":
        "POST",

      "purpose":
        "Embedding generation"
    }}
  ],

  "security_features": [

    "API authentication",

    "rate limiting",

    "tenant isolation",

    "request validation"
  ],

  "reasoning":
    "vLLM with TensorRT selected for scalable low-latency inference."
}}
"""