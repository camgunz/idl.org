from flask import request, session

from idl import app
from idl.cache import cache
from idl.database import idl_session
from idl.database.models import LeaguesAndConferences, Team, seasons
from idl.database.stats import get_team_stats_for_league_and_season
from idl.views.utils import get_season_team_stats, render_template, \
                            set_session_defaults

@app.route('/season/leaderboards')
def season_leaders():
    set_session_defaults()
    season = session['season']
    league = session['league']
    return render_template('leaders.mako', **{
        'section': 'season',
        'subsection': 'leaders',
        'seasons': seasons().all(),
        'leaders': season.get_regular_season_leaders(league)
    })

@app.route('/season/stats/players')
def season_player_stats():
    set_session_defaults()
    season = session['season']
    league = session['league']
    key = cache.generate_key('season', 'stats', 'players', season.id, league.id)
    cached_season_player_stats = cache.get(key)
    if cached_season_player_stats:
        stats = cached_season_player_stats
    else:
        stats = season.get_regular_season_stats(league)
        cache.set(key, stats)
    return render_template('player_stats.mako', **{
        'section': 'season',
        'subsection': 'players',
        'seasons': seasons().all(),
        'stats': stats,
        'order_by': request.args.get('order_by', 'player')
    })

@app.route('/season/stats/teams')
def season_team_stats():
    set_session_defaults()
    season = session['season']
    league = session['league']
    key = cache.generate_key('season', 'stats', 'teams', season.id, league.id)
    cached_season_team_stats = cache.get(key)
    if cached_season_team_stats:
        stats = cached_season_team_stats
    else:
        stats = get_season_team_stats(league, season)
        cache.set(key, stats)
    return render_template('team_stats.mako', **{
        'section': 'season',
        'subsection': 'teams',
        'stats': stats,
        'seasons': seasons().all(),
        'order_by': request.args.get('order_by', 'team')
    })

