from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import date

from app.database import get_logger
from app.repositories.players_repository import PlayersRepository
from app.repositories.teams_repository import TeamsRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = get_logger("players")


@router.get("/players")
async def players_page(
    request: Request,
    repo: PlayersRepository = Depends(PlayersRepository)
):
    players = await repo.get_all()
    return templates.TemplateResponse(
        request=request,
        name="players.html",
        context={"players": players}
    )


@router.get("/players/add")
async def add_player_page(
    request: Request,
    teams_repo: TeamsRepository = Depends(TeamsRepository)
):
    teams = await teams_repo.get_all()
    return templates.TemplateResponse(
        request=request,
        name="player_form.html",
        context={"teams": teams, "player": None}
    )


@router.post("/players/add")
async def add_player(
    request: Request,
    repo: PlayersRepository = Depends(PlayersRepository),
    name: str = Form(...),
    position: str = Form(...),
    birth_date: str = Form(...),
    height: int = Form(...),
    team_id: int = Form(...)
):
    name = name.strip()
    position = position.strip()
    birth_date_obj = date.fromisoformat(birth_date)

    player_id = await repo.create(name, position, birth_date_obj, height, team_id)
    logger.info(f"Создан игрок: {name}, id={player_id}")
    return RedirectResponse(url="/players", status_code=303)


@router.get("/players/{player_id}/edit")
async def edit_player_page(
    player_id: int,
    request: Request,
    repo: PlayersRepository = Depends(PlayersRepository),
    teams_repo: TeamsRepository = Depends(TeamsRepository)
):
    player = await repo.get_by_id(player_id)
    teams = await teams_repo.get_all()
    return templates.TemplateResponse(
        request=request,
        name="player_form.html",
        context={"teams": teams, "player": player}
    )


@router.post("/players/{player_id}/edit")
async def edit_player(
    player_id: int,
    request: Request,
    repo: PlayersRepository = Depends(PlayersRepository),
    name: str = Form(...),
    position: str = Form(...),
    birth_date: str = Form(...),
    height: int = Form(...),
    team_id: int = Form(...)
):
    name = name.strip()
    position = position.strip()
    birth_date_obj = date.fromisoformat(birth_date)

    await repo.update(player_id, name, position, birth_date_obj, height, team_id)
    logger.info(f"Обновлён игрок id={player_id}: {name}")
    return RedirectResponse(url="/players", status_code=303)


@router.post("/players/{player_id}/delete")
async def delete_player(
    player_id: int,
    repo: PlayersRepository = Depends(PlayersRepository)
):
    await repo.delete(player_id)
    logger.info(f"Удалён игрок id={player_id}")
    return RedirectResponse(url="/players", status_code=303)
