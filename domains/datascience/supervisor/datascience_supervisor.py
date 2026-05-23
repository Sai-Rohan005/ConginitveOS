# domains/datascience/supervisor/datascience_supervisory.py

"""
CognitiveOS - Data Science Supervisor
---------------------------------------------------------

Responsibilities:
- orchestrate data science workflows
- coordinate DS agents
- optimize ML pipelines
- manage EDA workflows
- coordinate feature engineering
- orchestrate training pipelines
- optimize visualization workflows
- enable deterministic DS cognition

Architecture:

Supervisor
    ↓
DS Agents
    ↓
Skills
    ↓
Core Runtime
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    List,
    Dict,
    Any,
)

# ============================================================
# WORKFLOW STEP
# ============================================================


@dataclass
class WorkflowStep:

    step_id: int

    agent: str

    task: str

    dependencies: List[int] = field(
        default_factory=list
    )

    parallelizable: bool = False

    expected_output: str = ""

    required_skills: List[str] = field(
        default_factory=list
    )

    execution_mode: str = (
        "hybrid"
    )

    runtime_backend: str = (
        "deterministic"
    )

    deterministic_execution: bool = (
        True
    )


# ============================================================
# SUPERVISOR RESULT
# ============================================================


@dataclass
class DataScienceSupervisorResult:

    orchestration_strategy: str

    workflow_steps: List[
        WorkflowStep
    ]

    execution_order: List[int]

    requires_reflection: bool

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# DATA SCIENCE SUPERVISOR
# ============================================================


class DataScienceSupervisor:

    """
    Deterministic Data Science Supervisor.
    """

    def __init__(self):

        # ====================================================
        # AVAILABLE AGENTS
        # ====================================================

        self.available_agents = [

            "eda_agent",

            "feature_engineering_agent",

            "ds_training_agent",

            "visualization_agent",
        ]

        # ====================================================
        # AVAILABLE SKILLS
        # ====================================================

        self.available_skills = [

            "pandas_skill",

            "numpy_skill",

            "visualization_skill",

            "feature_engineering_skill",

            "model_training_skill",

            "statistical_analysis_skill",
        ]

    # ========================================================
    # MAIN SUPERVISION
    # ========================================================

    def supervise(
        self,
        query: str,
    ) -> DataScienceSupervisorResult:

        query_lower = query.lower()

        workflow_steps = []

        step_id = 1

        # ====================================================
        # EDA WORKFLOW
        # ====================================================

        if any(

            keyword in query_lower

            for keyword in [

                "eda",

                "analyze dataset",

                "data analysis",

                "statistics",

                "dataset exploration",
            ]
        ):

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="eda_agent",

                    task=(
                        "Perform exploratory "
                        "data analysis"
                    ),

                    expected_output=(
                        "EDA report"
                    ),

                    required_skills=[

                        "pandas_skill",

                        "numpy_skill",

                        "statistical_analysis_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            eda_step = step_id

            step_id += 1

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="visualization_agent",

                    task=(
                        "Generate EDA "
                        "visualizations"
                    ),

                    dependencies=[
                        eda_step
                    ],

                    expected_output=(
                        "Visualization dashboard"
                    ),

                    required_skills=[

                        "visualization_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # FEATURE ENGINEERING WORKFLOW
        # ====================================================

        elif any(

            keyword in query_lower

            for keyword in [

                "feature engineering",

                "feature selection",

                "feature extraction",

                "preprocessing",
            ]
        ):

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="eda_agent",

                    task=(
                        "Analyze dataset "
                        "structure"
                    ),

                    expected_output=(
                        "Data analysis"
                    ),

                    required_skills=[

                        "pandas_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            eda_step = step_id

            step_id += 1

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="feature_engineering_agent",

                    task=(
                        "Perform feature "
                        "engineering"
                    ),

                    dependencies=[
                        eda_step
                    ],

                    expected_output=(
                        "Optimized features"
                    ),

                    required_skills=[

                        "feature_engineering_skill",

                        "numpy_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # TRAINING WORKFLOW
        # ====================================================

        elif any(

            keyword in query_lower

            for keyword in [

                "train model",

                "machine learning",

                "classification",

                "regression",

                "training",
            ]
        ):

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="eda_agent",

                    task=(
                        "Analyze training "
                        "dataset"
                    ),

                    expected_output=(
                        "Dataset insights"
                    ),

                    required_skills=[

                        "pandas_skill",

                        "statistical_analysis_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            eda_step = step_id

            step_id += 1

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="feature_engineering_agent",

                    task=(
                        "Engineer optimized "
                        "features"
                    ),

                    dependencies=[
                        eda_step
                    ],

                    expected_output=(
                        "Feature pipeline"
                    ),

                    required_skills=[

                        "feature_engineering_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            feature_step = step_id

            step_id += 1

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="ds_training_agent",

                    task=(
                        "Train and evaluate "
                        "machine learning model"
                    ),

                    dependencies=[
                        feature_step
                    ],

                    expected_output=(
                        "Trained ML model"
                    ),

                    required_skills=[

                        "model_training_skill",

                        "numpy_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            train_step = step_id

            step_id += 1

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="visualization_agent",

                    task=(
                        "Generate training "
                        "visualizations"
                    ),

                    dependencies=[
                        train_step
                    ],

                    expected_output=(
                        "Performance charts"
                    ),

                    required_skills=[

                        "visualization_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # VISUALIZATION WORKFLOW
        # ====================================================

        elif any(

            keyword in query_lower

            for keyword in [

                "visualization",

                "dashboard",

                "charts",

                "graphs",

                "plot",
            ]
        ):

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="visualization_agent",

                    task=(
                        "Generate data "
                        "visualizations"
                    ),

                    expected_output=(
                        "Visualization output"
                    ),

                    required_skills=[

                        "visualization_skill",

                        "pandas_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # GENERAL DATA SCIENCE
        # ====================================================

        else:

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="eda_agent",

                    task=(
                        "Perform exploratory "
                        "data analysis"
                    ),

                    expected_output=(
                        "EDA report"
                    ),

                    required_skills=[

                        "pandas_skill",

                        "statistical_analysis_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            eda_step = step_id

            step_id += 1

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="feature_engineering_agent",

                    task=(
                        "Build feature "
                        "engineering pipeline"
                    ),

                    dependencies=[
                        eda_step
                    ],

                    expected_output=(
                        "Feature pipeline"
                    ),

                    required_skills=[

                        "feature_engineering_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            feature_step = step_id

            step_id += 1

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="ds_training_agent",

                    task=(
                        "Train predictive "
                        "model"
                    ),

                    dependencies=[
                        feature_step
                    ],

                    expected_output=(
                        "ML model"
                    ),

                    required_skills=[

                        "model_training_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            training_step = step_id

            step_id += 1

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="visualization_agent",

                    task=(
                        "Generate insights "
                        "dashboard"
                    ),

                    dependencies=[
                        training_step
                    ],

                    expected_output=(
                        "Dashboard"
                    ),

                    required_skills=[

                        "visualization_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # EXECUTION ORDER
        # ====================================================

        execution_order = [

            step.step_id

            for step in workflow_steps
        ]

        # ====================================================
        # RETURN
        # ====================================================

        return DataScienceSupervisorResult(

            orchestration_strategy=(

                "Deterministic Data Science "
                "Workflow Orchestration"
            ),

            workflow_steps=workflow_steps,

            execution_order=execution_order,

            requires_reflection=True,

            metadata={

                "domain":
                    "dataScience",

                "workflow_size":
                    len(workflow_steps),

                "agents_used": [

                    step.agent

                    for step in workflow_steps
                ],

                "skills_used": list(

                    {

                        skill

                        for step in workflow_steps

                        for skill in (
                            step.required_skills
                        )
                    }
                ),

                "estimated_llm_calls":
                    len(workflow_steps),

                "deterministic_runtime":
                    True,
            },
        )

    # ========================================================
    # EXPORT SUPERVISION
    # ========================================================

    def export_supervision(
        self,
        result: DataScienceSupervisorResult,
    ) -> Dict[str, Any]:

        return {

            "orchestration_strategy":

                result
                .orchestration_strategy,

            "execution_order":

                result.execution_order,

            "requires_reflection":

                result.requires_reflection,

            "workflow_steps": [

                {

                    "step_id":
                        step.step_id,

                    "agent":
                        step.agent,

                    "task":
                        step.task,

                    "dependencies":
                        step.dependencies,

                    "parallelizable":
                        step.parallelizable,

                    "expected_output":
                        step.expected_output,

                    "required_skills":
                        step.required_skills,

                    "execution_mode":
                        step.execution_mode,

                    "runtime_backend":
                        step.runtime_backend,

                    "deterministic_execution":
                        (
                            step
                            .deterministic_execution
                        ),
                }

                for step in (
                    result.workflow_steps
                )
            ],

            "metadata":
                result.metadata,
        }