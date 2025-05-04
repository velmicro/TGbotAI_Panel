from aiogram import Router, types
from aiogram.filters import Command
from bot.config import load_settings
import logging

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    settings = load_settings()
    welcome_message = f"Привет! Я {settings.get('name', 'TG BotAI')}, твой {settings.get('role', 'ассистент')}. Чем могу помочь?"
    await message.answer(welcome_message)
    logging.info(f"Команда /start выполнена для пользователя {message.from_user.id}")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_message = "Я могу ответить на ваши вопросы или выполнить команды:\n/start - Начать\n/help - Показать помощь"
    await message.answer(help_message)
    logging.info(f"Команда /help выполнена для пользователя {message.from_user.id}")