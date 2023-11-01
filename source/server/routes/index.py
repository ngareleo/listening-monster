from flask import Blueprint, render_template, request


bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/", methods=("GET", "POST"))
def hello_traveller():
    if request.method == "GET":
        return render_template("pages/index.html")
    return "sent"
