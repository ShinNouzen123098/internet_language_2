# Модель для работы с таблицей contacts

async def create_contact(db, name: str, email: str, message: str):
    """Сохранить сообщение обратной связи в БД."""
    await db.execute("""
        INSERT INTO contacts (name, email, message)
        VALUES ($1, $2, $3)
    """, name, email, message)


async def get_all_contacts(db):
    """Получить все сообщения"""
    rows = await db.fetch("""
        SELECT id, name, email, message, created_at
        FROM contacts
        ORDER BY created_at DESC
    """)
    return rows
