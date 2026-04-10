import json
import re

import anthropic
import streamlit as st


def analyze_cv_gaps(cv_text: str, jd_dict: dict) -> dict:
    """
    Analyze gaps between CV and JD.
    Returns structured gap analysis.
    """
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    jd_text = jd_dict.get("full_text", "")[:2500]

    system = """You are a CV gap analyzer. Compare a CV against a job description
and identify missing skills, tools, and experience.

Respond with JSON only — no other text:
{
  "missing_tools": [
    {"name": "Databricks", "jd_context": "required for pipeline work", "category": "tool"}
  ],
  "missing_skills": [
    {"name": "ETL/ELT pipeline development", "jd_context": "core requirement", "category": "skill"}
  ],
  "existing_strengths": [
    "Python proficiency matches JD requirement",
    "LLM/RAG experience directly relevant"
  ],
  "rewrite_suggestions": [
    "Emphasize data pipeline work in thesis bullet points",
    "Reframe M&A data work as structured data processing"
  ]
}

Rules:
- missing_tools: specific technologies/platforms mentioned in JD but absent from CV
- missing_skills: capabilities required by JD not evidenced in CV
- Keep existing_strengths to top 3-4 most relevant matches
- Keep rewrite_suggestions to top 3-4 most impactful changes
- Be precise — only flag things truly missing, not things that can be inferred"""

    user_msg = f"""JOB DESCRIPTION:
{jd_text}

CANDIDATE CV:
{cv_text[:4000]}

Identify gaps and strengths."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )

    text = response.content[0].text
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except (json.JSONDecodeError, ValueError):
            pass
    return {
        "missing_tools": [],
        "missing_skills": [],
        "existing_strengths": [],
        "rewrite_suggestions": [],
    }
