# core/skills/skill_loader.py

"""
CognitiveOS - Skill Loader
---------------------------------------------------------

Responsibilities:
- dynamically load skills
- cache reusable skills
- inject skills into agents
- support multi-domain execution
- optimize runtime performance
- enable deterministic cognition

Architecture:

Agents
    ↓
Skill Loader
    ↓
Skill Registry
    ↓
Skill Instances
"""

from __future__ import annotations

import traceback

from typing import (
    Dict,
    Any,
    List,
    Optional,
)

# ============================================================
# REGISTRY
# ============================================================

from core.skills.skill_registry import (
    get_skill_registry,
)

# ============================================================
# SKILL LOADER
# ============================================================


class SkillLoader:

    """
    Dynamic skill loading system.
    """

    def __init__(self):

        self.skill_registry = (
            get_skill_registry()
        )

        # ====================================================
        # SKILL CACHE
        # ====================================================

        self.skill_cache: Dict[
            str,
            Any,
        ] = {}

    # ========================================================
    # LOAD SINGLE SKILL
    # ========================================================

    def load_skill(
        self,
        skill_name: str,
        use_cache: bool = True,
    ) -> Any:

        try:

            # ================================================
            # CACHE HIT
            # ================================================

            if (

                use_cache

                and skill_name in (
                    self.skill_cache
                )
            ):

                return self.skill_cache[
                    skill_name
                ]

            # ================================================
            # CREATE SKILL
            # ================================================

            skill = (

                self.skill_registry
                .create_skill(
                    skill_name
                )
            )

            # ================================================
            # CACHE
            # ================================================

            if use_cache:

                self.skill_cache[
                    skill_name
                ] = skill

            return skill

        except Exception as e:

            raise RuntimeError(

                f"Failed to load "
                f"skill '{skill_name}': "
                f"{str(e)}"
            )

    # ========================================================
    # LOAD MULTIPLE SKILLS
    # ========================================================

    def load_skills(
        self,
        skill_names: List[str],
        use_cache: bool = True,
    ) -> Dict[str, Any]:

        loaded_skills = {}

        failed_skills = {}

        for skill_name in skill_names:

            try:

                skill = self.load_skill(

                    skill_name=skill_name,

                    use_cache=use_cache,
                )

                loaded_skills[
                    skill_name
                ] = skill

            except Exception as e:

                failed_skills[
                    skill_name
                ] = str(e)

        return {

            "success":
                len(failed_skills) == 0,

            "loaded_skills":
                loaded_skills,

            "failed_skills":
                failed_skills,
        }

    # ========================================================
    # BUILD SKILL CONTEXT
    # ========================================================

    def build_skill_context(
        self,
        required_skills: List[str],
        global_context: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        try:

            global_context = (
                global_context or {}
            )

            # ================================================
            # LOAD SKILLS
            # ================================================

            skill_result = self.load_skills(

                required_skills
            )

            skill_context = {

                "skills":
                    skill_result.get(
                        "loaded_skills",
                        {},
                    ),

                "skill_count":
                    len(
                        skill_result.get(
                            "loaded_skills",
                            {},
                        )
                    ),

                "failed_skills":
                    skill_result.get(
                        "failed_skills",
                        {},
                    ),

                "shared_context":
                    global_context.get(
                        "shared_context",
                        {},
                    ),

                "artifacts":
                    global_context.get(
                        "artifacts",
                        [],
                    ),

                "agent_outputs":
                    global_context.get(
                        "agent_outputs",
                        {},
                    ),
            }

            return {

                "success":
                    True,

                "skill_context":
                    skill_context,
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
    # EXECUTE SKILL METHOD
    # ========================================================

    async def execute_skill_method(
        self,
        skill_name: str,
        method_name: str,
        *args,
        **kwargs,
    ) -> Dict[str, Any]:

        try:

            # ================================================
            # LOAD SKILL
            # ================================================

            skill = self.load_skill(
                skill_name
            )

            # ================================================
            # VALIDATE METHOD
            # ================================================

            if not hasattr(
                skill,
                method_name,
            ):

                raise AttributeError(

                    f"Method '{method_name}' "
                    f"not found in skill "
                    f"'{skill_name}'"
                )

            method = getattr(
                skill,
                method_name,
            )

            # ================================================
            # EXECUTE
            # ================================================

            if callable(method):

                result = await method(
                    *args,
                    **kwargs,
                )

            else:

                result = method

            return {

                "success":
                    True,

                "skill":
                    skill_name,

                "method":
                    method_name,

                "result":
                    result,
            }

        except Exception as e:

            return {

                "success":
                    False,

                "skill":
                    skill_name,

                "method":
                    method_name,

                "error":
                    str(e),

                "traceback":
                    traceback.format_exc(),
            }

    # ========================================================
    # CLEAR CACHE
    # ========================================================

    def clear_cache(
        self,
    ):

        self.skill_cache.clear()

    # ========================================================
    # REMOVE SKILL FROM CACHE
    # ========================================================

    def remove_from_cache(
        self,
        skill_name: str,
    ):

        if skill_name in (
            self.skill_cache
        ):

            del self.skill_cache[
                skill_name
            ]

    # ========================================================
    # CACHE INFO
    # ========================================================

    def cache_info(
        self,
    ) -> Dict[str, Any]:

        return {

            "cached_skills":
                len(self.skill_cache),

            "skills": list(

                self.skill_cache.keys()
            ),
        }

    # ========================================================
    # EXPORT STATE
    # ========================================================

    def export_state(
        self,
    ) -> Dict[str, Any]:

        return {

            "registered_skills":

                self.skill_registry
                .export_registry(),

            "cached_skills":

                list(
                    self.skill_cache.keys()
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

            "registered_skills":

                (
                    self.skill_registry
                    .healthcheck()
                ),

            "cached_skills":
                len(self.skill_cache),
        }


# ============================================================
# GLOBAL LOADER
# ============================================================

GLOBAL_SKILL_LOADER = (
    SkillLoader()
)

# ============================================================
# FACTORY
# ============================================================


def get_skill_loader():

    return GLOBAL_SKILL_LOADER