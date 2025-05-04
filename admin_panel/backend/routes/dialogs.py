from fastapi import APIRouter, HTTPException
import json
import os
import logging
from admin_panel.backend.models.dialogs import DialogEntry
from bot.config import DIALOGS_FILE

router = APIRouter(prefix="/dialogs", tags=["Dialogs"])

# Получение всех диалогов
@router.get("/")
async def get_dialogs():
    try:
        if not os.path.exists(DIALOGS_FILE):
            return {"dialogs": []}
        with open(DIALOGS_FILE, "r", encoding="utf-8") as f:
            dialogs = json.load(f)
        logging.info("Загружены диалоги")
        return {"dialogs": dialogs}
    except Exception as e:
        logging.error(f"Ошибка при загрузке диалогов: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

# Добавление диалога
@router.post("/add")
async def add_dialog(entry: DialogEntry):
    try:
        dialogs = []
        if os.path.exists(DIALOGS_FILE):
            with open(DIALOGS_FILE, "r", encoding="utf-8") as f:
                dialogs = json.load(f)
        
        new_entry = entry.dict()
        new_entry["id"] = max([d.get("id", 0) for d in dialogs], default=0) + 1
        dialogs.append(new_entry)
        
        with open(DIALOGS_FILE, "w", encoding="utf-8") as f:
            json.dump(dialogs, f, indent=4, ensure_ascii=False)
        
        logging.info(f"Добавлен диалог: {new_entry['question']}")
        return {"message": "Диалог добавлен", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при добавлении диалога: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Обновление диалога
@router.put("/{dialog_id}")
async def update_dialog(dialog_id: int, entry: DialogEntry):
    try:
        if not os.path.exists(DIALOGS_FILE):
            raise HTTPException(status_code=404, detail="Диалоги не найдены")
        
        with open(DIALOGS_FILE, "r", encoding="utf-8") as f:
            dialogs = json.load(f)
        
        for i, d in enumerate(dialogs):
            if d["id"] == dialog_id:
                dialogs[i] = {"id": dialog_id, **entry.dict()}
                break
        else:
            raise HTTPException(status_code=404, detail="Диалог не найден")
        
        with open(DIALOGS_FILE, "w", encoding="utf-8") as f:
            json.dump(dialogs, f, indent=4, ensure_ascii=False)
        
        logging.info(f"Обновлён диалог {dialog_id}")
        return {"message": "Диалог обновлён", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при обновлении диалога {dialog_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

# Удаление диалога
@router.delete("/{dialog_id}")
async def delete_dialog(dialog_id: int):
    try:
        if not os.path.exists(DIALOGS_FILE):
            raise HTTPException(status_code=404, detail="Диалоги не найдены")
        
        with open(DIALOGS_FILE, "r", encoding="utf-8") as f:
            dialogs = json.load(f)
        
        dialogs = [d for d in dialogs if d["id"] != dialog_id]
        
        with open(DIALOGS_FILE, "w", encoding="utf-8") as f:
            json.dump(dialogs, f, indent=4, ensure_ascii=False)
        
        logging.info(f"Удалён диалог {dialog_id}")
        return {"message": "Диалог удалён", "status": "success"}
    except Exception as e:
        logging.error(f"Ошибка при удалении диалога {dialog_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")