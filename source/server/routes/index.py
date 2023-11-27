from flask import Blueprint, request, g
from sqlalchemy import select
from source.server.db import get_db
from source.server.models import Audio, Transcription, User
from source.server.utils import TemplateRules


bp = Blueprint("index", __name__, url_prefix="/")
db = get_db()


@TemplateRules.returns_page
@bp.route("/", methods=("GET", "POST"))
def hello_traveller():
    if request.method == "GET":
        user: User = g.user  # for type hints
        if user:
            all_audios = user.audios
            audio = None
            transcriptions = None
            if len(all_audios) > 0:
                audio = all_audios[0]
                transcriptions = audio.transcriptions
            return TemplateRules.render_html_page(
                "index",
                audios=all_audios,
                audio=audio,
                transcriptions=transcriptions,
            )
        return TemplateRules.render_html_page("auth", login=True)
    return "sent"
