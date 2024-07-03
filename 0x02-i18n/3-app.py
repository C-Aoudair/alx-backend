#!/usr/bin/env python3
""" a simple flask app"""

from flask import Flask, render_template
from flask_babel import Babel, gettext as _

app = Flask(__name__)


class Config:
    """ Config Class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determines the best match with our supported languages"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index():
    """return index.html page"""
    return render_template(
        '3-index.html',
        home_title=_("home_title"),
        home_header=_("home_header")
    )


if __name__ == '__main__':
    app.run()
