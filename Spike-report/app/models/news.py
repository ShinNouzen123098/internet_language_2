# Модель для работы с таблицей news

async def get_all_news(db):
    """Получить все новости, сначала самые свежие."""
    rows = await db.fetch("""
        SELECT id, title, content, image_path, created_at
        FROM news
        ORDER BY created_at DESC
    """)
    return rows


async def get_news_by_id(db, news_id: int):
    """Получить одну новость по id."""
    row = await db.fetchrow("""
        SELECT id, title, content, image_path, created_at
        FROM news
        WHERE id = $1
    """, news_id)
    # $1 — это параметризованный запрос, защита от SQL-инъекций.
    # asyncpg подставит news_id вместо $1 безопасно.
    return row
