import io
from pypdf import PdfReader
from docx import Document


def parse_pdf(file) -> str:
    reader = PdfReader(file)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n\n".join(text_parts)


def parse_docx(file) -> str:
    doc = Document(file)
    text_parts = []
    for para in doc.paragraphs:
        if para.text.strip():
            text_parts.append(para.text)
    return "\n\n".join(text_parts)


def parse_document(file) -> str:
    name = file.name.lower()
    if name.endswith(".pdf"):
        return parse_pdf(file)
    elif name.endswith(".docx"):
        return parse_docx(file)
    else:
        return f"[Unsupported file type: {name}]"
