from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import TELEGRAM_TOKEN
from bot.handlers.commands import router as commands_router
from bot.handlers.knowledge_base import router as knowledge_router
from bot.handlers.dialogs import router as dialogs_router
from bot.utils.logging_config import setup_logging
import asyncio
import logging

# Настройка логирования
setup_logging()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

def register_handlers():
    dp.include_router(dialogs_router)  # Диалоги имеют приоритет
    dp.include_router(knowledge_router)
    dp.include_router(commands_router)

async def start_bot():
    register_handlers()
    logging.info("Запуск бота...")
    await dp.start_polling(bot)

async def stop_bot():
    logging.info("Остановка бота...")
    await dp.stop_polling()

async def reload_bot():
    logging.info("Перезагрузка бота...")
    await stop_bot()
    dp.handlers.clear()
    await start_bot()