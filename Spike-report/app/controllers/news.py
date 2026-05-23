from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.repositories.news_repository import NewsRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
@router.get("/news")
async def news_page(
    request: Request,
    repo: NewsRepository = Depends(NewsRepository)
):
    """
    Теперь Repository приходит через DI — FastAPI сам создаёт
    NewsRepository и передаёт его в функцию. NewsRepository в свою
    очередь сам получает db через свой Depends(get_db).
    Цепочка DI: get_db → NewsRepository → news_page
    """
    news_list = await repo.get_all()
    return templates.TemplateResponse(
        request=request,
        name="news.html",
        context={"news_list": news_list}
    )
