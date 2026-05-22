# domains/aiEngineering/agents/training_agent.py

"""
CognitiveOS - Training Agent
---------------------------------------------------------

Responsibilities:
- generate training pipelines
- generate fine-tuning systems
- generate distributed training setups
- build multimodal training workflows
- optimize training performance
- generate evaluation pipelines
- create production-grade ML workflows

This agent behaves like:
- Senior ML Engineer
- Deep Learning Engineer
- Training Infrastructure Engineer
- AI Research Engineer
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
class TrainingAgentState:

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
# TRAINING AGENT
# ============================================================


class TrainingAgent:

    """
    Production-grade AI training agent.
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

            training_type = result.get(
                "training_type",
                "fine_tuning",
            )

            framework = result.get(
                "framework",
                "PyTorch",
            )

            model_architecture = result.get(
                "model_architecture",
                "",
            )

            dataset_strategy = result.get(
                "dataset_strategy",
                {},
            )

            preprocessing_pipeline = result.get(
                "preprocessing_pipeline",
                [],
            )

            training_pipeline = result.get(
                "training_pipeline",
                [],
            )

            distributed_training = result.get(
                "distributed_training",
                {},
            )

            optimization_strategy = result.get(
                "optimization_strategy",
                {},
            )

            evaluation_pipeline = result.get(
                "evaluation_pipeline",
                [],
            )

            monitoring = result.get(
                "monitoring",
                [],
            )

            deployment_strategy = result.get(
                "deployment_strategy",
                {},
            )

            hardware_requirements = result.get(
                "hardware_requirements",
                {},
            )

            scalability_features = result.get(
                "scalability_features",
                [],
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "training_agent",

                "training_type":
                    training_type,

                "framework":
                    framework,

                "model_architecture":
                    model_architecture,

                "dataset_strategy":
                    dataset_strategy,

                "preprocessing_pipeline":
                    preprocessing_pipeline,

                "training_pipeline":
                    training_pipeline,

                "distributed_training":
                    distributed_training,

                "optimization_strategy":
                    optimization_strategy,

                "evaluation_pipeline":
                    evaluation_pipeline,

                "monitoring":
                    monitoring,

                "deployment_strategy":
                    deployment_strategy,

                "hardware_requirements":
                    hardware_requirements,

                "scalability_features":
                    scalability_features,

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
                    "training_agent",

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
You are the Training Agent for CognitiveOS.

Your role is to:
- design training pipelines
- build fine-tuning systems
- optimize distributed training
- design evaluation workflows
- create scalable ML training architectures
- optimize GPU utilization
- improve model performance
- generate production-grade AI workflows

You think like:
- Senior ML Engineer
- Deep Learning Engineer
- Distributed Training Engineer
- AI Infrastructure Architect

Focus on:
- scalability
- GPU efficiency
- training stability
- reproducibility
- evaluation quality
- fault tolerance
- distributed training
- production-readiness

You MUST:
- design REAL training systems
- avoid toy implementations
- optimize for performance
- include monitoring and evaluation
- include distributed training if required
- include deployment strategy

Return ONLY valid JSON.

JSON FORMAT:

{{
  "training_type":
    "llm_fine_tuning",

  "framework":
    "PyTorch",

  "model_architecture":
    "Llama-3-8B",

  "dataset_strategy": {{

    "dataset_type":
      "instruction_tuning",

    "data_format":
      "jsonl",

    "augmentation":
      true
  }},

  "preprocessing_pipeline": [

    "tokenization",

    "data cleaning",

    "deduplication",

    "dynamic batching"
  ],

  "training_pipeline": [

    "mixed precision training",

    "gradient checkpointing",

    "distributed dataloading",

    "periodic checkpointing"
  ],

  "distributed_training": {{

    "strategy":
      "DeepSpeed ZeRO-3",

    "multi_gpu":
      true,

    "nodes":
      4
  }},

  "optimization_strategy": {{

    "optimizer":
      "AdamW",

    "scheduler":
      "cosine decay",

    "learning_rate":
      "2e-5"
  }},

  "evaluation_pipeline": [

    "validation perplexity",

    "BLEU evaluation",

    "hallucination scoring",

    "human evaluation"
  ],

  "monitoring": [

    "Weights & Biases",

    "GPU telemetry",

    "training metrics",

    "loss tracking"
  ],

  "deployment_strategy": {{

    "serving":
      "vLLM",

    "containerization":
      "Docker",

    "orchestration":
      "Kubernetes"
  }},

  "hardware_requirements": {{

    "gpu":
      "A100 80GB",

    "gpu_count":
      8,

    "storage":
      "2TB NVMe"
  }},

  "scalability_features": [

    "distributed training",

    "fault-tolerant checkpoints",

    "elastic scaling",

    "gradient accumulation"
  ],

  "reasoning":
    "DeepSpeed selected for efficient large-scale fine-tuning."
}}
"""