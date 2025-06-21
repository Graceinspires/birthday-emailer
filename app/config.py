import os

from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
IS_SEEDED = os.getenv("IS_SEEDED", False)
SCHEDULER_API_ENABLED = True
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
