class Team:
    """Класс-модель для одной записи из таблицы teams."""
    def __init__(self, row):
        self.id = row["id"]
        self.name = row["name"]
        self.city = row["city"]


class TeamsModel:
    """Модель для работы с таблицей teams."""

    def __init__(self):
        self.items = []

    async def load_all(self, db):
        """Загрузить все команды в self.items."""
        rows = await db.fetch("""
            SELECT id, name, city
            FROM teams
            ORDER BY name
        """)
        self.items = [Team(row) for row in rows]

    async def load_filtered(self, db, search: str):
        """
        Загрузить команды с фильтрацией на уровне БД.
        ILIKE — регистронезависимый поиск в PostgreSQL.
        % — wildcard: найти строки где name содержит search в любом месте.
        """
        rows = await db.fetch("""
            SELECT id, name, city
            FROM teams
            WHERE name ILIKE $1
            ORDER BY name
        """, f"%{search}%")
        self.items = [Team(row) for row in rows]
