from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os, uuid, shutil

from backend.database import get_db
from backend.models import Note
from backend.utils.whisper_utils import transcribe_audio
from backend.utils.grammar_utils import correct_grammar
from backend.utils.summarizer_utils import summarize_text

router = APIRouter(prefix="/live", tags=["Live"])

LIVE_DIR = "live_audio"
os.makedirs(LIVE_DIR, exist_ok=True)


@router.post("/audio")
def process_live_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = f"{uuid.uuid4()}.webm"
    file_path = os.path.join(LIVE_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe_audio(file_path)
    corrected_text = correct_grammar(transcript)
    summary = summarize_text(corrected_text)

    note = Note(
        input_type="live",
        original_text=transcript,
        corrected_text=corrected_text,
        summary=summary,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return {
        "id": note.id,
        "original_text": transcript,
        "corrected_text": corrected_text,
        "summary": summary,
    }
