# domains/dataScience/agents/feature_engineering_agent.py

"""
CognitiveOS - Feature Engineering Agent
---------------------------------------------------------

Responsibilities:
- design feature engineering pipelines
- create ML-ready features
- detect feature leakage
- optimize feature selection
- engineer temporal/statistical features
- generate encoding strategies
- improve model performance
- reduce dimensionality

This agent behaves like:
- Senior ML Engineer
- Feature Engineering Specialist
- Applied Data Scientist
- ML Research Engineer
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
class FeatureEngineeringAgentState:

    query: str

    task: str

    dataset_metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    eda_context: Dict[
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
# FEATURE ENGINEERING AGENT
# ============================================================


class FeatureEngineeringAgent:

    """
    Production-grade Feature Engineering agent.
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

EDA Context:
{eda_context}

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

                        "eda_context":
                            str(
                                context.get(
                                    "eda_context",
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

            feature_strategy = result.get(
                "feature_strategy",
                {},
            )

            generated_features = result.get(
                "generated_features",
                [],
            )

            categorical_encoding = result.get(
                "categorical_encoding",
                {},
            )

            scaling_strategy = result.get(
                "scaling_strategy",
                {},
            )

            missing_value_strategy = result.get(
                "missing_value_strategy",
                {},
            )

            dimensionality_reduction = result.get(
                "dimensionality_reduction",
                {},
            )

            feature_selection = result.get(
                "feature_selection",
                {},
            )

            leakage_analysis = result.get(
                "leakage_analysis",
                {},
            )

            temporal_features = result.get(
                "temporal_features",
                [],
            )

            aggregation_features = result.get(
                "aggregation_features",
                [],
            )

            interaction_features = result.get(
                "interaction_features",
                [],
            )

            feature_importance_estimation = result.get(
                "feature_importance_estimation",
                [],
            )

            preprocessing_pipeline = result.get(
                "preprocessing_pipeline",
                [],
            )

            optimization_recommendations = result.get(
                "optimization_recommendations",
                [],
            )

            ml_impact = result.get(
                "ml_impact",
                {},
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            engineering_score = result.get(
                "engineering_score",
                0.0,
            )

            risks = result.get(
                "risks",
                [],
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "feature_engineering_agent",

                "feature_strategy":
                    feature_strategy,

                "generated_features":
                    generated_features,

                "categorical_encoding":
                    categorical_encoding,

                "scaling_strategy":
                    scaling_strategy,

                "missing_value_strategy":
                    missing_value_strategy,

                "dimensionality_reduction":
                    dimensionality_reduction,

                "feature_selection":
                    feature_selection,

                "leakage_analysis":
                    leakage_analysis,

                "temporal_features":
                    temporal_features,

                "aggregation_features":
                    aggregation_features,

                "interaction_features":
                    interaction_features,

                "feature_importance_estimation":
                    feature_importance_estimation,

                "preprocessing_pipeline":
                    preprocessing_pipeline,

                "optimization_recommendations":
                    optimization_recommendations,

                "ml_impact":
                    ml_impact,

                "production_readiness":
                    production_readiness,

                "engineering_score":
                    engineering_score,

                "risks":
                    risks,

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
                    "feature_engineering_agent",

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
You are the Feature Engineering Agent
for CognitiveOS.

Your role is to:
- engineer ML-ready features
- improve model performance
- detect feature leakage
- optimize preprocessing
- reduce dimensionality
- design feature pipelines
- recommend encoding/scaling strategies
- improve feature quality

You think like:
- Senior ML Engineer
- Applied Data Scientist
- Feature Engineering Specialist
- ML Research Engineer

Focus on:
- categorical encoding
- feature interactions
- temporal features
- aggregation features
- leakage prevention
- feature selection
- scaling normalization
- dimensionality reduction

You MUST:
- generate REALISTIC feature strategies
- prevent target leakage
- optimize model generalization
- recommend scalable preprocessing
- assess production ML readiness
- prioritize model performance gains

Return ONLY valid JSON.

JSON FORMAT:

{{
  "feature_strategy": {{

    "objective":
      "fraud detection optimization",

    "pipeline_type":
      "supervised ML",

    "feature_count_target":
      120
  }},

  "generated_features": [

    "transaction_velocity",

    "rolling_avg_spend",

    "device_risk_score",

    "location_frequency"
  ],

  "categorical_encoding": {{

    "high_cardinality":
      "target encoding",

    "low_cardinality":
      "one-hot encoding"
  }},

  "scaling_strategy": {{

    "numeric_features":
      "standard scaler",

    "outlier_sensitive":
      "robust scaler"
  }},

  "missing_value_strategy": {{

    "numeric":
      "median imputation",

    "categorical":
      "most frequent"
  }},

  "dimensionality_reduction": {{

    "recommended":
      true,

    "method":
      "PCA",

    "target_dimensions":
      40
  }},

  "feature_selection": {{

    "method":
      "mutual information",

    "selected_features":
      60
  }},

  "leakage_analysis": {{

    "leakage_detected":
      false,

    "risk_level":
      "low"
  }},

  "temporal_features": [

    "hour_of_day",

    "day_of_week",

    "rolling_transaction_count"
  ],

  "aggregation_features": [

    "customer_avg_spend",

    "merchant_risk_score"
  ],

  "interaction_features": [

    "device_x_location",

    "amount_x_frequency"
  ],

  "feature_importance_estimation": [

    "transaction_amount",

    "device_id",

    "velocity_score"
  ],

  "preprocessing_pipeline": [

    "imputation",

    "encoding",

    "scaling",

    "feature selection"
  ],

  "optimization_recommendations": [

    "remove multicollinearity",

    "reduce sparse features",

    "apply robust scaling"
  ],

  "ml_impact": {{

    "expected_accuracy_gain":
      "8-12%",

    "training_efficiency":
      "improved"
  }},

  "production_readiness":
    "high",

  "engineering_score":
    8.9,

  "risks": [

    "high cardinality explosion",

    "potential overfitting"
  ],

  "reasoning":
    "Feature engineering pipeline improves model robustness and reduces noise."
}}
"""