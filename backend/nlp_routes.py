# nlp_routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from crud import create_note, get_notes, delete_note
from models import Note

import shutil
import tempfile
import os
from fastapi.responses import StreamingResponse

try:
    import whisper
    WHISPER_AVAILABLE = True
except Exception:
    WHISPER_AVAILABLE = False

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

router = APIRouter(prefix="/api")

@router.post("/summarize-text")
def summarize_text(payload: dict, db: Session = Depends(get_db)):
    text = payload.get("text", "")
    input_type = payload.get("input_type", "pasted")

    note = analyze_and_create_note(text, input_type, db)

    return {
        "id": note.id,
        "corrected_text": note.corrected_text,
        "summary": note.summary
    }


def analyze_and_create_note(text: str, input_type: str, db: Session):
    # Centralized analysis -> create note
    corrected_text, summary = analyze_text(text)

    note = create_note(
        db=db,
        input_type=input_type,
        original_text=text,
        corrected_text=corrected_text,
        summary=summary
    )

    return note


def analyze_text(text: str):
    # Return corrected_text and summary without persisting.
    corrected_text = f"Correct: {text.capitalize()}" if text else ""
    summary = extract_keywords(text, top_n=8) if text else ""
    return corrected_text, summary


@router.post("/analyze-preview")
def analyze_preview(payload: dict):
    """Analyze text without saving a note. Returns corrected_text and summary."""
    text = payload.get("text", "")
    corrected_text, summary = analyze_text(text)
    return {"corrected_text": corrected_text, "summary": summary}


def extract_keywords(text: str, top_n: int = 6):
    # Very small keyword extractor: token frequency minus stopwords.
    import re
    from collections import Counter

    stopwords = {
        'the','and','is','in','to','of','a','an','that','it','on','for','with','as','are','was','were','be','by','this','from','or','at','but','not'
    }

    # normalize
    words = re.findall(r"\b[\w']+\b", text.lower())
    candidates = [w for w in words if w.isalpha() and w not in stopwords]
    if not candidates:
        return ''

    counts = Counter(candidates)
    most = [w for w, _ in counts.most_common(top_n)]
    return ', '.join(most)


def extract_summary(text: str, max_points: int = 3, max_words: int = 18):
    """Extract a short, extractive summary as bullet points preserving context.

    Algorithm:
    - Split into sentences
    - Score sentences by number of content words (non-stopwords)
    - Pick top scoring sentences (up to max_points)
    - Preserve original order and truncate each sentence to max_words words
    """
    import re
    from collections import Counter

    if not text or not text.strip():
        return ''

    stopwords = {
        'the','and','is','in','to','of','a','an','that','it','on','for','with','as','are','was','were','be','by','this','from','or','at','but','not','he','she','they','we','you','i','his','her','their'
    }

    # split into sentences (keeps punctuation)
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]
    if not sentences:
        return ''

    # score sentences by count of content words
    def sentence_score(s):
        words = re.findall(r"\b[\w']+\b", s.lower())
        return sum(1 for w in words if w.isalpha() and w not in stopwords)

    scored = [(i, s, sentence_score(s)) for i, s in enumerate(sentences)]
    # pick top by score
    scored_sorted = sorted(scored, key=lambda x: x[2], reverse=True)
    top = scored_sorted[:max_points]
    # restore original order
    top_sorted = sorted(top, key=lambda x: x[0])

    points = []
    for _, sent, _ in top_sorted:
        words = sent.split()
        if len(words) > max_words:
            pt = ' '.join(words[:max_words]).rstrip(' ,;:') + '...'
        else:
            pt = sent
        points.append(pt.strip())

    # format as short bullet-lines separated by newlines
    return '\n'.join(f"- {p}" for p in points)

@router.get("/notes")
def fetch_notes(db: Session = Depends(get_db)):
    notes = get_notes(db)

    return [
        {
            "id": note.id,
            "input_type": note.input_type,
            "original_text": note.original_text,
            "corrected_text": note.corrected_text,
            "summary": note.summary,
            "created_at": note.created_at
        }
        for note in notes
    ]


@router.delete("/notes/{note_id}")
def delete_note_route(note_id: int, db: Session = Depends(get_db)):
    success = delete_note(db, note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")

    return {"status": "deleted", "id": note_id}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # save uploaded file to a temp file
    suffix = os.path.splitext(file.filename)[1] or ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = tmp.name
        shutil.copyfileobj(file.file, tmp)

    # try to transcribe using whisper if available
    transcription = ""
    if WHISPER_AVAILABLE:
        try:
            model = whisper.load_model("base")
            result = model.transcribe(tmp_path)
            transcription = result.get("text", "")
        except Exception:
            transcription = "(transcription failed)"
    else:
        transcription = "(whisper not available on server)"

    input_type = "audio"
    if file.content_type and file.content_type.startswith("video"):
        input_type = "video"

    # cleanup temp file
    try:
        os.unlink(tmp_path)
    except Exception:
        pass

    # Return transcription to the client so they can edit/confirm before analysis
    return {"transcription": transcription, "input_type": input_type}


@router.get("/notes/{note_id}/pdf")
def notes_pdf(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    def generate_pdf():
        # create PDF in-memory
        from io import BytesIO
        from reportlab.lib.units import inch
        from reportlab.lib.utils import simpleSplit

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Document metadata
        c.setTitle(f"NoteAssist Note {note.id}")
        c.setAuthor("NoteAssist")

        # Layout settings
        left_margin = 0.75 * inch
        right_margin = 0.75 * inch
        top_margin = 0.75 * inch
        bottom_margin = 0.75 * inch
        usable_width = width - left_margin - right_margin
        y_start = height - top_margin

        # Title
        title = f"Note #{note.id}"
        subtitle = (note.summary or "").strip()
        c.setFont("Helvetica-Bold", 18)
        c.drawString(left_margin, y_start, title)
        y = y_start - 24

        if subtitle:
            c.setFont("Helvetica-Oblique", 11)
            c.drawString(left_margin, y, subtitle)
            y -= 18

        # metadata line (date, input type)
        meta = f"Created: {note.created_at}    Type: {note.input_type}"
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0.25, 0.25, 0.25)
        c.drawString(left_margin, y, meta)
        y -= 20

        # draw a separator
        c.setStrokeColorRGB(0.9, 0.9, 0.9)
        c.setLineWidth(0.5)
        c.line(left_margin, y, width - right_margin, y)
        y -= 14

        # Body text (corrected_text)
        body = (note.corrected_text or "").strip()
        if not body:
            body = "(no content)"

        font_name = "Helvetica"
        font_size = 11
        leading = font_size + 4

        c.setFont(font_name, font_size)
        c.setFillColorRGB(0, 0, 0)

        lines = []
        for paragraph in body.splitlines():
            if not paragraph:
                lines.append("")
                continue
            wrapped = simpleSplit(paragraph, font_name, font_size, usable_width)
            lines.extend(wrapped)

        # paginate
        page_num = 1
        for i, line in enumerate(lines):
            if y - leading < bottom_margin:
                # footer with page number
                c.setFont("Helvetica", 9)
                c.setFillColorRGB(0.4, 0.4, 0.4)
                c.drawRightString(width - right_margin, bottom_margin - 10, f"Page {page_num}")
                c.showPage()
                page_num += 1
                # reset
                y = height - top_margin
                c.setFont("Helvetica", font_size)

            c.drawString(left_margin, y, line)
            y -= leading

        # final footer
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawRightString(width - right_margin, bottom_margin - 10, f"Page {page_num}")

        c.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = generate_pdf()
    headers = {"Content-Disposition": f"attachment; filename=note_{note_id}.pdf"}
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)
