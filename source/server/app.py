from flask import Flask, render_template, request
import os


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "app.sqlite")
    )

    from .db import init_app

    init_app(app)

    if test_config is None:
        app.config.from_pyfile(
            "config.py",
        )
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET", "POST"])
    def hello_traveller():
        if request.method == "GET":
            return render_template("index.html")
        return "sent"

    return app
