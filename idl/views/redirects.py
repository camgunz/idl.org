from flask import abort, redirect, url_for

from idl import app

@app.route('/favicon.ico')
def favicon():
    return redirect('/'.join((app.config['STATIC_URL'], 'favicon.ico')))

@app.route('/info/forums')
def forums():
    forums_url = app.config.get('FORUMS_URL')
    if forums_url:
        return redirect(forums_url)
    else:
        abort(404)

@app.route('/info/wiki')
def wiki():
    wiki_url = app.config.get('WIKI_URL')
    if wiki_url:
        return redirect(wiki_url)
    else:
        abort(404)

###
# [CG] In order to maintain old URL compatibility (for the URLs anyone cares
#      about) these redirects are necessary.  I think it's best to put them
#      here instead of the webserver config so they can't be accidentally
#      forgotten or misconfigured.
###

@app.route('/demos')
def redirect_demos():
    return redirect(url_for('demos'))

@app.route('/standings')
def redirect_standings():
    return redirect(url_for('standings'))

@app.route('/schedule')
def redirect_schedule():
    return redirect(url_for('schedule'))

@app.route('/playoffs')
def redirect_playoffs():
    return redirect(url_for('playoffs'))

@app.route('/stats/games/<int:game_id>')
def redirect_stats(game_id):
    return redirect(url_for('game_results', game_id=game_id))

@app.route('/rules')
def redirect_rules():
    return redirect(url_for('rules'))

@app.route('/maps')
def redirect_map_profiles():
    return redirect(url_for('map_profiles'))

@app.route('/maps/<wad_name>')
def redirect_wads(wad_name):
    return redirect(url_for('wads', wad_name=wad_name))

@app.route('/maps/<wad_name>/<int:map_number>')
def redirect_map(wad_name, map_number):
    return redirect(url_for('maps', wad_name=wad_name, map_number=map_number))

