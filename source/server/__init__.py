from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


app = Flask(__name__, static_folder="static")
sql_instance = SQLAlchemy(model_class=Base)


class ListeningMonster:
    app = None
    db = None
    test_config = None
    migrate = None

    def __init__(self, flask: Flask, db: SQLAlchemy, migrate=Migrate, test_config=None):
        ListeningMonster.app = flask
        ListeningMonster.db = db
        ListeningMonster.test_config = test_config
        ListeningMonster.migrate = migrate

        app = ListeningMonster.app
        db = ListeningMonster.db
        config = None

        from .routes.auth import bp as auth_bp
        from .routes.index import bp as index_bp
        from .routes.upload import bp as upload_bp
        from .config import DevelopmentConfig, ProductionConfig

        if app.debug:
            config = DevelopmentConfig(instance_path=app.instance_path)
        else:
            config = ProductionConfig(instance_path=app.instance_path)

        app.config.from_object(config)

        db.init_app(app)
        migrate = Migrate(app, db)

        if test_config is None:
            app.config.from_pyfile(
                "config.py",
            )
        else:
            app.config.from_mapping(test_config)

        required_directories = {
            "audio": os.path.join(str(app.static_folder), "audio"),  # Should not fail
            "db": app.instance_path,
        }
        self._ensure_required_directories_exists(required_directories)
        app.register_blueprint(auth_bp)
        app.register_blueprint(index_bp)
        app.register_blueprint(upload_bp)

        with app.app_context():
            db.create_all()

    def _ensure_required_directories_exists(self, dirs: dict[str, str]):
        for k, v in dirs.items():
            print(f"[Log] Initialising {k}", end=" ")
            if os.path.exists(v):
                print(f"{k} found in location: {v}")
            else:
                try:
                    print(f"Initializing {k} in location {v}")
                    os.makedirs(v)
                except OSError as e:
                    print(f"Error {e} occurred")


def create_app():
    return ListeningMonster(
        app,
        sql_instance,
    ).app
