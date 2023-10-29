from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = (
        get_db().execute("SELECT * FROM user WHERE id = ?", (user_id)).fetchone()
        if user_id
        else None
    )


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        error = None

        username = request.form["username"]
        password = request.form["password"]
        db = get_db()

        if not username:
            error = "Username is required"

        elif not password:
            error = "Password is required"

        if not error:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already taken"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        error = None
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()

        if not username:
            error = "Username is required"

        elif not password:
            error = "Password is required"

        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username)
        ).fetchone()

        if not user:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
