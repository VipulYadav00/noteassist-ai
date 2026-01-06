from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Note
from backend.schemas import AnalyzeTextRequest
from backend.utils.grammar_utils import correct_grammar
from backend.utils.summarizer_utils import summarize_text

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("/text")
def analyze_text(
    payload: AnalyzeTextRequest,
    db: Session = Depends(get_db)
):
    corrected_text = correct_grammar(payload.text)
    summary = summarize_text(corrected_text)

    note = Note(
        input_type="paste",
        original_text=payload.text,
        corrected_text=corrected_text,
        summary=summary,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return {
        "id": note.id,
        "corrected_text": corrected_text,
        "summary": summary,
    }
