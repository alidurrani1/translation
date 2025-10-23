from app.models import Base
from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    source = Column(Text, nullable=False)
    embedding = Column(Vector(384))  # 384 is the dimension for MiniLM embeddings
