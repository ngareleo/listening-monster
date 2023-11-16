from flask import Blueprint, render_template, request, g


bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/", methods=("GET", "POST"))
def hello_traveller():
    if request.method == "GET":
        if g.user:
            return render_template("pages/index.html")
        return render_template("pages/auth.html", login=True)
    return "sent"
