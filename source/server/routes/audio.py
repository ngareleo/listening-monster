import os
from sqlite3 import IntegrityError
from flask import Blueprint, current_app, flash, g, request
from sqlalchemy import select
from source.engine.tools.audio_splitter import TimebasedAudioSplitter
from source.engine.transcriber.transcriber import Transcriber
from source.server.db import get_db
from source.server.models import Audio, Transcription, User
from source.server.utils import TemplateRules, login_required

bp = Blueprint("audio", __name__, url_prefix="/audio")
db = get_db()
transcriber = Transcriber()


@TemplateRules.returns_segement
@login_required
@bp.route("/<uuid:uid>")
def open_audio(uid: str):
    if request.method == "POST":
        return "Wrong method requested", 400

    user: User = g.user
    audio = db.session.scalars(select(Audio).where(Audio.uid == str(uid))).first()
    if not audio or audio.user_id != user.id:
        # TODO: Add further logging
        flash("Something went wrong")
        return TemplateRules.render_html_segment("right-nav"), 500

    return TemplateRules.render_html_segment("right-nav", audio=audio)


@TemplateRules.returns_segement
@login_required
@bp.route("/generate/<uuid:uid>")
def generate(uid: str):
    if request.method == "POST":
        return "Wrong method", 400

    user: User = g.user
    audio = db.session.scalars(select(Audio).where(Audio.uid == str(uid))).first()

    if not audio or audio.user_id != user.id:
        flash("Something went wrong")
        return TemplateRules.render_html_segment("right-nav")

    audio_loc = os.path.join(
        str(current_app.static_folder), "audio", f"{str(audio.uid)}.mp3"
    )
    audio_splitter = TimebasedAudioSplitter(audio_loc, 10)
    transcription = Transcription(
        value=transcriber.transcribe(audio_splitter), audio_id=audio.id
    )
    db.session.add(transcription)

    try:
        db.session.commit()
    except IntegrityError as ie:
        flash("Sorry something went wrong")
        print(ie.sqlite_errorname)
        return TemplateRules.render_html_segment("righ-nav")

    return TemplateRules.render_html_segment(
        "right-nav", audio=audio, transcription=transcription
    )


@bp.route("/player/<uuid:uid>")
def player(uid: str):
    if request.method == "POST":
        return "Wrong request", 400

    user: User = g.user
    audio = db.session.scalars(select(Audio).where(Audio.uid == str(uid))).first()

    if not audio:
        flash("Something went wrong")
        return "<p>Error</p>", 400

    if audio.user_id != user.id:
        flash("Something went wrong")
        return "<p>Error</p>", 401

    return TemplateRules.render_html_segment(
        "audio-player", location=f"/static/audio/{uid}.mp3"
    )
