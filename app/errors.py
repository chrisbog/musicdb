from flask import render_template
from app import app, db
import sys,traceback


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):

    output = traceback.format_exc().splitlines()

    db.session.rollback()
    return render_template('500.html',display=output), 500