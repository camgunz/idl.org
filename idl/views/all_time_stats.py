from flask import request, session

from idl import app
from idl.database import idl_session
from idl.database.models import seasons, GamesAndRounds
from idl.database.stats import get_base_player_stats
from idl.views.utils import get_latest_games, render_template, \
                            set_session_defaults

@app.route('/profiles/stats/players')
def all_time_player_stats():
    set_session_defaults()
    round_ids = [
        gar.round.id for gar in idl_session.query(GamesAndRounds).all()
    ]
    return render_template('all_time_player_stats.mako', **{
        'section': 'profiles',
        'subsection': 'player stats',
        'stats': get_base_player_stats(round_ids),
        'order_by': request.args.get('order_by', 'player'),
        'games': get_latest_games()
    })

