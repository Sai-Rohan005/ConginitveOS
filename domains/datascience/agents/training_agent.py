# domains/dataScience/agents/training_agent.py

"""
CognitiveOS - Model Training Agent
---------------------------------------------------------

Responsibilities:
- design ML training pipelines
- select optimal models
- optimize hyperparameters
- configure distributed training
- evaluate training strategies
- prevent overfitting
- optimize GPU utilization
- generate production-ready training plans

This agent behaves like:
- Senior ML Engineer
- Deep Learning Engineer
- AI Research Engineer
- Distributed Training Specialist
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

    dataset_metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    feature_context: Dict[
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
# TRAINING AGENT
# ============================================================


class TrainingAgent:

    """
    Production-grade ML Training Agent.
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

Dataset Metadata:
{dataset_metadata}

Feature Context:
{feature_context}

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

                        "dataset_metadata":
                            str(
                                context.get(
                                    "dataset_metadata",
                                    {},
                                )
                            ),

                        "feature_context":
                            str(
                                context.get(
                                    "feature_context",
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

            training_strategy = result.get(
                "training_strategy",
                {},
            )

            selected_models = result.get(
                "selected_models",
                [],
            )

            hyperparameter_strategy = result.get(
                "hyperparameter_strategy",
                {},
            )

            data_split_strategy = result.get(
                "data_split_strategy",
                {},
            )

            distributed_training = result.get(
                "distributed_training",
                {},
            )

            gpu_optimization = result.get(
                "gpu_optimization",
                {},
            )

            regularization_strategy = result.get(
                "regularization_strategy",
                {},
            )

            augmentation_strategy = result.get(
                "augmentation_strategy",
                {},
            )

            early_stopping = result.get(
                "early_stopping",
                {},
            )

            evaluation_metrics = result.get(
                "evaluation_metrics",
                [],
            )

            cross_validation = result.get(
                "cross_validation",
                {},
            )

            experiment_tracking = result.get(
                "experiment_tracking",
                {},
            )

            model_serving_strategy = result.get(
                "model_serving_strategy",
                {},
            )

            expected_performance = result.get(
                "expected_performance",
                {},
            )

            bottlenecks = result.get(
                "bottlenecks",
                [],
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            training_score = result.get(
                "training_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "training_agent",

                "training_strategy":
                    training_strategy,

                "selected_models":
                    selected_models,

                "hyperparameter_strategy":
                    hyperparameter_strategy,

                "data_split_strategy":
                    data_split_strategy,

                "distributed_training":
                    distributed_training,

                "gpu_optimization":
                    gpu_optimization,

                "regularization_strategy":
                    regularization_strategy,

                "augmentation_strategy":
                    augmentation_strategy,

                "early_stopping":
                    early_stopping,

                "evaluation_metrics":
                    evaluation_metrics,

                "cross_validation":
                    cross_validation,

                "experiment_tracking":
                    experiment_tracking,

                "model_serving_strategy":
                    model_serving_strategy,

                "expected_performance":
                    expected_performance,

                "bottlenecks":
                    bottlenecks,

                "optimization_recommendations":
                    optimization_recommendations,

                "production_readiness":
                    production_readiness,

                "training_score":
                    training_score,

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
You are the Model Training Agent
for CognitiveOS.

Your role is to:
- design ML training pipelines
- optimize model selection
- configure distributed training
- tune hyperparameters
- improve model generalization
- optimize GPU utilization
- prevent overfitting
- maximize production performance

You think like:
- Senior ML Engineer
- AI Research Engineer
- Deep Learning Specialist
- Distributed Systems Engineer

Focus on:
- model architecture
- distributed training
- GPU efficiency
- hyperparameter optimization
- regularization
- generalization
- inference optimization
- scalability

You MUST:
- recommend REALISTIC models
- optimize training efficiency
- minimize overfitting
- improve production readiness
- optimize inference performance
- recommend scalable pipelines

Return ONLY valid JSON.

JSON FORMAT:

{{
  "training_strategy": {{

    "problem_type":
      "classification",

    "training_type":
      "supervised learning",

    "pipeline":
      "distributed GPU training"
  }},

  "selected_models": [

    "XGBoost",

    "LightGBM",

    "TabTransformer"
  ],

  "hyperparameter_strategy": {{

    "search_method":
      "Bayesian Optimization",

    "max_trials":
      50
  }},

  "data_split_strategy": {{

    "train":
      0.7,

    "validation":
      0.15,

    "test":
      0.15
  }},

  "distributed_training": {{

    "enabled":
      true,

    "framework":
      "DDP",

    "multi_gpu":
      true
  }},

  "gpu_optimization": {{

    "mixed_precision":
      true,

    "gradient_accumulation":
      true
  }},

  "regularization_strategy": {{

    "dropout":
      0.3,

    "weight_decay":
      0.0001
  }},

  "augmentation_strategy": {{

    "enabled":
      true,

    "methods":
      [
        "SMOTE",
        "noise injection"
      ]
  }},

  "early_stopping": {{

    "enabled":
      true,

    "patience":
      10
  }},

  "evaluation_metrics": [

    "accuracy",

    "f1-score",

    "roc_auc"
  ],

  "cross_validation": {{

    "enabled":
      true,

    "folds":
      5
  }},

  "experiment_tracking": {{

    "tool":
      "MLflow",

    "logging":
      true
  }},

  "model_serving_strategy": {{

    "framework":
      "FastAPI",

    "inference":
      "batched"
  }},

  "expected_performance": {{

    "accuracy":
      "92-95%",

    "latency":
      "<100ms"
  }},

  "bottlenecks": [

    "GPU memory limits",

    "class imbalance"
  ],

  "optimization_recommendations": [

    "enable AMP",

    "reduce feature sparsity",

    "optimize batch size"
  ],

  "production_readiness":
    "high",

  "training_score":
    9.1,

  "reasoning":
    "Distributed GPU training with optimized feature engineering improves scalability and performance."
}}
"""