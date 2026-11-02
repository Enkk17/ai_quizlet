EXAM AI
Specifica tecnica completa del progetto
Master Project Specification – Versione 1.0

Tipologia: Piattaforma personale di preparazione agli esami basata su intelligenza artificiale locale
Nome progetto: Exam AI
Modello AI: Qwen3
Runtime AI: Ollama
Backend: Python + FastAPI
Frontend: Next.js + TypeScript
Database relazionale: PostgreSQL
Vector Database: Qdrant
Sistema operativo di sviluppo: Windows
Hardware: NVIDIA RTX 3090 24 GB VRAM, 16 GB RAM
Modalità di funzionamento: Local-first, con elaborazione AI locale
Stato: Specifica architetturale e funzionale iniziale

INDICE
Visione generale del progetto
Obiettivi e principi fondamentali
Hardware e ambiente di esecuzione
Stack tecnologico
Architettura generale
Struttura completa del repository
Architettura del backend
Architettura del frontend
Database relazionale
Gestione dei documenti
Analisi e processamento dei PDF
Importazione delle domande ufficiali Markdown
Knowledge Base e RAG
Integrazione con Qwen3 e Ollama
Question Generation Engine
Sistema di simulazione degli esami
Sistema di correzione delle risposte
Analisi degli errori
Progressi giornalieri
Sistema di ripasso intelligente
Analytics e dashboard
Interfaccia utente
API REST
Sicurezza e privacy
Gestione della qualità e delle allucinazioni
Logging e monitoraggio
Backup e persistenza
Configurazione e variabili d'ambiente
Docker e infrastruttura
Performance e ottimizzazione hardware
Testing e validazione
Roadmap di sviluppo
Requisiti funzionali
Requisiti non funzionali
Criteri di completamento
Regole architetturali da rispettare
Visione futura del progetto

1. VISIONE GENERALE DEL PROGETTO

Exam AI è una piattaforma personale di preparazione agli esami che utilizza un modello linguistico locale per analizzare materiale didattico, comprendere gli argomenti, generare domande a risposta multipla, correggere le risposte e monitorare l'apprendimento nel tempo.

Il sistema non deve essere un semplice generatore casuale di quiz.

Deve comportarsi come un tutor digitale che conosce il materiale di studio, conosce le domande ufficiali dell'esame e tiene traccia delle prestazioni dello studente.

L'obiettivo è realizzare un ambiente nel quale sia possibile:

Caricare libri, dispense e capitoli in PDF.
Analizzare automaticamente il contenuto dei documenti.
Identificare capitoli, sottocapitoli e argomenti.
Importare domande ufficiali da file Markdown.
Collegare le domande ufficiali ai contenuti didattici.
Generare nuove domande utilizzando Qwen3.
Creare simulazioni personalizzate.
Svolgere quiz a risposta multipla.
Ricevere correzioni e spiegazioni.
Analizzare gli errori commessi.
Individuare le lacune nella preparazione.
Monitorare i progressi giornalieri.
Pianificare automaticamente il ripasso degli argomenti.
Misurare il livello di preparazione complessivo.

La piattaforma deve funzionare principalmente in locale, senza inviare documenti, risposte o dati personali a servizi AI esterni.

1.1 Filosofia del progetto

Exam AI deve seguire cinque principi fondamentali.

1. Source-grounded learning

Le domande generate devono basarsi sul materiale didattico caricato.

2. Official questions priority

Le domande ufficiali devono essere conservate e riconosciute come una fonte distinta e privilegiata.

3. Measurable learning

Ogni risposta deve essere registrata e contribuire alla valutazione dei progressi.

4. Adaptive learning

Il sistema deve proporre domande in funzione delle lacune dello studente.

5. Local-first architecture

Il modello AI, i documenti e i dati devono rimanere sotto il controllo dell'utente.

2. OBIETTIVI E PRINCIPALI FUNZIONALITÀ

Il sistema è suddiviso in otto macroaree.

Modulo	Responsabilità
Document Manager	Gestione PDF e Markdown
Document Intelligence	Analisi e comprensione dei documenti
Knowledge Base	Indicizzazione semantica
AI Engine	Comunicazione con Qwen3
Question Engine	Generazione e gestione domande
Exam Engine	Simulazioni e svolgimento quiz
Learning Engine	Errori, progressi e ripassi
Analytics Engine	Statistiche e dashboard

Tutti i moduli devono essere indipendenti dal punto di vista logico, ma comunicare attraverso servizi e API ben definiti.

3. HARDWARE E AMBIENTE DI ESECUZIONE 3.1 Hardware disponibile

Configurazione di riferimento:

Componente	Specifica
Sistema operativo	Windows
RAM	16 GB
GPU	NVIDIA RTX 3090
VRAM	24 GB
Runtime AI	Ollama
Modello generativo	Qwen3
Hosting	Computer locale

La RTX 3090 permette di eseguire modelli quantizzati di dimensioni interessanti.

La RAM di sistema è invece una risorsa da gestire attentamente, soprattutto durante l'elaborazione di PDF molto grandi.

3.2 Configurazione dei modelli

Modello generativo iniziale:

qwen3:8b

Modello embedding iniziale:

nomic-embed-text

In alternativa, potrà essere valutato un modello della famiglia Qwen3 Embedding.

La scelta definitiva degli embeddings dovrà tenere conto di:

Qualità del recupero semantico.
Dimensione dei vettori.
Lingua italiana.
Velocità di inferenza.
Consumo di VRAM.
Compatibilità con Qdrant.
3.3 Ambiente software

Componenti necessari:

Windows 10/11.
Python 3.12.
Node.js LTS.
npm.
Docker Desktop.
WSL2.
NVIDIA Driver aggiornato.
Ollama.
PostgreSQL.
Qdrant.

Docker Desktop sarà utilizzato inizialmente per i database.

Ollama rimarrà installato direttamente sul sistema host.

Frontend e backend verranno avviati separatamente durante lo sviluppo.

4. STACK TECNOLOGICO 4.1 Frontend

Next.js + TypeScript

Responsabilità:

Dashboard principale.
Gestione documenti.
Visualizzazione capitoli.
Configurazione simulazioni.
Interfaccia quiz.
Risultati.
Statistiche.
Gestione ripassi.
Configurazioni.

L'interfaccia dovrà essere responsive e progettata con un design moderno, pulito e professionale.

Librerie previste:

Libreria	Utilizzo
Tailwind CSS	Styling
Lucide React	Icone
Recharts	Grafici
React Hook Form	Gestione form
Zod	Validazione frontend
TanStack Query	Gestione richieste e cache
4.2 Backend

Python + FastAPI

Responsabilità:

Gestione delle richieste.
Orchestrazione dei servizi.
Integrazione con Ollama.
Elaborazione dei PDF.
Parsing Markdown.
Generazione domande.
Correzione risposte.
Gestione database.
Analytics.

L'AI non dovrà mai accedere direttamente al database.

Tutte le operazioni saranno orchestrate dal backend.

4.3 Database

PostgreSQL

Responsabile della persistenza dei dati strutturati.

Qdrant

Responsabile della ricerca vettoriale e semantica sui contenuti dei documenti.

I due database hanno responsabilità differenti e non devono essere utilizzati come sostituti l'uno dell'altro.

4.4 PDF Processing

Tecnologie:

PyMuPDF.
OCRmyPDF.
Tesseract OCR.

PyMuPDF sarà il sistema primario di estrazione.

OCR sarà attivato quando il documento non contiene testo estraibile o quando la qualità dell'estrazione è insufficiente.

4.5 Comunicazione AI

Ollama API:

/api/tags
/api/generate
/api/chat
/api/embed

La comunicazione sarà gestita da un client Python centralizzato.

5. ARCHITETTURA GENERALE

L'architettura complessiva sarà organizzata in livelli.

text
EXAM AI
|
|
NEXT.JS FRONTEND
|
|
FASTAPI
|
+-------------+-------------+
|             |             |
|             |             |
DOCUMENT       QUESTION      LEARNING
SERVICE        SERVICE       SERVICE
|             |             |
+-------------+-------------+
|
AI ENGINE
|
OLLAMA
|
QWEN3
|
+-------------+-------------+
|                           |
POSTGRESQL                    QDRANT
|                           |
DATI STRUTTURATI             EMBEDDINGS

5.1 Separazione delle responsabilità

Il frontend non deve conoscere i dettagli interni di Qwen.

Il backend deve esporre API indipendenti dal provider AI.

Qwen deve occuparsi di:

Comprensione linguistica.
Generazione delle domande.
Generazione delle spiegazioni.
Classificazione degli argomenti.
Analisi qualitativa degli errori.

Il backend deve occuparsi di:

Calcolo dei punteggi.
Registrazione delle risposte.
Gestione delle sessioni.
Controllo delle risposte corrette.
Calcolo delle statistiche.
Pianificazione dei ripassi.
Validazione dei dati.

Questo permette di sostituire Qwen con un altro modello senza riscrivere il resto della piattaforma.

6. STRUTTURA COMPLETA DEL REPOSITORY

Struttura di riferimento:

text
exam-ai/
│
├── apps/
│   └── web/
│       ├── public/
│       ├── src/
│       │   ├── app/
│       │   │   ├── page.tsx
│       │   │   ├── dashboard/
│       │   │   ├── documents/
│       │   │   ├── exams/
│       │   │   ├── questions/
│       │   │   ├── analytics/
│       │   │   ├── reviews/
│       │   │   └── settings/
│       │   │
│       │   ├── components/
│       │   │   ├── layout/
│       │   │   ├── dashboard/
│       │   │   ├── documents/
│       │   │   ├── quiz/
│       │   │   ├── analytics/
│       │   │   └── common/
│       │   │
│       │   ├── hooks/
│       │   ├── lib/
│       │   ├── services/
│       │   ├── types/
│       │   └── styles/
│       │
│       ├── package.json
│       └── .env.local
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   ├── ai.py
│   │   │   │   ├── documents.py
│   │   │   │   ├── chapters.py
│   │   │   │   ├── questions.py
│   │   │   │   ├── exams.py
│   │   │   │   ├── answers.py
│   │   │   │   ├── analytics.py
│   │   │   │   └── reviews.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── security.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── database/
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   └── repositories/
│   │   │
│   │   ├── schemas/
│   │   │   ├── document.py
│   │   │   ├── question.py
│   │   │   ├── exam.py
│   │   │   ├── answer.py
│   │   │   └── analytics.py
│   │   │
│   │   ├── services/
│   │   │   ├── ollama/
│   │   │   │   ├── client.py
│   │   │   │   ├── generation.py
│   │   │   │   └── embeddings.py
│   │   │   │
│   │   │   ├── ingestion/
│   │   │   │   ├── pdf_parser.py
│   │   │   │   ├── ocr.py
│   │   │   │   ├── markdown_parser.py
│   │   │   │   ├── document_analyzer.py
│   │   │   │   └── chunker.py
│   │   │   │
│   │   │   ├── rag/
│   │   │   │   ├── retriever.py
│   │   │   │   ├── indexer.py
│   │   │   │   └── context_builder.py
│   │   │   │
│   │   │   ├── questions/
│   │   │   │   ├── generator.py
│   │   │   │   ├── validator.py
│   │   │   │   ├── classifier.py
│   │   │   │   └── deduplicator.py
│   │   │   │
│   │   │   ├── exams/
│   │   │   │   ├── builder.py
│   │   │   │   ├── session.py
│   │   │   │   └── correction.py
│   │   │   │
│   │   │   ├── learning/
│   │   │   │   ├── error_analyzer.py
│   │   │   │   ├── progress_tracker.py
│   │   │   │   ├── topic_analyzer.py
│   │   │   │   └── spaced_repetition.py
│   │   │   │
│   │   │   └── analytics/
│   │   │       ├── daily.py
│   │   │       ├── topics.py
│   │   │       └── performance.py
│   │   │
│   │   ├── tasks/
│   │   └── main.py
│   │
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── infrastructure/
│   ├── docker-compose.yml
│   └── postgres/
│
├── storage/
│   ├── uploads/
│   │   ├── pdfs/
│   │   └── official_questions/
│   │
│   ├── processed/
│   │   ├── extracted/
│   │   └── metadata/
│   │
│   └── backups/
│
├── docs/
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   └── development.md
│
├── .env.example
├── .gitignore
├── README.md
└── PROJECT_SPECIFICATION.md

La struttura potrà evolvere, ma non dovrà trasformarsi in un unico file contenente tutta la logica applicativa.

7. ARCHITETTURA DEL BACKEND

Il backend deve seguire una struttura a livelli.

7.1 API Layer

Responsabile della comunicazione HTTP.

Deve:

Ricevere richieste.
Validare input.
Richiamare i servizi.
Restituire risultati.
Gestire errori HTTP.

Non deve contenere logica AI complessa.

7.2 Service Layer

Contiene la logica applicativa.

Esempi:

DocumentService.
QuestionService.
ExamService.
AnalyticsService.
LearningService.
7.3 Repository Layer

Gestisce l'accesso al database.

Esempi:

DocumentRepository.
QuestionRepository.
ExamRepository.
AttemptRepository.
7.4 AI Service Layer

Gestisce il collegamento con Ollama e le operazioni AI.

Deve essere indipendente dalle route HTTP.

7.5 Background Tasks

Le operazioni pesanti non devono bloccare le richieste HTTP.

Esempi:

OCR.
Analisi di PDF grandi.
Indicizzazione documentale.
Generazione di grandi quantità di domande.
Ricalcolo delle statistiche.

Per il primo MVP si possono utilizzare task asincroni e un sistema di job persistenti nel database.

Successivamente potrà essere introdotta una coda dedicata, ad esempio Redis + RQ o Celery.

Ogni job deve avere:

ID.
Tipo.
Stato.
Data di creazione.
Data di completamento.
Eventuale errore.
Percentuale di avanzamento.

Stati:

PENDING.
PROCESSING.
COMPLETED.
FAILED.
CANCELLED.
8\. ARCHITETTURA DEL FRONTEND

Il frontend deve offrire un'esperienza semplice e intuitiva.

8.1 Navigazione principale

Sidebar:

Dashboard.
Documenti.
Capitoli.
Domande.
Simulazioni.
Progressi.
Ripasso.
Impostazioni.
8.2 Dashboard

La dashboard rappresenta il punto di ingresso.

Deve mostrare:

Percentuale di risposte corrette.
Numero di domande risposte.
Numero di domande ufficiali svolte.
Numero di domande AI svolte.
Tempo totale di studio.
Argomenti più deboli.
Argomenti più forti.
Andamento giornaliero.
Ripassi in scadenza.
Ultime sessioni.

I dati devono essere reali, provenienti dal database.

Non devono essere utilizzati valori fittizi nell'applicazione finale.

8.3 Pagina Documenti

Funzionalità:

Upload PDF.
Upload Markdown.
Elenco documenti.
Stato di elaborazione.
Visualizzazione dimensione.
Numero di pagine.
Capitoli identificati.
Data di importazione.
Possibilità di eliminazione.
Possibilità di reindicizzazione.

Stati del documento:

UPLOADED.
PROCESSING.
ANALYZED.
INDEXED.
FAILED.
8.4 Pagina Capitoli

Visualizzazione gerarchica:

text
Libro di riferimento
│
├── Capitolo 1
│   ├── Argomento 1.1
│   ├── Argomento 1.2
│   └── Argomento 1.3
│
├── Capitolo 2
│   ├── Argomento 2.1
│   └── Argomento 2.2
│
└── Capitolo 3

Per ogni capitolo:

Numero di domande ufficiali.
Numero di domande AI.
Percentuale di corrette.
Tempo medio di risposta.
Stato di preparazione.
8.5 Pagina Simulazioni

Permette di creare una sessione d'esame personalizzata.

8.6 Pagina Analytics

Contiene grafici e statistiche.

8.7 Pagina Ripasso

Visualizza gli argomenti da ripassare oggi, quelli imminenti e quelli completati.

9. DATABASE RELAZIONALE

PostgreSQL è la fonte di verità per tutti i dati strutturati.

9.1 Tabella documents

Campi:

Campo	Tipo	Descrizione
id	UUID	Identificativo
filename	VARCHAR	Nome originale
stored_path	TEXT	Percorso file
document_type	ENUM	PDF / MARKDOWN
file_hash	VARCHAR	Hash SHA-256
file_size	BIGINT	Dimensione
status	ENUM	Stato elaborazione
total_pages	INTEGER	Numero pagine
created_at	TIMESTAMP	Importazione
updated_at	TIMESTAMP	Aggiornamento

Lo SHA-256 servirà per identificare file duplicati.

9.2 Tabella chapters

Campi:

id.
document_id.
parent_id.
title.
chapter_number.
description.
start_page.
end_page.
order_index.

Deve supportare una struttura gerarchica.

9.3 Tabella topics

Campi:

id.
chapter_id.
name.
description.
keywords.
created_at.

Gli argomenti devono poter essere associati a più documenti, se necessario.

9.4 Tabella document_chunks

Campi:

id.
document_id.
chapter_id.
topic_id.
content.
page_start.
page_end.
chunk_index.
content_hash.
created_at.

Qdrant conserverà i vettori e i metadati necessari al recupero.

PostgreSQL conserverà il testo originale e i riferimenti documentali.

9.5 Tabella questions

Campi:

id.
document_id.
chapter_id.
topic_id.
question_text.
explanation.
question_type.
source_type.
difficulty.
correct_option_id.
status.
created_at.
updated_at.

Tipologie:

OFFICIAL.
AI_GENERATED.
AI_VERIFIED.

Le domande devono essere versionate quando vengono modificate.

9.6 Tabella question_options

Campi:

id.
question_id.
option_key.
option_text.
is_correct.
order_index.

Ogni domanda a risposta multipla avrà inizialmente quattro alternative.

La risposta corretta non dovrà essere esposta nelle API pubbliche durante lo svolgimento del quiz.

9.7 Tabella question_sources

Campi:

id.
question_id.
document_id.
chunk_id.
page_number.
source_type.
relevance_score.

Permette di collegare una domanda alle fonti utilizzate per crearla o verificarla.

9.8 Tabella exams

Campi:

id.
title.
mode.
total_questions.
time_limit_seconds.
status.
started_at.
completed_at.
created_at.
9.9 Tabella exam_questions

Campi:

id.
exam_id.
question_id.
order_index.
question_snapshot.

La snapshot permette di conservare la versione della domanda utilizzata nella simulazione anche se successivamente la domanda viene modificata.

9.10 Tabella answer_attempts

Campi:

id.
exam_id.
question_id.
selected_option_id.
is_correct.
response_time_seconds.
answered_at.
attempt_number.

La registrazione deve essere immutabile: non sovrascrivere i tentativi precedenti.

9.11 Tabella topic_progress

Campi:

id.
topic_id.
total_attempts.
correct_attempts.
incorrect_attempts.
accuracy_percentage.
average_response_time.
last_attempt_at.
mastery_score.

Questi valori possono essere aggiornati tramite aggregazioni dei tentativi.

9.12 Tabella review_schedule

Campi:

id.
topic_id.
due_date.
interval_days.
repetition_count.
easiness_factor.
last_reviewed_at.
status.
9.13 Tabelle aggiuntive

Prevedere inoltre:

ai_generation_jobs.
document_processing_jobs.
daily_learning_stats.
question_tags.
exam_configuration.
app_settings.
audit_logs.

Le migrazioni devono essere gestite tramite Alembic.

10. GESTIONE DEI DOCUMENTI

Il Document Manager deve gestire due categorie principali.

Materiale didattico:

PDF.
Dispense.
Libri.
Appunti.

Domande ufficiali:

File Markdown.
Eventuali successive importazioni strutturate.

I documenti devono essere salvati localmente.

Il database conserva i metadati e i riferimenti ai file.

Il sistema non deve dipendere dai nomi originali dei documenti per identificare i record.

11. PDF PROCESSING ENGINE

Questa è una delle componenti centrali del progetto.

11.1 Pipeline
text
UPLOAD PDF
|
v
VALIDAZIONE FILE
|
v
CALCOLO SHA-256
|
v
ESTRAZIONE TESTO
|
v
CONTROLLO QUALITÀ
|
+------> OCR SE NECESSARIO
|
v
RICONOSCIMENTO STRUTTURA
|
v
IDENTIFICAZIONE CAPITOLI
|
v
IDENTIFICAZIONE ARGOMENTI
|
v
CHUNKING
|
v
SALVATAGGIO DATABASE
|
v
GENERAZIONE EMBEDDINGS
|
v
INDICIZZAZIONE QDRANT
|
v
DOCUMENTO ANALIZZATO

11.2 Estrazione del testo

PyMuPDF deve estrarre:

Testo.
Numero di pagina.
Posizione del testo.
Blocchi.
Eventuali informazioni strutturali.

Il sistema deve preservare il collegamento tra testo e pagina originale.

11.3 OCR

Se il PDF è una scansione:

Rilevare la scarsa presenza di testo.
Attivare OCR.
Estrarre il contenuto riconosciuto.
Registrare che il testo deriva da OCR.

Non applicare OCR indiscriminatamente a ogni documento.

11.4 Analisi della struttura

Il sistema deve identificare:

Titolo del documento.
Capitoli.
Sottocapitoli.
Sezioni.
Definizioni.
Elenchi.
Tabelle, quando possibile.
Formule.
Concetti principali.

L'identificazione deve combinare regole strutturali e AI.

Non bisogna affidare interamente la struttura documentale a Qwen.

11.5 Chunking

Il documento deve essere suddiviso in porzioni semanticamente coerenti.

Configurazione iniziale indicativa:

Dimensione: 500–900 token.
Overlap: 80–120 token.
Rispetto dei confini dei paragrafi.
Mantenimento dei riferimenti alle pagine.

Il chunking dovrà essere configurabile.

Non dividere arbitrariamente un paragrafo a metà se è possibile conservarne l'unità semantica.

11.6 Metadati

Ogni chunk deve conservare:

Document ID.
Capitolo.
Argomento.
Pagina iniziale.
Pagina finale.
Indice.
Hash.
Contenuto.
12\. IMPORTAZIONE DELLE DOMANDE UFFICIALI MARKDOWN

Il file .md rappresenta una fonte fondamentale.

Le domande ufficiali devono essere considerate dati strutturati, non semplice testo da passare al modello.

12.1 Formato Markdown consigliato
markdown

# Anatomia

## Capitolo 1 - Sistema scheletrico

### Domanda 1

Quale funzione svolge il sistema scheletrico?

A. Funzione A
B. Funzione B
C. Funzione C
D. Funzione D

**Risposta corretta:** B

**Spiegazione:** Eventuale spiegazione.

### Domanda 2

Quale affermazione è corretta?

A. Opzione A
B. Opzione B
C. Opzione C
D. Opzione D

**Risposta corretta:** C

12.2 Parser Markdown

Il parser deve:

Leggere il file.
Identificare capitoli.
Identificare domande.
Estrarre alternative.
Identificare la risposta corretta.
Estrarre eventuali spiegazioni.
Normalizzare il testo.
Verificare la struttura.
Identificare duplicati.
Salvare nel database.
12.3 Validazione

Una domanda ufficiale è valida se:

Contiene il testo della domanda.
Contiene tutte le alternative richieste.
Contiene una sola risposta corretta.
Non contiene alternative vuote.
Non è un duplicato non intenzionale.

Le domande incomplete devono essere segnalate.

Non devono essere eliminate silenziosamente.

12.4 Integrità delle domande ufficiali

Le domande ufficiali devono essere conservate fedelmente.

Il sistema può aggiungere:

Argomento.
Capitolo.
Tag.
Spiegazione supplementare.
Riferimenti ai PDF.

Non deve modificare automaticamente il testo originale.

Le modifiche devono essere tracciate e reversibili.

13. KNOWLEDGE BASE E RAG

RAG significa Retrieval-Augmented Generation.

È il sistema che permette a Qwen di utilizzare i contenuti dei PDF senza doverli inserire integralmente nel prompt.

13.1 Funzionamento
text
DOMANDA / ARGOMENTO
|
v
EMBEDDING DELLA QUERY
|
v
RICERCA QDRANT
|
v
RECUPERO CHUNK
|
v
FILTRAGGIO PER CAPITOLO
|
v
CONTESTO RILEVANTE
|
v
QWEN3
|
v
RISULTATO STRUTTURATO

13.2 Embeddings

Gli embeddings convertono il testo in vettori numerici.

Il sistema utilizzerà un modello dedicato.

La dimensione dei vettori deve essere letta dalla configurazione del modello e utilizzata coerentemente nella creazione della collection Qdrant.

Non deve essere impostata arbitrariamente.

13.3 Qdrant

Collection iniziale:

exam_documents

Payload:

json
{
"document_id": "uuid",
"chapter_id": "uuid",
"topic_id": "uuid",
"chunk_id": "uuid",
"page_start": 14,
"page_end": 15,
"content_hash": "sha256"
}

Il contenuto testuale potrà essere conservato anche nel payload, ma PostgreSQL rimarrà la fonte principale del testo originale.

13.4 Retrieval

Il sistema deve supportare:

Ricerca semantica.
Filtri per documento.
Filtri per capitolo.
Filtri per argomento.
Ricerca per pagine.
Recupero dei chunk più pertinenti.

Successivamente potrà essere introdotto un reranker.

13.5 Aggiornamento dell'indice

Se un documento viene aggiornato:

Ricalcolare l'hash.
Identificare i chunk modificati.
Rimuovere i vettori obsoleti.
Inserire i nuovi vettori.
Aggiornare i metadati.

Evitare di indicizzare ripetutamente lo stesso documento.

14. INTEGRAZIONE QWEN3 E OLLAMA 14.1 Responsabilità

Qwen3 deve svolgere attività linguistiche.

Non deve decidere autonomamente:

Se una risposta è corretta.
Il punteggio di un esame.
La percentuale di preparazione.
La data del prossimo ripasso.
La validità di una transazione.

Queste attività appartengono al backend.

14.2 Client centralizzato

Creare un unico OllamaClient.

Responsabilità:

Connessione.
Verifica stato.
Elenco modelli.
Generazione.
Chat.
Embeddings.
Timeout.
Gestione errori.
Logging.

Non creare richieste HTTP indipendenti a Ollama in ogni modulo.

14.3 Output strutturato

Utilizzare JSON Schema quando supportato dall'endpoint Ollama.

Il modello deve produrre risposte validate.

Esempio:

json
{
"question": "Quale affermazione è corretta?",
"options": [
{"id": "A", "text": "Opzione A"},
{"id": "B", "text": "Opzione B"},
{"id": "C", "text": "Opzione C"},
{"id": "D", "text": "Opzione D"}
],
"correct_answer": "B",
"explanation": "Spiegazione didattica.",
"difficulty": "medium",
"topic": "Anatomia",
"source_references": [
{
"document_id": "uuid",
"page": 14
}
]
}

14.4 Prompt Engineering

Creare prompt separati per:

Generazione domande.
Spiegazione risposte.
Classificazione argomenti.
Analisi degli errori.
Verifica coerenza.
Generazione distrattori.

I prompt devono essere versionati.

Ogni generazione deve poter essere ricondotta alla versione del prompt utilizzata.

14.5 Gestione del modello

Il modello deve essere configurabile.

Non hardcodare il nome Qwen3 in ogni servizio.

Configurazione centrale:

MODEL_NAME.
TEMPERATURE.
CONTEXT_LENGTH.
MAX_OUTPUT_TOKENS.
REQUEST_TIMEOUT.
NUM_PARALLEL.

I valori definitivi saranno determinati attraverso test reali sulla RTX 3090.

15. QUESTION GENERATION ENGINE

Il motore di generazione delle domande è uno dei componenti più importanti.

15.1 Modalità disponibili
Modalità A – Domande ufficiali

Utilizza esclusivamente domande importate dal portale ufficiale.

Le domande devono essere presentate senza alterazioni sostanziali.

Modalità B – Domande generate dall'AI

Qwen crea nuove domande basandosi sui contenuti dei PDF.

Le domande devono essere pertinenti al programma.

Modalità C – Modalità mista

Combina domande ufficiali e domande AI.

La distribuzione deve essere configurabile.

Esempio:

60% ufficiali.
40% AI.
Modalità D – Ripasso mirato

Genera o seleziona domande sugli argomenti con prestazioni insufficienti.

Modalità E – Simulazione d'esame

Crea un esame completo con distribuzione delle domande, tempo e difficoltà configurabili.

15.2 Parametri di generazione

L'utente deve poter specificare:

Capitolo.
Sottocapitolo.
Argomento.
Numero di domande.
Difficoltà.
Fonte delle domande.
Distribuzione ufficiali/AI.
Possibilità di ripetere domande già viste.
Modalità di correzione.
15.3 Difficoltà

Tre livelli iniziali:

Easy

Verifica definizioni e concetti fondamentali.

Medium

Verifica comprensione e collegamenti tra concetti.

Hard

Verifica ragionamento, applicazione e distinzioni tra concetti simili.

La difficoltà deve essere coerente con il contenuto del materiale didattico.

15.4 Distrattori

Le alternative errate devono essere plausibili.

Non devono essere:

Assurde.
Ambigue.
Equivalenti alla risposta corretta.
Contraddittorie rispetto alla domanda.
Estranee al materiale didattico.

Ogni domanda deve avere una sola risposta corretta.

15.5 Verifica delle domande

Prima del salvataggio:

Validare JSON.
Verificare numero alternative.
Verificare risposta corretta.
Controllare riferimenti.
Controllare coerenza della spiegazione.
Rilevare duplicati.
Controllare che la domanda sia basata sul contesto recuperato.

Le domande AI non sufficientemente supportate devono essere scartate o contrassegnate per revisione.

Non devono essere automaticamente classificate come verificate.

15.6 Provenienza

Ogni domanda deve avere una provenienza:

OFFICIAL.
AI_GENERATED.
AI_VERIFIED.

Una domanda AI_VERIFIED deve avere evidenze documentali e superare i controlli previsti.

16. EXAM ENGINE

Il motore degli esami gestisce le simulazioni.

16.1 Creazione esame

Configurazione:

Nome.
Capitoli.
Argomenti.
Numero di domande.
Tempo massimo.
Modalità.
Difficoltà.
Percentuale domande ufficiali.
Percentuale domande AI.
16.2 Avvio esame

Quando viene avviato:

Creare una sessione.
Selezionare le domande.
Registrare l'ordine.
Conservare snapshot delle domande.
Iniziare il timer.
Registrare la data.
16.3 Svolgimento

Durante il quiz:

Visualizzare una domanda alla volta.
Mostrare quattro alternative.
Permettere selezione della risposta.
Permettere navigazione.
Mostrare domande completate.
Mostrare tempo residuo.
Permettere eventuale revisione.

La risposta corretta non deve essere trasmessa prima della correzione.

16.4 Modalità di correzione

Due modalità.

Correzione immediata

Dopo ogni risposta viene mostrato l'esito e la spiegazione.

Correzione finale

Le risposte vengono valutate solo al termine della simulazione.

16.5 Risultati

Mostrare:

Risposte corrette.
Risposte errate.
Domande non risposte.
Percentuale.
Tempo totale.
Tempo medio per domanda.
Risultati per capitolo.
Risultati per argomento.
Confronto tra domande ufficiali e AI.
17\. ANSWER EVALUATION ENGINE

La correzione delle risposte deve essere deterministica.

La logica è semplice:

text
selected_option_id == correct_option_id

Se coincidono:

Risposta corretta.
Incremento corrette.
Aggiornamento statistiche.

Altrimenti:

Risposta errata.
Incremento errori.
Registrazione della risposta selezionata.
Aggiornamento delle statistiche.

Non chiedere a Qwen di decidere se una risposta a scelta multipla è corretta quando la risposta corretta è già presente nel database.

Qwen può essere utilizzato per generare una spiegazione aggiuntiva, non per sostituire il sistema di correzione.

18. ERROR ANALYSIS ENGINE

Il sistema deve analizzare gli errori in modo intelligente.

Non basta mostrare il numero di risposte sbagliate.

Bisogna identificare quali concetti non sono stati compresi.

18.1 Dati analizzati
Domanda.
Risposta selezionata.
Risposta corretta.
Capitolo.
Argomento.
Fonte.
Tempo impiegato.
Numero di tentativi.
Storico dello stesso argomento.
18.2 Classificazione degli errori

Categorie:

Mancanza di conoscenza.
Confusione tra concetti.
Errore di interpretazione.
Distrazione.
Difficoltà applicativa.
Dimenticanza.
Risposta casuale.

Queste categorie sono ipotesi, non fatti certi.

Il sistema può utilizzare il modello per suggerire una classificazione, ma deve conservarne anche il livello di confidenza.

18.3 Analisi automatica

Esempio:

text
ARGOMENTO: Fisiologia

Domande svolte: 20
Risposte corrette: 11
Risposte errate: 9

Accuratezza: 55%

Problema individuato:
Difficoltà nella comprensione dei meccanismi
di regolazione.

Azioni suggerite:

- Ripassare il paragrafo 2.3.
- Ripetere le domande errate.
- Svolgere 10 domande mirate.

Le raccomandazioni devono essere basate sui dati reali.

18.4 Errori ricorrenti

Il sistema deve rilevare:

Argomenti sbagliati ripetutamente.
Domande già sbagliate in precedenza.
Errori dopo un ripasso.
Argomenti con accuratezza in diminuzione.
19\. PROGRESSI GIORNALIERI

Ogni attività deve contribuire allo storico dello studente.

19.1 Metriche giornaliere
Domande svolte.
Risposte corrette.
Risposte errate.
Percentuale di corrette.
Tempo di studio.
Numero di simulazioni.
Argomenti affrontati.
Ripassi completati.
19.2 Grafici

Dashboard giornaliera:

Andamento precisione.
Domande svolte per giorno.
Tempo di studio.
Progressi per capitolo.
Progressi per argomento.
19.3 Storico

L'utente deve poter consultare:

Oggi.
Ultimi 7 giorni.
Ultimi 30 giorni.
Ultimi 90 giorni.
Tutto lo storico.
19.4 Calcolo delle percentuali

Formula:

text
accuracy =
(correct_answers / total_answered) * 100

Le domande non risposte devono essere conteggiate separatamente.

La percentuale complessiva deve essere calcolata sui tentativi effettivi, evitando di confondere il numero di domande con quello delle sessioni.

19.5 Serie giornaliera

È possibile introdurre un sistema di streak.

Uno streak rappresenta il numero di giorni consecutivi in cui lo studente ha svolto attività valida.

La soglia minima giornaliera deve essere configurabile.

20. SPACED REPETITION ENGINE

Il sistema deve pianificare i ripassi.

Si può partire da una versione adattata di SM-2.

20.1 Principio

Un argomento non deve essere considerato appreso semplicemente perché è stato risposto correttamente una volta.

Il sistema deve osservare le prestazioni nel tempo.

20.2 Parametri
Ultimo ripasso.
Numero di ripetizioni.
Intervallo.
Accuratezza.
Tempo medio.
Difficoltà.
Errori ricorrenti.
20.3 Esempio
text
ARGOMENTO: Anatomia

Primo ripasso: oggi
Secondo ripasso: tra 1 giorno
Terzo ripasso: tra 3 giorni
Quarto ripasso: tra 6 giorni
Quinto ripasso: tra 12 giorni

Gli intervalli devono essere modificabili.

20.4 Regole

Se l'utente sbaglia ripetutamente:

Ridurre l'intervallo.
Proporre nuove domande.
Suggerire la lettura del materiale.

Se risponde correttamente in modo consistente:

Aumentare gradualmente l'intervallo.

Il sistema deve distinguere tra apprendimento recente e conoscenza consolidata.

21. ANALYTICS ENGINE

Le statistiche devono essere basate sui tentativi salvati.

21.1 KPI principali
Accuratezza complessiva.
Domande totali.
Domande ufficiali svolte.
Domande AI svolte.
Tempo medio di risposta.
Ore di studio.
Argomenti deboli.
Argomenti forti.
Ripassi in scadenza.
Andamento temporale.
21.2 Performance per capitolo

Esempio:

Capitolo	Accuratezza	Stato
Anatomia	92%	Forte
Fisiologia	83%	Buono
Patologia	61%	Da migliorare
Farmacologia	48%	Critico

Le soglie devono essere configurabili.

21.3 Performance per fonte

Confrontare:

Domande ufficiali.
Domande AI.
Domande AI verificate.

Questo permette di valutare se la generazione AI sta effettivamente preparando lo studente al formato dell'esame.

21.4 Affidabilità delle statistiche

Una percentuale basata su due risposte non deve essere interpretata allo stesso modo di una percentuale basata su cento risposte.

La dashboard deve mostrare anche la quantità di dati utilizzata.

22. INTERFACCIA UTENTE

Il design deve essere moderno, professionale e orientato allo studio.

22.1 Direzione visuale

Caratteristiche:

Dark mode.
Layout pulito.
Sidebar.
Cards.
Grafici.
Tabelle.
Indicatori di stato.
Navigazione semplice.

Deve essere prevista anche una light mode.

22.2 Dashboard

Sezioni:

Panoramica.
Progressi.
Attività recente.
Argomenti deboli.
Ripassi.
Stato AI.
22.3 Document Manager

Sezioni:

Documenti caricati.
Stato elaborazione.
Capitoli.
Argomenti.
Domande ufficiali associate.
22.4 Quiz Interface

Elementi:

Numero domanda.
Testo.
Quattro risposte.
Navigazione.
Timer.
Progress bar.
Pulsante conferma.
22.5 Exam Results

Elementi:

Voto o punteggio.
Percentuale.
Risposte corrette.
Risposte errate.
Spiegazioni.
Fonti.
Analisi degli errori.
23\. API REST

Base URL:

http://localhost:8000/api

Tutte le API devono avere schemi Pydantic.

23.1 Health
Metodo	Endpoint	Descrizione
GET	/health	Stato backend
GET	/ai/status	Stato Ollama
GET	/ai/models	Modelli disponibili
POST	/ai/test	Test generazione
23.2 Documents
Metodo	Endpoint	Descrizione
GET	/documents	Lista documenti
POST	/documents/upload	Upload PDF
POST	/documents/import-md	Import Markdown
GET	/documents/{id}	Dettaglio
DELETE	/documents/{id}	Eliminazione
POST	/documents/{id}/process	Elaborazione
POST	/documents/{id}/reindex	Reindicizzazione
GET	/documents/{id}/chapters	Capitoli
23.3 Chapters
Metodo	Endpoint	Descrizione
GET	/chapters	Lista capitoli
GET	/chapters/{id}	Dettaglio
GET	/chapters/{id}/topics	Argomenti
GET	/chapters/{id}/questions	Domande
23.4 Questions
Metodo	Endpoint	Descrizione
GET	/questions	Lista domande
POST	/questions/generate	Generazione AI
GET	/questions/{id}	Dettaglio
PATCH	/questions/{id}	Modifica
DELETE	/questions/{id}	Eliminazione
POST	/questions/{id}/verify	Verifica
23.5 Exams
Metodo	Endpoint	Descrizione
POST	/exams	Creazione esame
GET	/exams	Lista sessioni
GET	/exams/{id}	Dettaglio
POST	/exams/{id}/start	Avvio
POST	/exams/{id}/answer	Risposta
POST	/exams/{id}/finish	Conclusione
GET	/exams/{id}/results	Risultati
23.6 Analytics
Metodo	Endpoint	Descrizione
GET	/analytics/overview	Panoramica
GET	/analytics/daily	Statistiche giornaliere
GET	/analytics/topics	Performance argomenti
GET	/analytics/chapters	Performance capitoli
GET	/analytics/sources	Performance per fonte
GET	/analytics/history	Storico
23.7 Reviews
Metodo	Endpoint	Descrizione
GET	/reviews/today	Ripassi di oggi
GET	/reviews/upcoming	Ripassi futuri
POST	/reviews/{id}/complete	Completa ripasso
GET	/reviews/history	Storico ripassi

Le API devono essere versionate quando necessario.

24. SICUREZZA E PRIVACY

Exam AI deve essere local-first.

24.1 Dati

Documenti, domande, risposte e statistiche devono rimanere localmente.

Non devono essere inviati automaticamente a provider esterni.

24.2 Upload

Validazioni:

Tipologia file.
Estensione.
MIME type.
Dimensione.
Hash.
Nome file normalizzato.

Non fidarsi esclusivamente dell'estensione.

24.3 Database
Credenziali in .env.
Nessuna password nel repository.
Backup regolari.
Accesso limitato ai servizi locali.
Migrazioni versionate.
24.4 API

Prevedere:

Validazione input.
Limiti dimensione upload.
Timeout.
Gestione errori.
CORS ristretto.
Protezione dalle richieste duplicate.

Se l'applicazione viene esposta sulla rete locale o su Internet, aggiungere autenticazione e autorizzazione prima della pubblicazione.

24.5 Protezione delle fonti

I documenti caricati devono essere trattati come dati, non come istruzioni per il modello.

Eventuali istruzioni presenti nei PDF non devono poter modificare il comportamento del sistema o i prompt di sistema.

24.6 Riservatezza

Non inviare informazioni dei documenti nei log ordinari.

Non conservare inutilmente prompt completi contenenti informazioni personali.

25. QUALITÀ E CONTROLLO DELLE ALLUCINAZIONI

Uno dei problemi più importanti dei sistemi generativi è la possibilità di creare informazioni inesatte.

Exam AI deve implementare controlli specifici.

25.1 Regola principale

Le domande AI devono essere basate su contenuti recuperati dai PDF.

25.2 Riferimenti

Ogni domanda generata deve avere riferimenti a:

Documento.
Capitolo.
Pagina.
Chunk.

I riferimenti devono essere verificati dal backend.

25.3 Domande non supportate

Se il contesto recuperato non contiene informazioni sufficienti:

Non generare la domanda.
Oppure segnalare che la copertura documentale è insufficiente.

Non inventare fonti.

25.4 Validazione indipendente

Il backend deve verificare:

Risposta corretta.
Alternative.
Coerenza.
Fonte.
Duplicati.

Per le domande più importanti si potrà utilizzare una seconda fase di verifica AI.

La verifica AI non deve essere considerata infallibile.

25.5 Distinzione delle fonti

Una domanda generata non deve essere presentata come domanda ufficiale.

La provenienza deve essere sempre visibile.

26. LOGGING E MONITORAGGIO

Registrare:

Errori applicativi.
Richieste API.
Durata delle operazioni.
Stato dei job.
Errori di Ollama.
Errori di Qdrant.
Errori database.
Tempi di generazione.

Non registrare indiscriminatamente contenuti completi dei documenti.

26.1 Monitoraggio AI

Visualizzare:

Modello attivo.
Connessione Ollama.
Tempo medio generazione.
Errori.
Modelli disponibili.
26.2 Monitoraggio infrastruttura

Visualizzare, dove disponibili:

Utilizzo GPU.
VRAM.
RAM.
Spazio storage.
Stato PostgreSQL.
Stato Qdrant.
27\. BACKUP E PERSISTENZA

I dati non devono andare persi dopo il riavvio del computer.

27.1 Backup PostgreSQL

Utilizzare pg_dump.

27.2 Backup documenti

Conservare:

PDF originali.
File Markdown originali.
Metadati.
Risultati delle elaborazioni.
27.3 Backup Qdrant

Utilizzare snapshot o una strategia di esportazione compatibile con la versione installata.

27.4 Ripristino

Il sistema deve poter recuperare:

Database.
Documenti.
Indice vettoriale.

I backup devono essere testati periodicamente.

28. CONFIGURAZIONE E VARIABILI D'AMBIENTE

Configurazione centrale.

dotenv
APP_NAME=Exam AI
APP_ENV=development

API_HOST=127.0.0.1
API_PORT=8000

OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:8b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

DATABASE_URL=postgresql+psycopg://exam_user:CHANGE_ME@localhost:5432/exam_ai

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=exam_documents

UPLOAD_DIR=../storage/uploads
PROCESSED_DIR=../storage/processed

MAX_UPLOAD_SIZE_MB=100

FRONTEND_URL=http://localhost:3000

AI_TEMPERATURE=0.3
AI_TIMEOUT=180
AI_MAX_OUTPUT_TOKENS=4096

CHUNK_SIZE=700
CHUNK_OVERLAP=100

Tutti i parametri devono essere modificabili senza modificare il codice.

Il file .env non deve essere versionato.

29. DOCKER E INFRASTRUTTURA 29.1 Servizi iniziali

Docker Compose deve gestire:

PostgreSQL.
Qdrant.

Ollama rimane sul sistema host.

Backend e frontend vengono avviati direttamente durante lo sviluppo.

29.2 Persistenza

Utilizzare volumi Docker per:

PostgreSQL.
Qdrant.
29.3 Ottimizzazione RAM

Con 16 GB di RAM:

Evitare container inutili.
Limitare i processi concorrenti di elaborazione PDF.
Evitare più inferenze contemporanee.
Evitare di caricare più modelli generativi sulla GPU.
Configurare limiti di memoria quando necessario.

L'uso della GPU da parte di Ollama deve essere verificato attraverso test reali.

30. PERFORMANCE E OTTIMIZZAZIONE HARDWARE 30.1 GPU

La RTX 3090 dispone di 24 GB di VRAM.

Il sistema deve sfruttare la GPU per l'inferenza, se correttamente supportata dai driver e da Ollama.

30.2 RAM

I 16 GB di RAM rendono importante la gestione delle risorse.

Strategie:

Elaborazione PDF in batch.
Limiti ai worker.
Chunking progressivo.
Evitare caricamenti completi non necessari.
Paginazione delle query database.
30.3 Generazione

La generazione di domande deve essere effettuata in batch controllati.

Non generare centinaia di domande in un'unica richiesta.

30.4 Cache

Possibile introdurre cache per:

Modelli.
Embeddings.
Recuperi ripetuti.
Statistiche.
Risultati di elaborazioni.

La cache non deve sostituire la persistenza.

31. TESTING E VALIDAZIONE 31.1 Unit Test

Testare:

PDF parser.
Markdown parser.
Chunker.
Question validator.
Answer evaluator.
Progress tracker.
Spaced repetition.
31.2 Integration Test

Testare:

PostgreSQL.
Qdrant.
Ollama.
API.
Upload documenti.
Generazione domande.
31.3 End-to-End Test

Simulare un intero percorso:

Upload PDF.
Elaborazione.
Import Markdown.
Indicizzazione.
Creazione esame.
Svolgimento.
Correzione.
Salvataggio tentativi.
Aggiornamento analytics.
Creazione ripasso.
31.4 Test AI

Valutare:

Pertinenza.
Correttezza.
Qualità distrattori.
Coerenza spiegazioni.
Rispetto delle fonti.
Duplicati.

Creare un dataset di test con domande e risposte note.

32. ROADMAP DI SVILUPPO

Lo sviluppo sarà suddiviso in milestone.

MILESTONE 1 – INFRASTRUCTURE & BOOTSTRAP

Obiettivo: applicazione avviabile.

Attività:

Creazione repository.
Configurazione Windows.
Installazione dipendenze.
Configurazione Docker.
PostgreSQL.
Qdrant.
Backend FastAPI.
Client Ollama.
Verifica Qwen3.
Frontend Next.js.
Dashboard.
Monitoraggio servizi.

Criterio di completamento:

Dashboard raggiungibile e connessione a Qwen3 verificata.

MILESTONE 2 – DATABASE E DOCUMENT MANAGER

Obiettivo: importare e gestire i materiali.

Attività:

SQLAlchemy.
Alembic.
Modelli database.
Repository.
Upload PDF.
Upload Markdown.
Hash documenti.
Gestione duplicati.
Elenco documenti.
Stato elaborazione.
Eliminazione documenti.

Criterio di completamento:

Possibilità di importare e conservare documenti in modo persistente.

MILESTONE 3 – DOCUMENT INTELLIGENCE

Obiettivo: comprendere i documenti.

Attività:

Estrazione testo.
OCR.
Analisi struttura.
Identificazione capitoli.
Identificazione sottocapitoli.
Identificazione argomenti.
Chunking.
Riferimenti pagina.
Embeddings.
Indicizzazione Qdrant.
Gestione errori.

Criterio di completamento:

PDF consultabili semanticamente per capitolo e argomento.

MILESTONE 4 – OFFICIAL QUESTIONS IMPORTER

Obiettivo: importare le domande ufficiali.

Attività:

Parser Markdown.
Riconoscimento domande.
Estrazione alternative.
Estrazione risposte.
Validazione.
Gestione domande incomplete.
Deduplicazione.
Collegamento capitoli.
Collegamento argomenti.
Visualizzazione domande.

Criterio di completamento:

Domande ufficiali archiviate e disponibili per i quiz.

MILESTONE 5 – QUESTION GENERATION ENGINE

Obiettivo: generare domande affidabili.

Attività:

Prompt engineering.
JSON Schema.
RAG.
Generazione per capitolo.
Generazione per argomento.
Difficoltà.
Distrattori.
Validazione.
Controllo duplicati.
Riferimenti documentali.
Verifica AI.

Criterio di completamento:

Generazione di domande a risposta multipla basate sui PDF e validate dal backend.

MILESTONE 6 – EXAM ENGINE

Obiettivo: permettere lo svolgimento dei quiz.

Attività:

Configurazione esame.
Selezione domande.
Distribuzione fonti.
Timer.
Interfaccia quiz.
Navigazione.
Salvataggio risposte.
Correzione.
Risultati.
Storico sessioni.

Criterio di completamento:

Simulazione completa e persistente.

MILESTONE 7 – LEARNING ENGINE

Obiettivo: analizzare l'apprendimento.

Attività:

Registrazione errori.
Analisi argomenti deboli.
Analisi errori ricorrenti.
Progressi giornalieri.
Statistiche capitoli.
Statistiche fonti.
Spaced repetition.
Ripasso intelligente.

Criterio di completamento:

Il sistema riconosce le lacune e programma attività mirate.

MILESTONE 8 – ANALYTICS E UX AVANZATA

Obiettivo: completare l'esperienza utente.

Attività:

Dashboard definitiva.
Grafici.
Storico.
Filtri.
Confronto temporale.
Performance per argomento.
Performance per fonte.
Sistema di notifiche.
Configurazioni personalizzate.

Criterio di completamento:

Dashboard completa e statistiche attendibili.

MILESTONE 9 – HARDENING E STABILITÀ

Obiettivo: rendere il sistema affidabile.

Attività:

Test completi.
Gestione errori.
Backup.
Restore.
Ottimizzazione memoria.
Ottimizzazione GPU.
Logging.
Documentazione.
Verifica privacy.

Criterio di completamento:

Applicazione stabile, ripristinabile e utilizzabile quotidianamente.

33. REQUISITI FUNZIONALI ID Requisito Priorità FR-001 Upload PDF Alta FR-002 Upload Markdown Alta FR-003 Estrazione testo PDF Alta FR-004 OCR Media FR-005 Identificazione capitoli Alta FR-006 Identificazione argomenti Alta FR-007 Import domande ufficiali Alta FR-008 RAG Alta FR-009 Generazione AI Alta FR-010 Modalità mista Alta FR-011 Quiz personalizzati Alta FR-012 Simulazione esame Alta FR-013 Correzione automatica Alta FR-014 Registrazione tentativi Alta FR-015 Analytics giornaliere Alta FR-016 Analisi errori Alta FR-017 Ripasso adattivo Alta FR-018 Dashboard Alta FR-019 Backup Alta FR-020 Monitoraggio AI Media
34. REQUISITI NON FUNZIONALI Performance L'interfaccia deve rimanere reattiva durante l'elaborazione documentale. I task lunghi devono essere asincroni. Le query devono essere paginabili. La generazione deve essere controllata. Affidabilità I dati devono essere persistenti. I job devono essere tracciati. Gli errori devono essere recuperabili. I tentativi devono essere immutabili. Manutenibilità Moduli indipendenti. Tipizzazione. Configurazione centralizzata. Test automatici. Migrazioni database. Documentazione. Privacy Elaborazione locale. Nessuna API AI esterna obbligatoria. Documenti conservati localmente. Log controllati. Scalabilità

L'architettura deve consentire in futuro:

Più utenti.
Più esami.
Più raccolte documentali.
Modelli AI differenti.
Modelli embedding differenti.
35\. CRITERI DI COMPLETAMENTO DEL PROGETTO

Exam AI sarà considerato completo quando sarà possibile effettuare il seguente percorso senza interventi manuali sul database:

Aprire l'applicazione.
Verificare lo stato di Ollama.
Caricare un PDF.
Attendere l'elaborazione.
Visualizzare capitoli e argomenti.
Importare un file Markdown.
Visualizzare le domande ufficiali.
Generare nuove domande AI.
Visualizzare i riferimenti alle fonti.
Creare una simulazione.
Svolgere il quiz.
Ricevere la correzione.
Visualizzare il risultato.
Consultare gli errori.
Visualizzare i progressi giornalieri.
Ricevere un piano di ripasso.
Tornare dopo alcuni giorni e continuare dallo storico precedente.

Tutte le informazioni devono essere persistenti.

Un riavvio dell'applicazione non deve comportare perdita di dati.

36. REGOLE ARCHITETTURALI DA RISPETTARE

Queste regole sono vincolanti per tutto lo sviluppo.

Non inserire tutta la logica nel file main.py.
Non chiamare Ollama direttamente dal frontend.
Non utilizzare Qwen per calcoli deterministici.
Non esporre le risposte corrette durante il quiz.
Non mescolare domande ufficiali e AI senza identificarne la provenienza.
Non generare domande senza riferimenti al materiale quando la modalità richiede grounding.
Non sovrascrivere lo storico delle risposte.
Non utilizzare dati fittizi nella dashboard definitiva.
Non salvare documenti soltanto in memoria temporanea.
Non duplicare i documenti senza controllo hash.
Non affidare a Qwen la struttura definitiva del database.
Non perdere i riferimenti alle pagine originali.
Non eseguire elaborazioni pesanti direttamente nelle richieste HTTP.
Non rendere dipendente l'applicazione da un singolo modello AI.
Non modificare domande ufficiali senza tracciarne le revisioni.
Non dichiarare verificata una domanda AI senza controlli effettivi.
Non esporre i servizi database a reti non necessarie.
Non introdurre nuove dipendenze senza una motivazione tecnica.
Ogni nuova funzionalità deve avere test adeguati.
Ogni milestone deve terminare con una verifica funzionante.
37\. VISIONE FUTURA DEL PROGETTO

Una volta completata la versione iniziale, Exam AI potrà evolversi.

37.1 AI Personal Tutor

Un assistente capace di rispondere a domande sul materiale didattico.

Esempio:

"Non ho capito la differenza tra questi due concetti."

Il sistema recupera i paragrafi pertinenti e costruisce una spiegazione.

37.2 Smart Exam Simulation

Simulazioni che riproducono la distribuzione delle domande ufficiali.

37.3 Adaptive Question Selection

Il sistema sceglie automaticamente le domande in funzione delle prestazioni.

37.4 Knowledge Gap Detection

Identificazione automatica dei concetti non sufficientemente compresi.

37.5 Exam Readiness Score

Indicatore di preparazione basato su:

Accuratezza.
Numero di domande svolte.
Prestazioni sulle domande ufficiali.
Stabilità dei risultati.
Copertura del programma.
Risultati recenti.
Ripassi completati.

Non deve essere una semplice media aritmetica.

Deve considerare anche la quantità e l'affidabilità dei dati.

37.6 Multiple Exam Profiles

Possibilità di gestire esami differenti, ciascuno con:

Documenti.
Domande ufficiali.
Argomenti.
Simulazioni.
Progressi indipendenti.
37.7 Export e report

Possibilità di esportare:

Risultati.
Errori.
Statistiche.
Domande.
Report PDF.
CONCLUSIONE

Exam AI deve diventare un sistema personale di apprendimento adattivo, non un semplice generatore di quiz.

L'architettura scelta consente di mantenere separate le responsabilità, utilizzare l'intelligenza artificiale localmente e costruire progressivamente tutte le funzionalità senza dover riscrivere il progetto.

La priorità è sviluppare una base solida:

Infrastructure.
Database.
Document Intelligence.
Official Questions Importer.
RAG.
Question Generation.
Exam Engine.
Learning Analytics.

Regola fondamentale dello sviluppo: ogni componente deve essere realmente funzionante, testabile e collegato agli altri componenti. Nessuna funzionalità deve essere considerata completata soltanto perché esiste la relativa interfaccia grafica.

Documento: EXAM AI – Master Project Specification
Versione: 1.0
Stato: Architettura iniziale approvata come base di sviluppo
Stack: Next.js + FastAPI + PostgreSQL + Qdrant + Ollama + Qwen3
Ambiente: Windows + NVIDIA RTX 3090
Modalità: Local-first