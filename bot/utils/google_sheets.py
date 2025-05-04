import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import logging
from bot.config import GOOGLE_SHEETS_CREDENTIALS, GOOGLE_SHEET_ID, KNOWLEDGE_BASE_DIR

async def sync_knowledge_base(base_name: str, create_new: bool = False):
    try:
        # Настройка доступа к Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS, scope)
        client = gspread.authorize(creds)
        
        # Открытие или создание таблицы
        spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)
        try:
            worksheet = spreadsheet.worksheet(base_name)
        except gspread.exceptions.WorksheetNotFound:
            if create_new:
                worksheet = spreadsheet.add_worksheet(title=base_name, rows=100, cols=4)
                worksheet.append_row(["ID", "Question", "Keywords", "Answer"])
            else:
                raise Exception(f"Таблица {base_name} не найдена")
        
        # Чтение данных из JSON
        json_file = os.path.join(KNOWLEDGE_BASE_DIR, f"{base_name}.json")
        if not os.path.exists(json_file):
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump([], f)
        
        with open(json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        
        # Обновление Google Sheets
        worksheet.clear()
        worksheet.append_row(["ID", "Question", "Keywords", "Answer"])
        for entry in json_data:
            worksheet.append_row([
                entry["id"],
                entry["question"],
                entry["keywords"],
                entry["answer"]
            ])
        
        # Чтение данных из Google Sheets
        sheet_data = worksheet.get_all_records()
        json_data = [
            {
                "id": row["ID"],
                "question": row["Question"],
                "keywords": row["Keywords"],
                "answer": row["Answer"]
            }
            for row in sheet_data
        ]
        
        # Обновление JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        
        logging.info(f"База знаний {base_name} синхронизирована с Google Sheets")
    except Exception as e:
        logging.error(f"Ошибка синхронизации базы знаний {base_name}: {str(e)}")
        raise