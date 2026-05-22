# domains/cybersecurity/agents/vuln_agent.py

"""
CognitiveOS - Vulnerability Assessment Agent
---------------------------------------------------------

Responsibilities:
- detect security vulnerabilities
- analyze insecure architectures
- assess OWASP risks
- identify misconfigurations
- evaluate API security
- assess infrastructure weaknesses
- recommend mitigations
- generate security reports

This agent behaves like:
- Vulnerability Researcher
- Security Auditor
- AppSec Engineer
- Cloud Security Engineer
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
class VulnerabilityAgentState:

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
# VULNERABILITY AGENT
# ============================================================


class VulnerabilityAgent:

    """
    Production-grade vulnerability assessment agent.
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

            vulnerability_summary = result.get(
                "vulnerability_summary",
                {},
            )

            owasp_findings = result.get(
                "owasp_findings",
                [],
            )

            api_security_issues = result.get(
                "api_security_issues",
                [],
            )

            infrastructure_risks = result.get(
                "infrastructure_risks",
                [],
            )

            cloud_security_findings = result.get(
                "cloud_security_findings",
                [],
            )

            authentication_issues = result.get(
                "authentication_issues",
                [],
            )

            authorization_issues = result.get(
                "authorization_issues",
                [],
            )

            data_exposure_risks = result.get(
                "data_exposure_risks",
                [],
            )

            insecure_configurations = result.get(
                "insecure_configurations",
                [],
            )

            dependency_risks = result.get(
                "dependency_risks",
                [],
            )

            severity_assessment = result.get(
                "severity_assessment",
                {},
            )

            exploitability = result.get(
                "exploitability",
                {},
            )

            compliance_gaps = result.get(
                "compliance_gaps",
                [],
            )

            remediation_plan = result.get(
                "remediation_plan",
                [],
            )

            security_best_practices = result.get(
                "security_best_practices",
                [],
            )

            production_risk = result.get(
                "production_risk",
                "medium",
            )

            overall_security_score = result.get(
                "overall_security_score",
                0.0,
            )

            reasoning = result.get(
                "reasoning",
                "",
            )

            return {

                "success": True,

                "agent":
                    "vuln_agent",

                "vulnerability_summary":
                    vulnerability_summary,

                "owasp_findings":
                    owasp_findings,

                "api_security_issues":
                    api_security_issues,

                "infrastructure_risks":
                    infrastructure_risks,

                "cloud_security_findings":
                    cloud_security_findings,

                "authentication_issues":
                    authentication_issues,

                "authorization_issues":
                    authorization_issues,

                "data_exposure_risks":
                    data_exposure_risks,

                "insecure_configurations":
                    insecure_configurations,

                "dependency_risks":
                    dependency_risks,

                "severity_assessment":
                    severity_assessment,

                "exploitability":
                    exploitability,

                "compliance_gaps":
                    compliance_gaps,

                "remediation_plan":
                    remediation_plan,

                "security_best_practices":
                    security_best_practices,

                "production_risk":
                    production_risk,

                "overall_security_score":
                    overall_security_score,

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
                    "vuln_agent",

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
You are the Vulnerability Assessment Agent
for CognitiveOS.

Your role is to:
- detect vulnerabilities
- assess OWASP risks
- analyze API security
- identify cloud security weaknesses
- detect insecure configurations
- evaluate dependency risks
- assess exploitability
- recommend mitigations

You think like:
- AppSec Engineer
- Security Auditor
- Cloud Security Engineer
- Vulnerability Researcher

Focus on:
- OWASP Top 10
- API Security Top 10
- JWT security
- cloud misconfigurations
- SSRF/XSS/SQLi
- dependency vulnerabilities
- privilege escalation
- data exposure
- insecure defaults
- weak authentication

You MUST:
- identify REALISTIC vulnerabilities
- avoid unsafe offensive instructions
- provide defensive recommendations
- assess production impact
- recommend secure architectures
- prioritize critical risks

Return ONLY valid JSON.

JSON FORMAT:

{{
  "vulnerability_summary": {{

    "application":
      "FastAPI Backend",

    "risk_level":
      "high",

    "critical_findings":
      3
  }},

  "owasp_findings": [

    "Broken Access Control",

    "Security Misconfiguration",

    "Identification and Authentication Failures"
  ],

  "api_security_issues": [

    "Missing rate limiting",

    "Improper input validation",

    "Exposed admin endpoints"
  ],

  "infrastructure_risks": [

    "Open internal ports",

    "Weak network segmentation"
  ],

  "cloud_security_findings": [

    "Public S3 bucket",

    "Overprivileged IAM role"
  ],

  "authentication_issues": [

    "Weak JWT expiration",

    "Refresh token reuse"
  ],

  "authorization_issues": [

    "Missing RBAC validation",

    "Improper admin checks"
  ],

  "data_exposure_risks": [

    "Sensitive logs exposed",

    "PII leakage risk"
  ],

  "insecure_configurations": [

    "Debug mode enabled",

    "Missing HTTPS enforcement"
  ],

  "dependency_risks": [

    "Outdated FastAPI version",

    "Vulnerable JWT library"
  ],

  "severity_assessment": {{

    "critical":
      2,

    "high":
      5,

    "medium":
      4
  }},

  "exploitability": {{

    "remote_exploitation":
      true,

    "privilege_escalation":
      true
  }},

  "compliance_gaps": [

    "OWASP API Security",

    "SOC2 logging requirements"
  ],

  "remediation_plan": [

    "Enable strict RBAC",

    "Rotate JWT secrets",

    "Add API throttling",

    "Patch vulnerable dependencies"
  ],

  "security_best_practices": [

    "Zero Trust",

    "WAF protection",

    "MFA",

    "Structured audit logging"
  ],

  "production_risk":
    "high",

  "overall_security_score":
    5.8,

  "reasoning":
    "The architecture contains multiple authentication and API security weaknesses."
}}
"""