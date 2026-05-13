from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.database import init_pool, close_pool
from app.controllers import news, players, teams, contacts


# lifespan — управляет жизненным циклом приложения.
# Код ДО yield выполняется при старте, код ПОСЛЕ yield — при остановке.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()   # при старте — создаём пул соединений с БД
    yield
    await close_pool()  # при остановке — закрываем все соединения


# Создаём приложение FastAPI
app = FastAPI(lifespan=lifespan)

# Подключаем папку со статическими файлами (css, js, img).
# Браузер сможет получить их по адресу /static/css/styles.css
app.mount(
    "/static",
    StaticFiles(directory="app/templates/static"),
    name="static"
)

# Подключаем контроллеры (роутеры).
# Каждый роутер отвечает за свою группу страниц.
app.include_router(news.router)
app.include_router(players.router)
app.include_router(teams.router)
app.include_router(contacts.router)
