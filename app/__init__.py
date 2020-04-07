from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

app= Flask(__name__)

app.secret_key = 'musicdbSecretKey'    # You have to use to add a flashed object

app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app,db)

from app.appconfig import AppConfig


# Create a global application configuration object
musicdb_config = AppConfig()

if musicdb_config.getitem("LOGGING") == 'DEBUG':
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)


from app import routes
