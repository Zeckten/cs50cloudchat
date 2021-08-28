import os

from flask import Flask
from flask_session import Session


def create_app():
    # create and configure the app
    appl = Flask(__name__)
    appl.config.from_mapping(
        SECRET_KEY = os.environ.get("SECRET_KEY"),
        TEMPLATES_AUTO_RELOAD = True,
        DATABASE = os.path.join(appl.root_path, 'cloudchat.db'),
    )


    from . import db
    db.init_app(appl)

    from . import auth
    appl.register_blueprint(auth.bp)

    from . import app
    appl.register_blueprint(app.bp)
    appl.add_url_rule('/', endpoint='index')

    return appl