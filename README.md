# RAG App Docker Setup

This project runs a **Python FastAPI app** with a **PostgreSQL database** using Docker Compose. The setup also uses `pgvector` for vector storage.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Optional: Ensure `rag_network` Docker network exists (or let Docker Compose create it).

```bash
docker network create --driver bridge rag_network || true

docker compose -f docker-compose.yml --profile basic-setup up -d --force-recreate
