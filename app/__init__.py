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

from app.utils import load_config_option

value = load_config_option("LOGGING")
print (f"{value}")

if value == "DEBUG":
    print("Setting Value to DEBUG")
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)-15s-%(funcName)-15s %(levelname)-8s %(message)s')
else:
    print("setting Value to INFO")
    logging.basicConfig(level=logging.INFO,format='%(asctime)-15s-%(funcName)-15s %(levelname)-8s %(message)s')


from app import routes
