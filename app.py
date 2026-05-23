# app.py

"""
CognitiveOS - Autonomous Cognitive Runtime
---------------------------------------------------------

UPDATED ENTRYPOINT ARCHITECTURE

app.py
    ↓
MasterOrchestrator
    ↓
DomainRouter
    ↓
DomainSupervisor
    ↓
WorkflowExecutor
    ↓
Agents + Skills

Responsibilities:
- provide runtime dashboard
- visualize cognition lifecycle
- visualize orchestration
- display routing
- display supervisors
- display runtime execution
- display artifacts
- show reflection + quality
- support multi-domain execution

Run:

streamlit run app.py
"""

from __future__ import annotations

import os
import io
import zipfile
import asyncio
import warnings
import logging

from datetime import datetime

import streamlit as st

# ============================================================
# SILENCE WARNINGS
# ============================================================

os.environ[
    "TRANSFORMERS_VERBOSITY"
] = "error"

os.environ[
    "TOKENIZERS_PARALLELISM"
] = "false"

warnings.filterwarnings(
    "ignore"
)

logging.getLogger(
    "transformers"
).setLevel(logging.ERROR)

logging.getLogger(
    "torch"
).setLevel(logging.ERROR)

logging.getLogger(
    "sentence_transformers"
).setLevel(logging.ERROR)

# ============================================================
# MASTER ORCHESTRATOR
# ============================================================

from core.orchestration.master_orchestration import (
    MasterOrchestrator,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="CognitiveOS",

    page_icon="🧠",

    layout="wide",
)

# ============================================================
# SESSION STATE
# ============================================================

if "execution_history" not in st.session_state:

    st.session_state.execution_history = []

# ============================================================
# TITLE
# ============================================================

st.title(
    "🧠 CognitiveOS"
)

st.markdown(
    """
Autonomous Multi-Domain Cognitive Runtime
"""
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "System Status"
    )

    st.success(
        "CognitiveOS Active"
    )

    st.markdown("---")

    st.subheader(
        "Execution Mode"
    )

    execution_mode = st.selectbox(

        "Select Mode",

        [

            "Fast",

            "Balanced",

            "Autonomous Repair",
        ],
    )

    st.markdown("---")

    st.subheader(
        "Execution Strategy"
    )

    enable_multi_domain = st.checkbox(

        "Enable Multi-Domain Execution",

        value=False,
    )

    st.markdown("---")

    st.subheader(
        "Available Domains"
    )

    st.markdown(
        """
- AI Engineering
- CyberSecurity
- Data Science
- DevOps
- Research
"""
    )

    st.markdown("---")

    st.subheader(
        "Execution History"
    )

    st.metric(

        "Executions",

        len(
            st.session_state
            .execution_history
        ),
    )

# ============================================================
# USER INPUT
# ============================================================

query = st.text_area(

    "Enter your task",

    height=200,

    placeholder="""
Examples:

1. Build scalable RAG pipeline using Llama and ChromaDB

2. Train fraud detection model and deploy on Kubernetes

3. Perform vulnerability analysis on JWT authentication

4. Generate literature review on multi-agent systems
""",
)

# ============================================================
# EXECUTION BUTTON
# ============================================================

execute_button = st.button(

    "Execute CognitiveOS",

    use_container_width=True,
)

# ============================================================
# EXECUTION
# ============================================================

if execute_button:

    if not query.strip():

        st.warning(
            "Please enter a query."
        )

        st.stop()

    # ========================================================
    # ORCHESTRATOR
    # ========================================================

    orchestrator = (
        MasterOrchestrator()
    )

    # ========================================================
    # EXECUTION STATUS UI
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Cognitive Runtime Lifecycle"
    )

    routing_status = st.empty()

    supervisor_status = st.empty()

    execution_status = st.empty()

    reflection_status = st.empty()

    aggregation_status = st.empty()

    runtime_status = st.empty()

    # ========================================================
    # EXECUTION FUNCTION
    # ========================================================

    async def run_execution():

        routing_status.info(
            "🧭 Routing Query..."
        )

        supervisor_status.info(
            "🧩 Initializing Supervisor..."
        )

        execution_status.info(
            "⚙️ Executing Workflow..."
        )

        reflection_status.info(
            "🔍 Reflection Pending..."
        )

        aggregation_status.info(
            "📦 Aggregating Outputs..."
        )

        runtime_status.info(
            "🚀 Runtime Initializing..."
        )

        # ====================================================
        # EXECUTION
        # ====================================================

        result = await (

            orchestrator.execute(

                query=query,

                enable_multi_domain=
                    enable_multi_domain,
            )
        )

        # ====================================================
        # COMPLETE STATUS
        # ====================================================

        routing_status.success(
            "✓ Routing Complete"
        )

        supervisor_status.success(
            "✓ Supervisor Ready"
        )

        execution_status.success(
            "✓ Workflow Executed"
        )

        reflection_status.success(
            "✓ Reflection Complete"
        )

        aggregation_status.success(
            "✓ Outputs Aggregated"
        )

        runtime_status.success(
            "✓ Runtime Complete"
        )

        return result

    # ========================================================
    # EXECUTE
    # ========================================================

    start_time = datetime.now()

    with st.spinner(
        "CognitiveOS Running..."
    ):

        orchestration_result = (
            asyncio.run(
                run_execution()
            )
        )

    end_time = datetime.now()

    total_execution_time = (

        end_time - start_time

    ).total_seconds()

    # ========================================================
    # FAILURE
    # ========================================================

    if not orchestration_result.success:

        st.error(
            "Execution Failed"
        )

        st.exception(

            orchestration_result
            .output
        )

        st.stop()

    # ========================================================
    # OUTPUT
    # ========================================================

    output = (
        orchestration_result.output
    )

    # ========================================================
    # STORE HISTORY
    # ========================================================

    st.session_state.execution_history.append(

        {

            "query":
                query,

            "output":
                output,
        }
    )

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown("---")

    st.header(
        "Execution Result"
    )

    # ========================================================
    # MODE
    # ========================================================

    st.subheader(
        "Execution Mode"
    )

    st.info(
        output.get(
            "mode",
            "single_domain",
        )
    )

    # ========================================================
    # DOMAIN
    # ========================================================

    if output.get("mode") == "single_domain":

        st.subheader(
            "Selected Domain"
        )

        st.success(

            output.get(
                "selected_domain",
                "unknown",
            )
        )

        st.subheader(
            "Routing Confidence"
        )

        st.metric(

            "Confidence",

            round(

                output.get(
                    "routing_confidence",
                    0.0,
                ),

                2,
            ),
        )

    # ========================================================
    # MULTI DOMAIN
    # ========================================================

    else:

        st.subheader(
            "Multi-Domain Execution"
        )

        domains = output.get(
            "domain_outputs",
            [],
        )

        for domain_result in domains:

            st.success(

                f"{domain_result['domain']} "
                f"✓"
            )

    # ========================================================
    # EXECUTION METRICS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Runtime Metrics"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Execution Time",

            f"{total_execution_time:.2f}s",
        )

    with col2:

        workflow_size = 0

        if (

            output.get("mode")
            == "single_domain"

        ):

            workflow_size = (

                output
                .get(
                    "supervision",
                    {},
                )
                .get(
                    "workflow_size",
                    0,
                )
            )

        st.metric(

            "Workflow Steps",

            workflow_size,
        )

    with col3:

        st.metric(

            "Multi Domain",

            str(
                enable_multi_domain
            ),
        )

    # ========================================================
    # SINGLE DOMAIN OUTPUT
    # ========================================================

    if output.get("mode") == "single_domain":

        execution = output.get(
            "execution",
            {},
        )

        execution_output = execution.get(
            "output",
            {},
        )

        # ====================================================
        # EXECUTION TRACE
        # ====================================================

        st.markdown("---")

        st.subheader(
            "Execution Trace"
        )

        trace = execution_output.get(
            "execution_trace",
            [],
        )

        if trace:

            for step in trace:

                success = step.get(
                    "success",
                    False,
                )

                if success:

                    st.success(step)

                else:

                    st.error(step)

        else:

            st.info(
                "No execution trace available."
            )

        # ====================================================
        # AGENT OUTPUTS
        # ====================================================

        st.markdown("---")

        st.subheader(
            "Agent Outputs"
        )

        agent_outputs = (

            execution_output.get(
                "agent_outputs",
                {},
            )
        )

        if agent_outputs:

            for agent_name, agent_output in (
                agent_outputs.items()
            ):

                with st.expander(
                    agent_name,
                    expanded=False,
                ):

                    st.json(
                        agent_output
                    )

        # ====================================================
        # TELEMETRY
        # ====================================================

        st.markdown("---")

        st.subheader(
            "Execution Telemetry"
        )

        telemetry = execution_output.get(
            "telemetry",
            {},
        )

        st.json(
            telemetry
        )

        # ====================================================
        # ARTIFACTS
        # ====================================================

        st.markdown("---")

        st.subheader(
            "Artifacts"
        )

        artifacts = execution_output.get(
            "artifacts",
            [],
        )

        if artifacts:

            st.json(
                artifacts
            )

        else:

            st.info(
                "No artifacts generated."
            )

        # ====================================================
        # REFLECTION
        # ====================================================

        st.markdown("---")

        st.subheader(
            "Reflection Summary"
        )

        reflection = execution_output.get(
            "reflection",
            "",
        )

        st.info(
            reflection
        )

        # ====================================================
        # DEBUG
        # ====================================================

        st.markdown("---")

        st.subheader(
            "Debug Validation"
        )

        debug = execution_output.get(
            "debug",
            {},
        )

        st.json(debug)

    # ========================================================
    # MULTI DOMAIN OUTPUT
    # ========================================================

    else:

        st.markdown("---")

        st.subheader(
            "Multi-Domain Outputs"
        )

        domain_outputs = output.get(
            "domain_outputs",
            [],
        )

        for domain_result in (
            domain_outputs
        ):

            with st.expander(

                domain_result[
                    "domain"
                ],

                expanded=False,
            ):

                st.json(
                    domain_result
                )

    # ========================================================
    # DOWNLOAD REPOSITORY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Download Workspace"
    )

    zip_buffer = io.BytesIO()

    workspace_path = (
        "workspace/current_project"
    )

    if os.path.exists(
        workspace_path
    ):

        with zipfile.ZipFile(

            zip_buffer,

            "w",

            zipfile.ZIP_DEFLATED,
        ) as zip_file:

            for root, dirs, files in os.walk(
                workspace_path
            ):

                for file in files:

                    file_path = os.path.join(
                        root,
                        file,
                    )

                    archive_name = (
                        os.path.relpath(

                            file_path,

                            workspace_path,
                        )
                    )

                    zip_file.write(

                        file_path,

                        archive_name,
                    )

        st.download_button(

            label=
                "⬇ Download Workspace",

            data=
                zip_buffer.getvalue(),

            file_name=
                "cognitiveos_workspace.zip",

            mime=
                "application/zip",

            use_container_width=True,
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "CognitiveOS • Autonomous Multi-Domain Cognitive Runtime"
)