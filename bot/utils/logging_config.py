import logging
import os
from logging.handlers import RotatingFileHandler
from bot.config import LOG_FILE

def setup_logging():
    # Создание директории для логов, если она не существует
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Настройка логгера
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Формат логов
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Файловый обработчик с ротацией
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Добавление обработчиков
    logger.handlers = []  # Очистка существующих обработчиков
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)