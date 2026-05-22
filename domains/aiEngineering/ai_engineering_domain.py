# domains/aiEngineering/ai_engineering_domain.py

"""
CognitiveOS - AI Engineering Domain
---------------------------------------------------------

Responsibilities:
- register AI Engineering agents
- connect AI supervisor
- execute AI workflows
- provide unified AI domain interface
- integrate with shared orchestration runtime

This becomes the entrypoint for:
- RAG systems
- LLM systems
- training systems
- inference systems
- vector databases
- AI evaluation pipelines
"""

from __future__ import annotations

from typing import (
    Dict,
    Any,
)

# ============================================================
# CORE EXECUTOR
# ============================================================

from core.orchestration.workflow_executor import (
    WorkflowExecutor,
)

# ============================================================
# SUPERVISOR
# ============================================================

from domains.aiEngineering.supervisor.ai_engineering_supervisor import (
    AIEngineeringSupervisor,
)

# ============================================================
# AGENTS
# ============================================================

from domains.aiEngineering.agents.llm_agent import (
    LLMAgent,
)

from domains.aiEngineering.agents.rag_agent import (
    RAGAgent,
)

from domains.aiEngineering.agents.training_agent import (
    TrainingAgent,
)

from domains.aiEngineering.agents.inference_agent import (
    InferenceAgent,
)

from domains.aiEngineering.agents.vector_db_agent import (
    VectorDBAgent,
)

from domains.aiEngineering.agents.evaluation_agent import (
    EvaluationAgent,
)

# ============================================================
# AI ENGINEERING DOMAIN
# ============================================================


class AIEngineeringDomain:

    """
    AI Engineering domain runtime.
    """

    def __init__(self):

        # ====================================================
        # DOMAIN NAME
        # ====================================================

        self.domain_name = (
            "aiEngineering"
        )

        # ====================================================
        # SUPERVISOR
        # ====================================================

        self.supervisor = (
            AIEngineeringSupervisor()
        )

        # ====================================================
        # SHARED EXECUTOR
        # ====================================================

        self.workflow_executor = (
            WorkflowExecutor()
        )

        # ====================================================
        # AGENT REGISTRY
        # ====================================================

        self.agent_registry = {

            "llm_agent":
                LLMAgent(),

            "rag_agent":
                RAGAgent(),

            "training_agent":
                TrainingAgent(),

            "inference_agent":
                InferenceAgent(),

            "vector_db_agent":
                VectorDBAgent(),

            "evaluation_agent":
                EvaluationAgent(),
        }

        # ====================================================
        # REGISTER AGENTS INTO EXECUTOR
        # ====================================================

        self.workflow_executor.agent_registry.update(

            self.agent_registry
        )

    # ========================================================
    # EXECUTE DOMAIN
    # ========================================================

    async def execute(
        self,
        query: str,
    ) -> Dict[str, Any]:

        # ====================================================
        # BUILD WORKFLOW
        # ====================================================

        supervision_result = (

            self.supervisor.supervise(
                query=query
            )
        )

        workflow_steps = (
            supervision_result.workflow_steps
        )

        # ====================================================
        # EXECUTE WORKFLOW
        # ====================================================

        execution_result = await (

            self.workflow_executor
            .execute_workflow(

                query=query,

                workflow_steps=
                    workflow_steps,
            )
        )

        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        return {

            "success":
                execution_result.success,

            "domain":
                self.domain_name,

            "query":
                query,

            "workflow": {

                "strategy":
                    supervision_result
                    .orchestration_strategy,

                "execution_order":
                    supervision_result
                    .execution_order,

                "steps": [

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

                    for step in (
                        workflow_steps
                    )
                ],
            },

            "final_output":
                execution_result.final_output,

            "memory_snapshot":
                execution_result.memory_snapshot,
        }

    # ========================================================
    # DOMAIN METADATA
    # ========================================================

    def metadata(self) -> Dict[str, Any]:

        return {

            "domain":
                self.domain_name,

            "capabilities": [

                "rag_systems",

                "llm_systems",

                "training_pipelines",

                "distributed_inference",

                "vector_databases",

                "ai_evaluation",

                "autonomous_agents",
            ],

            "agents": list(

                self.agent_registry.keys()
            ),

            "supervisor":
                self.supervisor.__class__.__name__,
        }

    # ========================================================
    # AVAILABLE AGENTS
    # ========================================================

    def available_agents(self):

        return list(
            self.agent_registry.keys()
        )

    # ========================================================
    # EXPORT CONFIG
    # ========================================================

    def export_config(self):

        return {

            "domain":
                self.domain_name,

            "agents":
                self.available_agents(),

            "metadata":
                self.metadata(),
        }


# ============================================================
# FACTORY
# ============================================================


def build_ai_engineering_domain():

    return AIEngineeringDomain()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    import asyncio

    async def main():

        domain = (
            build_ai_engineering_domain()
        )

        result = await domain.execute(

            query=(
                "Build a scalable "
                "RAG system using "
                "Qdrant and FastAPI"
            )
        )

        print("\n")
        print("=" * 80)
        print("AI ENGINEERING RESULT")
        print("=" * 80)
        print(result)

    asyncio.run(main())