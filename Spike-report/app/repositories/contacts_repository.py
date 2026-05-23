from app.models.contact import Contact
from app.database import get_db
from fastapi import Depends
from asyncpg import Connection


class ContactsRepository:

    def __init__(self, db: Connection = Depends(get_db)):
        self.db = db

    async def create(self, name: str, email: str, message: str) -> None:
        """Сохранить новое сообщение."""
        await self.db.execute("""
            INSERT INTO contacts (name, email, message)
            VALUES ($1, $2, $3)
        """, name, email, message)

    async def get_all(self) -> list[Contact]:
        """Получить все сообщения."""
        rows = await self.db.fetch("""
            SELECT id, name, email, message, created_at
            FROM contacts ORDER BY created_at DESC
        """)
        return [Contact.model_validate(dict(row)) for row in rows]
