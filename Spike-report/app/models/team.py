from pydantic import BaseModel, field_validator


class Team(BaseModel):
    """Модель команды — только данные и их валидация."""
    id: int
    name: str
    city: str

    @field_validator("name", "city")
    @classmethod
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()

    model_config = {"from_attributes": True}
