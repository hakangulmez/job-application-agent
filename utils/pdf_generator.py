import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT


def generate_pdf(cover_letter_text: str, profile_dict: dict, jd_dict: dict) -> io.BytesIO:
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "Name",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        spaceAfter=2,
    )
    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        spaceAfter=2,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        spaceAfter=6,
        alignment=TA_LEFT,
    )
    bold_style = ParagraphStyle(
        "BoldLine",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    story = []

    # Header
    name = profile_dict.get("full_name", "")
    email = profile_dict.get("email", "")
    phone = profile_dict.get("phone", "")

    if name:
        story.append(Paragraph(name, name_style))

    contact_parts = [p for p in [email, phone] if p]
    if contact_parts:
        story.append(Paragraph(" | ".join(contact_parts), contact_style))

    address_parts = [
        p for p in [
            profile_dict.get("address", ""),
            profile_dict.get("city", ""),
            profile_dict.get("postal_code", ""),
            profile_dict.get("country", ""),
        ] if p
    ]
    if address_parts:
        story.append(Paragraph(", ".join(address_parts), contact_style))

    story.append(Spacer(1, 18))

    # Date
    story.append(Paragraph(date.today().strftime("%B %d, %Y"), body_style))
    story.append(Spacer(1, 12))

    # Recipient
    company = jd_dict.get("company", "Hiring Manager")
    if company:
        story.append(Paragraph(company, body_style))
    location = jd_dict.get("location", "")
    if location:
        story.append(Paragraph(location, body_style))

    story.append(Spacer(1, 12))

    # Salutation
    story.append(Paragraph("Dear Hiring Manager,", body_style))
    story.append(Spacer(1, 6))

    # Body paragraphs
    paragraphs = [p.strip() for p in cover_letter_text.split("\n\n") if p.strip()]
    for para_text in paragraphs:
        para_text = para_text.replace("\n", " ")
        # Escape XML special chars for reportlab
        para_text = (
            para_text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        story.append(Paragraph(para_text, body_style))

    story.append(Spacer(1, 12))

    # Closing
    story.append(Paragraph("Best regards,", body_style))
    if name:
        story.append(Paragraph(name, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
