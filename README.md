# Exam AI

MVP local-first per la preparazione agli esami. Include:

- importazione di PDF (estrazione testo con PyMuPDF quando disponibile);
- importazione strutturata di domande Markdown;
- archivio persistente SQLite per sviluppo locale;
- sessioni quiz con correzione deterministica;
- statistiche per fonte e argomento, più ripassi adattivi;
- integrazione opzionale con Ollama (`qwen3:8b`) per lo stato del modello.

## Avvio rapido

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

In un secondo terminale:

```bash
cd apps/web
npm install
npm run dev
```

Aprire <http://localhost:3000>. API e documentazione OpenAPI: <http://localhost:8000/docs>.

La configurazione è in `.env.example`. I dati locali sono salvati in `storage/`.

## Avvio dell'infrastruttura completa

Con Docker installato:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Questo avvia PostgreSQL, Qdrant, backend e frontend con volumi persistenti.
