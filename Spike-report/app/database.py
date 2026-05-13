import os
import logging
import asyncpg
from dotenv import load_dotenv

# Читаем переменные из файла .env
load_dotenv()

# ============================================
# Логгер
# ============================================

# Настраиваем формат логов: время | уровень | сообщение
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def get_logger(name: str = "spike_report") -> logging.Logger:
    """
    Dependency Injection для логгера.

    - logger.info("всё хорошо")        — обычное сообщение
    - logger.warning("странно")        — предупреждение
    - logger.error("что-то сломалось") — ошибка

    Через DI контроллер получает готовый логгер не создавая его сам.
    """
    return logging.getLogger(name)


# ============================================
# База данных
# ============================================

# Собираем строку подключения из переменных окружения
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Пул соединений — создаётся один раз при старте приложения.
pool: asyncpg.Pool = None


async def init_pool():
    """Вызывается при старте приложения — создаёт пул соединений."""
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)


async def close_pool():
    """Вызывается при остановке приложения — закрывает все соединения."""
    global pool
    if pool:
        await pool.close()


async def get_db():
    """
    Dependency Injection для подключения к БД.

    FastAPI автоматически передаёт готовое соединение в контроллер.
    После завершения запроса соединение возвращается в пул.
    """
    async with pool.acquire() as connection:
        yield connection
