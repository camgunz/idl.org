from flask import request, session

from flaskext.mako import render_template as render_mako_template

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from idl import app
from idl.database import forum_session, idl_session
from idl.database.stats import get_team_stats_for_league_and_season
from idl.database.models import ConferencesAndDivisions, DivisionsAndTeams, \
                                GamesAndRounds, League, \
                                LeaguesAndConferences, Season, Game, Round, \
                                ForumMember

def get_forum_member(username):
    q = forum_session.query(ForumMember)
    q = q.filter('UPPER(member_name) = UPPER(:username)')
    q = q.params(username=username)
    try:
        return q.one()
    except (NoResultFound, MultipleResultsFound):
        return None

def get_latest_season():
    q = idl_session.query(Season)
    return q.order_by(Season.year.desc(), Season.season).first()

def get_latest_games():
    idl = idl_session.query(League).filter(League.short_name=='IDL').one()
    games = idl_session.query(Game)
    games = games.filter(Game.has_been_played==True)
    games = games.filter(Game.league==idl)
    games = games.filter(Game.scheduled_for != None)
    games = games.filter(Game.forfeiting_team==None)
    games = games.order_by(Game.scheduled_for.desc())
    return games.limit(6).all()

def get_games_for_player(player):
    return idl_session.query(Game).filter(and_(
        Game.rounds.any(Round.id.in_([r.id for r in player.rounds])),
        Game.season_id==session['season'].id,
        Game.has_been_played==True
    )).order_by(Game.week_id.desc()).all()

def get_latest_games_for_player(player):
    return idl_session.query(Game).filter(and_(
        Game.rounds.any(Round.id.in_([r.id for r in player.rounds])),
        Game.season_id==get_latest_season().id,
        Game.has_been_played==True
    )).order_by(Game.week_id.desc()).all()

def get_conferences_for_league_and_season(league, season):
    q = idl_session.query(LeaguesAndConferences)
    q = q.filter(and_(
        LeaguesAndConferences.league==league,
        LeaguesAndConferences.season==season,
    ))
    return [cad.conference for cad in q.all()]

def get_teams_for_league_and_season(league, season):
    teams = []
    for conference in get_conferences_for_league_and_season(league, season):
        for division in conference.get_divisions_for_season(season):
            for team in division.get_current_teams_for_season(season):
                teams.append(team)
    return teams

def set_session_defaults():
    if 'season' in request.args:
        try:
            season = idl_session.query(Season).get(request.args['season'])
        except (NoResultFound, MultipleResultsFound), e:
            season = get_latest_season()
    elif 'season_id' in session:
        try:
            season = idl_session.query(Season).get(session['season_id'])
        except (NoResultFound, MultipleResultsFound), e:
            season = get_latest_season()
    else:
        season = get_latest_season()
    idl = idl_session.query(League).filter(League.short_name=='IDL').one()
    session['season'] = season
    session['season_id'] = season.id
    session['league'] = idl

def get_season_team_stats(season, league):
    teams = get_teams_for_league_and_season(league, season)
    return get_team_stats_for_league_and_season(teams, league, season)

def get_player_profile(player):
    seen_rounds = set()
    seen_games = set()
    game_count = wins = losses = ties = 0
    frags = deaths = flag_touches = flag_captures = flag_returns = 0
    aliases = player.aliases
    for round in player.rounds:
        seen_rounds.add(round.id)
        for frag in round.frags:
            if frag.fraggee in aliases:
                deaths += 1
            elif frag.fragger in aliases and frag.fragger_id != frag.fraggee_id:
                frags += 1
        for flag_touch in round.flag_touches:
            if flag_touch.alias in aliases:
                flag_touches += 1
                if flag_touch.resulted_in_score:
                    flag_captures += 1
        for flag_return in round.flag_returns:
            if flag_return.alias in aliases:
                flag_returns += 1
    q = idl_session.query(GamesAndRounds)
    for gnr in q.filter(GamesAndRounds.round_id.in_(seen_rounds)).all():
        game = gnr.game
        if game.id in seen_games:
            continue
        seen_games.add(game.id)
        team_one = game.team_one
        team_two = game.team_two
        team_one_players = game.get_players_for_team(team_one)
        team_two_players = game.get_players_for_team(team_two)
        winner = game.winner
        if player not in team_one_players and player not in team_two_players:
            continue
        game_count += 1
        if not winner:
            ties += 1
        elif winner == team_one and player in team_one_players:
            wins += 1
        elif winner == team_two and player in team_two_players:
            wins += 1
        else:
            losses += 1
    return {
        'round_count': len(seen_rounds),
        'game_count': game_count,
        'win_count': wins,
        'loss_count': losses,
        'tie_count': ties,
        'record': '-'.join([str(x) for x in (wins, losses, ties)]),
        'pct': game_count and '%.3f' % ((wins + (ties / 2)) / game_count) or 0,
        'frags': frags,
        'deaths': deaths,
        'flag_touches': flag_touches,
        'flag_captures': flag_captures,
        'flag_returns': flag_returns
    }

def render_template(path, **kwargs):
    kwargs['config'] = app.config
    return render_mako_template(path, **kwargs)

