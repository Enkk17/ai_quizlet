# Exam AI — Stato del progetto

## Scopo

Questo documento è il recap operativo dello stato di implementazione rispetto alla specifica `ai.md`.

Legenda:

- **100%**: implementato e verificato nel MVP attuale.
- **Parziale**: esiste una prima implementazione, ma non soddisfa ancora tutta la specifica.
- **Mancante**: non ancora implementato; eventuali servizi Docker o configurazioni sono soltanto predisposti.

## Implementato al 100% nel perimetro MVP

| Area | Implementazione presente |
|---|---|
| Bootstrap applicativo | Backend FastAPI e frontend Next.js avviabili separatamente. |
| Health backend | `GET /api/health`. |
| Frontend base | Dashboard responsive con navigazione, metriche, documenti recenti e avvio quiz. |
| Upload file | Upload di PDF, Markdown e Markdown esteso. |
| Persistenza file | Salvataggio locale con nome interno UUID. |
| Hash duplicati | SHA-256 e rifiuto dei documenti già importati. |
| Importazione Markdown | Parsing di capitoli, domande, quattro opzioni, risposta corretta e spiegazione. |
| Domande ufficiali | Conservazione della fonte `OFFICIAL` e pubblicazione senza risposta corretta nell’API quiz. |
| Quiz base | Creazione di una sessione con selezione casuale delle domande. |
| Correzione | Confronto deterministico tra opzione selezionata e risposta corretta. |
| Tentativi | Registrazione persistente di ogni risposta senza sovrascrivere il tentativo precedente. |
| Risultati base | Conteggio risposte, corrette, errate e percentuale di accuratezza. |
| Analytics base | Domande svolte, corrette, accuratezza, domande ufficiali e argomenti. |
| Ripasso base | Visualizzazione dei ripassi scaduti e aggiornamento dell’intervallo dopo il completamento. |
| Container applicativi | Dockerfile funzionanti per backend e frontend. |
| Infrastruttura locale | PostgreSQL, Qdrant, backend e frontend definiti in Docker Compose. |
| Persistenza Docker | Volumi configurati per dati applicativi, PostgreSQL e Qdrant. |
| Verifiche eseguite | Build frontend, build immagini Docker e smoke test dei servizi completati. |

## Implementato parzialmente

| Area | Stato attuale | Mancanze principali |
|---|---|---|
| Milestone 1 — Infrastructure | Stack locale predisposto e avviato. | Mancano monitoraggio completo, Ollama verificato con Qwen3 reale e setup Windows documentato in dettaglio. |
| Milestone 2 — Document Manager | Upload, hash, persistenza e lista documenti funzionanti. | Mancano PostgreSQL, SQLAlchemy, Alembic, stati/job persistenti, dettaglio, eliminazione e reindicizzazione. |
| PDF processing | Estrazione testo con PyMuPDF e conteggio pagine. | Mancano controllo qualità, OCR, struttura, capitoli/argomenti automatici, chunking semantico e pipeline asincrona. |
| Official questions importer | Parser per il formato Markdown previsto. | Mancano segnalazione persistente degli input incompleti, deduplicazione esplicita, revisioni e collegamenti avanzati alle fonti. |
| Exam Engine | Creazione, risposta, correzione e risultati base. | Mancano snapshot, avvio separato, timer, navigazione, modalità di correzione, domande non risposte e risultati dettagliati. |
| Learning Engine | Tentativi e ripasso con intervallo raddoppiato. | Mancano analisi errori, topic progress, SM-2 completo, lacune e raccomandazioni. |
| Analytics | Panoramica globale e performance per argomento. | Mancano serie giornaliere, storico, streak, capitoli, fonti, grafici, affidabilità statistica e readiness score. |
| Ollama | Endpoint di stato e configurazione del modello. | Mancano client centralizzato, chat/generazione, embeddings, timeout avanzati, JSON Schema e gestione degli errori AI. |
| Frontend | Dashboard e quiz in una singola pagina. | Mancano pagine dedicate a documenti, capitoli, domande, esami, analytics, ripassi, risultati e impostazioni. |
| Sicurezza upload | Estensione verificata e limite implicito del server. | Mancano MIME validation completa, limite configurabile, autenticazione, rate limiting e audit log. |

## Mancante rispetto ad `ai.md`

### Architettura e database

- Separazione completa in API, service, repository e AI service layer.
- PostgreSQL come fonte di verità applicativa.
- SQLAlchemy e migrazioni Alembic.
- Modelli completi per `topics`, `document_chunks`, `question_options`,
  `question_sources`, `exam_questions`, `topic_progress`, `review_schedule`,
  `daily_learning_stats`, job, tag, configurazioni e audit log.
- Versionamento e revisioni delle domande ufficiali.

### Document intelligence e RAG

- OCR con OCRmyPDF/Tesseract.
- Riconoscimento affidabile di capitoli, sottocapitoli, sezioni e argomenti.
- Chunking configurabile con overlap e riferimenti alle pagine.
- Modello embedding `nomic-embed-text`.
- Collection Qdrant `exam_documents`.
- Indicizzazione, filtri, retrieval semantico e reindicizzazione differenziale.
- Protezione dei contenuti documentali come dati, non istruzioni per il modello.

### AI e question generation

- Client Ollama unico per `/api/tags`, `/api/generate`, `/api/chat` e `/api/embed`.
- Generazione AI grounded su contesto recuperato.
- Modalità ufficiale, AI, mista, ripasso mirato e simulazione.
- Parametri per difficoltà, capitoli, argomenti e distribuzione delle fonti.
- Validazione delle domande, controllo duplicati, distrattori e riferimenti.
- Stati `AI_GENERATED` e `AI_VERIFIED`.
- Prompt versionati e tracciabilità delle generazioni.

### API mancanti o incomplete

- `/ai/models` e `/ai/test`.
- Dettaglio, eliminazione, processamento e reindicizzazione documenti.
- Capitoli per documento, dettaglio capitolo, topic e domande per capitolo.
- Generazione, dettaglio, modifica, eliminazione e verifica domande.
- Lista, dettaglio e avvio esami.
- Analytics giornaliere, capitoli, fonti e storico.
- Ripassi futuri e storico ripassi.

### Learning, UX e operatività

- Analisi delle categorie di errore e degli errori ricorrenti.
- Piano di ripasso completo basato su accuratezza, difficoltà e storico.
- Dashboard completa con grafici e dati per capitolo/fonte.
- Pagine separate per tutte le aree indicate nella specifica.
- Background jobs per PDF, OCR, indicizzazione e generazione.
- Logging strutturato e monitoraggio di AI, PostgreSQL, Qdrant, RAM e GPU.
- Backup/restore di PostgreSQL, file e Qdrant.
- Autenticazione prima dell’esposizione sulla rete.
- Paginazione delle API e gestione completa degli errori.

### Testing

- Unit test per parser PDF, parser Markdown, chunker, validator, correzione,
  progress tracker e spaced repetition.
- Integration test per PostgreSQL, Qdrant, Ollama, upload e API.
- Test end-to-end del flusso completo.
- Dataset e test di qualità per le domande AI.

## Roadmap consigliata

1. Migrare la persistenza da SQLite a PostgreSQL con SQLAlchemy e Alembic.
2. Separare `main.py` nei moduli API, servizi, repository e schemi.
3. Implementare pipeline PDF, chunking, embeddings e Qdrant.
4. Implementare il client Ollama e la generazione di domande grounded.
5. Completare Exam Engine, Learning Engine e analytics.
6. Sviluppare le pagine frontend mancanti.
7. Aggiungere job asincroni, sicurezza, backup e monitoraggio.
8. Aggiungere test unitari, d’integrazione ed end-to-end.

## Valutazione sintetica

Il repository contiene un **MVP dimostrabile e avviabile**, non ancora il prodotto
completo descritto in `ai.md`.

Stima orientativa per milestone:

| Milestone | Completamento stimato |
|---|---:|
| 1 — Infrastructure & Bootstrap | 70% |
| 2 — Database e Document Manager | 45% |
| 3 — Document Intelligence | 15% |
| 4 — Official Questions Importer | 55% |
| 5 — Question Generation Engine | 5% |
| 6 — Exam Engine | 40% |
| 7 — Learning Engine | 20% |
| 8 — Analytics e UX avanzata | 20% |
| 9 — Hardening e stabilità | 15% |

