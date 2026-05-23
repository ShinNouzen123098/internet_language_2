from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator


class Contact(BaseModel):
    """
    Модель обратной связи.
    EmailStr — Pydantic автоматически проверяет формат email.
    Для этого нужно установить: pip install pydantic[email]
    """
    id: int
    name: str
    email: EmailStr
    message: str
    created_at: datetime

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Имя не может быть пустым")
        return v.strip()

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Сообщение не может быть пустым")
        return v.strip()

    model_config = {"from_attributes": True}
