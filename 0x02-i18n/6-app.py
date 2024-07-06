#!/usr/bin/env python3
""" a simple flask app with i18n"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _

app = Flask(__name__)


class Config:
    """Config Class"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.before_request
def get_user():
    """get a user"""
    login_as = request.args.get("login_as")
    if login_as:
        user = users.get(int(login_as))
        if user:
            g.user = user


@babel.localeselector
def get_locale():
    """Determines the best match with our supported languages"""
    locale = request.args.get("locale", None)
    if locale and locale in app.config["LANGUAGES"]:
        return locale

    user = getattr(g, 'user', None)
    if user is not None:
        locale = user.get("locale")
        if locale and locale in app.config["LANGUAGES"]:
            return locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/", strict_slashes=False)
def index():
    """return index.html page"""
    user = getattr(g, "user", None)
    username = user["name"] if user else None
    return render_template(
            "6-index.html", get_locale=get_locale, username=username
            )


if __name__ == "__main__":
    app.run()
