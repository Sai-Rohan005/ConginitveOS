# app.py

"""
CognitiveOS - Streamlit App
---------------------------------------------------------

Responsibilities:
- provide UI for CognitiveOS
- execute cognitive workflows
- visualize execution lifecycle
- display agent outputs
- show execution logs
- display artifacts
- render final response

Run:

streamlit run app.py
"""

from __future__ import annotations

import asyncio
import streamlit as st

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
Autonomous Cognitive Runtime System
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

    st.write(
        len(
            st.session_state
            .execution_history
        ),
        "executions"
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
    # CREATE GRAPH
    # ========================================================

    graph = CognitiveGraph()

    # ========================================================
    # EXECUTION UI
    # ========================================================

    st.markdown("---")

    st.subheader(
        "Execution Lifecycle"
    )

    execution_container = st.container()

    with execution_container:

        planner_status = st.empty()

        supervisor_status = st.empty()

        executor_status = st.empty()

        reflection_status = st.empty()

        aggregation_status = st.empty()

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
            "⚙️ Executor Waiting..."
        )

        reflection_status.info(
            "🔍 Reflection Waiting..."
        )

        aggregation_status.info(
            "📦 Aggregation Waiting..."
        )

        # ====================================================
        # EXECUTE GRAPH
        # ====================================================

        result = await graph.execute(
            query
        )

        # ====================================================
        # UPDATE STATUS
        # ====================================================

        planner_status.success(
            "✓ Planning Complete"
        )

        supervisor_status.success(
            "✓ Workflow Generated"
        )

        executor_status.success(
            "✓ Agent Execution Complete"
        )

        reflection_status.success(
            "✓ Reflection Cycle Complete"
        )

        aggregation_status.success(
            "✓ Final Aggregation Complete"
        )

        return result

    # ========================================================
    # RUN EXECUTION
    # ========================================================

    with st.spinner(
        "CognitiveOS Running..."
    ):

        runtime_state = asyncio.run(
            run_execution()
        )

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
    # FINAL OUTPUT
    # ========================================================

    st.markdown("---")

    st.header(
        "Final Response"
    )

    st.markdown(
        runtime_state.final_output
    )

    # ========================================================
    # EXECUTION DETAILS
    # ========================================================

    st.markdown("---")

    with st.expander(
        "Execution Metadata",
        expanded=False,
    ):

        st.json(
            runtime_state.metadata
        )

    # ========================================================
    # AGENT OUTPUTS
    # ========================================================

    with st.expander(
        "Agent Outputs",
        expanded=False,
    ):

        st.json(
            runtime_state.execution_result.get(
                "agent_outputs",
                {},
            )
        )

    # ========================================================
    # ARTIFACTS
    # ========================================================

    with st.expander(
        "Artifacts",
        expanded=False,
    ):

        st.json(
            runtime_state.execution_result.get(
                "artifacts",
                [],
            )
        )

    # ========================================================
    # EXECUTION LOGS
    # ========================================================

    with st.expander(
        "Execution Logs",
        expanded=False,
    ):

        st.json(
            runtime_state.execution_result.get(
                "execution_logs",
                [],
            )
        )

    # ========================================================
    # REFLECTION NOTES
    # ========================================================

    with st.expander(
        "Reflection Notes",
        expanded=False,
    ):

        st.json(
            runtime_state.execution_result.get(
                "reflection_notes",
                [],
            )
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "CognitiveOS • Autonomous Cognitive Runtime"
)