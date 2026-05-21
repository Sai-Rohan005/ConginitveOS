# domains/software_engineering/agents/aggregator_agent.py

"""
CognitiveOS - Deterministic Aggregator Agent
---------------------------------------------------------

Responsibilities:
- aggregate workflow outputs
- synthesize execution results
- summarize runtime repairs
- summarize architecture
- summarize APIs
- generate engineering reports
- produce final user-facing output

This is now:
- deterministic first
- LLM optional
- runtime-aware
- artifact-aware
"""

from __future__ import annotations

import json
import traceback

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
# STATE
# ============================================================


@dataclass
class AggregatorAgentState:

    query: str

    agent_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    reflection_notes: List[
        str
    ] = field(default_factory=list)

    artifacts: List[Any] = field(
        default_factory=list
    )

    runtime_repairs: List[
        Dict[str, Any]
    ] = field(default_factory=list)

    metrics: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    final_response: str = ""


# ============================================================
# AGGREGATOR AGENT
# ============================================================


class AggregatorAgent:

    """
    Deterministic engineering report generator.
    """

    def __init__(self):

        pass

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def run(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        try:

            query = context.get(
                "query",
                "",
            )

            agent_outputs = context.get(
                "agent_outputs",
                {},
            )

            artifacts = context.get(
                "artifacts",
                [],
            )

            runtime_repairs = context.get(
                "runtime_repairs",
                [],
            )

            reflection_notes = context.get(
                "reflection_notes",
                [],
            )

            metrics = context.get(
                "metrics",
                {},
            )

            # =================================================
            # EXTRACT OUTPUTS
            # =================================================

            architecture_output = (
                self._find_agent_output(
                    agent_outputs,
                    "architecture_agent",
                )
            )

            code_output = (
                self._find_agent_output(
                    agent_outputs,
                    "code_agent",
                )
            )

            debug_output = (
                self._find_agent_output(
                    agent_outputs,
                    "debug_agent",
                )
            )

            # =================================================
            # BUILD FINAL REPORT
            # =================================================

            report = []

            report.append(
                "# CognitiveOS Engineering Report\n"
            )

            # =================================================
            # OVERVIEW
            # =================================================

            report.append(
                "## Overview\n"
            )

            report.append(
                f"User Request:\n{query}\n"
            )

            # =================================================
            # ARCHITECTURE
            # =================================================

            report.append(
                "## Architecture\n"
            )

            if architecture_output:

                architecture_type = (
                    architecture_output.get(
                        "architecture_type",
                        "N/A",
                    )
                )

                report.append(
                    f"Architecture Type: {architecture_type}\n"
                )

                services = (
                    architecture_output.get(
                        "services",
                        [],
                    )
                )

                if services:

                    report.append(
                        "### Services\n"
                    )

                    for service in services:

                        report.append(
                            f"- {service}\n"
                        )

            # =================================================
            # GENERATED FILES
            # =================================================

            report.append(
                "## Generated Files\n"
            )

            if code_output:

                generated_files = (
                    code_output.get(
                        "generated_files",
                        [],
                    )
                )

                for file_data in generated_files:

                    file_path = (
                        file_data.get(
                            "file_path",
                            "",
                        )
                    )

                    purpose = (
                        file_data.get(
                            "purpose",
                            "",
                        )
                    )

                    report.append(
                        f"- {file_path} → {purpose}\n"
                    )

            # =================================================
            # APIs
            # =================================================

            report.append(
                "## APIs\n"
            )

            if code_output:

                apis = (
                    code_output.get(
                        "api_implementations",
                        [],
                    )
                )

                for api in apis:

                    endpoint = api.get(
                        "endpoint",
                        "",
                    )

                    method = api.get(
                        "method",
                        "",
                    )

                    description = api.get(
                        "description",
                        "",
                    )

                    report.append(
                        f"- [{method}] {endpoint} → {description}\n"
                    )

            # =================================================
            # EXECUTION VALIDATION
            # =================================================

            report.append(
                "## Runtime Validation\n"
            )

            if code_output:

                execution_validation = (
                    code_output.get(
                        "execution_validation",
                        {},
                    )
                )

                success = (
                    execution_validation.get(
                        "success",
                        False,
                    )
                )

                return_code = (
                    execution_validation.get(
                        "return_code",
                        -1,
                    )
                )

                report.append(
                    f"Execution Success: {success}\n"
                )

                report.append(
                    f"Return Code: {return_code}\n"
                )

                stderr = (
                    execution_validation.get(
                        "stderr",
                        "",
                    )
                )

                if stderr:

                    report.append(
                        "\n### Runtime Errors\n"
                    )

                    report.append(
                        f"```text\n{stderr}\n```\n"
                    )

            # =================================================
            # RUNTIME REPAIRS
            # =================================================

            report.append(
                "## Runtime Repairs\n"
            )

            if runtime_repairs:

                for repair in runtime_repairs:

                    content = getattr(
                        repair,
                        "content",
                        repair,
                    )

                    strategy = (
                        content.get(
                            "strategy",
                            "unknown",
                        )
                    )

                    report.append(
                        f"- Applied Repair: {strategy}\n"
                    )

            else:

                report.append(
                    "No runtime repairs required.\n"
                )

            # =================================================
            # DEBUGGING INSIGHTS
            # =================================================

            report.append(
                "## Debugging Insights\n"
            )

            if debug_output:

                issues = (
                    debug_output.get(
                        "recommended_fixes",
                        [],
                    )
                )

                if issues:

                    for issue in issues:

                        report.append(
                            f"- {issue}\n"
                        )

            # =================================================
            # REFLECTION
            # =================================================

            report.append(
                "## Reflection Insights\n"
            )

            if reflection_notes:

                for note in reflection_notes:

                    report.append(
                        f"- {note}\n"
                    )

            # =================================================
            # EXECUTION METRICS
            # =================================================

            report.append(
                "## Execution Metrics\n"
            )

            for key, value in metrics.items():

                report.append(
                    f"- {key}: {value}\n"
                )

            # =================================================
            # FINAL RECOMMENDATIONS
            # =================================================

            report.append(
                "## Final Recommendations\n"
            )

            report.append(
                "- Add CI/CD pipelines\n"
            )

            report.append(
                "- Add observability and logging\n"
            )

            report.append(
                "- Add integration testing\n"
            )

            report.append(
                "- Add production monitoring\n"
            )

            report.append(
                "- Add rate limiting and security middleware\n"
            )

            final_output = "\n".join(
                report
            )

            return {

                "success": True,

                "agent":
                    "aggregator_agent",

                "final_output":
                    final_output,
            }

        except Exception as e:

            return {

                "success": False,

                "agent":
                    "aggregator_agent",

                "error":
                    str(e),

                "traceback":
                    traceback.format_exc(),
            }

    # ========================================================
    # FIND AGENT OUTPUT
    # ========================================================

    def _find_agent_output(

        self,

        agent_outputs,

        agent_name,
    ):

        for value in agent_outputs.values():

            if not isinstance(
                value,
                dict,
            ):

                continue

            if (
                value.get("agent")
                == agent_name
            ):

                return value

        return None