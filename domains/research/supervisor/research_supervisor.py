# domains/research/research_supervisor.py

"""
CognitiveOS - Research Supervisor
---------------------------------------------------------

Responsibilities:
- orchestrate research workflows
- coordinate research agents
- optimize literature pipelines
- manage summarization workflows
- coordinate citation generation
- build autonomous research pipelines
- minimize redundant LLM calls
- enable deterministic research cognition

Architecture:

Supervisor
    ↓
Research Agents
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
class ResearchSupervisorResult:

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
# RESEARCH SUPERVISOR
# ============================================================


class ResearchSupervisor:

    """
    Deterministic Research Supervisor.
    """

    def __init__(self):

        # ====================================================
        # AVAILABLE AGENTS
        # ====================================================

        self.available_agents = [

            "search_agent",

            "summarize_agent",

            "citation_agent",

            "report_agent",
        ]

        # ====================================================
        # AVAILABLE SKILLS
        # ====================================================

        self.available_skills = [

            "semantic_search_skill",

            "paper_ranking_skill",

            "citation_format_skill",

            "report_generation_skill",

            "summarization_skill",
        ]

    # ========================================================
    # MAIN SUPERVISION
    # ========================================================

    def supervise(
        self,
        query: str,
    ) -> ResearchSupervisorResult:

        query_lower = query.lower()

        workflow_steps = []

        step_id = 1

        # ====================================================
        # LITERATURE SEARCH WORKFLOW
        # ====================================================

        if any(

            keyword in query_lower

            for keyword in [

                "search",

                "papers",

                "literature",

                "research papers",

                "find papers",
            ]
        ):

            # ================================================
            # SEARCH
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="search_agent",

                    task=(
                        "Search and retrieve "
                        "relevant research papers"
                    ),

                    expected_output=(
                        "Research search results"
                    ),

                    required_skills=[

                        "semantic_search_skill",

                        "paper_ranking_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            search_step = step_id

            step_id += 1

            # ================================================
            # SUMMARIZATION
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="summarize_agent",

                    task=(
                        "Summarize retrieved "
                        "research papers"
                    ),

                    dependencies=[
                        search_step
                    ],

                    expected_output=(
                        "Paper summaries"
                    ),

                    required_skills=[

                        "summarization_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # CITATION WORKFLOW
        # ====================================================

        elif any(

            keyword in query_lower

            for keyword in [

                "citation",

                "references",

                "bibliography",

                "apa",

                "ieee",
            ]
        ):

            # ================================================
            # SEARCH
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="search_agent",

                    task=(
                        "Retrieve scholarly "
                        "sources"
                    ),

                    expected_output=(
                        "Research sources"
                    ),

                    required_skills=[

                        "semantic_search_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            search_step = step_id

            step_id += 1

            # ================================================
            # CITATION
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="citation_agent",

                    task=(
                        "Generate scholarly "
                        "citations"
                    ),

                    dependencies=[
                        search_step
                    ],

                    expected_output=(
                        "Formatted citations"
                    ),

                    required_skills=[

                        "citation_format_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # REPORT GENERATION WORKFLOW
        # ====================================================

        elif any(

            keyword in query_lower

            for keyword in [

                "report",

                "survey",

                "review",

                "research report",

                "technical report",
            ]
        ):

            # ================================================
            # SEARCH
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="search_agent",

                    task=(
                        "Retrieve relevant "
                        "research papers"
                    ),

                    expected_output=(
                        "Research corpus"
                    ),

                    required_skills=[

                        "semantic_search_skill",

                        "paper_ranking_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            search_step = step_id

            step_id += 1

            # ================================================
            # SUMMARIZATION
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="summarize_agent",

                    task=(
                        "Summarize technical "
                        "research findings"
                    ),

                    dependencies=[
                        search_step
                    ],

                    expected_output=(
                        "Research summaries"
                    ),

                    required_skills=[

                        "summarization_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            summarize_step = step_id

            step_id += 1

            # ================================================
            # CITATION
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="citation_agent",

                    task=(
                        "Generate scholarly "
                        "citations and references"
                    ),

                    dependencies=[
                        summarize_step
                    ],

                    expected_output=(
                        "Validated citations"
                    ),

                    required_skills=[

                        "citation_format_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            citation_step = step_id

            step_id += 1

            # ================================================
            # REPORT
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="report_agent",

                    task=(
                        "Generate structured "
                        "research report"
                    ),

                    dependencies=[
                        citation_step
                    ],

                    expected_output=(
                        "Research report"
                    ),

                    required_skills=[

                        "report_generation_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # SUMMARIZATION WORKFLOW
        # ====================================================

        elif any(

            keyword in query_lower

            for keyword in [

                "summarize",

                "summary",

                "explain paper",

                "compress",
            ]
        ):

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="summarize_agent",

                    task=(
                        "Summarize research "
                        "documents"
                    ),

                    expected_output=(
                        "Research summary"
                    ),

                    required_skills=[

                        "summarization_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

        # ====================================================
        # GENERAL RESEARCH
        # ====================================================

        else:

            # ================================================
            # SEARCH
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="search_agent",

                    task=(
                        "Search relevant "
                        "research literature"
                    ),

                    expected_output=(
                        "Research results"
                    ),

                    required_skills=[

                        "semantic_search_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            search_step = step_id

            step_id += 1

            # ================================================
            # SUMMARIZE
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="summarize_agent",

                    task=(
                        "Summarize retrieved "
                        "knowledge"
                    ),

                    dependencies=[
                        search_step
                    ],

                    expected_output=(
                        "Research summary"
                    ),

                    required_skills=[

                        "summarization_skill",
                    ],

                    runtime_backend="deterministic",

                    deterministic_execution=True,
                )
            )

            summarize_step = step_id

            step_id += 1

            # ================================================
            # REPORT
            # ================================================

            workflow_steps.append(

                WorkflowStep(

                    step_id=step_id,

                    agent="report_agent",

                    task=(
                        "Generate structured "
                        "research insights"
                    ),

                    dependencies=[
                        summarize_step
                    ],

                    expected_output=(
                        "Research report"
                    ),

                    required_skills=[

                        "report_generation_skill",
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

        return ResearchSupervisorResult(

            orchestration_strategy=(

                "Deterministic Research "
                "Workflow Orchestration"
            ),

            workflow_steps=workflow_steps,

            execution_order=execution_order,

            requires_reflection=True,

            metadata={

                "domain":
                    "research",

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
    # EXPORT
    # ========================================================

    def export_supervision(
        self,
        result: ResearchSupervisorResult,
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