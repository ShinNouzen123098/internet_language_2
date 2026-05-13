# Модель для работы с таблицей players
# Реализует полный CRUD: Create, Read, Update, Delete

async def get_all_players(db):
    """
    Получить всех игроков вместе с названием команды.
    JOIN объединяет две таблицы: players и teams.
    LEFT JOIN: взять всех игроков, даже если у них нет команды.
    """
    rows = await db.fetch("""
        SELECT p.id, p.name, p.position, p.birth_date, p.height,
               t.name AS team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.id
        ORDER BY p.name
    """)
    return rows


async def get_player_by_id(db, player_id: int):
    """Получить одного игрока по id."""
    row = await db.fetchrow("""
        SELECT p.id, p.name, p.position, p.birth_date, p.height,
               p.team_id, t.name AS team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.id
        WHERE p.id = $1
    """, player_id)
    return row


async def create_player(db, name: str, position: str,
                         birth_date: str, height: int, team_id: int):
    """Создать нового игрока. Возвращает id созданной записи."""
    row = await db.fetchrow("""
        INSERT INTO players (name, position, birth_date, height, team_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
    """, name, position, birth_date, height, team_id)
    return row["id"]


async def update_player(db, player_id: int, name: str, position: str,
                         birth_date: str, height: int, team_id: int):
    """Обновить данные игрока."""
    await db.execute("""
        UPDATE players
        SET name = $1, position = $2, birth_date = $3,
            height = $4, team_id = $5
        WHERE id = $6
    """, name, position, birth_date, height, team_id, player_id)


async def delete_player(db, player_id: int):
    """Удалить игрока по id."""
    await db.execute("""
        DELETE FROM players
        WHERE id = $1
    """, player_id)
