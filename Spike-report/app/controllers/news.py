from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.models.news import NewsModel

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
@router.get("/news")
async def news_page(request: Request, db=Depends(get_db)):
    model = NewsModel()
    await model.load_all(db)

    return templates.TemplateResponse(
        request=request,
        name="news.html",
        context={"news_list": model.items}
    )
