import os
from pathlib import Path

os.environ["DATABASE_PATH"] = "/tmp/exam-ai-test.db"
os.environ["UPLOAD_DIR"] = "/tmp/exam-ai-test-uploads"

Path(os.environ["DATABASE_PATH"]).unlink(missing_ok=True)
Path(os.environ["UPLOAD_DIR"]).mkdir(parents=True, exist_ok=True)

from fastapi.testclient import TestClient

from app.main import app, chunks_for_text


MARKDOWN = """# Anatomia
## Capitolo 1 - Sistema scheletrico
### Domanda 1
Quale funzione svolge il sistema scheletrico?
A. Movimento
B. Digestione
C. Respirazione
D. Filtrazione
**Risposta corretta:** A
**Spiegazione:** Sostiene il corpo e contribuisce al movimento.
"""


def test_import_exam_and_analytics():
    with TestClient(app) as client:
        response = client.post(
            "/api/documents/upload",
            files={"file": ("questions.md", MARKDOWN.encode(), "text/markdown")},
        )
        assert response.status_code == 200
        document_id = response.json()["id"]
        job = client.post(f"/api/documents/{document_id}/process")
        assert job.status_code == 200
        assert client.get(f"/api/jobs/{job.json()['job_id']}").json()["status"] == "COMPLETED"
        assert client.get("/api/questions").json()[0]["source_type"] == "OFFICIAL"

        exam = client.post("/api/exams", json={"title": "Test", "question_count": 1})
        assert exam.status_code == 200
        exam_id = exam.json()["id"]
        question_id = exam.json()["questions"][0]["id"]

        answer = client.post(
            f"/api/exams/{exam_id}/answer",
            json={"question_id": question_id, "selected_option": "A"},
        )
        assert answer.status_code == 200
        assert answer.json()["is_correct"] is True
        result = client.post(f"/api/exams/{exam_id}/finish")
        assert result.json()["accuracy"] == 100.0
        assert client.get("/api/analytics/daily").status_code == 200
        assert client.get("/api/reviews/today").status_code == 200


def test_chunking_preserves_overlap():
    chunks = chunks_for_text(" ".join(f"w{i}" for i in range(25)), size=10, overlap=2)
    assert len(chunks) == 3
    assert chunks[0].split()[-2:] == chunks[1].split()[:2]


def test_upload_validation_and_progress():
    with TestClient(app) as client:
        invalid = client.post(
            "/api/documents/upload",
            files={"file": ("fake.pdf", b"not a pdf", "application/pdf")},
        )
        assert invalid.status_code == 415
        assert client.get("/api/analytics/progress").status_code == 200
        assert client.get("/api/analytics/errors").status_code == 200
        assert client.get("/api/settings").status_code == 200
        assert client.post("/api/backups").status_code == 200
        assert client.get("/api/audit").status_code == 200
        assert client.get("/api/documents?limit=1&offset=0").status_code == 200
        assert client.get("/api/questions?limit=1&offset=0").status_code == 200
        assert client.get("/api/jobs?limit=1&offset=0").status_code == 200


def test_generated_question_keeps_source(monkeypatch):
    async def fake_generate(prompt, schema):
        return {
            "question": "Quale funzione svolge lo scheletro?",
            "options": {"A": "Sostegno", "B": "Digestione", "C": "Vista", "D": "Udito"},
            "correct_answer": "A",
            "explanation": "Fornisce sostegno.",
            "topic": "Sistema scheletrico",
        }

    import app.main as module
    monkeypatch.setattr(module, "ollama_generate", fake_generate)
    with TestClient(app) as client:
        generated = client.post("/api/questions/generate", json={})
        assert generated.status_code == 200
        question_id = generated.json()["id"]
        sources = client.get(f"/api/questions/{question_id}/sources")
        assert sources.status_code == 200
        assert sources.json()[0]["relevance_score"] == 1.0
