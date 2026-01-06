from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os, uuid, shutil

from backend.database import get_db
from backend.models import Note
from backend.utils.whisper_utils import transcribe_audio
from backend.utils.grammar_utils import correct_grammar
from backend.utils.summarizer_utils import summarize_text

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/media")
def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1️⃣ Transcribe
    transcript = transcribe_audio(file_path)

    # 2️⃣ Grammar correction
    corrected_text = correct_grammar(transcript)

    # 3️⃣ Summarization
    summary = summarize_text(corrected_text)

    # 4️⃣ Save to DB
    note = Note(
        input_type="upload",
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
