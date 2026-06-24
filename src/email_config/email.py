from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.core.settings import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)


async def send_welcome_mail(email: str, name: str):
    message = MessageSchema(
        subject="Welcome!",
        recipients=[email],
        body=f"Hello {name}, Welcome to our platform!",
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)