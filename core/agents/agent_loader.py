# core/agents/agent_loader.py

"""
CognitiveOS - Agent Loader
---------------------------------------------------------

Responsibilities:
- dynamically load agents
- inject runtime context
- inject skills dynamically
- initialize execution environments
- support dependency injection
- manage reusable instances
- optimize runtime execution
- enable deterministic cognition
- provide runtime diagnostics
- support multi-domain execution

Architecture:

Workflow Executor
        ↓
Agent Loader
        ↓
Agent Registry
        ↓
Skill Loader
        ↓
Agent Instance
"""

from __future__ import annotations

import time
import traceback

from typing import (
    Dict,
    Any,
    Optional,
    List,
)

# ============================================================
# REGISTRY
# ============================================================

from core.agents.agent_registry import (
    get_agent_registry,
)

# ============================================================
# SKILL LOADER
# ============================================================

from core.skills.skill_loader import (
    get_skill_loader,
)

# ============================================================
# AGENT LOADER
# ============================================================


class AgentLoader:

    """
    Production-grade dynamic agent loader.
    """

    def __init__(self):

        self.agent_registry = (
            get_agent_registry()
        )

        self.skill_loader = (
            get_skill_loader()
        )

        # ====================================================
        # CACHE
        # ====================================================

        self.agent_cache: Dict[
            str,
            Any,
        ] = {}

        # ====================================================
        # METRICS
        # ====================================================

        self.loader_metrics = {

            "total_agent_loads": 0,

            "cache_hits": 0,

            "cache_misses": 0,

            "failed_loads": 0,
        }

    # ========================================================
    # LOAD AGENT
    # ========================================================

    def load_agent(
        self,
        agent_name: str,
        use_cache: bool = True,
    ) -> Any:

        start_time = time.time()

        try:

            self.loader_metrics[
                "total_agent_loads"
            ] += 1

            # ================================================
            # CACHE HIT
            # ================================================

            if (

                use_cache

                and agent_name in (
                    self.agent_cache
                )
            ):

                self.loader_metrics[
                    "cache_hits"
                ] += 1

                return self.agent_cache[
                    agent_name
                ]

            # ================================================
            # CACHE MISS
            # ================================================

            self.loader_metrics[
                "cache_misses"
            ] += 1

            # ================================================
            # CREATE AGENT
            # ================================================

            agent = (

                self.agent_registry
                .create_agent(
                    agent_name
                )
            )

            # ================================================
            # AGENT INIT HOOK
            # ================================================

            if hasattr(
                agent,
                "initialize",
            ):

                agent.initialize()

            # ================================================
            # CACHE
            # ================================================

            if use_cache:

                self.agent_cache[
                    agent_name
                ] = agent

            # ================================================
            # PROFILE
            # ================================================

            load_time = (
                time.time() - start_time
            )

            if hasattr(
                agent,
                "_loader_metadata",
            ):

                agent._loader_metadata = {}

            agent._loader_metadata = {

                "loaded_at":
                    time.time(),

                "load_time":
                    load_time,

                "cached":
                    use_cache,
            }

            return agent

        except Exception as e:

            self.loader_metrics[
                "failed_loads"
            ] += 1

            raise RuntimeError(

                f"Failed to load "
                f"agent '{agent_name}': "
                f"{str(e)}"
            )

    # ========================================================
    # LOAD AGENT WITH SKILLS
    # ========================================================

    def load_agent_with_skills(
        self,
        agent_name: str,
        required_skills: Optional[
            List[str]
        ] = None,
        use_cache: bool = True,
    ) -> Dict[str, Any]:

        try:

            # ================================================
            # LOAD AGENT
            # ================================================

            agent = self.load_agent(

                agent_name=agent_name,

                use_cache=use_cache,
            )

            # ================================================
            # LOAD SKILLS
            # ================================================

            skill_result = (

                self.skill_loader
                .load_skills(

                    required_skills or []
                )
            )

            loaded_skills = (

                skill_result.get(
                    "loaded_skills",
                    {},
                )
            )

            failed_skills = (

                skill_result.get(
                    "failed_skills",
                    {},
                )
            )

            # ================================================
            # SKILL INJECTION
            # ================================================

            if hasattr(
                agent,
                "set_skills",
            ):

                agent.set_skills(
                    loaded_skills
                )

            else:

                setattr(

                    agent,

                    "skills",

                    loaded_skills,
                )

            # ================================================
            # AGENT METADATA
            # ================================================

            metadata = (

                self.agent_registry
                .get_agent_metadata(
                    agent_name
                )
            )

            return {

                "success":
                    True,

                "agent":
                    agent,

                "skills":
                    loaded_skills,

                "failed_skills":
                    failed_skills,

                "metadata":
                    metadata,
            }

        except Exception as e:

            return {

                "success":
                    False,

                "error":
                    str(e),

                "traceback":
                    traceback.format_exc(),
            }

    # ========================================================
    # BUILD EXECUTION CONTEXT
    # ========================================================

    def build_execution_context(
        self,
        workflow_step,
        global_context: Dict[
            str,
            Any,
        ],
    ) -> Dict[str, Any]:

        try:

            # ================================================
            # LOAD AGENT + SKILLS
            # ================================================

            load_result = (

                self
                .load_agent_with_skills(

                    workflow_step.agent,

                    getattr(workflow_step, "required_skills", [])
                )
            )

            if not load_result.get(
                "success"
            ):

                raise RuntimeError(

                    load_result.get(
                        "error"
                    )
                )

            # ================================================
            # EXECUTION CONTEXT
            # ================================================

            execution_context = {

                # ============================================
                # AGENT
                # ============================================

                "agent":
                    load_result[
                        "agent"
                    ],

                # ============================================
                # SKILLS
                # ============================================

                "skills":
                    load_result[
                        "skills"
                    ],

                # ============================================
                # SKILL FAILURES
                # ============================================

                "failed_skills":
                    load_result.get(
                        "failed_skills",
                        {},
                    ),

                # ============================================
                # AGENT METADATA
                # ============================================

                "agent_metadata":
                    load_result.get(
                        "metadata",
                        {},
                    ),

                # ============================================
                # WORKFLOW
                # ============================================

                "workflow_step":
                    workflow_step,

                # ============================================
                # QUERY
                # ============================================

                "query":
                    global_context.get(
                        "query",
                        "",
                    ),

                # ============================================
                # TASK
                # ============================================

                "task":
                    workflow_step.task,

                # ============================================
                # ARTIFACTS
                # ============================================

                "artifacts":
                    global_context.get(
                        "artifacts",
                        [],
                    ),

                # ============================================
                # AGENT OUTPUTS
                # ============================================

                "agent_outputs":
                    global_context.get(
                        "agent_outputs",
                        {},
                    ),

                # ============================================
                # SHARED CONTEXT
                # ============================================

                "shared_context":
                    global_context.get(
                        "shared_context",
                        {},
                    ),

                # ============================================
                # EXECUTION STRATEGY
                # ============================================

                "runtime_backend":
                    workflow_step.runtime_backend,

                "execution_mode":
                    workflow_step.execution_mode,

                "deterministic_execution":
                    (
                        workflow_step
                        .deterministic_execution
                    ),

                # ============================================
                # LOADER METADATA
                # ============================================

                "loader_metrics":
                    self.loader_metrics,
            }

            return execution_context

        except Exception as e:

            return {

                "success":
                    False,

                "error":
                    str(e),

                "traceback":
                    traceback.format_exc(),
            }

    # ========================================================
    # PRELOAD AGENTS
    # ========================================================

    def preload_agents(
        self,
        agent_names: List[str],
    ) -> Dict[str, Any]:

        loaded = []

        failed = []

        for agent_name in agent_names:

            try:

                self.load_agent(
                    agent_name
                )

                loaded.append(
                    agent_name
                )

            except Exception as e:

                failed.append(

                    {

                        "agent":
                            agent_name,

                        "error":
                            str(e),
                    }
                )

        return {

            "loaded":
                loaded,

            "failed":
                failed,
        }

    # ========================================================
    # CLEAR CACHE
    # ========================================================

    def clear_cache(
        self,
    ):

        self.agent_cache.clear()

    # ========================================================
    # REMOVE AGENT FROM CACHE
    # ========================================================

    def remove_from_cache(
        self,
        agent_name: str,
    ):

        if agent_name in (
            self.agent_cache
        ):

            del self.agent_cache[
                agent_name
            ]

    # ========================================================
    # CACHE INFO
    # ========================================================

    def cache_info(
        self,
    ) -> Dict[str, Any]:

        return {

            "cached_agents":
                len(self.agent_cache),

            "agents":
                list(
                    self.agent_cache.keys()
                ),
        }

    # ========================================================
    # EXPORT LOADER STATE
    # ========================================================

    def export_state(
        self,
    ) -> Dict[str, Any]:

        return {

            "registered_agents":

                self.agent_registry
                .export_registry(),

            "cached_agents":

                list(
                    self.agent_cache.keys()
                ),

            "metrics":
                self.loader_metrics,
        }

    # ========================================================
    # AGENT CAPABILITIES
    # ========================================================

    def get_agent_capabilities(
        self,
        agent_name: str,
    ) -> Dict[str, Any]:

        metadata = (

            self.agent_registry
            .get_agent_metadata(
                agent_name
            )
        )

        return {

            "agent":
                agent_name,

            "metadata":
                metadata,

            "cached":
                (
                    agent_name
                    in self.agent_cache
                ),
        }

    # ========================================================
    # HEALTHCHECK
    # ========================================================

    def healthcheck(
        self,
    ) -> Dict[str, Any]:

        return {

            "status":
                "healthy",

            "registered_agents":

                (
                    self.agent_registry
                    .healthcheck()
                ),

            "cached_agents":
                len(self.agent_cache),

            "metrics":
                self.loader_metrics,
        }


# ============================================================
# GLOBAL LOADER
# ============================================================

GLOBAL_AGENT_LOADER = (
    AgentLoader()
)

# ============================================================
# FACTORY
# ============================================================


def get_agent_loader():

    return GLOBAL_AGENT_LOADER