import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database import db


class Birthday(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
