import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# Переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8000))
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Проверка обязательных переменных
required_env_vars = {
    "TELEGRAM_TOKEN": TELEGRAM_TOKEN,
    "GROQ_API_KEY": GROQ_API_KEY,
    "GOOGLE_SHEETS_CREDENTIALS": GOOGLE_SHEETS_CREDENTIALS,
    "GOOGLE_SHEET_ID": GOOGLE_SHEET_ID
}
for var_name, var_value in required_env_vars.items():
    if not var_value:
        raise ValueError(f"{var_name} не найден в .env файле. Укажите его, например: {var_name}=your-value")

# Пути к файлам и папкам
SETTINGS_FILE = Path("bot/data/settings.json")
KNOWLEDGE_BASE_DIR = Path("bot/data/knowledge_base")
DIALOGS_FILE = Path("bot/data/dialogs.json")

def load_settings():
    """
    Загружает настройки бота из JSON-файла.
    
    Returns:
        dict: Словарь с настройками бота. Если файл не существует или повреждён,
              возвращает настройки по умолчанию.
    """
    default_settings = {
        "ai_model": "llama3-8b-8192",
        "name": "TG BotAI",
        "role": "ассистент",
        "goal": "помогать пользователям",
        "tasks": [],
        "restrictions": [],
        "group_trigger_name": null,
        "check_subscription": False,
        "group_type": null,
        "subscription_group": null,
        "subscription_group_id": null,
        "subscription_message": null,
        "language": "ru",
        "show_typing_message": False,
        "typing_message_text": "Панда пишет...",
        "knowledge_bases": ["default"]
    }

    try:
        if not SETTINGS_FILE.exists():
            # Создаём файл с настройками по умолчанию, если он не существует
            SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, ensure_ascii=False, indent=4)
            return default_settings

        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        return settings
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка загрузки настроек: {e}. Используются настройки по умолчанию.")
        return default_settings

def save_settings(settings):
    """
    Сохраняет настройки бота в JSON-файл.
    
    Args:
        settings (dict): Словарь с настройками бота.
    """
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка сохранения настроек: {e}")