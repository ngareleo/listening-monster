from flask import Blueprint, render_template
from ..utils import login_required


bp = Blueprint("upload", __name__, url_prefix="/upload")


@login_required
@bp.route("/", methods=("GET", "POST"))
def upload():
    return render_template("upload.html")
