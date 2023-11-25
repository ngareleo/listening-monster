import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from source.server.utils import ensure_required_directories_exists


class Base(DeclarativeBase):
    pass


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
app = Flask(__name__, static_folder="static")
sql_instance = SQLAlchemy(model_class=Base, metadata=metadata)
migrate = Migrate(render_as_batch=True)


def create_app() -> Flask:
    from .routes.auth import bp as auth_bp
    from .routes.index import bp as index_bp
    from .routes.upload import bp as upload_bp
    from .config import DevelopmentConfig, ProductionConfig

    if app.debug:
        config = DevelopmentConfig(instance_path=app.instance_path)
    else:
        config = ProductionConfig(instance_path=app.instance_path)

    app.config.from_object(config)

    sql_instance.init_app(app)
    migrate.init_app(app, sql_instance)

    required_directories = {
        "audio": os.path.join(str(app.static_folder), "audio"),  # Should not fail
        "db": app.instance_path,
    }
    ensure_required_directories_exists(required_directories)
    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(upload_bp)

    with app.app_context():
        sql_instance.create_all()

    return app
