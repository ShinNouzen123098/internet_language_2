from datetime import date
from pydantic import BaseModel, field_validator
from typing import Optional


class Player(BaseModel):
    """Модель игрока — только данные и их валидация."""
    id: int
    name: str
    position: str
    birth_date: date
    height: int
    team_id: Optional[int] = None
    team_name: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Имя не может быть пустым")
        return v.strip()

    @field_validator("height")
    @classmethod
    def height_valid(cls, v):
        if not (150 <= v <= 230):
            raise ValueError("Рост должен быть от 150 до 230 см")
        return v

    @field_validator("birth_date")
    @classmethod
    def birth_date_valid(cls, v):
        if v.year < 1950 or v.year > 2010:
            raise ValueError("Некорректная дата рождения")
        return v

    model_config = {"from_attributes": True}
