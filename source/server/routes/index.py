from flask import Blueprint, request, g
from sqlalchemy import select
from source.server.db import get_db
from source.server.models import Audio, User

from source.server.utils import TemplateRules


bp = Blueprint("index", __name__, url_prefix="/")
db = get_db()


@TemplateRules.returns_page
@bp.route("/", methods=("GET", "POST"))
def hello_traveller():
    if request.method == "GET":
        user: User = g.user  # for type hints
        if user:
            user_audio = db.session.scalars(
                select(Audio)
                .where(Audio.user_id == user.id)
                .order_by(Audio._last_modified)
            ).all()
            return TemplateRules.render_html_page("index", audios=user_audio)
        return TemplateRules.render_html_page("auth", login=True)
    return "sent"
