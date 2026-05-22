# domains/dataScience/agents/visualization_agent.py

"""
CognitiveOS - Visualization Agent
---------------------------------------------------------

Responsibilities:
- design analytical visualizations
- recommend dashboards
- create chart strategies
- optimize data storytelling
- identify visualization patterns
- improve explainability
- support BI workflows
- generate production visualization plans

This agent behaves like:
- Data Visualization Engineer
- BI Analyst
- Analytics Architect
- Data Storytelling Specialist
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
class VisualizationAgentState:

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
# VISUALIZATION AGENT
# ============================================================


class VisualizationAgent:

    """
    Production-grade Visualization Agent.
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

                        "eda_context":
                            str(
                                context.get(
                                    "eda_context",
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

            dashboard_strategy = result.get(
                "dashboard_strategy",
                {},
            )

            recommended_visualizations = result.get(
                "recommended_visualizations",
                [],
            )

            chart_selection = result.get(
                "chart_selection",
                {},
            )

            statistical_visualizations = result.get(
                "statistical_visualizations",
                [],
            )

            business_visualizations = result.get(
                "business_visualizations",
                [],
            )

            ml_visualizations = result.get(
                "ml_visualizations",
                [],
            )

            anomaly_visualizations = result.get(
                "anomaly_visualizations",
                [],
            )

            correlation_visualizations = result.get(
                "correlation_visualizations",
                [],
            )

            interactive_dashboard = result.get(
                "interactive_dashboard",
                {},
            )

            realtime_visualization = result.get(
                "realtime_visualization",
                {},
            )

            visualization_stack = result.get(
                "visualization_stack",
                [],
            )

            storytelling_strategy = result.get(
                "storytelling_strategy",
                {},
            )

            accessibility_recommendations = result.get(
                "accessibility_recommendations",
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

            visualization_score = result.get(
                "visualization_score",
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
                    "visualization_agent",

                "dashboard_strategy":
                    dashboard_strategy,

                "recommended_visualizations":
                    recommended_visualizations,

                "chart_selection":
                    chart_selection,

                "statistical_visualizations":
                    statistical_visualizations,

                "business_visualizations":
                    business_visualizations,

                "ml_visualizations":
                    ml_visualizations,

                "anomaly_visualizations":
                    anomaly_visualizations,

                "correlation_visualizations":
                    correlation_visualizations,

                "interactive_dashboard":
                    interactive_dashboard,

                "realtime_visualization":
                    realtime_visualization,

                "visualization_stack":
                    visualization_stack,

                "storytelling_strategy":
                    storytelling_strategy,

                "accessibility_recommendations":
                    accessibility_recommendations,

                "optimization_recommendations":
                    optimization_recommendations,

                "production_readiness":
                    production_readiness,

                "visualization_score":
                    visualization_score,

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
                    "visualization_agent",

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
You are the Visualization Agent
for CognitiveOS.

Your role is to:
- design visualization systems
- recommend dashboards
- improve data storytelling
- optimize analytical insights
- support ML explainability
- build production BI workflows
- improve interpretability
- recommend scalable visual analytics

You think like:
- BI Architect
- Visualization Engineer
- Data Storytelling Expert
- Analytics Engineer

Focus on:
- dashboard design
- chart selection
- explainability
- anomaly visualization
- statistical insights
- real-time analytics
- accessibility
- scalability

You MUST:
- recommend REALISTIC visualizations
- optimize interpretability
- improve business insights
- support ML explainability
- design production dashboards
- minimize visualization clutter

Return ONLY valid JSON.

JSON FORMAT:

{{
  "dashboard_strategy": {{

    "dashboard_type":
      "executive analytics",

    "layout":
      "multi-panel",

    "refresh_mode":
      "real-time"
  }},

  "recommended_visualizations": [

    "correlation heatmap",

    "feature importance bar chart",

    "anomaly scatter plot",

    "time series trend chart"
  ],

  "chart_selection": {{

    "categorical":
      "bar chart",

    "continuous":
      "histogram",

    "time_series":
      "line chart"
  }},

  "statistical_visualizations": [

    "distribution plots",

    "boxplots",

    "violin plots"
  ],

  "business_visualizations": [

    "KPI dashboard",

    "revenue trends",

    "customer segmentation"
  ],

  "ml_visualizations": [

    "confusion matrix",

    "ROC curve",

    "SHAP importance"
  ],

  "anomaly_visualizations": [

    "outlier scatterplots",

    "anomaly timelines"
  ],

  "correlation_visualizations": [

    "pair plots",

    "heatmaps"
  ],

  "interactive_dashboard": {{

    "enabled":
      true,

    "framework":
      "Plotly Dash"
  }},

  "realtime_visualization": {{

    "enabled":
      true,

    "streaming":
      "WebSocket"
  }},

  "visualization_stack": [

    "Plotly",

    "Dash",

    "Streamlit"
  ],

  "storytelling_strategy": {{

    "focus":
      "executive insights",

    "narrative":
      "trend and anomaly driven"
  }},

  "accessibility_recommendations": [

    "colorblind-safe palette",

    "responsive layouts",

    "high contrast mode"
  ],

  "optimization_recommendations": [

    "reduce dashboard clutter",

    "use lazy loading",

    "aggregate large datasets"
  ],

  "production_readiness":
    "high",

  "visualization_score":
    9.0,

  "risks": [

    "visual overload",

    "high rendering latency"
  ],

  "reasoning":
    "Interactive dashboards improve insight discovery and business decision-making."
}}
"""