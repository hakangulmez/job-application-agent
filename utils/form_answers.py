import anthropic
import streamlit as st


def generate_form_answers(
    applicant_text: str,
    jd_dict: dict,
    profile_dict: dict,
    extra_questions: str,
) -> dict:
    # Standard fields from profile (no API call needed)
    answers = {
        "Full Name": profile_dict.get("full_name", ""),
        "Email": profile_dict.get("email", ""),
        "Phone": profile_dict.get("phone", ""),
        "Address": profile_dict.get("address", ""),
        "City": profile_dict.get("city", ""),
        "Country": profile_dict.get("country", ""),
        "Postal Code": profile_dict.get("postal_code", ""),
        "Target Compensation": f"\u20ac{profile_dict.get('compensation', 24000):,}",
        "Available Start Date": profile_dict.get("start_date", ""),
        "Notice Period": profile_dict.get("notice_period", ""),
        "Work Authorization": profile_dict.get("work_auth", ""),
        "How did you hear about this position?": profile_dict.get("referral_source", ""),
    }

    # If there are extra questions, use Claude to answer them
    extra_questions = extra_questions.strip()
    if not extra_questions:
        return answers

    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

    user_message = f"""Answer the following job application form questions concisely.
Each answer must be under 200 characters. Use only facts from the applicant's documents.
If you cannot determine an answer, write "N/A".

JOB TITLE: {jd_dict.get('title', 'N/A')}
COMPANY: {jd_dict.get('company', 'N/A')}

APPLICANT PROFILE:
{applicant_text[:8000]}

QUESTIONS (answer each one):
{extra_questions}

Format your response as:
Q: <question>
A: <answer>
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system="You are a helpful assistant filling out job application forms. Be concise, honest, and professional. Use only information provided.",
        messages=[{"role": "user", "content": user_message}],
    )

    # Parse Q/A pairs from response
    response_text = response.content[0].text
    current_q = None
    for line in response_text.splitlines():
        line = line.strip()
        if line.startswith("Q:"):
            current_q = line[2:].strip()
        elif line.startswith("A:") and current_q:
            answers[current_q] = line[2:].strip()
            current_q = None

    return answers
