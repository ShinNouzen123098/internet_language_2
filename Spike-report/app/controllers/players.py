from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database import get_db, get_logger
from app.models import players as players_model
from app.models import teams as teams_model

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = get_logger("players")


@router.get("/players")
async def players_page(request: Request, db=Depends(get_db)):
    """Страница со списком всех игроков."""
    all_players = await players_model.get_all_players(db)
    return templates.TemplateResponse(
        request=request,
        name="players.html",
        context={"players": all_players}
    )


@router.get("/players/add")
async def add_player_page(request: Request, db=Depends(get_db)):
    """Страница с формой добавления нового игрока."""
    all_teams = await teams_model.get_all_teams(db)
    return templates.TemplateResponse(
        request=request,
        name="player_form.html",
        context={"teams": all_teams, "player": None}
    )


@router.post("/players/add")
async def add_player(
    request: Request,
    db=Depends(get_db),
    name: str = Form(...),
    position: str = Form(...),
    birth_date: str = Form(...),
    height: int = Form(...),
    team_id: int = Form(...)
):
    """Обработка формы — сохраняем нового игрока в БД."""
    name = name.strip()
    position = position.strip()

    player_id = await players_model.create_player(
        db, name, position, birth_date, height, team_id
    )
    logger.info(f"Создан игрок: {name}, id={player_id}")

    return RedirectResponse(url="/players", status_code=303)


@router.get("/players/{player_id}/edit")
async def edit_player_page(player_id: int, request: Request, db=Depends(get_db)):
    """Страница редактирования игрока."""
    player = await players_model.get_player_by_id(db, player_id)
    all_teams = await teams_model.get_all_teams(db)
    return templates.TemplateResponse(
        request=request,
        name="player_form.html",
        context={"teams": all_teams, "player": player}
    )


@router.post("/players/{player_id}/edit")
async def edit_player(
    player_id: int,
    request: Request,
    db=Depends(get_db),
    name: str = Form(...),
    position: str = Form(...),
    birth_date: str = Form(...),
    height: int = Form(...),
    team_id: int = Form(...)
):
    """Обработка формы редактирования."""
    name = name.strip()
    position = position.strip()

    await players_model.update_player(
        db, player_id, name, position, birth_date, height, team_id
    )
    logger.info(f"Обновлён игрок id={player_id}: {name}")

    return RedirectResponse(url="/players", status_code=303)


@router.post("/players/{player_id}/delete")
async def delete_player(player_id: int, db=Depends(get_db)):
    """Удаление игрока."""
    await players_model.delete_player(db, player_id)
    logger.info(f"Удалён игрок id={player_id}")

    return RedirectResponse(url="/players", status_code=303)
