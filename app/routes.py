from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy.sql import select

from app.database import db
from app.models import Birthday

router = Blueprint("main", __name__)


@router.route("/")
def index():
    statement = select(Birthday)
    birthdays = db.session.execute(statement).scalars().all()
    return render_template("index.html", data=birthdays)


@router.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        birthday = request.form["birthday"]
        date = datetime.strptime(birthday, "%Y-%m-%d").date()

        statement = select(Birthday).where(Birthday.email == email)
        existing_birthday = db.session.execute(statement).scalar_one_or_none()
        if existing_birthday is None:
            new_birthday = Birthday(email=email, name=name, date=date)
            db.session.add(new_birthday)
            db.session.commit()

        return redirect(url_for("main.index"))

    return render_template("add.html")


@router.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        birthday = request.form["birthday"]
        date = datetime.strptime(birthday, "%Y-%m-%d").date()

        statement = select(Birthday).where(Birthday.email == email)
        birthday_to_update = db.session.execute(statement).scalar_one_or_none()
        if birthday_to_update:
            birthday_to_update.name = name
            birthday_to_update.date = date
            db.session.commit()

        return redirect(url_for("main.index"))

    email = request.args.get("email")
    birthday = select(Birthday).where(Birthday.email == email)
    birthday = db.session.execute(birthday).scalar_one_or_none()
    if birthday is None:
        return redirect(url_for("main.index"))

    return render_template(
        "edit.html",
        name=birthday.name,
        email=birthday.email,
        birthday=birthday.date,
    )


@router.route("/delete")
def delete():
    email = request.args.get("email")
    birthday = select(Birthday).where(Birthday.email == email)
    birthday = db.session.execute(birthday).scalar_one_or_none()
    if birthday is None:
        return redirect(url_for("main.index"))

    db.session.delete(birthday)
    db.session.commit()
    return redirect(url_for("main.index"))
