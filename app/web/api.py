from app.main import app
from embeddings.embed import get_embeddings
from embeddings.retrival import answer_query
from .utils import translate_to_en

@app.get("/query")
def query(q: str):
    _, embeddings_model = get_embeddings([])
    query_en = translate_to_en(q)
    answer = answer_query(query_en, embeddings_model)
    return {"answer": answer}
