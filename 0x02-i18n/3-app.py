#!/usr/bin/env python3
""" a simple flask app with i18n"""

from flask import Flask, render_template, request
from flask_babel import Babel, gettext as _


class Config:
    """ Config Class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Determines the best match with our supported languages
    Returns:
        stre: best match
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index():
    """render index.html page
    Returns:
        html tmeplate 3-index.html
    """
    return render_template('3-index.html', get_locale=get_locale)


if __name__ == '__main__':
    app.run()
