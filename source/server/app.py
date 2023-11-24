from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(test_config=None):
    from .routes.auth import bp as auth_bp
    from .routes.index import bp as index_bp
    from .routes.upload import bp as upload_bp
    from .config import DevelopmentConfig, ProductionConfig

    config = None

    app = Flask(__name__)
    if app.debug:
        config = DevelopmentConfig(instance_path=app.instance_path)
    else:
        config = ProductionConfig(instance_path=app.instance_path)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        app.config.from_pyfile(
            "config.py",
        )
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(upload_bp)

    with app.app_context():
        db.create_all()

    return app
