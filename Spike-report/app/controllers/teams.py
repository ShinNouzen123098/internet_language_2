from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.models import teams as teams_model

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/tournaments")
async def tournaments_page(request: Request, db=Depends(get_db), search: str = None):
    """Страница турниров — показывает таблицу команд из БД.
    search — необязательный параметр фильтрации из строки запроса (?search=...)
    """
    all_teams = await teams_model.get_all_teams(db)

    # Фильтруем на сервере если передан поисковый запрос
    if search:
        all_teams = [t for t in all_teams if search.lower() in t["name"].lower()]

    return templates.TemplateResponse(
        request=request,
        name="tournaments.html",
        context={"teams": all_teams, "search": search}
    )
