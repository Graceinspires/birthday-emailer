import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask_apscheduler import APScheduler
from sqlalchemy import select

from app.database import db

from .models import Birthday

load_dotenv()

scheduler = APScheduler()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
if not BREVO_API_KEY:
    raise ValueError("BREVO_API_KEY environment variable is not set")


def send_birthday_email(name, email):
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY,
    }
    data = {
        "sender": {
            "name": "Birthday Emailer",
            "email": "victoramomodu@gmail.com",
        },
        "to": [{"email": email, "name": name}],
        "subject": f"Happy Birthday, {name}!",
        "htmlContent": """
        <!DOCTYPE html>
        <html>
        <head>
          <title>Happy Birthday</title>
        </head>
        <body>
          <h1>Happy Birthday!</h1>
          <p>Wishing you a wonderful day filled with joy and surprises.</p>
        </body>
        </html>
        """,
    }

    requests.post(
        url=url,
        headers=headers,
        json=data,
    )


@scheduler.task("cron", id="birthday_email_scheduler", hour=6)
def check_birthdays():
    today = datetime.today().date()
    statement = select(Birthday).where(Birthday.date == today)
    found_birthdays = db.session.execute(statement).scalars().all()
    for birthday in found_birthdays:
        send_birthday_email(birthday.name, birthday.email)


if __name__ == "__main__":
    send_birthday_email("Daniyan Opeyemi", "helxie3@gmail.com")
