# app.py

"""
CognitiveOS - Autonomous Runtime Dashboard
---------------------------------------------------------

Responsibilities:
- provide UI for CognitiveOS
- visualize execution lifecycle
- display runtime cognition
- render generated repositories
- show execution timeline
- display runtime validation
- show patch history
- render artifacts
- display reflection insights

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

warnings.filterwarnings("ignore")

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
# IMPORT COGNITIVE GRAPH
# ============================================================

from core.cognitive_graph import (
    CognitiveGraph,
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
Autonomous Software Engineering Runtime
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
        "Domains"
    )

    st.markdown(
        """
- Software Engineering
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

    height=180,

    placeholder="""
Example:

Build a scalable FastAPI backend
for real-time chat with JWT auth,
Redis caching, Docker deployment,
and websocket support.
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
    # GRAPH
    # ========================================================

    graph = CognitiveGraph()

    # ========================================================
    # EXECUTION LIFECYCLE UI
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Execution Lifecycle"
    )

    planner_status = st.empty()

    supervisor_status = st.empty()

    executor_status = st.empty()

    reflection_status = st.empty()

    aggregation_status = st.empty()

    runtime_status = st.empty()

    # ========================================================
    # EXECUTION FUNCTION
    # ========================================================

    async def run_execution():

        planner_status.info(
            "🧠 Planning..."
        )

        supervisor_status.info(
            "🧩 Supervisor Initializing..."
        )

        executor_status.info(
            "⚙️ Runtime Executor Starting..."
        )

        reflection_status.info(
            "🔍 Reflection Waiting..."
        )

        aggregation_status.info(
            "📦 Aggregation Waiting..."
        )

        runtime_status.info(
            "🚀 Runtime Waiting..."
        )

        # ====================================================
        # EXECUTE GRAPH
        # ====================================================

        result = await graph.execute(
            query
        )

        # ====================================================
        # STATUS COMPLETE
        # ====================================================

        planner_status.success(
            "✓ Planning Complete"
        )

        supervisor_status.success(
            "✓ Workflow Generated"
        )

        executor_status.success(
            "✓ Runtime Execution Complete"
        )

        reflection_status.success(
            "✓ Reflection Complete"
        )

        aggregation_status.success(
            "✓ Aggregation Complete"
        )

        runtime_status.success(
            "✓ Runtime Validation Complete"
        )

        return result

    # ========================================================
    # EXECUTE
    # ========================================================

    start_time = datetime.now()

    with st.spinner(
        "CognitiveOS Running..."
    ):

        runtime_state = asyncio.run(
            run_execution()
        )

    end_time = datetime.now()

    total_execution_time = (
        end_time - start_time
    ).total_seconds()

    # ========================================================
    # STORE HISTORY
    # ========================================================

    st.session_state.execution_history.append(

        {

            "query":
                query,

            "result":
                runtime_state.final_output,
        }
    )

    # ========================================================
    # EXECUTION RESULT
    # ========================================================

    execution_result = (
        runtime_state.execution_result
    )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    st.markdown("---")

    st.header(
        "Final Response"
    )

    st.markdown(
        runtime_state.final_output
    )

    # ========================================================
    # EXECUTION METRICS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Runtime Metrics"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Execution Time",

            f"{total_execution_time:.2f}s",
        )

    with col2:

        st.metric(

            "Artifacts",

            len(
                execution_result.get(
                    "artifacts",
                    [],
                )
            ),
        )

    with col3:

        st.metric(

            "Logs",

            len(
                execution_result.get(
                    "execution_logs",
                    [],
                )
            ),
        )

    with col4:

        runtime_health = (
            execution_result.get(
                "runtime_health_score",
                "medium",
            )
        )

        st.metric(

            "Runtime Health",

            runtime_health,
        )

    # ========================================================
    # EXECUTION TIMELINE
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Execution Timeline"
    )

    timeline = execution_result.get(
        "execution_timeline",
        [],
    )

    if timeline:

        for event in timeline:

            event_type = event.get(
                "event",
                ""
            )

            if "failed" in event_type:

                st.error(event)

            elif "runtime_failure" in event_type:

                st.warning(event)

            elif "completed" in event_type:

                st.success(event)

            else:

                st.info(event)

    else:

        st.info(
            "No execution timeline available."
        )

    # ========================================================
    # GENERATED FILES
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Generated Repository"
    )

    generated_files = execution_result.get(
        "generated_files",
        [],
    )

    if generated_files:

        for file in generated_files:

            file_path = file.get(
                "path",
                "unknown.py"
            )

            content = file.get(
                "content",
                ""
            )

            language = "python"

            if file_path.endswith(".json"):

                language = "json"

            elif file_path.endswith(".yml"):

                language = "yaml"

            elif file_path.endswith(".md"):

                language = "markdown"

            with st.expander(
                file_path,
                expanded=False,
            ):

                st.code(
                    content,
                    language=language,
                )

    else:

        st.info(
            "No generated files available."
        )

    # ========================================================
    # WORKSPACE TREE
    # ========================================================

    st.markdown("---")

    with st.expander(
        "Workspace Tree",
        expanded=False,
    ):

        workspace_snapshot = (
            execution_result.get(
                "workspace_snapshot",
                [],
            )
        )

        st.json(
            workspace_snapshot
        )

    # ========================================================
    # RUNTIME VALIDATION
    # ========================================================

    st.markdown("---")

    with st.expander(
        "Runtime Validation",
        expanded=False,
    ):

        runtime_validation = (
            execution_result.get(
                "runtime_validation",
                {},
            )
        )

        stdout = runtime_validation.get(
            "stdout",
            ""
        )

        stderr = runtime_validation.get(
            "stderr",
            ""
        )

        return_code = (
            runtime_validation.get(
                "return_code",
                -1,
            )
        )

        st.subheader(
            "Return Code"
        )

        st.write(return_code)

        st.subheader(
            "STDOUT"
        )

        st.code(stdout)

        st.subheader(
            "STDERR"
        )

        if stderr:

            st.error(stderr)

        else:

            st.success(
                "No runtime errors detected."
            )

    # ========================================================
    # PATCH HISTORY
    # ========================================================

    st.markdown("---")

    with st.expander(
        "Patch History",
        expanded=False,
    ):

        patch_history = (
            execution_result.get(
                "patch_history",
                [],
            )
        )

        if patch_history:

            for patch in patch_history:

                st.warning(
                    patch
                )

        else:

            st.success(
                "No patches applied."
            )

    # ========================================================
    # ARTIFACTS
    # ========================================================

    st.markdown("---")

    with st.expander(
        "Artifacts",
        expanded=False,
    ):

        st.json(
            execution_result.get(
                "artifacts",
                [],
            )
        )

    # ========================================================
    # EXECUTION LOGS
    # ========================================================

    st.markdown("---")

    with st.expander(
        "Execution Logs",
        expanded=False,
    ):

        st.json(
            execution_result.get(
                "execution_logs",
                [],
            )
        )

    # ========================================================
    # REFLECTION NOTES
    # ========================================================

    st.markdown("---")

    with st.expander(
        "Reflection Notes",
        expanded=False,
    ):

        st.json(
            execution_result.get(
                "reflection_notes",
                [],
            )
        )

    # ========================================================
    # DOWNLOAD GENERATED REPOSITORY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Download Repository"
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

                    archive_name = os.path.relpath(
                        file_path,
                        workspace_path,
                    )

                    zip_file.write(
                        file_path,
                        archive_name,
                    )

        st.download_button(

            label=
                "⬇ Download Repository",

            data=
                zip_buffer.getvalue(),

            file_name=
                "cognitiveos_project.zip",

            mime=
                "application/zip",

            use_container_width=True,
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "CognitiveOS • Autonomous Software Engineering Runtime"
)