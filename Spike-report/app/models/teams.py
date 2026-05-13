# Модель для работы с таблицей teams

async def get_all_teams(db):
    """Получить все команды — используется для таблицы Суперлиги
    и для выпадающего списка при добавлении игрока."""
    rows = await db.fetch("""
        SELECT id, name, city
        FROM teams
        ORDER BY name
    """)
    return rows
