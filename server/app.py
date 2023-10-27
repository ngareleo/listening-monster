from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_traveller():
    return "<p>Hello Traveller</p>"
