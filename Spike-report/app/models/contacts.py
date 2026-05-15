class Contact:
    """Класс-модель для одной записи из таблицы contacts."""
    def __init__(self, row):
        self.id = row["id"]
        self.name = row["name"]
        self.email = row["email"]
        self.message = row["message"]
        self.created_at = row["created_at"]


class ContactsModel:
    """Модель для работы с таблицей contacts."""

    def __init__(self):
        self.items = []

    async def create(self, db, name: str, email: str, message: str):
        """Сохранить новое сообщение обратной связи."""
        await db.execute("""
            INSERT INTO contacts (name, email, message)
            VALUES ($1, $2, $3)
        """, name, email, message)

    async def load_all(self, db):
        """Загрузить все сообщения."""
        rows = await db.fetch("""
            SELECT id, name, email, message, created_at
            FROM contacts
            ORDER BY created_at DESC
        """)
        self.items = [Contact(row) for row in rows]
