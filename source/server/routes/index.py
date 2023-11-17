from flask import Blueprint, render_template, request, g

from source.server.utils import TemplateRules


bp = Blueprint("index", __name__, url_prefix="/")


@TemplateRules.returns_page
@bp.route("/", methods=("GET", "POST"))
def hello_traveller():
    if request.method == "GET":
        if g.user:
            return TemplateRules.render_html_page("index")
        return TemplateRules.render_html_page("auth", login=True)
    return "sent"
