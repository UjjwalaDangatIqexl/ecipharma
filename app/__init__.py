from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from utils.config_utils import Config
import os

mongo = PyMongo()
mail = Mail()


def ensure_temp_directory():
    if not os.path.exists('temp'):
        os.makedirs('temp')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    global mongo

    mongo.init_app(app)
    app.config['mongo'] = mongo
    ensure_temp_directory()

    mail.init_app(app)

    # Register blueprints here
    from .controllers.auth_controller import auth_bp
    from .controllers.document_controller import document_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)

    return app

