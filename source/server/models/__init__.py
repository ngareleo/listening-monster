from typing import NoReturn, List
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from source.server import sql_instance


class T(DeclarativeBase):
    pass


class Base:
    _date_added: Mapped[datetime] = mapped_column(
        "date_added", DateTime, default=datetime.now(), deferred=True
    )
    _last_modified: Mapped[datetime] = mapped_column(
        "last_modified", DateTime, default=datetime.now(), deferred=True
    )

    @property
    def date_added(self):
        return self._date_added.strftime("%m/%d/%Y")

    @date_added.setter
    def date_added(self, date: datetime):
        self._date_added = date

    @property
    def last_modified(self):
        return self._last_modified.strftime("%m/%d/%Y")

    @last_modified.setter
    def last_modified(self, date: datetime):
        self._last_modified = date


class User(sql_instance.Model, Base, T):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        "username", String, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column("email", String, unique=True)
    _password_hash: Mapped[str] = mapped_column(
        "_password_hash", String, nullable=False
    )
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
        return f"<User {self.username}>"


class Audio(sql_instance.Model, Base, T):
    __tablename__ = "audio"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    label: Mapped[str] = mapped_column("label", String, nullable=False)
    description: Mapped[str] = mapped_column("description", String, nullable=False)
    _length: Mapped[int] = mapped_column("_length", Integer, nullable=False)
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="audios")
    uid: Mapped[str] = mapped_column("uid", String, nullable=False, unique=True)
    transcriptions: Mapped[List["Transcription"]] = relationship(back_populates="audio")

    @property
    def length(self) -> str:
        # Get the length in HH:MM:SS format from minutes
        h = int(self._length // 3600)
        m = int(self._length // 60)
        s = int(self._length % 60)
        return "".join(
            [
                f"{h} Hrs " if h > 0 else "",
                f"{m} Min " if m > 0 else "",
                f"{s} Secs" if s > 0 else "",
            ]
        )

    @length.setter
    def length(self, length: int) -> None:
        """Length in secs"""
        self._length = length

    def __str__(self) -> str:
        return f"<Audio {self.label}>"


class Transcription(sql_instance.Model, Base, T):
    __tablename__ = "transcription"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    value: Mapped[str] = mapped_column("value", String, nullable=False)
    audio_id: Mapped[int] = mapped_column("audio_id", ForeignKey("audio.id"))
    audio: Mapped["Audio"] = relationship(back_populates="transcriptions")
