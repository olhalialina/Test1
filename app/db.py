# app/db.py

import os
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Шлях до CSV-файлу з даними про коктейлі
DATA_FILE = "data/finalcocktails.csv"
# Шлях до файлу з FAISS-індексом
INDEX_FILE = "cocktail_index.faiss"

def get_cocktails_df():
    """
    Завантаження датасету коктейлів із CSV-файлу.
    Додається колонка 'description' для генерації embeddings.
    Адаптується до різних назв колонок (наприклад, 'glass' або 'glassType').
    """
    try:
        df = pd.read_csv(DATA_FILE)
        
        # Визначаємо, які колонки потрібні та можливі альтернативи
        required_map = {
            'name': ['name'],
            'alcoholic': ['alcoholic'],
            'glass': ['glass', 'glassType'],  # дозволяємо 'glass' або 'glassType'
            'ingredients': ['ingredients'],
            'instructions': ['instructions']
        }
        
        # Перевіряємо, чи присутня хоча б одна з альтернатив для кожного ключа
        for key, alternatives in required_map.items():
            if not any(col in df.columns for col in alternatives):
                raise ValueError(f"CSV-файл повинен містити колонку для '{key}'. Знайдено: {set(df.columns)}")
            # Якщо основна назва key відсутня, але знайдена альтернатива, переіменовуємо її
            if key not in df.columns:
                for alt in alternatives:
                    if alt in df.columns:
                        df.rename(columns={alt: key}, inplace=True)
                        break

        # Формуємо опис для кожного коктейлю
        df["description"] = df.apply(
            lambda row: f"{row['name']} - це {row['alcoholic']} коктейль, який подається в {row['glass']}. "
                        f"Він містить {row['ingredients']}. {row['instructions']}",
            axis=1,
        )
        return df
    except Exception as e:
        print("Помилка при завантаженні CSV:", e)
        raise

def create_faiss_index(df, embedding_model):
    """
    Створення FAISS-індексу з використанням описів коктейлів.
    """
    descriptions = df["description"].tolist()
    # Генеруємо embeddings для кожного опису
    embeddings = embedding_model.encode(descriptions)
    
    # Отримуємо розмірність embeddings
    d = embeddings.shape[1]
    # Створюємо індекс, використовуючи L2 (євклідова відстань)
    index = faiss.IndexFlatL2(d)
    # Додаємо embeddings в індекс (переконуємося, що вони типу float32)
    index.add(np.array(embeddings).astype("float32"))
    
    # Зберігаємо індекс у файл
    faiss.write_index(index, INDEX_FILE)
    print(f"FAISS-індекс створено та збережено у {INDEX_FILE}")
    return index

def get_faiss_index():
    """
    Повертає FAISS-індекс. Якщо індекс не знайдено, створює його.
    """
    if os.path.exists(INDEX_FILE):
        try:
            index = faiss.read_index(INDEX_FILE)
            print(f"FAISS-індекс завантажено з файлу {INDEX_FILE}")
            return index
        except Exception as e:
            print("Помилка при завантаженні FAISS-індексу:", e)
            raise
    else:
        print("FAISS-індекс не знайдено. Створення нового індексу...")
        df = get_cocktails_df()
        # Завантаження моделі для генерації embeddings
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        index = create_faiss_index(df, embedding_model)
        return index
