from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
STORAGE = ROOT / "storage"
UPLOADS = Path(os.getenv("UPLOAD_DIR", STORAGE / "uploads"))
DB_PATH = Path(os.getenv("DATABASE_PATH", STORAGE / "exam_ai.db"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
UPLOADS.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
              id TEXT PRIMARY KEY, filename TEXT NOT NULL, stored_path TEXT NOT NULL,
              document_type TEXT NOT NULL, file_hash TEXT NOT NULL UNIQUE,
              file_size INTEGER NOT NULL, status TEXT NOT NULL, total_pages INTEGER DEFAULT 0,
              extracted_text TEXT DEFAULT '', created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS chapters (
              id TEXT PRIMARY KEY, document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
              title TEXT NOT NULL, chapter_number INTEGER, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS questions (
              id TEXT PRIMARY KEY, document_id TEXT REFERENCES documents(id) ON DELETE SET NULL,
              chapter_id TEXT REFERENCES chapters(id) ON DELETE SET NULL, topic TEXT,
              question_text TEXT NOT NULL, explanation TEXT, source_type TEXT NOT NULL,
              difficulty TEXT NOT NULL, correct_option TEXT NOT NULL, options_json TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS exams (
              id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL,
              question_ids TEXT NOT NULL, created_at TEXT NOT NULL, completed_at TEXT
            );
            CREATE TABLE IF NOT EXISTS attempts (
              id TEXT PRIMARY KEY, exam_id TEXT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
              question_id TEXT NOT NULL REFERENCES questions(id), selected_option TEXT,
              is_correct INTEGER NOT NULL, response_time_seconds REAL DEFAULT 0,
              answered_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS reviews (
              id TEXT PRIMARY KEY, topic TEXT NOT NULL UNIQUE, due_date TEXT NOT NULL,
              interval_days INTEGER NOT NULL DEFAULT 1, repetition_count INTEGER NOT NULL DEFAULT 0,
              last_reviewed_at TEXT, status TEXT NOT NULL DEFAULT 'DUE'
            );
            """
        )


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def row_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row) if row else {}


def question_public(row: sqlite3.Row) -> dict[str, Any]:
    import json
    item = row_dict(row)
    item["options"] = json.loads(item.pop("options_json"))
    item.pop("correct_option", None)
    return item


class ExamCreate(BaseModel):
    title: str = "Simulazione"
    question_count: int = Field(default=10, ge=1, le=100)
    source_type: str = "MIXED"
    topic: str | None = None


class AnswerCreate(BaseModel):
    question_id: str
    selected_option: str | None = Field(default=None, pattern=r"^[A-D]$")
    response_time_seconds: float = Field(default=0, ge=0)


app = FastAPI(title="Exam AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "exam-ai"}


@app.get("/api/ai/status")
async def ai_status() -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()
            models = [m.get("name") for m in response.json().get("models", [])]
            return {"available": True, "url": OLLAMA_URL, "model": OLLAMA_MODEL, "models": models}
    except (httpx.HTTPError, ValueError):
        return {"available": False, "url": OLLAMA_URL, "model": OLLAMA_MODEL, "models": []}


@app.get("/api/documents")
def documents() -> list[dict[str, Any]]:
    with db() as conn:
        return [row_dict(r) for r in conn.execute(
            "SELECT id, filename, document_type, file_size, status, total_pages, created_at "
            "FROM documents ORDER BY created_at DESC"
        )]


def extract_pdf(data: bytes) -> tuple[str, int]:
    try:
        import fitz
        document = fitz.open(stream=data, filetype="pdf")
        return "\n".join(page.get_text() for page in document), len(document)
    except (ImportError, RuntimeError, ValueError):
        return "", 0


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, Any]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".md", ".markdown"}:
        raise HTTPException(415, "Sono supportati solo PDF e Markdown")
    data = await file.read()
    if not data:
        raise HTTPException(400, "Il file è vuoto")
    digest = hashlib.sha256(data).hexdigest()
    with db() as conn:
        duplicate = conn.execute("SELECT id FROM documents WHERE file_hash = ?", (digest,)).fetchone()
        if duplicate:
            raise HTTPException(409, "Documento già importato")
    document_id = str(uuid.uuid4())
    target = UPLOADS / f"{document_id}{suffix}"
    target.write_bytes(data)
    text, pages = extract_pdf(data) if suffix == ".pdf" else (data.decode("utf-8", errors="replace"), 0)
    document_type = "PDF" if suffix == ".pdf" else "MARKDOWN"
    with db() as conn:
        conn.execute(
            "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (document_id, file.filename, str(target), document_type, digest, len(data),
             "ANALYZED", pages, text, now()),
        )
    if document_type == "MARKDOWN":
        import_markdown_questions(document_id, text)
    return {"id": document_id, "filename": file.filename, "status": "ANALYZED", "total_pages": pages}


def import_markdown_questions(document_id: str, text: str) -> int:
    chapter = "Generale"
    current: dict[str, Any] | None = None
    count = 0
    with db() as conn:
        for line in text.splitlines():
            heading = re.match(r"^##\s+(.+)", line.strip())
            question_heading = re.match(r"^###\s+Domanda\s*(\d+)?", line.strip(), re.I)
            if heading:
                chapter = heading.group(1).strip()
            if question_heading:
                if current:
                    count += save_question(conn, document_id, chapter, current)
                current = {"text": "", "options": {}, "correct": None, "explanation": ""}
                continue
            if current is None:
                continue
            option = re.match(r"^([A-D])\.\s+(.+)", line.strip())
            answer = re.match(r"^\*\*Risposta corretta:\*\*\s*([A-D])", line.strip(), re.I)
            explanation = re.match(r"^\*\*Spiegazione:\*\*\s*(.*)", line.strip(), re.I)
            if option:
                current["options"][option.group(1)] = option.group(2).strip()
            elif answer:
                current["correct"] = answer.group(1).upper()
            elif explanation:
                current["explanation"] = explanation.group(1).strip()
            elif line.strip() and not line.startswith("#"):
                current["text"] += (" " if current["text"] else "") + line.strip()
        if current:
            count += save_question(conn, document_id, chapter, current)
    return count


def save_question(conn: sqlite3.Connection, document_id: str, chapter: str, item: dict[str, Any]) -> int:
    options = item["options"]
    if not item["text"] or len(options) != 4 or item["correct"] not in options:
        return 0
    chapter_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{document_id}:{chapter}"))
    conn.execute(
        "INSERT OR IGNORE INTO chapters VALUES (?, ?, ?, ?, ?)",
        (chapter_id, document_id, chapter, None, now()),
    )
    conn.execute(
        "INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), document_id, chapter_id, chapter, item["text"],
         item["explanation"], "OFFICIAL", "medium", item["correct"], json.dumps(options), now()),
    )
    return 1


@app.get("/api/questions")
def questions(source_type: str | None = None, topic: str | None = None) -> list[dict[str, Any]]:
    query = "SELECT * FROM questions WHERE 1=1"
    args: list[str] = []
    if source_type and source_type != "MIXED":
        query += " AND source_type = ?"; args.append(source_type)
    if topic:
        query += " AND topic = ?"; args.append(topic)
    query += " ORDER BY created_at DESC"
    with db() as conn:
        return [question_public(r) for r in conn.execute(query, args)]


@app.get("/api/chapters")
def chapters() -> list[dict[str, Any]]:
    with db() as conn:
        return [row_dict(r) for r in conn.execute(
            "SELECT c.*, COUNT(q.id) AS question_count FROM chapters c "
            "LEFT JOIN questions q ON q.chapter_id = c.id GROUP BY c.id ORDER BY c.title"
        )]


@app.post("/api/exams")
def create_exam(payload: ExamCreate) -> dict[str, Any]:
    with db() as conn:
        query = "SELECT * FROM questions WHERE 1=1"
        args: list[Any] = []
        if payload.source_type != "MIXED":
            query += " AND source_type = ?"; args.append(payload.source_type)
        if payload.topic:
            query += " AND topic = ?"; args.append(payload.topic)
        query += " ORDER BY RANDOM() LIMIT ?"; args.append(payload.question_count)
        selected = conn.execute(query, args).fetchall()
        if not selected:
            raise HTTPException(400, "Nessuna domanda disponibile")
        exam_id = str(uuid.uuid4())
        ids = [r["id"] for r in selected]
        conn.execute("INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?)",
                     (exam_id, payload.title, "IN_PROGRESS", ",".join(ids), now(), None))
        return {"id": exam_id, "title": payload.title, "status": "IN_PROGRESS",
                "questions": [question_public(r) for r in selected]}


@app.post("/api/exams/{exam_id}/answer")
def answer(exam_id: str, payload: AnswerCreate) -> dict[str, Any]:
    with db() as conn:
        exam = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        question = conn.execute("SELECT * FROM questions WHERE id = ?", (payload.question_id,)).fetchone()
        if not exam or not question or payload.question_id not in exam["question_ids"].split(","):
            raise HTTPException(404, "Esame o domanda non trovati")
        correct = payload.selected_option == question["correct_option"]
        attempt = str(uuid.uuid4())
        conn.execute("INSERT INTO attempts VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (attempt, exam_id, payload.question_id, payload.selected_option, int(correct),
                      payload.response_time_seconds, now()))
        return {"attempt_id": attempt, "is_correct": correct}


@app.post("/api/exams/{exam_id}/finish")
def finish_exam(exam_id: str) -> dict[str, Any]:
    with db() as conn:
        exam = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not exam:
            raise HTTPException(404, "Esame non trovato")
        conn.execute("UPDATE exams SET status = 'COMPLETED', completed_at = ? WHERE id = ?", (now(), exam_id))
        return exam_results(conn, exam_id)


def exam_results(conn: sqlite3.Connection, exam_id: str) -> dict[str, Any]:
    attempts = conn.execute("SELECT * FROM attempts WHERE exam_id = ?", (exam_id,)).fetchall()
    total = len(attempts)
    correct = sum(a["is_correct"] for a in attempts)
    return {"exam_id": exam_id, "answered": total, "correct": correct,
            "incorrect": total - correct, "accuracy": round(correct / total * 100, 1) if total else 0}


@app.get("/api/exams/{exam_id}/results")
def results(exam_id: str) -> dict[str, Any]:
    with db() as conn:
        if not conn.execute("SELECT id FROM exams WHERE id = ?", (exam_id,)).fetchone():
            raise HTTPException(404, "Esame non trovato")
        return exam_results(conn, exam_id)


@app.get("/api/analytics/overview")
def analytics() -> dict[str, Any]:
    with db() as conn:
        totals = conn.execute(
            "SELECT COUNT(*) total, COALESCE(SUM(is_correct), 0) correct, "
            "COALESCE(SUM(CASE WHEN q.source_type='OFFICIAL' THEN 1 ELSE 0 END), 0) official "
            "FROM attempts a JOIN questions q ON q.id = a.question_id"
        ).fetchone()
        topics = conn.execute(
            "SELECT q.topic, COUNT(*) attempts, ROUND(AVG(a.is_correct) * 100, 1) accuracy "
            "FROM attempts a JOIN questions q ON q.id = a.question_id GROUP BY q.topic ORDER BY accuracy"
        ).fetchall()
        due = conn.execute("SELECT COUNT(*) count FROM reviews WHERE due_date <= ?", (date.today().isoformat(),)).fetchone()["count"]
        total = totals["total"]
        return {"questions_answered": total, "correct_answers": totals["correct"],
                "accuracy": round(totals["correct"] / total * 100, 1) if total else 0,
                "official_answered": totals["official"], "due_reviews": due,
                "topics": [row_dict(r) for r in topics]}


@app.get("/api/reviews/today")
def reviews_today() -> list[dict[str, Any]]:
    with db() as conn:
        return [row_dict(r) for r in conn.execute("SELECT * FROM reviews WHERE due_date <= ? ORDER BY due_date", (date.today().isoformat(),))]


@app.post("/api/reviews/{review_id}/complete")
def complete_review(review_id: str) -> dict[str, Any]:
    with db() as conn:
        review = conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
        if not review:
            raise HTTPException(404, "Ripasso non trovato")
        interval = min(review["interval_days"] * 2, 60)
        due = date.today() + timedelta(days=interval)
        conn.execute("UPDATE reviews SET interval_days = ?, repetition_count = repetition_count + 1, due_date = ?, last_reviewed_at = ?, status = 'SCHEDULED' WHERE id = ?",
                     (interval, due.isoformat(), now(), review_id))
        return row_dict(conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone())
