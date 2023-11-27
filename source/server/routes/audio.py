from flask import Blueprint, flash, g, request
from sqlalchemy import select
from source.server.db import get_db
from source.server.models import Audio, User
from source.server.utils import TemplateRules, login_required

bp = Blueprint("audio", __name__, url_prefix="/audio")
db = get_db()


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
        return TemplateRules.render_html_segment("right-nav.html"), 500

    return TemplateRules.render_html_segment("right-nav.html", audio=audio)
