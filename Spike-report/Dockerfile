# Берём официальный образ Python
FROM python:3.12-slim

# Рабочая папка внутри контейнера
WORKDIR /app

# Сначала копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код
COPY . .

# Запускаем сервер на порту 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
