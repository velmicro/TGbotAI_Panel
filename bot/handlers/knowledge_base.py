from aiogram import Router, types
from bot.ai_integration import generate_response
from bot.config import load_settings
import logging

router = Router()

@router.message()
async def handle_knowledge_base(message: types.Message):
    settings = load_settings()
    
    # Проверка подписки, если требуется
    if settings.get("check_subscription", False):
        group_id = settings.get("subscription_group_id") or settings.get("subscription_group")
        if group_id:
            try:
                member = await message.bot.get_chat_member(group_id, message.from_user.id)
                if member.status in ["left", "kicked"]:
                    await message.answer(settings.get("subscription_message", "Пожалуйста, подпишитесь на группу!"))
                    return
            except Exception as e:
                logging.error(f"Ошибка проверки подписки: {str(e)}")
        
    # Показ сообщения "Панда пишет..."
    if settings.get("show_typing_message", False):
        await message.answer(settings.get("typing_message_text", "Панда пишет..."))
    
    # Генерация ответа
    response = await generate_response(message.text, settings)
    await message.answer(response)
    logging.info(f"Обработан запрос базы знаний от пользователя {message.from_user.id}: {message.text}")