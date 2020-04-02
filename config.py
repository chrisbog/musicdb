import os
import logging

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir, 'musicdb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUGAPP=True



