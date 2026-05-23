from app.models.team import Team
from app.database import get_db
from fastapi import Depends
from asyncpg import Connection


class TeamsRepository:
    """Repository для таблицы teams. Не хранит состояние."""

    def __init__(self, db: Connection = Depends(get_db)):
        self.db = db

    async def get_all(self) -> list[Team]:
        """Получить все команды."""
        rows = await self.db.fetch("""
            SELECT id, name, city FROM teams ORDER BY name
        """)
        return [Team.model_validate(dict(row)) for row in rows]

    async def get_filtered(self, search: str) -> list[Team]:
        """Получить команды с фильтрацией на уровне БД."""
        rows = await self.db.fetch("""
            SELECT id, name, city FROM teams
            WHERE name ILIKE $1
            ORDER BY name
        """, f"%{search}%")
        return [Team.model_validate(dict(row)) for row in rows]
