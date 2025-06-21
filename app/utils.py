import datetime

from sqlalchemy import select

from app.database import db
from app.models import Birthday


def seed_database():
    import csv

    with open("./data/birthday_project.csv", "r") as csv_file:
        is_header = True
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if is_header:
                is_header = False
                continue

            try:
                statement = select(Birthday).where(Birthday.email == row["email"])
                existing_birthday = db.session.execute(statement).scalar_one_or_none()
                if existing_birthday is None:
                    continue

                year = int(row["birth_year"])
                month = int(row["birth_month"])
                day = int(row["birth_day"])
                birth_date = datetime.date(year, month, day)
                new_birthday = Birthday(
                    name=row["names"],
                    email=row["email"],
                    date=birth_date,
                )
                db.session.add(new_birthday)
                db.session.commit()

            except Exception as e:
                print(f"Error seeding database: {e}")
