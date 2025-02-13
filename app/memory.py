# app/memory.py

import threading

# Глобальна змінна для збереження пам'яті користувача (наприклад, улюблені інгредієнти чи коктейлі)
_memory_lock = threading.Lock()
_memory_store = []  # У цьому прикладі зберігаємо повідомлення у вигляді списку рядків

def add_to_memory(message: str):
    """
    Додає повідомлення з улюбленими інгредієнтами/коктейлями до пам'яті.
    
    :param message: Повідомлення користувача, яке містить інформацію про улюблені інгредієнти.
    """
    with _memory_lock:
        _memory_store.append(message)
        print(f"[Memory] Додано повідомлення: {message}")

def get_memory():
    """
    Повертає копію збереженої пам'яті користувача.
    
    :return: Список збережених повідомлень.
    """
    with _memory_lock:
        return list(_memory_store)
