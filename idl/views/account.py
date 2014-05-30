from flask import abort, redirect, request, session, url_for

from idl import app
from idl.database import idl_session

from idl.views.utils import get_latest_games_for_player, get_forum_member, \
                            render_template

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    forum_member = get_forum_member(username)
    if forum_member is None:
        print "No forum member named %s" % (username)
        abort(401)
    if password != app.config['ADMIN_PASSWORD'] and not \
       forum_member.authenticate(password):
        abort(401)
    player = forum_member.player
    session['username'] = player.name
    if player.name in app.config['ADMINS']:
        session['is_admin'] = True
    else:
        session['is_admin'] = False
    session.permanent = True
    games = get_latest_games_for_player(player)
    return render_template('account_box.mako', games=games)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('random_player_profile'))

