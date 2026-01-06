from pydantic import BaseModel
from typing import Optional


# =========================
# ANALYZE (Paste Text)
# =========================

class AnalyzeTextRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    corrected_text: str
    summary: Optional[str] = None


# =========================
# EXPORT PDF
# =========================

class ExportRequest(BaseModel):
    title: str
    filename: str
    corrected_text: str
    summary: str


# =========================
# UPLOAD (Audio / Video)
# =========================

class UploadResponse(BaseModel):
    filename: str
    transcribed_text: str
    corrected_text: Optional[str] = None
    summary: Optional[str] = None
