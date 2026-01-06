from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

DB_USER = "root"
DB_PASSWORD = quote_plus("@root123")  # change if needed
DB_HOST = "localhost"
DB_NAME = "ai_notes"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ✅ THIS WAS MISSING
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
