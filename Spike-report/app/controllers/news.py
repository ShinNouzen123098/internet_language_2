from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.models import news as news_model

# Роутер
router = APIRouter()

# Шаблонизатор - ищет HTML-файлы в папке app/templates/
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
@router.get("/news")
async def news_page(request: Request, db=Depends(get_db)):
    """
    Страница новостей — главная страница сайта.

    Depends(get_db) — это и есть Dependency Injection:
    FastAPI сам вызовет get_db() и передаст соединение с БД
    в параметр db. Нам не нужно думать об этом вручную.
    """
    all_news = await news_model.get_all_news(db)

    # Рендерим шаблон и передаём в него данные.
    # Всё что передано сюда — доступно в HTML через {{ переменная }}
    return templates.TemplateResponse(
        request=request,
        name="news.html",
        context={"news_list": all_news}
    )
