from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.models.teams import TeamsModel

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/tournaments")
async def tournaments_page(request: Request, db=Depends(get_db), search: str = None):
    model = TeamsModel()

    # Фильтрация теперь на уровне БД, а не в Python
    if search:
        await model.load_filtered(db, search)
    else:
        await model.load_all(db)

    return templates.TemplateResponse(
        request=request,
        name="tournaments.html",
        context={"teams": model.items, "search": search}
    )
