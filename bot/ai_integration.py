from groq import Groq
from bot.config import GROQ_API_KEY
import logging
import json
import os
from bot.config import KNOWLEDGE_BASE_DIR

client = Groq(api_key=GROQ_API_KEY)

async def generate_response(message: str, settings: dict) -> str:
    try:
        # Загрузка активных баз знаний
        knowledge_bases = settings.get("knowledge_bases", ["default"])
        knowledge_data = []
        for base in knowledge_bases:
            file_path = os.path.join(KNOWLEDGE_BASE_DIR, f"{base}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    knowledge_data.extend(json.load(f))
        
        # Поиск релевантных записей
        relevant_entries = []
        for entry in knowledge_data:
            if entry["question"].lower() in message.lower() or any(kw.lower() in message.lower() for kw in entry["keywords"].split(",")):
                relevant_entries.append(entry)
        
        # Формирование промпта
        prompt = f"""
        Вы - {settings.get('name', 'TG BotAI')}, {settings.get('role', 'ассистент')}.
        Ваша цель: {settings.get('goal', 'помогать пользователям')}.
        Ограничения: {', '.join(settings.get('restrictions', []))}.
        Используйте язык: {settings.get('language', 'ru')}.
        
        Пользователь написал: {message}
        
        Используйте следующую информацию из базы знаний, если она релевантна:
        {json.dumps(relevant_entries, ensure_ascii=False, indent=2)}
        
        Ответьте максимально полезно и естественно.
        """
        
        # Запрос к Groq
        completion = client.chat.completions.create(
            model=settings.get("ai_model", "llama3-8b-8192"),
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=1024
        )
        
        response = completion.choices[0].message.content
        logging.info(f"Сгенерирован ответ для сообщения: {message}")
        return response
    except Exception as e:
        logging.error(f"Ошибка генерации ответа: {str(e)}")
        return "Извините, произошла ошибка. Попробуйте позже."