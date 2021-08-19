import os

from flask import Flask
from flask_session import Session


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='p7S^qJFf!kj*bH$5xP2rmJk@aJd8F46rzsKqf$k9ooofe6r72^b2yyX8T648QZ*qv5dJSif6kKCZ8AsR*DFPs9gUV^bfSXUNV&Ub^hZcYR3V^UckYuHQMBGCGWs2RGD',
        DATABASE=os.path.join(app.root_path, 'cloudchat.db'),
    )

    app.config['TEMPLATES_AUTO_RELOAD'] = True


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    return app