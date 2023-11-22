from typing import NoReturn
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from source.server import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True)
    _password_hash: Mapped[str] = mapped_column(String, nullable=False)

    @property
    def password(self) -> NoReturn:
        raise AttributeError("Not allowed to access password")

    @password.setter
    def password(self, password: str):
        self._password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self._password_hash, password)

    def __str__(self) -> str:
        return f"< User {self.username} >"
