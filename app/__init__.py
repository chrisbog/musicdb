from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from logging.handlers import RotatingFileHandler

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

app= Flask(__name__)

app.secret_key = 'musicdbSecretKey'    # You have to use to add a flashed object

app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app,db)

from app.appconfig import AppConfig


# Set the Version Number
version = ".9b"

# Create a global application configuration object
musicdb_config = AppConfig()

logging.getLogger()
handler = RotatingFileHandler("musicdb.log",maxBytes=1000000,backupCount=5)
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s-%(funcName)-15s %(levelname)-8s %(message)s', \
                    handlers=[handler,logging.StreamHandler()])
if musicdb_config.getitem("LOGGING") == 'DEBUG':
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)



from app import routes, models, errors
