from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.repositories.teams_repository import TeamsRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/tournaments")
async def tournaments_page(
    request: Request,
    repo: TeamsRepository = Depends(TeamsRepository),
    search: str = None
):
    if search:
        teams = await repo.get_filtered(search)
    else:
        teams = await repo.get_all()

    return templates.TemplateResponse(
        request=request,
        name="tournaments.html",
        context={"teams": teams, "search": search}
    )
