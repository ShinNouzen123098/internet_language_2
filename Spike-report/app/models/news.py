from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class NewsItem(BaseModel):
    """
    Модель — только описание данных, никакой логики БД.
    Pydantic автоматически валидирует поля при создании объекта.
    """
    id: int
    title: str
    content: str
    image_path: Optional[str] = None
    created_at: datetime

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Заголовок не может быть пустым")
        return v.strip()

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Содержимое не может быть пустым")
        return v.strip()

    model_config = {"from_attributes": True}
