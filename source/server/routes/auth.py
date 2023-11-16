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
        get_db().execute("SELECT * FROM user WHERE id = ?",
                         [int(user_id)]).fetchone()  # guranteed this will never fail
        if user_id
        else None
    )


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]
        passwords_identical = password == confirm_password

        if not passwords_identical:
            flash("Passwords do not match")

        if not username:
            flash("Username is required")

        elif not password:
            flash("Password is required")

        if passwords_identical and username and password:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                flash(f"User {username} is already taken")
            else:
                return redirect(url_for("auth.login"))

    return render_template("pages/auth.html", login=False)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username:
            flash("Username is required")

        elif not password:
            flash("Password is required")

        db = get_db()
        user = None
        try:
            user = db.execute(
                "SELECT * FROM user WHERE username = ?", [username]
            ).fetchone()
        except Exception as e:
            print(e)
        if not user:
            flash("Incorrect username")
        elif not check_password_hash(user["password"], password):
            flash("Incorrect password")
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index.hello_traveller"))

    return render_template("pages/auth.html", login=True)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
