from __future__ import division

import random

from flask import abort, request, session

from sqlalchemy import or_

from idl import app
from idl.cache import cache
from idl.database import idl_session
from idl.database.models import StoredPlayer
from idl.views.utils import get_games_for_player, get_forum_member, \
                            get_player_profile, render_template, \
                            set_session_defaults

@app.route('/profiles/players')
def random_player_profile():
    player = None
    q = idl_session.query(StoredPlayer)
    if request.is_xhr:
        if 'player_name' not in request.args:
            abort(400)
        search_string = request.args['player_name'].join(('%', '%'))
        players = q.filter(StoredPlayer.name.ilike(search_string)).all()
        return render_template(
            'player_profile_search_results.mako', players=players
        )
    if 'username' in session:
        player = q.get(session['username'])
    if player is None or 'username' not in session:
        while True:
            player = q[random.randrange(0, q.count())]
            if player.rounds:
                break
    return render_player_profile(player)

@app.route('/profiles/players/<player_name>')
def player_profile(player_name):
    if request.is_xhr:
        profile_only = True
    else:
        profile_only = False
    player = idl_session.query(StoredPlayer).get(player_name)
    if not player:
        forum_member = get_forum_member(player_name)
        if forum_member:
            player = forum_member.player
    if not player:
        abort(404)
    return render_player_profile(player, profile_only)

def render_player_profile(player, profile_only=False):
    set_session_defaults()
    if not profile_only and 'username' in session:
        p = idl_session.query(StoredPlayer).get(session['username'])
        games = get_games_for_player(p)
    else:
        games = []
    if profile_only:
        template = 'player_profile.mako'
    else:
        template = 'player_profiles.mako'
    key = cache.generate_key('profiles', 'players', player.name)
    profile = cache.get(key)
    if not profile:
        profile = get_player_profile(player)
        cache.set(key, profile)
    return render_template(template, **{
        'section': 'profiles',
        'subsection': 'players',
        'player': player,
        'profile': profile,
        'games': games,
    })

