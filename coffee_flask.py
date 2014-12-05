#!/usr/bin/env python
"""Coffee Flask"""

import logging, logging.handlers
import gevent
import json
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from logging.handlers import RotatingFileHandler
from flask import Flask, Response, request, render_template

from sse import ServerSentEvent

FILE_HANDLER = RotatingFileHandler('log/flask.log')
FILE_HANDLER.setLevel(logging.WARNING)

APP = Flask(__name__)
APP.logger.addHandler(FILE_HANDLER)

THIRSTERS = []
SUBSCRIPTIONS = []

class Thirster(object):
    """Person with coffee time window"""
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    @staticmethod
    def add_thirster(form):
        """Add/update a new Thirster to the list"""
        name = form['name']
        start = form['start']
        end = form['end']
        for thirster in THIRSTERS:
            if thirster.name == name:
                THIRSTERS.remove(thirster)
                break
        THIRSTERS.append(Thirster(name, start, end))

    @staticmethod
    def encode_all():
        """Serialise and join every Thirster for transmission"""
        ret = []
        for thirster in THIRSTERS:
            ret.append(thirster.dict())
        ret = json.dumps(ret)
        return ret

    def encode(self):
        """Serialise for sending to js client code"""
        return [json.dumps(self.dict())]

    def dict(self):
        """Get a dictionary representation of this Tirster"""
        ret = {"name": self.name, "start": self.start, "end": self.end}
        return ret

@APP.route("/")
def main():
    """Site main page"""
    return render_template('main.html', thirsters=THIRSTERS)

@APP.route("/thirst", methods=['GET', 'POST'])
def thirst():
    """Indicate waiting for coffee"""
    name = request.args.get('name', '')

    Thirster.add_thirster(request.form)

    def notify():
        """Send out update to all connected clients"""
        msg = Thirster.encode_all()
        for sub in SUBSCRIPTIONS:
            sub.put(msg)
    gevent.spawn(notify)

    return render_template('main.html', name=name)
    # return "<H1>{0:s} Thirsts</H1>".format(name)

@APP.route("/subscribe")
def subscribe():
    """Event streamer"""
    APP.logger.info("New subscriber")
    def gen():
        """Closure around a connected client"""
        queue = Queue()
        SUBSCRIPTIONS.append(queue)
        try:
            while True:
                result = queue.get()
                event = ServerSentEvent(str(result))
                yield event.encode()
        except GeneratorExit: # Or maybe use flask signals
            SUBSCRIPTIONS.remove(queue)

    return Response(gen(), mimetype="text/event-stream")

if __name__ == "__main__":
    APP.debug = True
    # THIRSTERS.append(Thirster("Alice", "3:45", "5:45"))
    # THIRSTERS.append(Thirster("Bob", "4:00", "5:30"))
    # THIRSTERS.append(Thirster("Charlotte", "4:15", "5:15"))
    SERVER = WSGIServer(("", 5000), APP)
    SERVER.serve_forever()
