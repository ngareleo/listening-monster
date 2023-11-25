from cProfile import label
import os
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
file_managing_thread = Timer(60.0 * 20, delete_file_from_path)  # needs to attain a lock


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
        if not f:
            flash("Audio file is required")

        if not title or not description or not f:
            return TemplateRules.render_html_segment("audio/audio-upload")

        is_title_used = audio_exists_in_db()

        if is_title_used:
            flash("Label provided has been used before")
            return TemplateRules.render_html_segment(
                "audio/audio-upload"
            )  # TODO: Add value details to render with pre-filled data

        filename = generate_uid()
        if not current_app.static_folder:
            return "Something went wrong back here", 500

        server_location = os.path.join(current_app.static_folder, "audio", filename)
        if not os.path.exists(server_location):
            # TODO: We need to A/B test this
            f.save(server_location)

            # Remove the audio file after 5 min on a separate thread
            file_managing_thread.args = server_location
            file_managing_thread.start()

        session["upload"] = {"id": filename, "label": label, "description": description}
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
    from source.engine import get_audio_file_length_in_ms

    if not request.method == "POST":
        return "Bad request", 400

    upload = session.get("upload")

    if not upload:
        return TemplateRules.render_html_segment("audio-upload")

    user: User = g.user
    title = upload.get("title")
    description = upload.get("description")
    uid = upload.get("id")

    server_location = os.path.join(
        str(current_app.static_folder),  # guranteed this None check will pass in prod
        "audio",
        uid,
    )

    if os.path.exists(server_location):
        # The countdown has not finished
        file_managing_thread.cancel()

    audio = Audio()
    audio.label = title
    audio.description = description
    audio.user_id = user.id
    audio.length = get_audio_file_length_in_ms(server_location) / (1000 * 60)

    db.session.add(audio)
    db.session.commit()

    flash("Image uploaded successfully 💾")
    return TemplateRules.render_html_segment("left-nav")


@TemplateRules.returns_segement
@login_required
@bp.route("/back")
def return_to_upload_page():
    return TemplateRules.render_html_segment("audio_upload")


def audio_exists_in_db(
    title: str,
) -> bool: 
    """Returns True is the audio file is recorded in db"""
    return db.session.scalars(select(Audio).where(Audio.label == title)) is not None


def generate_uid() -> str:
    is_unique = False
    uid = uuid4()
    while not is_unique:
        is_unique = (
            uid is not None
            and db.session.scalars(
                select(Audio).where(Audio.uid == str(uid.bytes))
            ).first()
            is None
        )
        if not is_unique:
            uid = uuid4()

    return str(uid.bytes)
