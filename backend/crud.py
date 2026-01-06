from sqlalchemy.orm import Session
from backend.models import Note


def create_note(db: Session, input_type, original_text, corrected_text, summary):
    note = Note(
        input_type=input_type,
        original_text=original_text,
        corrected_text=corrected_text,
        summary=summary
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes(db: Session):
    return db.query(Note).order_by(Note.created_at.desc()).all()

def delete_note(db: Session, note_id: int) -> bool:
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return False

    db.delete(note)
    db.commit()
    return True
