# domains/cybersecurity/agents/authsecurity_agent.py

"""
CognitiveOS - Authentication Security Agent
---------------------------------------------------------

Responsibilities:
- analyze authentication systems
- validate JWT security
- detect auth vulnerabilities
- design secure auth architectures
- validate OAuth2/OpenID flows
- detect insecure token handling
- recommend security hardening
- assess session management

This agent behaves like:
- Application Security Engineer
- IAM Security Architect
- Red Team Engineer
- Zero Trust Security Engineer
"""

from __future__ import annotations

import os
import traceback

from typing import (
    Dict,
    Any,
)

from dataclasses import (
    dataclass,
    field,
)

import dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain_core.output_parsers import (
    JsonOutputParser,
)

dotenv.load_dotenv()

api_key = os.getenv(
    "GOOGLE_API_KEY"
)

# ============================================================
# STATE
# ============================================================


@dataclass
class AuthSecurityAgentState:

    query: str

    task: str

    architecture_context: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    previous_outputs: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    artifacts: Dict[
        str,
        Any,
    ] = field(default_factory=dict)

    output: Dict[
        str,
        Any,
    ] = field(default_factory=dict)


# ============================================================
# AUTH SECURITY AGENT
# ============================================================


class AuthSecurityAgent:

    """
    Production-grade authentication
    security analysis agent.
    """

    def __init__(self):

        self.model = os.getenv(

            "GOOGLE_MODEL",

            "gemini-2.0-flash",
        )

        self.llm = ChatGoogleGenerativeAI(

            model=self.model,

            google_api_key=api_key,

            temperature=0.1,
        )

        self.parser = JsonOutputParser()

        # ====================================================
        # PROMPT
        # ====================================================

        self.prompt = (

            ChatPromptTemplate.from_messages(

                [

                    (

                        "system",

                        self._system_prompt(),
                    ),

                    (

                        "human",

                        """
User Query:
{query}

Assigned Task:
{task}

Architecture Context:
{architecture_context}

Previous Outputs:
{previous_outputs}

Artifacts:
{artifacts}
                        """,
                    ),
                ]
            )
        )

        # ====================================================
        # CHAIN
        # ====================================================

        self.chain = (

            self.prompt

            | self.llm

            | self.parser
        )

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    async def run(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        try:

            result = await (

                self.chain.ainvoke(

                    {

                        "query":
                            context.get(
                                "query",
                                "",
                            ),

                        "task":
                            context.get(
                                "task",
                                "",
                            ),

                        "architecture_context":
                            str(
                                context.get(
                                    "shared_context",
                                    {},
                                )
                            ),

                        "previous_outputs":
                            str(
                                context.get(
                                    "agent_outputs",
                                    {},
                                )
                            ),

                        "artifacts":
                            str(
                                context.get(
                                    "artifacts",
                                    {},
                                )
                            ),
                    }
                )
            )

            # =================================================
            # SAFE EXTRACTION
            # =================================================

            authentication_architecture = result.get(
                "authentication_architecture",
                {},
            )

            jwt_security = result.get(
                "jwt_security",
                {},
            )

            oauth_analysis = result.get(
                "oauth_analysis",
                {},
            )

            session_security = result.get(
                "session_security",
                {},
            )

            zero_trust_analysis = result.get(
                "zero_trust_analysis",
                {},
            )

            vulnerabilities = result.get(
                "vulnerabilities",
                [],
            )

            attack_vectors = result.get(
                "attack_vectors",
                [],
            )

            mitigations = result.get(
                "mitigations",
                [],
            )

            security_headers = result.get(
                "security_headers",
                [],
            )

            rate_limiting = result.get(
                "rate_limiting",
                {},
            )

            token_lifecycle = result.get(
                "token_lifecycle",
                {},
            )

            production_readiness = result.get(
                "production_readiness",
                "",
            )

            overall_risk = result.get(
                "overall_risk",
                "medium",
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "authsecurity_agent",

                "authentication_architecture":
                    authentication_architecture,

                "jwt_security":
                    jwt_security,

                "oauth_analysis":
                    oauth_analysis,

                "session_security":
                    session_security,

                "zero_trust_analysis":
                    zero_trust_analysis,

                "vulnerabilities":
                    vulnerabilities,

                "attack_vectors":
                    attack_vectors,

                "mitigations":
                    mitigations,

                "security_headers":
                    security_headers,

                "rate_limiting":
                    rate_limiting,

                "token_lifecycle":
                    token_lifecycle,

                "production_readiness":
                    production_readiness,

                "overall_risk":
                    overall_risk,

                "reasoning":
                    reasoning,
            }

        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            return {

                "success": False,

                "agent":
                    "authsecurity_agent",

                "error":
                    str(e),

                "traceback":
                    traceback.format_exc(),
            }

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    def _system_prompt(self):

        return """
You are the Authentication Security Agent
for CognitiveOS.

Your role is to:
- analyze authentication systems
- validate JWT implementations
- detect auth vulnerabilities
- secure session management
- validate OAuth2/OpenID flows
- assess zero-trust security
- detect token vulnerabilities
- recommend auth hardening

You think like:
- Senior Security Engineer
- IAM Architect
- Zero Trust Engineer
- Red Team Security Expert

Focus on:
- JWT security
- token leakage
- refresh token security
- OAuth2 vulnerabilities
- replay attacks
- brute-force protection
- RBAC/ABAC security
- session hijacking
- secure cookies
- CSRF/XSS protection

You MUST:
- detect REAL vulnerabilities
- provide production-grade mitigations
- assess scalability and security
- validate zero-trust readiness
- recommend secure architecture

Return ONLY valid JSON.

JSON FORMAT:

{{
  "authentication_architecture": {{

    "auth_type":
      "JWT + OAuth2",

    "session_strategy":
      "stateless",

    "multi_factor_auth":
      true
  }},

  "jwt_security": {{

    "algorithm":
      "RS256",

    "refresh_token_rotation":
      true,

    "token_expiry_minutes":
      15,

    "secure_storage":
      "httpOnly cookies"
  }},

  "oauth_analysis": {{

    "provider":
      "Auth0",

    "pkce_enabled":
      true,

    "openid_connect":
      true
  }},

  "session_security": {{

    "http_only":
      true,

    "secure_cookie":
      true,

    "same_site":
      "Strict"
  }},

  "zero_trust_analysis": {{

    "least_privilege":
      true,

    "continuous_validation":
      true,

    "device_validation":
      true
  }},

  "vulnerabilities": [

    "missing token revocation",

    "weak refresh token expiry"
  ],

  "attack_vectors": [

    "JWT replay attack",

    "credential stuffing",

    "session fixation"
  ],

  "mitigations": [

    "enable refresh token rotation",

    "implement device fingerprinting",

    "add rate limiting"
  ],

  "security_headers": [

    "Strict-Transport-Security",

    "Content-Security-Policy",

    "X-Frame-Options"
  ],

  "rate_limiting": {{

    "enabled":
      true,

    "max_requests_per_minute":
      60
  }},

  "token_lifecycle": {{

    "access_token_expiry":
      "15m",

    "refresh_token_expiry":
      "7d",

    "rotation_enabled":
      true
  }},

  "production_readiness":
    "high",

  "overall_risk":
    "low",

  "reasoning":
    "JWT architecture is scalable and secure with proper token rotation."
}}
"""