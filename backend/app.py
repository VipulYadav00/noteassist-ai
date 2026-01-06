from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routers import analyze, upload, live, history, export

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NoteAssist API")

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (ONE consistent style)
app.include_router(analyze.router)
app.include_router(upload.router)
app.include_router(live.router)
app.include_router(history.router)
app.include_router(export.router)


@app.get("/")
def root():
    return {"status": "NoteAssist backend running"}
