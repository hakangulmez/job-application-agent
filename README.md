# Job Application Agent

A Streamlit web app that generates tailored cover letters and pre-fills application form answers using Claude AI. Upload your CV and documents, paste a job description URL, and get a professional cover letter in seconds.

## Features

- **Profile management** — save your personal info once, reuse across applications
- **Job description fetching** — automatically extracts title, company, requirements, and contact email from a URL
- **AI cover letter generation** — Claude writes a tailored 4-paragraph cover letter based on your actual documents
- **AI-generated form answers** — standard fields auto-filled from your profile, job-specific questions answered by Claude
- **One-page optimized formatting** — cover letters fit on a single A4 page with professional layout
- **Clickable mailto email link in DOCX header** — HR can click your email to open their mail client
- **LinkedIn and GitHub hyperlinks in header** — clickable links in the generated DOCX
- **Autocomplete disabled on address fields** — prevents browser autofill from overwriting your input
- **DOCX and PDF export** — download your cover letter in either format

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/hakangulmez/job-application-agent.git
   cd job-application-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API key**
   ```bash
   mkdir -p .streamlit
   echo 'ANTHROPIC_API_KEY = "your-key-here"' > .streamlit/secrets.toml
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Fill your profile** — go to the "My Profile" tab and enter your details, then click Save Profile
2. **Create an application** — go to "New Application", paste a job description URL (or paste the text manually), upload your CV and any supporting documents
3. **Generate** — click "Generate Application" to get your cover letter and form answers. Edit the letter if needed, then download as DOCX or PDF

## Author

Hakan Zeki Gulmez

## License

MIT
