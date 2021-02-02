from typing import Union

from flask import Flask, g, request
from flask.helpers import get_env
from flask_assets import Environment
from flask_babel import Babel, lazy_gettext
from flask_login import LoginManager
from flask_moment import Moment

from . import (
    STATIC_PATH, admin, api, auth, cli, config, models, templating, views
)
from .md import markdown
from .tasks import mail
import logging


def create_app(env: Union[str, None] = None) -> Flask:
    env = env or get_env()
    app = Flask(__name__, static_folder=STATIC_PATH)  # type: Flask
    app.config.from_object(config.config_dict[env])
    Moment(app)
    app.logger.setLevel(logging.DEBUG)
    mail.init_app(app)
    babel = Babel(app)
    models.init_app(app)
    cli.init_app(app)
    views.init_app(app)
    if get_env() == "development":
        admin.init_app(app)
    templating.init_app(app)
    api.init_app(app)
    auth.init_app(app)
    Environment(app)

    @babel.localeselector
    def get_locale():
        lang = request.accept_languages.best_match(['zh', 'en'])
        if not lang and 'site' in g:
            lang = g.site['locale']
        if lang == 'zh':
            lang = 'zh_Hans_CN'
        return lang

    login_manager = LoginManager(app)
    login_manager.login_message = lazy_gettext('Please login')
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def get_user(uid):
        return models.User.query.get(uid)

    @app.shell_context_processor
    def shell_context():
        return {'db': models.db, 'Post': models.Post, 'markdown': markdown}

    return app
