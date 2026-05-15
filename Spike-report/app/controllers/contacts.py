from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database import get_db, get_logger
from app.models.contacts import ContactsModel

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = get_logger("contacts")


@router.get("/contact")
async def contact_page(request: Request, sent: str = None):
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
    name = name.strip()
    email = email.strip()
    message = message.strip()

    model = ContactsModel()
    await model.create(db, name, email, message)
    logger.info(f"Новое сообщение от: {name} ({email})")

    return RedirectResponse(url="/contact?sent=ok", status_code=303)
