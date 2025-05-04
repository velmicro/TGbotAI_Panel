from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from bot.config import SETTINGS_FILE, load_settings
from groq import Groq
from bot.config import GROQ_API_KEY
import logging
import asyncio
from bot.main import start_bot, stop_bot, reload_bot
from bot.utils.logging_config import setup_logging
from admin_panel.backend.models.bot_settings import BotSettings

# Настройка логирования
setup_logging()

router = APIRouter()

# Путь к файлу логов
LOG_FILE = "admin_panel/logs/app.log"

# Получение списка моделей Groq
@router.get("/models")
async def get_models():
    try:
        client = Groq(api_key=GROQ_API_KEY)
        models = [
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768"
        ]
        logging.info("Получен список моделей")
        return {"models": models}
    except Exception as e:
        logging.error(f"Ошибка при получении моделей: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

# Получение текущих настроек
@router.get("/settings")
async def get_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        if 'group_type' not in settings:
            settings['group_type'] = "open" if settings.get('subscription_group') else "closed" if settings.get('subscription_group_id') else None
        if 'show_typing_message' not in settings:
            settings['show_typing_message'] = False
        if 'typing_message_text' not in settings:
            settings['typing_message_text'] = "Панда пишет..."
        if 'knowledge_bases' not in settings:
            settings['knowledge_bases'] = ["default"]
        logging.info("Настройки загружены")
        return settings
    except Exception as e:
        logging.error(f"Ошибка при загрузке настроек: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

# Обновление настроек
@router.post("/settings")
async def update_settings(settings: BotSettings):
    try:
        valid_models = [
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768"
        ]
        if settings.ai_model not in valid_models:
            logging.error(f"Недопустимая модель AI: {settings.ai_model}")
            raise HTTPException(status_code=400, detail="Выберите действительную модель AI")
        
        current_settings = load_settings()
        updated_settings = settings.dict(exclude_unset=True)
        for key, value in updated_settings.items():
            current_settings[key] = value
        
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(current_settings, f, indent=4, ensure_ascii=False)
        logging.info("Настройки обновлены")
        return {"message": "Настройки успешно обновлены", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при обновлении настроек: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Перезагрузка настроек бота
@router.post("/reload")
async def reload_settings():
    try:
        logging.info("Инициируется перезагрузка настроек бота")
        await reload_bot()
        logging.info("Настройки бота успешно перезагружены")
        return {"message": "Настройки бота успешно обновлены", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при перезагрузке настроек: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при перезагрузке настроек: {str(e)}")

# Запуск бота
@router.post("/start")
async def start_bot_endpoint():
    try:
        logging.info("Инициируется запуск бота")
        await start_bot()
        logging.info("Бот успешно запущен")
        return {"message": "Бот успешно запущен", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при запуске бота: {str(e)}")

# Остановка бота
@router.post("/stop")
async def stop_bot_endpoint():
    try:
        logging.info("Инициируется остановка бота")
        await stop_bot()
        logging.info("Бот успешно остановлен")
        return {"message": "Бот успешно остановлен", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при остановке бота: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при остановке бота: {str(e)}")

# Получение логов
@router.get("/logs")
async def get_logs():
    try:
        if not os.path.exists(LOG_FILE):
            return {"logs": ""}
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.read()
        logging.info("Логи загружены для админ-панели")
        return {"logs": logs}
    except Exception as e:
        logging.error(f"Ошибка при чтении логов: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

# Очистка логов
@router.post("/clear-logs")
async def clear_logs():
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")
        logging.info("Логи очищены через админ-панель")
        return {"message": "Логи успешно очищены", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при очистке логов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")