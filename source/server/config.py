import os


class BaseConfig(object):
    def __init__(self, instance_path: str) -> None:
        BaseConfig.SECRET_KEY = "dev"
        BaseConfig.DATABASE = f"sqlite:///{os.path.join(instance_path, "app.sqlite")}"


class DevelopmentConfig(BaseConfig):
    def __init__(self, instance_path: str) -> None:
        DevelopmentConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(instance_path, "app.sqlite")}"
        super().__init__(instance_path)


class ProductionConfig(BaseConfig):
    def __init__(self, instance_path: str) -> None:
        ProductionConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(instance_path, "app.sqlite")}"
        super().__init__(instance_path)
