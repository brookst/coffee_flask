#!/usr/bin/env python
"""Coffee Flask"""

import logging, logging.handlers
from logging.handlers import RotatingFileHandler
from flask import Flask, request, render_template

FILE_HANDLER = RotatingFileHandler('log/flask.log')
FILE_HANDLER.setLevel(logging.WARNING)

APP = Flask(__name__)
APP.logger.addHandler(FILE_HANDLER)

@APP.route("/")
def main():
    """Site main page"""
    return render_template('main.html')

@APP.route("/thirst")
def thirst():
    """Indicate waiting for coffee"""
    name = request.args.get('name', '')
    return render_template('main.html', name=name)
    # return "<H1>{0:s} Thirsts</H1>".format(name)

if __name__ == "__main__":
    APP.debug = True
    APP.run()
