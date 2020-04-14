from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging


app= Flask(__name__)

app.secret_key = 'musicdbSecretKey'    # You have to use to add a flashed object

app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app,db)

#from app.appconfig import AppConfig



from app import routes, models, errors




