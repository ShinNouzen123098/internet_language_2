from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database import get_db, get_logger
from app.models.players import PlayersModel
from app.models.teams import TeamsModel

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = get_logger("players")


@router.get("/players")
async def players_page(request: Request, db=Depends(get_db)):
    model = PlayersModel()
    await model.load_all(db)
    return templates.TemplateResponse(
        request=request,
        name="players.html",
        context={"players": model.items}
    )


@router.get("/players/add")
async def add_player_page(request: Request, db=Depends(get_db)):
    teams = TeamsModel()
    await teams.load_all(db)
    return templates.TemplateResponse(
        request=request,
        name="player_form.html",
        context={"teams": teams.items, "player": None}
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
    name = name.strip()
    position = position.strip()

    model = PlayersModel()
    player_id = await model.create(db, name, position, birth_date, height, team_id)
    logger.info(f"Создан игрок: {name}, id={player_id}")

    return RedirectResponse(url="/players", status_code=303)


@router.get("/players/{player_id}/edit")
async def edit_player_page(player_id: int, request: Request, db=Depends(get_db)):
    model = PlayersModel()
    await model.load_by_id(db, player_id)

    teams = TeamsModel()
    await teams.load_all(db)

    return templates.TemplateResponse(
        request=request,
        name="player_form.html",
        context={"teams": teams.items, "player": model.item}
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
    name = name.strip()
    position = position.strip()

    model = PlayersModel()
    await model.update(db, player_id, name, position, birth_date, height, team_id)
    logger.info(f"Обновлён игрок id={player_id}: {name}")

    return RedirectResponse(url="/players", status_code=303)


@router.post("/players/{player_id}/delete")
async def delete_player(player_id: int, db=Depends(get_db)):
    model = PlayersModel()
    await model.delete(db, player_id)
    logger.info(f"Удалён игрок id={player_id}")

    return RedirectResponse(url="/players", status_code=303)
