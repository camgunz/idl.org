from flask import abort, jsonify, request, session

from idl import app
from idl.database import idl_session
from idl.database.models import Administrator, contributors, seasons
from idl.database.models import Season, Server
from idl.views.utils import get_latest_games, get_latest_season, \
                            render_template

@app.route('/info/season_wad')
def season_wad():
    if request.headers.get('accept', 'text/html') == 'application/json':
        return jsonify(wad=get_latest_season().wad)
    else:
        abort(404)

@app.route('/info/history')
def history():
    return render_template('history.mako', **{
        'section': 'info',
        'subsection': 'history',
        'games': get_latest_games()
    })

@app.route('/info/rules')
def rules():
    return render_template('rules.mako', **{
        'section': 'info',
        'subsection': 'rules',
        'games': get_latest_games()
    })

@app.route('/info/administrators')
def administrators():
    admins = idl_session.query(Administrator).filter_by(date_left=None).all()
    return render_template('administrators.mako', **{
        'section': 'info',
        'subsection': 'administrators',
        'administrators': admins,
        'games': get_latest_games()
    })

@app.route('/info/servers')
def servers():
    if request.headers.get('accept', 'text/html') == 'application/json':
        all_servers = idl_session.query(Server).all()
        return jsonify(servers=dict([(server.name, {
            'address': server.address, 'password': server.password
        }) for server in all_servers]))
    else:
        q = idl_session.query(Server)
        q = q.order_by(Server.name, Server.address)
        return render_template('servers.mako', **{
            'section': 'info',
            'subsection': 'servers',
            'servers': q.all(),
            'games': get_latest_games()
        })

@app.route('/info/credits')
def credits():
    return render_template('credits.mako', **{
        'section': 'info',
        'subsection': 'credits',
        'contributors': contributors().all(),
        'games': get_latest_games()
    })

