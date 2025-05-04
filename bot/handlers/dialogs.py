from aiogram import Router, types
import json
import os
from bot.config import DIALOGS_FILE
import logging

router = Router()

@router.message()
async def handle_dialogs(message: types.Message):
    try:
        if not os.path.exists(DIALOGS_FILE):
            return
        
        with open(DIALOGS_FILE, "r", encoding="utf-8") as f:
            dialogs = json.load(f)
        
        # Поиск точного совпадения вопроса
        for dialog in dialogs:
            if dialog["question"].lower().strip() == message.text.lower().strip():
                await message.answer(dialog["answer"])
                logging.info(f"Найден диалог для вопроса: {message.text}")
                return
    except Exception as e:
        logging.error(f"Ошибка обработки диалогов: {str(e)}")