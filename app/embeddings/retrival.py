from sqlalchemy import select
from app.main import SessionLocal
from app.models import DocumentEmbedding
from langchain.chat_models import ChatOpenAI

from langchain.schema import Document as LC_Document

def retrieve_similar(query, embeddings_model, top_k=3):
    query_vector = embeddings_model.embed(query)
    session = SessionLocal()
    # similarity search
    stmt = select(DocumentEmbedding).order_by(DocumentEmbedding.embedding.l2_distance(query_vector)).limit(top_k)
    results = session.execute(stmt).scalars().all()
    session.close()
    return [LC_Document(page_content=r.content, metadata={"source": r.source}) for r in results]

def answer_query(query, embeddings_model):
    llm = ChatOpenAI(temperature=0)
    docs = retrieve_similar(query, embeddings_model)
    context = "\n".join([f"[{d.metadata['source']}]: {d.page_content}" for d in docs])
    prompt = f"Answer the question using the context below:\n{context}\nQuestion: {query}"
    return llm(prompt)
