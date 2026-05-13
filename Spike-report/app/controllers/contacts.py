from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database import get_db, get_logger
from app.models import contacts as contacts_model

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Получаем логгер через DI — один раз для всего контроллера
logger = get_logger("contacts")


@router.get("/contact")
async def contact_page(request: Request, sent: str = None):
    """Страница обратной связи."""
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={"sent": sent == "ok"}
    )


@router.post("/contact")
async def send_contact(
    request: Request,
    db=Depends(get_db),
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    """Обработка формы — сохраняем сообщение в БД."""
    name = name.strip()
    email = email.strip()
    message = message.strip()

    await contacts_model.create_contact(db, name, email, message)

    # Логируем факт отправки — будет видно в терминале Docker
    logger.info(f"Новое сообщение обратной связи от: {name} ({email})")

    return RedirectResponse(url="/contact?sent=ok", status_code=303)
