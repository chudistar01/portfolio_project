import os

from flask import Flask

from . import db, register

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    db.init_app(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flight_application.sqlite'),
    )
    app.register_blueprint(register.user_bp)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    
    return app

