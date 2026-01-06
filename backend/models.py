from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime
from backend.database import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    # paste | upload | live
    input_type = Column(Text, nullable=False)

    original_text = Column(Text, nullable=False)
    corrected_text = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
