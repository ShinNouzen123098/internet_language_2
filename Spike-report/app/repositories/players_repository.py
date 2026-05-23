from datetime import date
from app.models.player import Player
from app.database import get_db
from fastapi import Depends
from asyncpg import Connection


class PlayersRepository:

    def __init__(self, db: Connection = Depends(get_db)):
        self.db = db

    async def get_all(self) -> list[Player]:
        """Получить всех игроков с названием команды через JOIN."""
        rows = await self.db.fetch("""
            SELECT p.id, p.name, p.position, p.birth_date, p.height,
                   p.team_id, t.name AS team_name
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.id
            ORDER BY p.name
        """)
        return [Player.model_validate(dict(row)) for row in rows]

    async def get_by_id(self, player_id: int) -> Player | None:
        """Получить одного игрока по id."""
        row = await self.db.fetchrow("""
            SELECT p.id, p.name, p.position, p.birth_date, p.height,
                   p.team_id, t.name AS team_name
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.id
            WHERE p.id = $1
        """, player_id)
        return Player.model_validate(dict(row)) if row else None

    async def create(self, name: str, position: str,
                     birth_date: date, height: int, team_id: int) -> int:
        """Создать игрока, вернуть его id."""
        row = await self.db.fetchrow("""
            INSERT INTO players (name, position, birth_date, height, team_id)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """, name, position, birth_date, height, team_id)
        return row["id"]

    async def update(self, player_id: int, name: str, position: str,
                     birth_date: date, height: int, team_id: int) -> None:
        """Обновить данные игрока."""
        await self.db.execute("""
            UPDATE players
            SET name=$1, position=$2, birth_date=$3, height=$4, team_id=$5
            WHERE id=$6
        """, name, position, birth_date, height, team_id, player_id)

    async def delete(self, player_id: int) -> None:
        """Удалить игрока."""
        await self.db.execute(
            "DELETE FROM players WHERE id = $1", player_id
        )
