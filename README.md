# Job application drafting tool

I built a Streamlit app to turn a CV, supporting documents and a job description into an editable application draft. It uses the Claude API to draft a cover letter and answers to job-specific questions, with DOCX and PDF export.

## What I implemented

The app stores reusable profile fields, parses uploaded documents and fetches a job description from a URL, with manual text entry as a fallback. It combines those inputs for drafting, then formats the letter and contact links for export.

I kept review and editing in the workflow: the output is a draft to check against the source documents. Producing a document does not establish that its claims are supported or that the applicant meets the role's requirements. This repository contains the Streamlit tool; it does not document the later local Alfred workflow.

## Run locally

Create a Python environment and install the requirements:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add `ANTHROPIC_API_KEY` to `.streamlit/secrets.toml`, then start the app:

```sh
streamlit run app.py
```

Enter a profile, upload the relevant documents and provide the job description. Review the generated text before downloading it. Document text is used in API requests; running generation requires an Anthropic account and incurs its API charges.

The main components are in `app.py` and `utils/`: document parsing, job-description fetching, drafting, form answers and document export.

Original code: [MIT](LICENSE).

Hakan Zeki Gülmez · [GitHub](https://github.com/hakangulmez)
