from flask import Flask

from .config import SQLALCHEMY_DATABASE_URI


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    from .database import db
    from .tasks import scheduler

    db.init_app(app)
    scheduler.init_app(app)

    from .routes import router

    app.register_blueprint(router)

    from .seed import seed_database

    with app.app_context():
        db.create_all()
        seed_database()
        scheduler.start()

    return app
