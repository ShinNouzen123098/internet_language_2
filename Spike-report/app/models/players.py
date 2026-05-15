class Player:
    """Класс-модель для одной записи из таблицы players."""
    def __init__(self, row):
        self.id = row["id"]
        self.name = row["name"]
        self.position = row["position"]
        self.birth_date = row["birth_date"]
        self.height = row["height"]
        self.team_id = row.get("team_id")
        self.team_name = row.get("team_name")


class PlayersModel:
    """Модель для работы с таблицей players."""

    def __init__(self):
        self.items = []
        self.item = None  # для одного игрока (get by id)

    async def load_all(self, db):
        """Загрузить всех игроков с названием команды через JOIN."""
        rows = await db.fetch("""
            SELECT p.id, p.name, p.position, p.birth_date, p.height,
                   p.team_id, t.name AS team_name
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.id
            ORDER BY p.name
        """)
        self.items = [Player(row) for row in rows]

    async def load_by_id(self, db, player_id: int):
        """Загрузить одного игрока по id."""
        row = await db.fetchrow("""
            SELECT p.id, p.name, p.position, p.birth_date, p.height,
                   p.team_id, t.name AS team_name
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.id
            WHERE p.id = $1
        """, player_id)
        self.item = Player(row) if row else None

    async def create(self, db, name: str, position: str,
                     birth_date: str, height: int, team_id: int):
        """Создать нового игрока."""
        row = await db.fetchrow("""
            INSERT INTO players (name, position, birth_date, height, team_id)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """, name, position, birth_date, height, team_id)
        return row["id"]

    async def update(self, db, player_id: int, name: str, position: str,
                     birth_date: str, height: int, team_id: int):
        """Обновить данные игрока."""
        await db.execute("""
            UPDATE players
            SET name = $1, position = $2, birth_date = $3,
                height = $4, team_id = $5
            WHERE id = $6
        """, name, position, birth_date, height, team_id, player_id)

    async def delete(self, db, player_id: int):
        """Удалить игрока."""
        await db.execute("""
            DELETE FROM players WHERE id = $1
        """, player_id)
