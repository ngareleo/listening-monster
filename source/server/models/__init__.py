from typing import NoReturn, List
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from source.server import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True)
    _password_hash: Mapped[str] = mapped_column(String, nullable=False)
    audios: Mapped[List["Audio"]] = relationship(back_populates="owner")

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


class Audio(db.Model):
    __tablename__ = "audio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    _label: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="audios")

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, lbl: str) -> None:
        # if user has used label before we get an integrity error
        self._label = f"{lbl}"

    def __str__(self) -> str:
        return f"< Audio {self._label} >"
