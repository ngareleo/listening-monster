import os
from dotenv import load_dotenv


class BaseConfig(object):
    def __init__(self, instance_path: str) -> None:
        load_dotenv(os.path.join(instance_path, ".env"))
        BaseConfig.SECRET_KEY = "dev"
        BaseConfig.AXIOM_API_KEY = os.getenv("AXIOM_API_KEY")
        BaseConfig.DATABASE = f"sqlite:///{os.path.join(instance_path, "app.sqlite")}"


class DevelopmentConfig(BaseConfig):
    def __init__(self, instance_path: str) -> None:
        DevelopmentConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(instance_path, "app.sqlite")}"
        super().__init__(instance_path)


class ProductionConfig(BaseConfig):
    def __init__(self, instance_path: str) -> None:
        ProductionConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(instance_path, "app.sqlite")}"
        super().__init__(instance_path)
