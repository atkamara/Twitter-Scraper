# -*- coding: latin-1 -*-
"""Initialize app."""
from flask import Flask
import os

def create_app():
    app                            = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    SECRET_KEY                     = os.urandom(32)
    app.config['SECRET_KEY']       = SECRET_KEY

    DEFAULT_FOLDER                 = os.path.join(app.instance_path[:-9],'app','static','data','json_default')

    app.config['DEFAULT_FOLDER']   = DEFAULT_FOLDER

    with app.app_context():
        from . import routes

        return app