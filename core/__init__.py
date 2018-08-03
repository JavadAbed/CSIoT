import core.config
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

# flask object
app = Flask(__name__, static_url_path="/static")

# configs
app.config.update(
    SESSION_COOKIE_PATH=core.config.session_cookie_path,
    SESSION_COOKIE_NAME=core.config.session_cookie_name,
    SERVER_NAME=core.config.server_name,
    SECRET_KEY=core.config.secret_key,
    SQLALCHEMY_DATABASE_URI=core.config.sqlalchemy_database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

# db
db = SQLAlchemy(app) 

# logging
logger = app.logger
handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

import core.routers
