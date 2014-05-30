from __future__ import with_statement

import shutil
import os.path
import operator

from zipfile import is_zipfile, ZipFile, ZIP_DEFLATED
from contextlib import nested

from flask import request, session

import boto

from boto.s3.key import Key

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from idl import app
from idl.database import idl_session
from idl.database.models import League, seasons, Week, Game, Team, \
                                StoredPlayer, Demo
from idl.views.utils import get_latest_games, render_template, \
                            set_session_defaults

def get_demos(week=None, game=None, team=None, player=None):
    league = idl_session.query(League).filter_by(short_name='IDL').one()
    q = idl_session.query(Demo).join(Game).join(Week)
    q = q.filter(Demo.game_id==Game.id)
    q = q.filter(and_(
        Game.season_id==session["season"].id,
        Game.league_id==league.id
    ))
    q = q.filter(Game.week_id==Week.id)
    q = q.filter(Game.season_id==session["season"].id)
    if week:
        q = q.filter(Game.week_id==week.id)
    if game:
        q = q.filter(Game.id==game.id)
    if team:
        q = q.filter(Demo.team_id==team.id)
    if player:
        q = q.filter(Demo.player_name==player.name)
    q = q.order_by(Week.number, Game.id, Demo.team_id, Demo.player_name)
    return q.all()

def upload_to_s3(filepath):
    conn = boto.connect_s3(
        app.config['S3_ACCESS_KEY'], app.config['S3_PRIVATE_KEY']
    )
    bucket = conn.get_bucket('idldemos')
    k = boto.s3.key.Key(bucket)
    k.key = os.path.basename(filepath)
    k.set_contents_from_filename(filepath)
    k.set_acl('public-read')

def test_filetype(fobj):
    try:
        data = fobj.read(4)
        if data == 'Rar!' or data.startswith('7z'):
            raise Exception('Invalid filetype')
    finally:
        fobj.seek(0)

@app.route('/season/demos')
def demos():
    set_session_defaults()
    league = session['league']
    season = session['season']
    week = game = team = player = None
    if 'week_id' in request.form:
        try:
            week = idl_session.query(Week).get(request.form['week_id'])
        except (NoResultFound, MultipleResultsFound):
            pass
    if 'game_id' in request.form:
        try:
            game = idl_session.query(Game).get(request.form['game_id'])
        except (NoResultFound, MultipleResultsFound):
            pass
    if 'team_id' in request.form:
        try:
            team = idl_session.query(Team).get(request.form['team_id'])
        except (NoResultFound, MultipleResultsFound):
            pass
    if 'player_name' in request.form:
        try:
            q = idl_session.query(StoredPlayer)
            player = q.get(request.form['player_name'])
        except (NoResultFound, MultipleResultsFound):
            pass
    all_demos = get_demos()
    if week or game or team or player:
        demos = get_demos(week, game, team, player)
    else:
        demos = all_demos

    demo_weeks = set()
    weeks, games, teams, players = (set(), set(), set(), set())
    for demo in all_demos:
        demo_weeks.add(demo.game.week)
        weeks.add((demo.game.week.id, demo.game.week.name))
        games.add((demo.game.id, demo.game.name))
        teams.add((demo.game.team_one.id, demo.game.team_one.name))
        teams.add((demo.game.team_two.id, demo.game.team_two.name))
        players.add(demo.player.name)
    demo_weeks = sorted(list(demo_weeks), key=operator.attrgetter('number'))

    missing_demos = set()
    if request.form.get('show_missing', '') == 'show_missing':
        for demo in all_demos:
            for player in demo.game.players_missing_demos:
                if player.name in players:
                    missing_demos.add((demo.game, player))

    if demos:
        current_game = demos[0].game
        current_week = current_game.week

        game_demos = []
        week_games = {}
        sorted_demos = {}
        for demo in demos:
            demo_game = demo.game
            demo_week = demo_game.week
            if demo_game != current_game:
                week_games[current_game] = game_demos
                current_game = demo_game
                game_demos = []
            if demo_week != current_week:
                sorted_demos[current_week] = week_games
                current_week = demo_week
                week_games = {}
            game_demos.append(demo)

        week_games[current_game] = game_demos
        sorted_demos[current_week] = week_games
        demos = sorted_demos

    all_weeks = idl_session.query(Week).order_by(Week.number).all()
    for week in all_weeks:
        games = week.get_games_for_league_and_season(league, season)
        if week not in demos:
            if games:
                demos[week] = dict([(g, []) for g in games])
            else:
                demos[week] = dict()
        else:
            for game in games:
                if game not in demos[week]:
                    demos[week][game] = []

    if request.is_xhr:
        return render_template('demo_list.mako', **{
            'demos': demos,
            'missing_demos': missing_demos
        })
    else:
        return render_template('demos.mako', **{
            'section': 'season',
            'subsection': 'demos',
            'league': league,
            'seasons': seasons().all(),
            'weeks': all_weeks,
            'all_demos': all_demos,
            'no_screenshot': app.config['NO_SCREENSHOT_URL'],
            'demos': demos,
            'demo_weeks': demo_weeks,
            'demo_games': sorted(list(games)),
            'demo_teams': sorted(list(teams)),
            'demo_players': sorted(list(players)),
            'missing_demos': missing_demos
        })

@app.route('/demos/upload', methods=['POST'])
def demo_upload():
    set_session_defaults()
    season = session['season']
    username = session.get('username', False)
    game_id = request.form.get('game', False)
    demo_file = request.files.get('demo', False)
    if False in (username, game_id, demo_file):
        abort(400)
    player = idl_session.query(StoredPlayer).get(username)
    if not player:
        abort(400)
    d = dict(func='demoUploadCompleted', error=None)
    try:
        game = idl_session.query(Game).get(game_id)
        fn = (
            u'%(league)s-%(season)s-%(team_one)svs%(team_two)s-'
            u'%(week)s-%(player)sPOV_%(wad)s.zdo'
        ) % dict(
            league   = game.league.short_name,
            season   = game.season.short_name,
            team_one = game.team_one.tag,
            team_two = game.team_two.tag,
            player   = player.name,
            wad      = str(game.season.wad)[:-4],
            week     = str(game.week).replace(' ', '')
        )
        storage_path = app.config['DEMO_FILE_PATH'].decode('utf8')
        demo_path = os.path.join(storage_path, fn).encode('utf8')
        demo_name = fn.encode('utf8')
        temp_demo_path = demo_path + u'.temp'
        if os.path.isfile(temp_demo_path):
            raise Exception(u'Upload already in progress')
        test_filetype(demo_file)
        with open(temp_demo_path, 'w') as fobj:
            shutil.copyfileobj(demo_file, fobj)
        zip_path = demo_path.replace('.zdo', '.zip')
        zip_name = os.path.basename(zip_path)
        to_unlink = [temp_demo_path]
        os.rename(temp_demo_path, demo_path)
        try:
            if is_zipfile(demo_path):
                os.rename(demo_path, zip_path)
            else:
                to_unlink = [demo_path]
                zipped_demo = ZipFile(zip_path, 'w', ZIP_DEFLATED)
                zipped_demo.write(demo_path, demo_name, ZIP_DEFLATED)
                zipped_demo.close()
                to_unlink.append(zip_path)
            upload_to_s3(zip_path)
        finally:
            for fp in [x for x in to_unlink if os.path.isfile(x)]:
                os.unlink(fp)
        demo = Demo()
        demo.file_name = zip_name
        demo.player_name = username
        team_one = game.team_one
        team_two = game.team_two
        if player in game.get_players_for_team(team_one):
            demo.team_id = team_one.id
        else:
            demo.team_id = team_two.id
        demo.game_id = game.id
        idl_session.add(demo)
        idl_session.commit()
    except Exception, e:
        d['error'] = unicode(e).replace('"', '\"').join(('"', '"'))
    return render_template('file_upload_result.mako', **d)

