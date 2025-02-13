# app/chat.py

from app.llm import generate_response
from app.memory import add_to_memory

def process_user_message(message: str) -> str:
    """
    Обробляє повідомлення користувача та повертає згенеровану відповідь.
    
    :param message: Повідомлення користувача.
    :return: Відповідь, згенерована LLM або, за потребою, власна логіка.
    """
    # Якщо повідомлення містить ключові слова про улюблені інгредієнти/коктейлі,
    # збережемо їх у пам'ять (можна доповнити більш розумною логікою)
    if "улюблені" in message.lower() or "favorite" in message.lower():
        add_to_memory(message)
        # Повертаємо просте підтвердження, або можна викликати LLM для додаткової обробки
        return "Я зберіг ваші улюблені інгредієнти для майбутніх рекомендацій."
    
    # Якщо повідомлення не містить специфічних ключових слів, генеруємо відповідь через LLM
    response = generate_response(message)
    return response
