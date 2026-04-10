import anthropic
import streamlit as st


SYSTEM_PROMPT = """You are writing a professional cover letter for a job application.
The applicant's full background is provided. The job description is provided.

Rules:
- Direct, technically precise tone. No filler phrases like 'I am excited',
  'I am passionate', 'perfectly aligns', 'I would be thrilled', 'I am eager'.
- 4 paragraphs:
  (1) Opening: state the role applied for, applicant's current degree/institution
      or most recent position, and ONE specific reason why this team/unit/company
      is a fit — drawn from the JD, not generic.
  (2) Strongest relevant experience: pick the project, thesis, or work experience
      from the applicant's documents that best matches the JD requirements.
      Be specific — include numbers, methods, tools, results where available.
  (3) Skills and remaining experience mapped to JD requirements. If there are
      clear gaps between the JD requirements and the applicant's background,
      acknowledge them briefly and honestly — do not pretend gaps don't exist.
  (4) Closing: state availability/start date from profile, one sentence on fit,
      no enthusiasm inflation.
- Use ONLY facts present in the applicant's documents and profile.
  Never invent experience, tools, or results.
- No bullet points.
- Output only the 4 paragraphs separated by blank lines.
  No salutation, no date, no address, no 'Dear', no 'Best regards'.
- Total length: 350-450 words.
- The letter must work for any applicant — engineer, economist, designer,
  marketer — based purely on what their documents contain."""


def generate_cover_letter(
    applicant_text: str,
    jd_dict: dict,
    app_type: str,
    profile_dict: dict,
) -> str:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

    jd_text = jd_dict.get("full_text", "")

    user_message = f"""Write a cover letter for the following job application.

APPLICATION TYPE: {app_type}

JOB DESCRIPTION:
{jd_text[:3000]}

APPLICANT DOCUMENTS (CV, transcripts, etc.):
{applicant_text[:6000]}

APPLICANT PROFILE:
- Name: {profile_dict.get('full_name', '')}
- Available from: {profile_dict.get('start_date', '')}
- Notice period: {profile_dict.get('notice_period', '')}

Select the most relevant experience from the applicant's documents \
for THIS specific job description. Do not default to thesis or \
academic work if work experience is more relevant."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text
