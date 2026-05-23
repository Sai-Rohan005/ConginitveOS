# core/orchestration/master_orchestrator.py

"""
CognitiveOS - Master Orchestrator
---------------------------------------------------------

Responsibilities:
- receive user queries
- route queries to correct domains
- invoke supervisors
- execute workflows
- manage multi-domain cognition
- aggregate execution results
- coordinate runtime orchestration
- provide autonomous cognition entrypoint

Architecture:

User Query
    ↓
Master Orchestrator
    ↓
Domain Router
    ↓
Supervisor
    ↓
Workflow Executor
    ↓
Agents + Skills
"""

from __future__ import annotations

import time
import traceback
import pprint

from typing import (
    Dict,
    Any,
    List,
)

# ============================================================
# ROUTER
# ============================================================

from core.orchestration.domain_router import (
    get_domain_router,
)

# ============================================================
# WORKFLOW EXECUTOR
# ============================================================

from core.orchestration.workflow_executor import (
    WorkflowExecutor,
)

# ============================================================
# TOOL EXECUTOR
# ============================================================

from core.tools.tool_executor import (
    ToolExecutor,
)

# ============================================================
# RESULT
# ============================================================


class MasterOrchestratorResult:

    def __init__(
        self,
        success: bool,
        output: Dict[
            str,
            Any,
        ],
    ):

        self.success = success

        self.output = output


# ============================================================
# MASTER ORCHESTRATOR
# ============================================================


class MasterOrchestrator:

    """
    Top-level orchestration brain
    for CognitiveOS.
    """

    def __init__(self):

        # ====================================================
        # ROUTER
        # ====================================================

        self.domain_router = (
            get_domain_router()
        )

        # ====================================================
        # TOOLS
        # ====================================================

        self.tool_executor = (
            ToolExecutor()
        )

        # ====================================================
        # EXECUTOR
        # ====================================================

        self.workflow_executor = (
            WorkflowExecutor(

                tool_executor=
                    self.tool_executor
            )
        )

        # ====================================================
        # ORCHESTRATION METRICS
        # ====================================================

        self.metrics = {

            "total_requests": 0,

            "successful_requests": 0,

            "failed_requests": 0,

            "multi_domain_requests": 0,

            "total_runtime": 0.0,
        }

    # ========================================================
    # LOGGING HELPERS
    # ========================================================

    def _log_step_start(
        self,
        step_name: str,
    ):

        print(
            f"\n---- STEP STARTED: {step_name}"
        )

    def _log_step_result(
        self,
        step_name: str,
        result: Any,
    ):

        print(
            f"---- STEP RESULT: {step_name}"
        )

        pprint.pprint(result)

        print(
            "-" * 80
        )


    

    # ========================================================
    # MAIN ENTRYPOINT
    # ========================================================

    async def execute(
        self,
        query: str,
        enable_multi_domain: bool = False,
    ) -> MasterOrchestratorResult:

        start_time = time.time()

        self.metrics[
            "total_requests"
        ] += 1

        try:

            # =================================================
            # EXECUTION START
            # =================================================

            self._log_step_start(
                "MASTER ORCHESTRATOR EXECUTION"
            )

            self._log_step_result(
                "INPUT",
                {
                    "query": query,
                    "enable_multi_domain":
                        enable_multi_domain,
                },
            )

            # =================================================
            # ROUTING
            # =================================================

            self._log_step_start(
                "ROUTING"
            )

            if enable_multi_domain:

                routing_result = (

                    self.domain_router
                    .multi_domain_route(
                        query
                    )
                )

            else:

                routing_result = (

                    self.domain_router
                    .route(
                        query
                    )
                )

            self._log_step_result(
                "ROUTING",
                routing_result,
            )

            # =================================================
            # ROUTING FAILURE
            # =================================================

            if not routing_result.get(
                "success",
                False,
            ):

                raise RuntimeError(

                    routing_result.get(
                        "error",
                        "Routing failed",
                    )
                )

            # =================================================
            # MULTI DOMAIN
            # =================================================

            if enable_multi_domain:

                self.metrics[
                    "multi_domain_requests"
                ] += 1

                self._log_step_start(
                    "MULTI DOMAIN EXECUTION"
                )

                result = await (
                    self._execute_multi_domain(

                        query,

                        routing_result,
                    )
                )

                self._log_step_result(
                    "MULTI DOMAIN EXECUTION",
                    result,
                )

            # =================================================
            # SINGLE DOMAIN
            # =================================================

            else:

                self._log_step_start(
                    "SINGLE DOMAIN EXECUTION"
                )

                result = await (
                    self._execute_single_domain(

                        query,

                        routing_result,
                    )
                )

                self._log_step_result(
                    "SINGLE DOMAIN EXECUTION",
                    result,
                )

            # =================================================
            # SUCCESS METRICS
            # =================================================

            runtime = (
                time.time() - start_time
            )

            self.metrics[
                "successful_requests"
            ] += 1

            self.metrics[
                "total_runtime"
            ] += runtime

            # =================================================
            # FINAL RESULT
            # =================================================

            final_result = {

                "success": True,

                "runtime_seconds":
                    runtime,

                "result":
                    result,
            }

            self._log_step_result(
                "FINAL RESULT",
                final_result,
            )

            return MasterOrchestratorResult(

                success=True,

                output=result,
            )

        except Exception as e:

            self.metrics[
                "failed_requests"
            ] += 1

            error_result = {

                "error":
                    str(e),

                "traceback":
                    traceback
                    .format_exc(),
            }

            self._log_step_result(
                "ERROR",
                error_result,
            )

            return MasterOrchestratorResult(

                success=False,

                output=error_result,
            )

    # ========================================================
    # SINGLE DOMAIN EXECUTION
    # ========================================================

    async def _execute_single_domain(
        self,
        query: str,
        routing_result: Dict[
            str,
            Any,
        ],
    ) -> Dict[str, Any]:

        # ====================================================
        # DOMAIN EXTRACTION
        # ====================================================

        self._log_step_start(
            "DOMAIN EXTRACTION"
        )

        domain = routing_result[
            "selected_domain"
        ]

        supervisor = routing_result[
            "supervisor"
        ]

        confidence = routing_result[
            "confidence"
        ]

        self._log_step_result(
            "DOMAIN EXTRACTION",
            {
                "domain":
                    domain,

                "confidence":
                    confidence,
            },
        )

        # ====================================================
        # SUPERVISION
        # ====================================================

        self._log_step_start(
            "SUPERVISION"
        )

        supervision_result = (
            supervisor.supervise(
                query
            )
        )

        workflow_steps = (
            supervision_result
            .workflow_steps
        )

        self._log_step_result(
            "SUPERVISION",
            {

                "strategy":

                    supervision_result
                    .orchestration_strategy,

                "execution_order":

                    supervision_result
                    .execution_order,

                "workflow_steps":
                    workflow_steps,

                "workflow_size":

                    len(
                        workflow_steps
                    ),
            },
        )

        # ====================================================
        # WORKFLOW EXECUTION
        # ====================================================

        self._log_step_start(
            "WORKFLOW EXECUTION"
        )

        execution_result = await (
            self.workflow_executor.execute_workflow(
                query=query,
                workflow_steps=workflow_steps,
            )
        )

        # SAFE DEBUG VALIDATION (prevents crash)
        validation = self._safe_validate_execution(execution_result)

        self._log_step_result(
            "WORKFLOW EXECUTION",
            {

                "success":

                    execution_result
                    .success,

                "final_output":

                    execution_result
                    .final_output,

                "memory_snapshot":

                    execution_result
                    .memory_snapshot,
            },
        )

        # ====================================================
        # FINAL RESULT
        # ====================================================

        final_output = {
            "query": query,
            "mode": "single_domain",
            "selected_domain": domain,
            "routing_confidence": confidence,

            "supervision": {
                "strategy": supervision_result.orchestration_strategy,
                "execution_order": supervision_result.execution_order,
                "workflow_size": len(workflow_steps),
            },

            "execution": {
                "success": execution_result.success,
                "output": execution_result.final_output,
                "memory_snapshot": execution_result.memory_snapshot,
            },

            # ✅ ADD THIS BLOCK
            "debug": {
                "validation": validation
            }
        }

        self._log_step_result(
            "SINGLE DOMAIN FINAL OUTPUT",
            final_output,
        )

        return final_output

    # ========================================================
    # MULTI DOMAIN EXECUTION
    # ========================================================

    async def _execute_multi_domain(
        self,
        query: str,
        routing_result: Dict[
            str,
            Any,
        ],
    ) -> Dict[str, Any]:

        domains = routing_result[
            "domains"
        ]

        multi_domain_outputs = []

        # ====================================================
        # EXECUTE EACH DOMAIN
        # ====================================================

        for index, domain_info in enumerate(
            domains,
            start=1,
        ):

            domain_name = (
                domain_info[
                    "domain"
                ]
            )

            supervisor = (
                domain_info[
                    "supervisor"
                ]
            )

            self._log_step_start(
                f"MULTI DOMAIN [{index}] "
                f"{domain_name.upper()} "
                f"SUPERVISION"
            )

            supervision_result = (
                supervisor.supervise(
                    query
                )
            )

            workflow_steps = (

                supervision_result
                .workflow_steps
            )

            self._log_step_result(
                f"{domain_name.upper()} SUPERVISION",
                {
                    "workflow_steps":
                        workflow_steps,

                    "workflow_size":
                        len(
                            workflow_steps
                        ),
                },
            )

            # ================================================
            # EXECUTION
            # ================================================

            self._log_step_start(
                f"{domain_name.upper()} "
                f"WORKFLOW EXECUTION"
            )

            execution_result = await (

                self.workflow_executor
                .execute_workflow(

                    query=query,

                    workflow_steps=
                        workflow_steps,
                )
            )

            domain_output = {

                "domain":
                    domain_name,

                "success":

                    execution_result
                    .success,

                "execution":

                    execution_result
                    .final_output,
            }

            self._log_step_result(
                f"{domain_name.upper()} EXECUTION RESULT",
                domain_output,
            )

            multi_domain_outputs.append(
                domain_output
            )

        # ====================================================
        # AGGREGATION
        # ====================================================

        aggregated_result = {

            "query":
                query,

            "mode":
                "multi_domain",

            "domains_executed":

                len(domains),

            "domain_outputs":
                multi_domain_outputs,
        }

        self._log_step_start(
            "MULTI DOMAIN AGGREGATION"
        )

        self._log_step_result(
            "MULTI DOMAIN AGGREGATION",
            aggregated_result,
        )

        return aggregated_result

    # ========================================================
    # QUICK EXECUTE
    # ========================================================

    async def quick_execute(
        self,
        query: str,
    ) -> Dict[str, Any]:

        self._log_step_start(
            "QUICK EXECUTE"
        )

        result = await self.execute(
            query=query
        )

        self._log_step_result(
            "QUICK EXECUTE RESULT",
            result.output,
        )

        return result.output

    # ========================================================
    # EXECUTE DOMAIN DIRECTLY
    # ========================================================

    async def execute_domain(
        self,
        domain_name: str,
        query: str,
    ) -> Dict[str, Any]:

        self._log_step_start(
            f"EXECUTE DOMAIN: {domain_name}"
        )

        supervisor = (

            self.domain_router
            .domain_registry
            .create_supervisor(
                domain_name
            )
        )

        self._log_step_result(
            "SUPERVISOR CREATED",
            {
                "domain":
                    domain_name,

                "supervisor":
                    str(supervisor),
            },
        )

        supervision_result = (
            supervisor.supervise(
                query
            )
        )

        self._log_step_result(
            "DOMAIN SUPERVISION",
            {
                "workflow_steps":

                    supervision_result
                    .workflow_steps,
            },
        )

        execution_result = await (

            self.workflow_executor
            .execute_workflow(

                query=query,

                workflow_steps=

                    supervision_result
                    .workflow_steps,
            )
        )

        final_output = {

            "domain":
                domain_name,

            "execution":
                execution_result
                .final_output,
        }

        self._log_step_result(
            "DOMAIN EXECUTION RESULT",
            final_output,
        )

        return final_output

    # ========================================================
    # EXPORT STATE
    # ========================================================

    def export_state(
        self,
    ) -> Dict[str, Any]:

        self._log_step_start(
            "EXPORT STATE"
        )

        state = {

            "metrics":
                self.metrics,

            "router":

                self.domain_router
                .export_state(),

            "workflow_executor":

                self.workflow_executor
                .telemetry,
        }

        self._log_step_result(
            "EXPORT STATE",
            state,
        )

        return state


    def _safe_validate_execution(self, execution_result):
        """
        Prevents crash due to signature mismatch in DeterministicDebugger.
        """

        debugger = getattr(self.workflow_executor, "debugger", None)

        if not debugger:
            return {
                "valid": True,
                "warning": "No debugger attached"
            }

        payload = getattr(execution_result, "final_output", None)

        try:
            # PRIMARY (NEW STANDARD)
            return debugger.validate_execution(
                execution_results=payload
            )
        except TypeError:
            try:
                # LEGACY SUPPORT (old signature)
                return debugger.validate_execution(
                    outputs=payload
                )
            except Exception as e:
                return {
                    "valid": False,
                    "error": str(e),
                }

    # ========================================================
    # HEALTHCHECK
    # ========================================================


    def healthcheck(
        self,
    ) -> Dict[str, Any]:

        self._log_step_start(
            "HEALTHCHECK"
        )

        health = {

            "status":
                "healthy",

            "metrics":
                self.metrics,

            "router":

                self.domain_router
                .healthcheck(),

            "workflow_runtime":
                "active",
        }

        self._log_step_result(
            "HEALTHCHECK",
            health,
        )

        return health


# ============================================================
# GLOBAL ORCHESTRATOR
# ============================================================

GLOBAL_MASTER_ORCHESTRATOR = (
    MasterOrchestrator()
)

# ============================================================
# FACTORY
# ============================================================


def get_master_orchestrator():

    return (
        GLOBAL_MASTER_ORCHESTRATOR
    )