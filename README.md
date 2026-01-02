NoteAssist – End-to-End NLP & Speech Processing System
NoteAssist is an end-to-end AI system designed to process **unstructured data** (text, audio, and speech) and transform it into clean, grammatically correct, summarized notes using modern Transformer-based models

The project demonstrates real-world deployment of NLP and speech models, including preprocessing, inference, storage, and export.

🎯 Project Objective

The goal of this project is to:
- Build a production-style NLP pipeline
- Apply state-of-the-art Transformer models
- Handle text, audio, and live speech data
- Deploy models using an API
- Store and manage outputs for further analysis

This project focuses on applied data science, not notebook-only experimentation.

🧩 Problem Being Solved

Real-world data is often:
- Unstructured
- Grammatically incorrect
- Very long
- Available as speech rather than text

Most tools solve only one part of the problem.  
NoteAssist unifies **speech recognition, text refinement, and summarization** into a single pipeline.

🧠 AI / ML Pipeline

Input (Text / Audio / Speech)
↓
Preprocessing
↓
Speech-to-Text (if audio)
↓
Grammar Correction
↓
Text Summarization
↓
Storage (Database)
↓
Export (PDF)

Models Used (Core of the Project)

1️⃣ Speech-to-Text Model

- Model: OpenAI Whisper (small)
- Developed by:OpenAI
- Task: Automatic Speech Recognition (ASR)

2️⃣ Grammar Correction Model

- Model: T5 (Text-to-Text Transfer Transformer)
- Developed by: Google Research

3️⃣ Text Summarization Model

- Model: facebook/bart-large-cnn
- Developed by: Meta (Facebook AI Research)

🗂️ Data Storage

- Database: MySQL
- ORM: SQLAlchemy

Each processed input is stored with:
- Input type (paste / upload / live)
- Original text
- Corrected text
- Summary
- Timestamp

This enables:
- Historical analysis
- Reuse of processed data
- Export of past results

📄 PDF Export

- Library: ReportLab
- Server-side PDF generation
- Enables offline sharing and reporting
- Same export pipeline for all input types

🏗️ Tech Stack (Supporting the ML Pipeline)

Backend
- Python
- FastAPI
- SQLAlchemy

Frontend (Minimal, for model validation)
- React
- Tailwind CSS

ML / NLP
- PyTorch
- Hugging Face Transformers
- OpenAI Whisper

NoteAssist demonstrates how modern NLP and speech models can be applied in a real-world, end-to-end data science pipeline, bridging the gap between machine learning research and production deployment.

