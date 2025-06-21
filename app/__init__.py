from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from .database import db
    from .tasks import scheduler

    db.init_app(app)
    scheduler.init_app(app)

    from .routes import router

    app.register_blueprint(router)

    with app.app_context():
        db.create_all()
        scheduler.start()

    return app
