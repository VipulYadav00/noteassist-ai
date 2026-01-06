from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Note

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/")
def get_history(db: Session = Depends(get_db)):
    return db.query(Note).order_by(Note.id.desc()).all()


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"message": "Deleted"}


@router.delete("/")
def delete_all_notes(db: Session = Depends(get_db)):
    db.query(Note).delete()
    db.commit()
    return {"message": "All history deleted"}


@router.delete("/bulk")
def delete_many(ids: dict, db: Session = Depends(get_db)):
    note_ids = ids.get("ids", [])
    if not note_ids:
        return {"message": "No IDs provided"}

    db.query(Note).filter(Note.id.in_(note_ids)).delete(
        synchronize_session=False
    )
    db.commit()
    return {"message": "Selected history deleted"}
