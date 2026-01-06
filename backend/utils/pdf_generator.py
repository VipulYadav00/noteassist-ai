from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime


def generate_pdf(
    title: str,
    corrected_text: str,
    summary: str,
):
    """
    Generates a professional PDF with summary and corrected text.
    Returns an in-memory buffer (StreamingResponse friendly).
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin_x = 40
    y = height - 50

    # ===== Title =====
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, y, title)
    y -= 30

    # ===== Timestamp =====
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        margin_x,
        y,
        f"Generated on: {datetime.now().strftime('%d %b %Y %H:%M')}",
    )
    y -= 30

    # ===== Summary Section =====
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin_x, y, "Summary")
    y -= 20

    pdf.setFont("Helvetica", 11)
    for line in summary.split(". "):
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 50
        pdf.drawString(margin_x + 10, y, f"- {line.strip()}")
        y -= 16

    y -= 20

    # ===== Corrected Text Section =====
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin_x, y, "Corrected Text")
    y -= 20

    pdf.setFont("Helvetica", 11)
    for line in corrected_text.split(". "):
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 50
        pdf.drawString(margin_x + 10, y, line.strip())
        y -= 16

    pdf.save()
    buffer.seek(0)
    return buffer
