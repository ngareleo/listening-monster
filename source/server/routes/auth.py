from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    request,
    session,
    url_for,
)
from sqlalchemy import select
from source.server.models import User
from source.server.utils import TemplateRules
from ..db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")
db = get_db()


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    user = db.session.scalars(select(User).where(User.id == user_id)).first()
    g.user = user


@TemplateRules.returns_page
@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        confirm_password = request.form["confirm-password"]
        passwords_identical = password == confirm_password

        if not passwords_identical:
            flash("Passwords do not match")

        if not username:
            flash("Username is required")
        elif not password:
            flash("Password is required")
        elif not email:
            flash("Email is required")

        if passwords_identical and username and password and email:
            try:
                user = User(username=username, password=password, email=email)
                db.session.add(user)
                db.session.commit()

            except db.IntegrityError:
                flash(f"User {username} is already taken")
            else:
                return redirect(url_for("auth.login"))

    return TemplateRules.render_html_page("auth.html", login=False)


@TemplateRules.returns_page
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username:
            flash("Username is required")

        elif not password:
            flash("Password is required")

        user = None
        try:
            user = db.session.scalars(
                select(User).where(User.username == username)
            ).first()
        except Exception as e:
            print(e)
        if not user:
            flash("Incorrect username")
        elif not user.verify_password(password):
            flash("Incorrect password")
        else:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index.hello_traveller"))

    return TemplateRules.render_html_page("auth.html", login=True)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
