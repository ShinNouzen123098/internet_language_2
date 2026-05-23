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
    news_list = await repo.get_all()
    return templates.TemplateResponse(
        request=request,
        name="news.html",
        context={"news_list": news_list}
    )
