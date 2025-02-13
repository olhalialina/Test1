# app/llm.py

from transformers import pipeline, set_seed

# Опціонально: встановлюємо seed для відтворюваності
set_seed(42)

# Створюємо pipeline для генерації тексту, використовуючи модель GPT-2
generator = pipeline("text-generation", model="gpt2", tokenizer="gpt2")

def generate_response(message: str) -> str:
    """
    Генерує відповідь на запит користувача за допомогою LLM.

    Аргументи:
        message (str): Вхідне повідомлення користувача.

    Повертає:
        str: Згенерована відповідь, що стосується коктейлів.
    """
    # Формуємо промпт для моделі
    prompt = f"User: {message}\nCocktail Advisor:"
    
    # Генеруємо текст із заданим промптом
    generated_output = generator(prompt, max_length=150, num_return_sequences=1)
    
    # Отримуємо згенерований текст
    generated_text = generated_output[0]['generated_text']
    
    # Видаляємо частину промпту, щоб залишити лише відповідь
    response = generated_text[len(prompt):].strip()
    
    return response
