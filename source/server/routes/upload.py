from threading import Timer
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, flash, render_template, request, url_for, g
from source.server.models import User
from ..utils import TemplateRules, login_required
import os


bp = Blueprint("upload", __name__, url_prefix="/upload")


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

        filename = f"{user.username}_{secure_filename(title)}"
        location = os.path.join("audio", filename)
        if not current_app.static_folder:
            return "Something went wrong back here", 500
        server_location = os.path.join(current_app.static_folder, location)

        if not os.path.exists(server_location):
            # We need to A/B test this
            f.save(server_location)

        # Remove the audio file after a min on a separate thread

        # TODO: Minor, If a user spams the upload, the file will stay here forever
        t = Timer(60.0, delete_file_from_path, (server_location))
        t.start()

        flash("Image uploaded successfully 💾")
        return TemplateRules.render_html_segment(
            "confirm-details",
            component=False,
            location=url_for("static", filename=location),
            title=title,
            descriptiond=description,
        )

    return render_template("upload.html")


@TemplateRules.returns_segement
@login_required
@bp.route("/back")
def return_to_upload_page():
    return TemplateRules.render_html_segment("audio_upload")


def delete_file_from_path(file: str):
    if os.path.exists(file):
        os.remove(file)
    else:
        raise ValueError("File doesn't exist")
