# app/utils.py

import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_request(message: str):
    """
    Логує повідомлення запиту користувача.
    """
    logging.info(f"Запит користувача: {message}")

def load_config(config_file: str):
    """
    Завантажує конфігурацію з файлу.
    (Поточна реалізація – заглушка, яку можна розширити за потреби)
    """
    logging.info(f"Завантаження конфігурації з файлу: {config_file}")
    # Тут можна реалізувати завантаження конфігурації за допомогою configparser або json
    return {}


