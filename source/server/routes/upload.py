import os
from sqlite3 import IntegrityError
from threading import Timer
from uuid import uuid4
from flask import (
    Blueprint,
    current_app,
    flash,
    render_template,
    request,
    session,
    url_for,
    g,
)
from sqlalchemy import select
from source.server.db import get_db
from source.server.models import Audio, User
from ..utils import TemplateRules, login_required

db = get_db()


def delete_file_from_path(file: str):
    if os.path.exists(file):
        os.remove(file)
    else:
        raise ValueError("File doesn't exist")


bp = Blueprint("upload", __name__, url_prefix="/upload")
pending_threads: dict[str, Timer] = {}


@TemplateRules.returns_segement
@login_required
@bp.route("/", methods=("GET", "POST"))
def index():
    """
    This route returns html segments exclusively"""
    if request.method == "POST":
        user: User = g.user
        title = request.form.get("title")
        description = request.form.get("description")
        f = request.files.get("audio")

        if not title:
            flash("Audio file title is required")
        if not description:
            flash("Please add description for audio file")
        if not f or not f.filename:
            flash("Audio file is required")

        if not title or not description or not f:
            return TemplateRules.render_html_segment("audio/audio-upload")

        if audio_exists_in_db(user_id=user.id, title=title):
            flash("Label provided has been used before")
            return TemplateRules.render_html_segment(
                "audio-upload"
            )  # TODO: Add value details to render with pre-filled data

        if not f.filename or not f.filename.endswith(".mp3"):
            flash("File is missing extension")
            return TemplateRules.render_html_segment("audio-segment")

        uid = generate_uid()
        filename = f"{uid}.mp3"

        if not current_app.static_folder:
            return "Something went wrong back here", 500

        server_location = os.path.join(current_app.static_folder, "audio", filename)
        if not os.path.exists(server_location):
            # TODO: We need to A/B test this
            f.save(server_location)

            # Remove the audio file after 5 min on a separate thread
            file_managing_thread = Timer(
                60.0 * 1, delete_file_from_path, (server_location,)
            )
            file_managing_thread.start()
            file_managing_thread.name = filename
            pending_threads[server_location] = file_managing_thread

        session["upload"] = {
            "id": filename,
            "label": title,
            "description": description,
            "uid": uid,
        }
        return TemplateRules.render_html_segment(
            "confirm-details",
            location=url_for("static", filename=f"audio/{filename}"),
            title=title,
            description=description,
        )

    return render_template("upload.html")


@TemplateRules.returns_segement
@login_required
@bp.route("/confirm")
def confirm_audio_file():
    # This is htmx triggerred so data is always present
    from source.engine import get_audio_file_length_in_secs

    if request.method == "POST":
        return "Bad request", 400

    upload = session.get("upload")

    if not upload:
        return TemplateRules.render_html_segment("audio-upload")

    user: User = g.user
    label = upload.get("label")
    description = upload.get("description")
    filename = upload.get("id")
    uid = upload.get("uid")

    server_location = os.path.join(
        str(current_app.static_folder),  # guranteed this None check will pass in prod
        "audio",
        filename,
    )

    if not os.path.exists(server_location):
        flash("Sorry, you delayed confirmation. Go back to reupload")
        return TemplateRules.render_html_segment("audio-upload")

    pending_threads[server_location].cancel()
    pending_threads.pop(
        server_location,
    )

    audio = Audio(
        label=label,
        description=description,
        user_id=user.id,
        uid=uid,
        length=get_audio_file_length_in_secs(server_location),
    )
    db.session.add(audio)

    try:
        db.session.commit()
    except IntegrityError as ie:
        flash("Sorry something went wrong")
        print(ie.sqlite_errorname)
        return TemplateRules.render_html_segment("audio-upload")

    audios = db.session.scalars(select(Audio).where(Audio.user_id == user.id)).all()

    flash("Image uploaded successfully 💾")
    return TemplateRules.render_html_segment("left-nav", audios=audios)


@TemplateRules.returns_segement
@login_required
@bp.route("/back")
def return_to_upload_page():
    return TemplateRules.render_html_segment("audio_upload")


def audio_exists_in_db(
    user_id: int,
    title: str,
) -> bool:
    """Returns True is the audio file is recorded in db"""

    return (
        db.session.scalars(
            select(Audio)
            .join(Audio.owner)
            .where(User.id == user_id)
            .where(Audio.label == title)
        ).first()
        is not None
    )


def generate_uid() -> str:
    is_unique = False
    uid = uuid4()
    while not is_unique:
        is_unique = (
            uid is not None
            and db.session.scalars(select(Audio).where(Audio.uid == str(uid))).first()
            is None
        )
        if not is_unique:
            uid = uuid4()

    return str(uid)
