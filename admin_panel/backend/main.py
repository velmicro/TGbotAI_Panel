from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from admin_panel.backend.routes.core import router as core_router
from admin_panel.backend.routes.knowledge_base import router as knowledge_router
from admin_panel.backend.routes.dialogs import router as dialogs_router
from bot.utils.logging_config import setup_logging

# Настройка логирования
setup_logging()

app = FastAPI(title="TG BotAI Admin Panel")

# Разрешаем CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="admin_panel/static"), name="static")

# Подключаем шаблоны
templates = Jinja2Templates(directory="admin_panel/templates")

# Подключаем маршруты
app.include_router(core_router)
app.include_router(knowledge_router)
app.include_router(dialogs_router)