# Модель соответствует таблице news.

class NewsItem:
    """Класс-модель для одной записи из таблицы news."""
    def __init__(self, row):
        self.id = row["id"]
        self.title = row["title"]
        self.content = row["content"]
        self.image_path = row["image_path"]
        self.created_at = row["created_at"]


class NewsModel:
    """Модель для работы с таблицей news."""

    def __init__(self):
        self.items = []  # данные хранятся внутри класса

    async def load_all(self, db):
        """Загрузить все новости в self.items."""
        rows = await db.fetch("""
            SELECT id, title, content, image_path, created_at
            FROM news
            ORDER BY created_at DESC
        """)
        self.items = [NewsItem(row) for row in rows]

    async def load_by_id(self, db, news_id: int):
        """Загрузить одну новость по id."""
        row = await db.fetchrow("""
            SELECT id, title, content, image_path, created_at
            FROM news
            WHERE id = $1
        """, news_id)
        self.items = [NewsItem(row)] if row else []
