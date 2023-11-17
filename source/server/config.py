import os
from flask import Flask


class BaseConfig(object):
    SECRET_KEY = "dev"

    def __init__(self, instance_path: str) -> None:
        BaseConfig.DATABASE = os.path.join(instance_path, "app.sqlite")
