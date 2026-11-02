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
| API documentali | Dettaglio, eliminazione, processamento, reindicizzazione e capitoli per documento. |
| API domande | Dettaglio, modifica, eliminazione, verifica e generazione strutturata via Ollama. |
| API esami | Lista, dettaglio e avvio sessioni oltre al flusso di risposta e conclusione. |
| API analytics | Statistiche giornaliere, argomenti, capitoli, fonti e storico esami. |
| API ripassi | Ripassi odierni, futuri e storico. |
| Test automatico | Test API del flusso importazione Markdown → esame → risposta → analytics. |
| Chunking base | Suddivisione configurabile del testo con overlap e persistenza dei chunk. |
| Container applicativi | Dockerfile funzionanti per backend e frontend. |
| Infrastruttura locale | PostgreSQL, Qdrant, backend e frontend definiti in Docker Compose. |
| Persistenza Docker | Volumi configurati per dati applicativi, PostgreSQL e Qdrant. |
| Verifiche eseguite | Build frontend, build immagini Docker e smoke test dei servizi completati. |

## Implementato parzialmente

| Area | Stato attuale | Mancanze principali |
|---|---|---|
| Milestone 1 — Infrastructure | Stack locale predisposto e avviato. | Mancano monitoraggio completo, Ollama verificato con Qwen3 reale e setup Windows documentato in dettaglio. |
| Milestone 2 — Document Manager | Upload, hash, persistenza, lista, dettaglio, eliminazione, processamento e reindicizzazione. | Mancano PostgreSQL, SQLAlchemy, Alembic e job persistenti. |
| PDF processing | Estrazione testo con PyMuPDF, chunking base e riferimenti ai chunk. | Mancano controllo qualità, OCR, struttura, capitoli/argomenti automatici e pipeline asincrona. |
| Official questions importer | Parser per il formato Markdown previsto. | Mancano segnalazione persistente degli input incompleti, deduplicazione esplicita, revisioni e collegamenti avanzati alle fonti. |
| Exam Engine | Creazione, lista, dettaglio, avvio, risposta, correzione e risultati base. | Mancano snapshot, timer, navigazione, modalità di correzione, domande non risposte e risultati dettagliati. |
| Learning Engine | Tentativi e ripasso con intervallo raddoppiato. | Mancano analisi errori, topic progress, SM-2 completo, lacune e raccomandazioni. |
| Analytics | Panoramica globale e performance per argomento. | Mancano serie giornaliere, storico, streak, capitoli, fonti, grafici, affidabilità statistica e readiness score. |
| Ollama | Client di generazione JSON strutturata ed embeddings configurabili. | Mancano chat, prompt versionati e verifica AI indipendente. |
| Qdrant/RAG | Collection, indicizzazione dei chunk e ricerca semantica sono implementate via API REST. | Mancano filtri avanzati, reranking e reindicizzazione differenziale. |
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
- Filtri avanzati, reranking e reindicizzazione differenziale Qdrant.
- Protezione dei contenuti documentali come dati, non istruzioni per il modello.

### AI e question generation

- Client Ollama unico per `/api/tags`, `/api/generate`, `/api/chat` e `/api/embed`.
- Generazione AI grounded su contesto recuperato.
- Modalità ufficiale, AI, mista, ripasso mirato e simulazione.
- Parametri per difficoltà, capitoli, argomenti e distribuzione delle fonti.
- Validazione delle domande, controllo duplicati, distrattori e riferimenti.
- Stati `AI_GENERATED` e `AI_VERIFIED`.
- Prompt versionati e tracciabilità delle generazioni.

### API ancora mancanti o incomplete

- Restano da completare gli endpoint di chunk, RAG, job, backup e configurazione.

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
3. Implementare filtri avanzati, reranking e reindicizzazione differenziale Qdrant.
4. Completare OCR, analisi strutturale e processamento asincrono dei PDF.
5. Completare Exam Engine, Learning Engine e analytics avanzate.
6. Sviluppare le pagine frontend mancanti.
7. Aggiungere job asincroni, sicurezza, backup e monitoraggio.
8. Aggiungere test unitari, d’integrazione, E2E e dataset AI.

## Valutazione sintetica

Il repository contiene un **MVP dimostrabile e avviabile**, non ancora il prodotto
completo descritto in `ai.md`.

Stima orientativa per milestone:

| Milestone | Completamento stimato |
|---|---:|
| 1 — Infrastructure & Bootstrap | 70% |
| 2 — Database e Document Manager | 55% |
| 3 — Document Intelligence | 30% |
| 4 — Official Questions Importer | 55% |
| 5 — Question Generation Engine | 25% |
| 6 — Exam Engine | 50% |
| 7 — Learning Engine | 25% |
| 8 — Analytics e UX avanzata | 30% |
| 9 — Hardening e stabilità | 15% |
