#!/usr/bin/env python

from flup.server.fcgi import WSGIServer
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from idl import app

app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)

if __name__ == "__main__":
    WSGIServer(app).run()

