from fastapi import APIRouter, HTTPException
import json
import os
import logging
from bot.utils.google_sheets import sync_knowledge_base
from admin_panel.backend.models.knowledge_base import KnowledgeEntry
from bot.config import KNOWLEDGE_BASE_DIR

router = APIRouter(prefix="/knowledge_base", tags=["Knowledge Base"])

# Получение списка баз знаний
@router.get("/bases")
async def get_knowledge_bases():
    try:
        bases = [f.split(".json")[0] for f in os.listdir(KNOWLEDGE_BASE_DIR) if f.endswith(".json")]
        logging.info("Получен список баз знаний")
        return {"bases": bases}
    except Exception as e:
        logging.error(f"Ошибка при получении баз знаний: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

# Получение записей из базы знаний
@router.get("/{base_name}")
async def get_knowledge_base(base_name: str):
    try:
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, f"{base_name}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="База знаний не найдена")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logging.info(f"Загружена база знаний: {base_name}")
        return {"entries": data}
    except Exception as e:
        logging.error(f"Ошибка при загрузке базы знаний {base_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

# Добавление записи в базу знаний
@router.post("/{base_name}/add")
async def add_knowledge_entry(base_name: str, entry: KnowledgeEntry):
    try:
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, f"{base_name}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="База знаний не найдена")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        new_entry = entry.dict()
        new_entry["id"] = max([e.get("id", 0) for e in data], default=0) + 1
        data.append(new_entry)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Синхронизация с Google Sheets
        await sync_knowledge_base(base_name)
        
        logging.info(f"Добавлена запись в базу знаний {base_name}")
        return {"message": "Запись добавлена", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при добавлении записи в {base_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Обновление записи
@router.put("/{base_name}/{entry_id}")
async def update_knowledge_entry(base_name: str, entry_id: int, entry: KnowledgeEntry):
    try:
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, f"{base_name}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="База знаний не найдена")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for i, e in enumerate(data):
            if e["id"] == entry_id:
                data[i] = {"id": entry_id, **entry.dict()}
                break
        else:
            raise HTTPException(status_code=404, detail="Запись не найдена")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Синхронизация с Google Sheets
        await sync_knowledge_base(base_name)
        
        logging.info(f"Обновлена запись {entry_id} в базе знаний {base_name}")
        return {"message": "Запись обновлена", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при обновлении записи {entry_id} в {base_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Удаление записи
@router.delete("/{base_name}/{entry_id}")
async def delete_knowledge_entry(base_name: str, entry_id: int):
    try:
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, f"{base_name}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="База знаний не найдена")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data = [e for e in data if e["id"] != entry_id]
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Синхронизация с Google Sheets
        await sync_knowledge_base(base_name)
        
        logging.info(f"Удалена запись {entry_id} из базы знаний {base_name}")
        return {"message": "Запись удалена", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при удалении записи {entry_id} из {base_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Создание новой базы знаний
@router.post("/create")
async def create_knowledge_base(base_name: str):
    try:
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, f"{base_name}.json")
        if os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="База знаний уже существует")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
        
        # Создание таблицы в Google Sheets
        await sync_knowledge_base(base_name, create_new=True)
        
        logging.info(f"Создана новая база знаний: {base_name}")
        return {"message": "База знаний создана", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при создании базы знаний {base_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Удаление базы знаний
@router.delete("/{base_name}")
async def delete_knowledge_base(base_name: str):
    try:
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, f"{base_name}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="База знаний не найдена")
        
        os.remove(file_path)
        logging.info(f"Удалена база знаний: {base_name}")
        return {"message": "База знаний удалена", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при удалении базы знаний {base_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Обновление базы знаний из Google Sheets
@router.post("/{base_name}/sync")
async def sync_knowledge_base_endpoint(base_name: str):
    try:
        await sync_knowledge_base(base_name)
        logging.info(f"База знаний {base_name} синхронизирована с Google Sheets")
        return {"message": "База знаний синхронизирована", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при синхронизации базы знаний {base_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")