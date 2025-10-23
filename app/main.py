import logging

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, DocumentEmbedding
from app.embeddings.embed import load_and_chunk, get_embeddings
from sqlalchemy.orm import Session


LOGGER = logging.info(__name__)

app = FastAPI(title="Rag Architecture Assesment", version="1.0")

DATABASE_URL = "postgresql+psycopg2://admin:admin123@postgresdb/rag_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

from app.web import api

DOCS = ["docs/doc1.txt"]

@app.on_event("startup")
def startup_event():
    """
    Runs when app starts: create table and insert docs with embeddings.
    """
    # 1. Create table
    Base.metadata.create_all(bind=engine)

    # 2. Load and chunk documents
    all_chunks = []
    for path in DOCS:
        all_chunks.extend(load_and_chunk(path))

    # 3. Generate embeddings
    vectors, _ = get_embeddings(all_chunks)

    # 4. Insert into database (skip if already exists)
    session: Session = SessionLocal()
    if session.query(DocumentEmbedding).count() == 0:
        for i, chunk in enumerate(all_chunks):
            doc = DocumentEmbedding(content=chunk.page_content, source=f"doc{i+1}", embedding=vectors[i])
            session.add(doc)
        session.commit()
        LOGGER.info("Documents inserted into pgvector table.")
    else:
        LOGGER.info("Documents already exist in database.")
    session.close()
