# core/orchestration/deterministic_planner.py

"""
CognitiveOS - Deterministic Planner
---------------------------------------------------------

Responsibilities:
- deterministic workflow planning
- domain identification
- workflow generation
- agent selection
- dependency planning
- execution ordering
- reflection strategy planning

This replaces unnecessary LLM planner calls
with deterministic orchestration intelligence.
"""

from __future__ import annotations

from typing import (
    Dict,
    Any,
    List,
)

from dataclasses import (
    dataclass,
    field,
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


# ============================================================
# PLANNER RESULT
# ============================================================


@dataclass
class PlannerResult:

    success: bool

    domain: str

    workflow_name: str

    orchestration_strategy: str

    requires_reflection: bool

    execution_order: List[int]

    workflow_steps: List[
        WorkflowStep
    ] = field(default_factory=list)

    metadata: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# DETERMINISTIC PLANNER
# ============================================================


class DeterministicPlanner:

    """
    Deterministic workflow planner.
    """

    def __init__(self):

        # ====================================================
        # DOMAIN ROUTING
        # ====================================================

        self.domain_keywords = {

            "softwareEngineering": [

                "fastapi",

                "backend",

                "frontend",

                "jwt",

                "authentication",

                "api",

                "microservice",

                "database",

                "docker",

                "websocket",

                "redis",

                "postgresql",

                "rest api",
            ],

            "aiEngineering": [

                "rag",

                "llm",

                "vector",

                "embedding",

                "langchain",

                "fine tuning",

                "transformer",

                "agentic",

                "prompt engineering",

                "retrieval",
            ],

            "cybersecurity": [

                "vulnerability",

                "security",

                "exploit",

                "xss",

                "csrf",

                "sql injection",

                "pentest",

                "malware",

                "jwt attack",
            ],

            "devops": [

                "kubernetes",

                "terraform",

                "ci/cd",

                "jenkins",

                "monitoring",

                "deployment",

                "infrastructure",

                "nginx",

                "helm",
            ],

            "research": [

                "research",

                "paper",

                "survey",

                "analysis",

                "benchmark",

                "evaluation",

                "comparison",
            ],

            "dataScience": [

                "pandas",

                "visualization",

                "regression",

                "classification",

                "data analysis",

                "machine learning",

                "feature engineering",
            ],
        }

    # ========================================================
    # MAIN PLANNING
    # ========================================================

    def plan(
        self,
        query: str,
    ) -> PlannerResult:

        # ====================================================
        # DOMAIN DETECTION
        # ====================================================

        domain = self._detect_domain(
            query
        )

        # ====================================================
        # WORKFLOW GENERATION
        # ====================================================

        workflow_steps = (
            self._build_workflow(
                domain,
                query,
            )
        )

        execution_order = [

            step.step_id

            for step in workflow_steps
        ]

        # ====================================================
        # STRATEGY
        # ====================================================

        orchestration_strategy = (
            self._determine_strategy(
                workflow_steps
            )
        )

        requires_reflection = (
            self._requires_reflection(
                query
            )
        )

        return PlannerResult(

            success=True,

            domain=domain,

            workflow_name=
                f"{domain}_workflow",

            orchestration_strategy=
                orchestration_strategy,

            requires_reflection=
                requires_reflection,

            execution_order=
                execution_order,

            workflow_steps=
                workflow_steps,

            metadata={

                "workflow_size":
                    len(workflow_steps),
            },
        )

    # ========================================================
    # DOMAIN DETECTION
    # ========================================================

    def _detect_domain(
        self,
        query: str,
    ) -> str:

        query = query.lower()

        scores = {}

        for domain, keywords in (
            self.domain_keywords.items()
        ):

            score = 0

            for keyword in keywords:

                if keyword in query:

                    score += 1

            scores[domain] = score

        best_domain = max(

            scores,

            key=scores.get
        )

        if scores[best_domain] == 0:

            return "softwareEngineering"

        return best_domain

    # ========================================================
    # BUILD WORKFLOW
    # ========================================================

    def _build_workflow(
        self,
        domain: str,
        query: str,
    ) -> List[WorkflowStep]:

        # ====================================================
        # SOFTWARE ENGINEERING
        # ====================================================

        if domain == "softwareEngineering":

            return [

                WorkflowStep(

                    step_id=1,

                    agent=
                        "architecture_agent",

                    task=
                        "Design scalable software architecture",

                    dependencies=[],

                    expected_output=
                        "Architecture specification",
                ),

                WorkflowStep(

                    step_id=2,

                    agent=
                        "code_agent",

                    task=
                        "Generate production-grade implementation",

                    dependencies=[1],

                    expected_output=
                        "Executable project",
                ),

                WorkflowStep(

                    step_id=3,

                    agent=
                        "debug_agent",

                    task=
                        "Validate runtime and architecture quality",

                    dependencies=[2],

                    expected_output=
                        "Debugging report",
                ),
            ]

        # ====================================================
        # AI ENGINEERING
        # ====================================================

        if domain == "aiEngineering":

            return [

                WorkflowStep(

                    step_id=1,

                    agent=
                        "rag_architecture_agent",

                    task=
                        "Design AI system architecture",

                    dependencies=[],

                    expected_output=
                        "AI architecture",
                ),

                WorkflowStep(

                    step_id=2,

                    agent=
                        "llm_pipeline_agent",

                    task=
                        "Generate AI pipeline",

                    dependencies=[1],

                    expected_output=
                        "AI implementation",
                ),

                WorkflowStep(

                    step_id=3,

                    agent=
                        "evaluation_agent",

                    task=
                        "Evaluate AI system",

                    dependencies=[2],

                    expected_output=
                        "Evaluation report",
                ),
            ]

        # ====================================================
        # CYBERSECURITY
        # ====================================================

        if domain == "cybersecurity":

            return [

                WorkflowStep(

                    step_id=1,

                    agent=
                        "security_architecture_agent",

                    task=
                        "Analyze security architecture",

                    dependencies=[],

                    expected_output=
                        "Security assessment",
                ),

                WorkflowStep(

                    step_id=2,

                    agent=
                        "vulnerability_agent",

                    task=
                        "Detect vulnerabilities",

                    dependencies=[1],

                    expected_output=
                        "Vulnerability report",
                ),

                WorkflowStep(

                    step_id=3,

                    agent=
                        "security_fix_agent",

                    task=
                        "Generate remediation fixes",

                    dependencies=[2],

                    expected_output=
                        "Security remediation",
                ),
            ]

        # ====================================================
        # DEVOPS
        # ====================================================

        if domain == "devops":

            return [

                WorkflowStep(

                    step_id=1,

                    agent=
                        "infra_agent",

                    task=
                        "Design infrastructure architecture",

                    dependencies=[],

                    expected_output=
                        "Infrastructure specification",
                ),

                WorkflowStep(

                    step_id=2,

                    agent=
                        "deployment_agent",

                    task=
                        "Generate deployment pipelines",

                    dependencies=[1],

                    expected_output=
                        "CI/CD pipeline",
                ),

                WorkflowStep(

                    step_id=3,

                    agent=
                        "monitoring_agent",

                    task=
                        "Generate monitoring stack",

                    dependencies=[2],

                    expected_output=
                        "Observability system",
                ),
            ]

        # ====================================================
        # RESEARCH
        # ====================================================

        if domain == "research":

            return [

                WorkflowStep(

                    step_id=1,

                    agent=
                        "research_agent",

                    task=
                        "Conduct research analysis",

                    dependencies=[],

                    expected_output=
                        "Research findings",
                ),

                WorkflowStep(

                    step_id=2,

                    agent=
                        "citation_agent",

                    task=
                        "Generate citations and references",

                    dependencies=[1],

                    expected_output=
                        "Research citations",
                ),

                WorkflowStep(

                    step_id=3,

                    agent=
                        "summary_agent",

                    task=
                        "Generate research summary",

                    dependencies=[2],

                    expected_output=
                        "Final research report",
                ),
            ]

        # ====================================================
        # DATA SCIENCE
        # ====================================================

        if domain == "dataScience":

            return [

                WorkflowStep(

                    step_id=1,

                    agent=
                        "data_analysis_agent",

                    task=
                        "Analyze dataset",

                    dependencies=[],

                    expected_output=
                        "Analysis results",
                ),

                WorkflowStep(

                    step_id=2,

                    agent=
                        "modeling_agent",

                    task=
                        "Generate ML pipeline",

                    dependencies=[1],

                    expected_output=
                        "ML model",
                ),

                WorkflowStep(

                    step_id=3,

                    agent=
                        "visualization_agent",

                    task=
                        "Generate visualizations",

                    dependencies=[2],

                    expected_output=
                        "Charts and reports",
                ),
            ]

        # ====================================================
        # DEFAULT
        # ====================================================

        return [

            WorkflowStep(

                step_id=1,

                agent=
                    "general_agent",

                task=
                    "Solve user request",

                dependencies=[],

                expected_output=
                    "General solution",
            )
        ]

    # ========================================================
    # ORCHESTRATION STRATEGY
    # ========================================================

    def _determine_strategy(
        self,
        workflow_steps: List[
            WorkflowStep
        ],
    ) -> str:

        if len(workflow_steps) <= 2:

            return (
                "Lightweight sequential execution"
            )

        return (
            "Sequential architecture-first "
            "execution with validation"
        )

    # ========================================================
    # REFLECTION REQUIREMENT
    # ========================================================

    def _requires_reflection(
        self,
        query: str,
    ) -> bool:

        query = query.lower()

        high_risk_keywords = [

            "production",

            "scalable",

            "distributed",

            "secure",

            "enterprise",

            "high performance",
        ]

        for keyword in high_risk_keywords:

            if keyword in query:

                return True

        return False

    # ========================================================
    # EXPORT PLAN
    # ========================================================

    def export_plan(
        self,
        result: PlannerResult,
    ) -> Dict[str, Any]:

        return {

            "success":
                result.success,

            "domain":
                result.domain,

            "workflow_name":
                result.workflow_name,

            "orchestration_strategy":
                result.orchestration_strategy,

            "requires_reflection":
                result.requires_reflection,

            "execution_order":
                result.execution_order,

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
                }

                for step
                in result.workflow_steps
            ],

            "metadata":
                result.metadata,
        }