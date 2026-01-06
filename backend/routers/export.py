from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.schemas import ExportRequest
from backend.utils.pdf_generator import generate_pdf

router = APIRouter(prefix="/export", tags=["Export"])


@router.post("/pdf")
def export_pdf(data: ExportRequest):
    """
    Exports corrected text and summary as a downloadable PDF.
    """
    buffer = generate_pdf(
        title=data.title,
        corrected_text=data.corrected_text,
        summary=data.summary,
    )

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{data.filename}.pdf"'
        },
    )
