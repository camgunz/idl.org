import os
import sys
import decimal

decimal.prec = 4
decimal.setcontext(decimal.ExtendedContext)

major, minor, point, bloo, blah = sys.version_info
if major != 2:
    raise Exception('You need Python version 2, not version 1, not version 3')
if minor < 5:
    raise Exception('You need at least Python 2.5')
if minor == 5:
    import simplejson as json
else:
    import json

from flask import Flask, g
from flaskext.mako import init_mako

app = Flask(__name__)
app.config.from_object('idl.config')
init_mako(app)

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    h = TimedRotatingFileHandler(
        os.path.join(app.config['HOME'], 'site.log'),
        when='midnight',
        backupCount=4
    )
    h.setLevel(logging.WARNING)
    app.logger.addHandler(h)

import ZDStack
ZDStack.set_configfile(os.path.join(app.config['HOME'], 'idl', 'zdstack.ini'))

import idl.cache
idl.cache.init()

import idl.database
import idl.views

from idl.database import idl_db_engine, idl_metadata
idl_metadata.create_all(idl_db_engine)

@app.before_request
def before_request():
    g.cache_connection = idl.cache.cache.get_connection()

@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, 'cache_connection'):
        g.cache_connection.close()
    idl.database.idl_session.remove()
    idl.database.forum_session.remove()

