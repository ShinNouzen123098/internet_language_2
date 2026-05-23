from app.models.news import NewsItem
from app.database import get_db
from fastapi import Depends
from asyncpg import Connection


class NewsRepository:
    """
    Repository — логика работы с БД для таблицы news.
    Не хранит состояние — только принимает запрос и возвращает данные.
    Получает db через DI в конструкторе.
    """

    def __init__(self, db: Connection = Depends(get_db)):
        self.db = db

    async def get_all(self) -> list[NewsItem]:
        """Получить все новости."""
        rows = await self.db.fetch("""
            SELECT id, title, content, image_path, created_at
            FROM news
            ORDER BY created_at DESC
        """)
        return [NewsItem.model_validate(dict(row)) for row in rows]

    async def get_by_id(self, news_id: int) -> NewsItem | None:
        """Получить одну новость по id."""
        row = await self.db.fetchrow("""
            SELECT id, title, content, image_path, created_at
            FROM news WHERE id = $1
        """, news_id)
        return NewsItem.model_validate(dict(row)) if row else None
