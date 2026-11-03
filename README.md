# Exam AI

MVP local-first per la preparazione agli esami. Include:

- importazione di PDF (estrazione testo con PyMuPDF quando disponibile);
- importazione strutturata di domande Markdown;
- archivio persistente SQLite per sviluppo locale;
- sessioni quiz con correzione deterministica;
- statistiche per fonte e argomento, più ripassi adattivi;
- integrazione opzionale con Ollama (`qwen3:8b`) per lo stato del modello.

## Avvio rapido per i primi test

Il percorso più semplice usa SQLite e non richiede PostgreSQL, Qdrant o Ollama.

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Windows CMD: .venv\Scripts\activate.bat
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

In un secondo terminale:

```bash
cd apps/web
npm install
npm run dev
```

Aprire <http://localhost:3000>. API e documentazione OpenAPI: <http://localhost:8000/docs>.

Per il primo test funzionale:

1. Aprire la dashboard.
2. Importare un file `.md`.
3. Premere **Avvia quiz** e rispondere alla domanda.

Esempio `questions.md`:

```markdown
# Anatomia
## Sistema scheletrico
### Domanda 1
Quale funzione svolge il sistema scheletrico?
A. Movimento
B. Digestione
C. Respirazione
D. Filtrazione
**Risposta corretta:** A
**Spiegazione:** Sostiene il corpo e contribuisce al movimento.
```

In alternativa, verificare solo l'API:

```bash
curl http://localhost:8000/api/health
curl -F "file=@questions.md" http://localhost:8000/api/documents/upload
curl http://localhost:8000/api/questions
```

La configurazione opzionale è in `.env.example`. I dati locali sono salvati in `storage/`.

## Avvio dell'infrastruttura completa

Con Docker Compose installato:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Questo avvia PostgreSQL, Qdrant, backend e frontend con volumi persistenti.

Docker non è necessario per il primo test: SQLite è il database predefinito,
mentre Ollama e Qdrant servono solo per le funzioni AI/RAG.

Le migrazioni PostgreSQL sono in `backend/migrations` e si applicano con:

```bash
cd backend
alembic upgrade head
```
