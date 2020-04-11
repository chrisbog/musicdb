import os
import logging

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir, 'musicdb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    logging.basicConfig(level=logging.INFO,format='%(asctime)-15s-%(funcName)-15s %(levelname)-8s %(message)s')

#from app.models import Configuration


