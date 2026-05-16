from datetime import date


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
        self.item = None

    async def load_all(self, db):
        rows = await db.fetch("""
            SELECT p.id, p.name, p.position, p.birth_date, p.height,
                   p.team_id, t.name AS team_name
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.id
            ORDER BY p.name
        """)
        self.items = [Player(row) for row in rows]

    async def load_by_id(self, db, player_id: int):
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
        birth_date_obj = date.fromisoformat(birth_date)

        row = await db.fetchrow("""
            INSERT INTO players (name, position, birth_date, height, team_id)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """, name, position, birth_date_obj, height, team_id)
        return row["id"]

    async def update(self, db, player_id: int, name: str, position: str,
                     birth_date: str, height: int, team_id: int):
        birth_date_obj = date.fromisoformat(birth_date)

        await db.execute("""
            UPDATE players
            SET name = $1, position = $2, birth_date = $3,
                height = $4, team_id = $5
            WHERE id = $6
        """, name, position, birth_date_obj, height, team_id, player_id)

    async def delete(self, db, player_id: int):
        await db.execute("""
            DELETE FROM players WHERE id = $1
        """, player_id)
