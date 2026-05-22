# domains/dataScience/agents/eda_agent.py

"""
CognitiveOS - Exploratory Data Analysis Agent
---------------------------------------------------------

Responsibilities:
- analyze datasets
- generate statistical summaries
- detect anomalies
- identify correlations
- assess data quality
- detect missing values
- recommend preprocessing
- generate insights for ML pipelines

This agent behaves like:
- Senior Data Scientist
- ML Analyst
- Analytics Engineer
- Statistical Researcher
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
class EDAAgentState:

    query: str

    task: str

    dataset_metadata: Dict[
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
# EDA AGENT
# ============================================================


class EDAAgent:

    """
    Production-grade Exploratory Data Analysis agent.
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

            dataset_summary = result.get(
                "dataset_summary",
                {},
            )

            statistical_analysis = result.get(
                "statistical_analysis",
                {},
            )

            missing_value_analysis = result.get(
                "missing_value_analysis",
                {},
            )

            correlation_analysis = result.get(
                "correlation_analysis",
                {},
            )

            anomaly_detection = result.get(
                "anomaly_detection",
                {},
            )

            feature_distributions = result.get(
                "feature_distributions",
                [],
            )

            class_imbalance = result.get(
                "class_imbalance",
                {},
            )

            feature_importance_candidates = result.get(
                "feature_importance_candidates",
                [],
            )

            preprocessing_recommendations = result.get(
                "preprocessing_recommendations",
                [],
            )

            visualization_recommendations = result.get(
                "visualization_recommendations",
                [],
            )

            ml_readiness = result.get(
                "ml_readiness",
                {},
            )

            data_quality_score = result.get(
                "data_quality_score",
                0.0,
            )

            risks = result.get(
                "risks",
                [],
            )

            insights = result.get(
                "insights",
                [],
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "eda_agent",

                "dataset_summary":
                    dataset_summary,

                "statistical_analysis":
                    statistical_analysis,

                "missing_value_analysis":
                    missing_value_analysis,

                "correlation_analysis":
                    correlation_analysis,

                "anomaly_detection":
                    anomaly_detection,

                "feature_distributions":
                    feature_distributions,

                "class_imbalance":
                    class_imbalance,

                "feature_importance_candidates":
                    feature_importance_candidates,

                "preprocessing_recommendations":
                    preprocessing_recommendations,

                "visualization_recommendations":
                    visualization_recommendations,

                "ml_readiness":
                    ml_readiness,

                "data_quality_score":
                    data_quality_score,

                "risks":
                    risks,

                "insights":
                    insights,

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
                    "eda_agent",

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
You are the Exploratory Data Analysis Agent
for CognitiveOS.

Your role is to:
- analyze datasets
- generate statistical insights
- detect anomalies
- assess data quality
- identify correlations
- recommend preprocessing
- assess ML readiness
- identify risks and biases

You think like:
- Senior Data Scientist
- Analytics Engineer
- ML Researcher
- Statistical Analyst

Focus on:
- missing values
- feature distributions
- outlier detection
- skewness
- multicollinearity
- class imbalance
- feature quality
- ML suitability

You MUST:
- generate REALISTIC insights
- assess production ML readiness
- identify data quality risks
- recommend preprocessing strategies
- detect potential bias issues
- prioritize statistical correctness

Return ONLY valid JSON.

JSON FORMAT:

{{
  "dataset_summary": {{

    "rows":
      120000,

    "columns":
      48,

    "target_column":
      "fraud",

    "dataset_type":
      "classification"
  }},

  "statistical_analysis": {{

    "numeric_features":
      32,

    "categorical_features":
      10,

    "datetime_features":
      6
  }},

  "missing_value_analysis": {{

    "missing_columns":
      [
        "salary",
        "credit_score"
      ],

    "overall_missing_percentage":
      4.2
  }},

  "correlation_analysis": {{

    "highly_correlated_features":
      [
        ["income", "salary"]
      ],

    "multicollinearity_risk":
      "medium"
  }},

  "anomaly_detection": {{

    "outlier_columns":
      [
        "transaction_amount"
      ],

    "outlier_percentage":
      2.3
  }},

  "feature_distributions": [

    "normal",

    "right_skewed",

    "bimodal"
  ],

  "class_imbalance": {{

    "imbalanced":
      true,

    "minority_class_percentage":
      8.5
  }},

  "feature_importance_candidates": [

    "transaction_amount",

    "device_id",

    "location"
  ],

  "preprocessing_recommendations": [

    "standard scaling",

    "missing value imputation",

    "SMOTE balancing"
  ],

  "visualization_recommendations": [

    "correlation heatmap",

    "boxplots",

    "distribution histograms"
  ],

  "ml_readiness": {{

    "ready":
      true,

    "recommended_models":
      [
        "XGBoost",
        "LightGBM"
      ]
  }},

  "data_quality_score":
    8.4,

  "risks": [

    "class imbalance",

    "multicollinearity"
  ],

  "insights": [

    "transaction amount strongly influences fraud detection",

    "missing salary values may introduce bias"
  ],

  "reasoning":
    "Dataset is mostly production-ready after preprocessing and balancing."
}}
"""