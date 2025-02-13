# app/main.py

from fastapi import FastAPI, Query, HTTPException
from app.db import get_faiss_index, get_cocktails_df
from app.chat import process_user_message
from app.llm import generate_response
from app.memory import add_to_memory, get_memory
from app.utils import log_request

app = FastAPI(
    title="Cocktail Advisor Chat",
    description="Retrieval-Augmented Generation (RAG) system for cocktail queries",
    version="1.0"
)

# Ініціалізація FAISS-індексу та завантаження даних коктейлів
index = get_faiss_index()       # має повертати FAISS-індекс
df = get_cocktails_df()           # має повертати DataFrame з даними про коктейлі

@app.get("/")
def root():
    return {"message": "Welcome to the Cocktail Advisor Chat!"}

@app.get("/search")
def search_cocktails(
    query: str = Query(..., description="Enter your cocktail query (e.g. lemon, non-alcoholic, etc.)"),
    k: int = 5
):
    """
    Пошук коктейлів з використанням FAISS-векторної бази даних.
    """
    try:
        # Завантаження моделі для генерації embedding'ів
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = embedding_model.encode([query])
        import numpy as np
        distances, indices = index.search(np.array(query_embedding), k)
        # Отримання назв коктейлів з DataFrame
        results = df.iloc[indices[0]]["name"].tolist()
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_endpoint(message: str):
    """
    Обробка повідомлення користувача та генерація відповіді з використанням LLM.
    """
    # Логування запиту (наприклад, для дебагу)
    log_request(message)
    # Обробка повідомлення (розбір запиту, збереження пам’яті, виклик LLM тощо)
    response = process_user_message(message)
    # Приклад: якщо повідомлення містить ключове слово "улюблені", додати до пам'яті
    if "улюблені" in message.lower():
        add_to_memory(message)
    # Можна також генерувати відповідь за допомогою LLM
    generated = generate_response(message)
    return {"message": message, "response": generated}

@app.get("/memory")
def get_user_favorites():
    """
    Отримання збереженої пам’яті користувача (улюблені інгредієнти/коктейлі).
    """
    memory_data = get_memory()
    return {"memory": memory_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
