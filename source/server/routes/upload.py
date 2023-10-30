from fileinput import filename
from flask import Blueprint, current_app, flash, render_template, request, url_for
from ..utils import login_required
import os


bp = Blueprint("upload", __name__, url_prefix="/upload")


@login_required
@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        f = request.files["audio"]
        if not current_app.static_folder:
            return "<p>Something went wrong</p>"

        location = f"/audio/{f.filename}"
        f.save(f"{current_app.static_folder}/{location}")
        flash("Image uploaded successfully 💾")
        return render_template(
            "sections/audio.html",
            location=url_for("static", filename=location),
        )
    return render_template("upload.html")
