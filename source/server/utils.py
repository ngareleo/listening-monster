import functools
from flask import g, redirect, render_template, url_for


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


class TemplateRules:
    @classmethod
    def render_html_segment(cls, loc: str, component=True, **kwargs) -> str:
        if loc.startswith("/"):
            loc = loc[1:]
        if loc.endswith(".html"):
            loc = loc[:-5]
        return render_template(
            f"components/{loc}.html" if component else f"sections/{loc}.html", **kwargs
        )

    @classmethod
    def render_html_page(cls, loc: str, **kwargs) -> str:
        if loc.startswith("/"):
            loc = loc[1:]
        if loc.endswith(".html"):
            loc = loc[:-5]
        return render_template(f"pages/{loc}.html", **kwargs)

    @classmethod
    def returns_segement(cls, func):
        """Just for clarity that this route is used by htmx and returns HTMLSegments"""
        return func

    @classmethod
    def returns_page(cls, func):
        """Just for clarity that this route returns entire HTML pages"""
        return func
