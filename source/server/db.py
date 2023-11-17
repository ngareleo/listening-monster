from flask import g


def get_db():
    return g.db
