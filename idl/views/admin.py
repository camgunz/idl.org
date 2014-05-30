import re
import decimal
import datetime
import operator
import traceback

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from ZDStack.LogEvent import LogEvent
from ZDStack.ZDSEventHandler import ManualEventHandler

from flask import abort, redirect, request, Response, session, url_for

from idl import app, json
from idl.cache import cache
from idl.database import idl_session, models
from idl.views.utils import get_player_profile, get_season_team_stats, \
                            render_template, set_session_defaults

LAYOUT = [
    (u'IDL Organization', [
        models.Alias,
        models.League,
        models.LeaguesAndConferences,
        models.Conference,
        models.ConferencesAndDivisions,
        models.Division,
        models.DivisionsAndTeams,
        models.Team,
        models.TeamsAndPlayers,
        models.StoredPlayer,
        models.ForumMembersAndPlayers
    ]),
    (u'IDL Season', [
        models.Season,
        models.SeasonsAndWeeks,
        models.LeaguesAndSeasons,
        models.Week,
        models.Game,
        models.GamesAndRounds,
        models.Round,
        models.Demo
    ]),
    (u'IDL Infrastructure', [
        models.Administrator,
        models.Map,
        models.Wad,
        models.MapScreenShot,
        models.Quote,
        models.Contributor,
        models.Server
    ])
]

MODELS = [
    models.Administrator,
    models.Alias,
    models.Conference,
    models.ConferencesAndDivisions,
    models.Contributor,
    models.Demo,
    models.DivisionsAndTeams,
    models.Division,
    models.ForumMembersAndPlayers,
    models.GamesAndRounds,
    models.Game,
    models.League,
    models.LeaguesAndSeasons,
    models.LeaguesAndConferences,
    models.Map,
    models.MapScreenShot,
    models.Quote,
    models.Round,
    models.StoredPlayer,
    models.Season,
    models.SeasonsAndWeeks,
    models.Server,
    models.Team,
    models.TeamsAndPlayers,
    models.Wad,
    models.Week
]

MODULES = [x.Admin.label for x in MODELS]

MODULES_TO_MODELS = dict(zip(MODULES, MODELS))

MODELS_TO_MODULES = dict(zip(MODELS, MODULES))

def admin_context(requires_module=False, requires_entry=False):
    set_session_defaults()
    d = {}
    params = {}
    d['LAYOUT'] = LAYOUT
    d['modules_to_models'] = MODULES_TO_MODELS.copy()
    params.update(request.args.to_dict())
    params.update(request.form.to_dict())
    if requires_entry and not requires_module:
        raise ValueError("Entries require a module")
    if not session.get('username', None) or not session.get('is_admin', None):
        abort(401)
    if requires_module and not 'module' in params:
        abort(404)
    if requires_entry and not 'entry' in params:
        abort(404)
    elif requires_module and not params['module'] in MODULES:
        if params['module'] != 'Game Log':
            raise Exception(u'Invalid Section: %s' % (params['module']))
    if requires_module:
        d['module'] = params['module']
        if d['module'] == 'Game Log':
            d['model'] = MODULES_TO_MODELS['Game']
        else:
            d['model'] = MODULES_TO_MODELS[d['module']]
    d['admin_entry'] = None
    if requires_entry:
        d['entry_id'] = params['entry']
        d['admin_entry'] = d['model'].Admin.get_entry(d['entry_id'])
    d['section'] = 'admin'
    d['subsection'] = 'admin'
    return d

@app.route('/admin')
def admin():
    return render_template('admin.mako', **admin_context())

@app.route('/admin/list')
def admin_list():
    try:
        d = admin_context(requires_module=True)
        d['admin_entries'] = d['model'].Admin.choices
        if d['module'] == 'Game Log':
            return render_template('admin_list_games.mako', **d)
        else:
            return render_template('admin_list.mako', **d)
    except Exception, e:
        return render_template('admin_error.mako', **{
            'section': 'admin',
            'subsection': 'admin',
            'error': str(e)
        })

@app.route('/admin/get')
def admin_get():
    try:
        d = admin_context(requires_module=True, requires_entry=True)
        if d['module'] == 'Demos':
            raise Exception(u'Modifying demos is disabled')
    except Exception, e:
        return render_template('admin_error.mako', **{
            'section': 'admin',
            'subsection': 'admin',
            'error': str(e)
        })
    if d['admin_entry'] is None:
        d['entry_id'] = None
        return redirect(url_for('admin_new'))
    return render_template('admin_view.mako', **d)

@app.route('/admin/set', methods=['POST'])
def admin_set():
    try:
        d = admin_context(requires_module=True, requires_entry=True)
        if d['module'] == 'Demos':
            raise Exception(u'Modifying demos is disabled')
    except Exception, e:
        return render_template('admin_error.mako', **{
            'section': 'admin',
            'subsection': 'admin',
            'error': str(e)
        })
    new_values = dict([
        x for x in request.form.to_dict().items() if x[0].startswith('new')
    ])
    d['admin_entry'].Admin.set_values(
        d['admin_entry'].Admin.get_id(d['admin_entry']),
        new_values
    )
    return render_template('admin_view.mako', **d)

@app.route('/admin/delete', methods=['POST'])
def admin_delete():
    try:
        d = admin_context(requires_module=True, requires_entry=True)
        if d['module'] == 'Demos':
            raise Exception(u'Modifying demos is disabled')
    except Exception, e:
        return render_template('admin_error.mako', **{
            'section': 'admin',
            'subsection': 'admin',
            'error': str(e)
        })
    m = d['admin_entry']
    m.Admin.delete_entry(m)
    d['admin_entry'] = None
    d['entry_id'] = None

@app.route('/admin/new', methods=['GET', 'POST'])
def admin_new():
    try:
        d = admin_context(requires_module=True)
    except Exception, e:
        return render_template('admin_error.mako', **{
            'section': 'admin',
            'subsection': 'admin',
            'error': str(e)
        })
    if request.method == 'POST':
        ###
        # [CG] A new entry has been posted, so the context has to be built up
        #      from the user-submitted values.
        ###
        new_values = dict([
            x for x in request.form.to_dict().items() if x[0].startswith('new')
        ])
        model_collection = MODULES_TO_MODELS[d['module']]()
        try:
            m = model_collection.Admin.new_entry(new_values)
        except IntegrityError, e:
            return render_template('admin_error.mako', **{
                'section': 'admin',
                'subsection': 'admin',
                'error': '%s already exists (%s)' % (d['module'], e)
            })
        d['entry_id'] = m.Admin.get_id(m)
        d['admin_entry'] = m.Admin.get_entry(d['entry_id'])
    ###
    # [CG] For POST requests this renders the newly-created entry.  For GET
    #      requests this renders a blank entry form.
    ###
    return render_template('admin_view.mako', **d)

@app.route('/admin/calendar')
def calendar():
    d = admin_context()
    if not 'timestamp' in request.args:
        abort(400)
    try:
        d['dt'] = datetime.datetime.strptime(
            request.args['timestamp'],
            '%Y-%m-%d %H:%M:%S'
        )
    except:
        abort(400)
    d['eid'] = request.args.get('eid', None)
    d['mclass'] = request.args.get('mclass', None)
    d['eclass'] = request.args.get('eclass', None)
    d['deid'] = request.args.get('deid', None)
    if request.args.get('hidden', False) == 'true':
        d['hidden'] = True
    else:
        d['hidden'] = False
    return render_template('calendar.mako', **d)

@app.route('/admin/game_logs', methods=['GET', 'POST'])
def game_logs():
    d = admin_context(requires_module=True, requires_entry=True)
    d['func'] = 'adminLogUploadCompleted'
    if request.method == 'GET':
        return render_template('admin_game_log_upload.mako', **d)
    game = d['admin_entry']
    try:
        events_filestorage = request.files.get('game_log', None)
        if not events_filestorage:
            abort(400)
        epoch = datetime.datetime(1970, 1, 1)
        q = idl_session.query(models.GamesAndRounds)
        gars = q.filter_by(game_id=game.id).all()
        event_dicts = json.loads(events_filestorage.read())['events']
        event_handler = ManualEventHandler()
        for ed in event_dicts:
            seconds, microseconds = map(int, ed['timestamp'].split('.'))
            td = datetime.timedelta(
                seconds=seconds,
                microseconds=microseconds
            )
            event = LogEvent(
                epoch + td,
                ed['type'],
                ed['data'],
                ed['category']
            )
            event_handler.get_handler(event.category)(event)
            if event.type == 'map_change':
                new_gar = models.GamesAndRounds()
                new_gar.game_id = game.id
                new_gar.round_id = event_handler.round_id
                new_gar.team_one_color_name = 'red'
                new_gar.team_two_color_name = 'blue'
                idl_session.add(new_gar)
        game.has_been_played = True
        idl_session.merge(game)
        for gar in gars:
            idl_session.delete(gar)
        idl_session.commit()
    except Exception, e:
        d['error'] = re.escape(str(e))
        return render_template('file_upload_result.mako', **d)
    return redirect(url_for('admin_rebuild_team_cache'), code=307)

@app.route('/admin/rebuild_team_cache', methods=['POST'])
def admin_rebuild_team_cache():
    d = admin_context(requires_module=True, requires_entry=True)
    d['func'] = 'adminLogUploadCompleted'
    decimal.prec = 4
    decimal.setcontext(decimal.ExtendedContext)
    game = d['admin_entry']
    season = game.season
    league = game.league
    team_one = game.team_one
    conference_one = team_one.get_conference_for_season(season)
    division_one = team_one.get_division_for_season(season)
    team_two = game.team_two
    conference_two = team_two.get_conference_for_season(season)
    division_two = team_two.get_division_for_season(season)
    cache.delete(cache.generate_key(
        'teams', 'regular_season_info', season.id, team_one.id
    ))
    cache.delete(cache.generate_key(
        'teams',
        'conference_record',
        season.id,
        conference_one.id,
        division_one.id,
        team_one.id
    ))
    cache.delete(cache.generate_key(
        'teams',
        'division_record',
        season.id,
        conference_one.id,
        division_one.id,
        team_one.id
    ))
    cache.delete(cache.generate_key(
        'teams', 'regular_season_info', season.id, team_two.id
    ))
    cache.delete(cache.generate_key(
        'teams',
        'conference_record',
        season.id,
        conference_two.id,
        division_two.id,
        team_two.id
    ))
    cache.delete(cache.generate_key(
        'teams',
        'division_record',
        season.id,
        conference_two.id,
        division_two.id,
        team_two.id
    ))
    cache.delete(cache.generate_key('games', 'stars', game.id))
    team_one.get_regular_season_info(season)
    team_one.get_conference_record(
        season, conference_one, division_one
    )
    team_one.get_division_record(season, division_one)
    team_two.get_regular_season_info(season)
    team_two.get_conference_record(
        season, conference_two, division_two
    )
    team_two.get_division_record(season, division_two)
    return redirect(url_for('admin_rebuild_player_cache'), code=307)

@app.route('/admin/rebuild_player_cache', methods=['POST'])
def admin_rebuild_player_cache():
    d = admin_context(requires_module=True, requires_entry=True)
    decimal.prec = 4
    decimal.setcontext(decimal.ExtendedContext)
    d['func'] = 'adminLogUploadCompleted'
    game = d['admin_entry']
    for player in game.players:
        cache.set(
            cache.generate_key('profiles', 'players', player.name),
            get_player_profile(player)
        )
    return redirect(url_for('admin_rebuild_game_stars_cache'), code=307)

@app.route('/admin/rebuild_game_stars_cache', methods=['POST'])
def admin_rebuild_game_stars_cache():
    d = admin_context(requires_module=True, requires_entry=True)
    decimal.prec = 4
    decimal.setcontext(decimal.ExtendedContext)
    d['func'] = 'adminLogUploadCompleted'
    game = d['admin_entry']
    stars = game.stars
    return redirect(url_for('admin_rebuild_season_stats_cache'), code=307)

@app.route('/admin/rebuild_season_stats_cache', methods=['POST'])
def admin_rebuild_season_stats_cache():
    d = admin_context(requires_module=True, requires_entry=True)
    decimal.prec = 4
    decimal.setcontext(decimal.ExtendedContext)
    d['func'] = 'adminLogUploadCompleted'
    game = d['admin_entry']
    stars = game.stars
    season = game.season
    league = game.league
    season_player_stats_key = cache.generate_key(
        'season', 'stats', 'players', season.id, league.id
    )
    season_team_stats_key = cache.generate_key(
        'season', 'stats', 'teams', season.id, league.id
    )
    cache.delete(season_player_stats_key)
    cache.delete(season_team_stats_key)
    cache.set(
        season_player_stats_key, season.get_regular_season_stats(league)
    )
    cache.set(
        season_team_stats_key, get_season_team_stats(season, league)
    )
    return render_template('file_upload_result.mako', **d)

