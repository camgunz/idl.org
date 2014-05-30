from flask import session

from idl import app
from idl.database import idl_session
from idl.database.models import League, seasons
from idl.views.utils import get_conferences_for_league_and_season, \
                            get_latest_games, render_template, \
                            set_session_defaults

@app.route('/season/standings')
def standings():
    set_session_defaults()
    season = session['season']
    league = session['league']
    conferences = {}
    for conference in get_conferences_for_league_and_season(league, season):
        conferences[conference] = {}
        for division in conference.get_divisions_for_season(season):
            conferences[conference][division] = []
            for team in division.get_current_teams_for_season(season):
                conferences[conference][division].append(team)
    return render_template('standings.mako', **{
        'section': 'season',
        'subsection': 'standings',
        'league': league,
        'seasons': seasons().all(),
        'conferences': conferences,
        'games': get_latest_games()
    })

