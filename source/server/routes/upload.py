from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, flash, render_template, request, url_for, g
from source.server.models import Audio, User
from ..utils import TemplateRules, login_required


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
        audio = Audio()
        audio.label = title
        audio
        filename = f"{user.username}_{secure_filename(title)}"
        location = f"/audio/{filename}"
        f.save(f"{current_app.static_folder}/{location}")
        flash("Image uploaded successfully 💾")

        return TemplateRules.render_html_segment(
            "confirm-details", location=url_for("static", filename=location)
        )

    return render_template("upload.html")
