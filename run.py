import uvicorn
import asyncio
from threading import Thread
from admin_panel.backend.main import app
from bot.main import start_bot
from bot.config import FASTAPI_PORT
import logging

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=FASTAPI_PORT, log_level="info")

async def main():
    # Запуск FastAPI в отдельном потоке
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Запуск бота
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())