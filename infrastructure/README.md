# Infrastructure

`docker compose -f infrastructure/docker-compose.yml up --build` avvia:

- PostgreSQL su `127.0.0.1:5432`;
- Qdrant su `127.0.0.1:6333`;
- API FastAPI su `127.0.0.1:8000`;
- frontend Next.js su `127.0.0.1:3000`.

I dati persistono nei volumi Docker `exam-ai_postgres_data`,
`exam-ai_qdrant_data` e `exam-ai_app_data`. Ollama resta sul sistema host;
su Linux il backend usa `host.docker.internal` tramite la configurazione
predefinita del compose.

Per arrestare i servizi senza cancellare i dati:

```bash
docker compose -f infrastructure/docker-compose.yml down
```

Per cancellare anche i dati persistenti:

```bash
docker compose -f infrastructure/docker-compose.yml down -v
```
