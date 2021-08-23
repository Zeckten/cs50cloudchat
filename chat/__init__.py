import os

from flask import Flask
from flask_session import Session


def create_app():
    # create and configure the app
    appl = Flask(__name__)
    appl.config.from_mapping(
        SECRET_KEY='p7S^qJFf!kj*bH$5xP2rmJk@aJd8F46rzsKqf$k9ooofe6r72^b2yyX8T648QZ*qv5dJSif6kKCZ8AsR*DFPs9gUV^bfSXUNV&Ub^hZcYR3V^UckYuHQMBGCGWs2RGD',
        DATABASE=os.path.join(appl.root_path, 'cloudchat.db'),
    )

    appl.config['TEMPLATES_AUTO_RELOAD'] = True


    # a simple page that says hello
    @appl.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(appl)

    from . import auth
    appl.register_blueprint(auth.bp)

    from . import app
    appl.register_blueprint(app.bp)
    appl.add_url_rule('/', endpoint='index')

    return appl