import decimal

decimal.prec = 4
decimal.setcontext(decimal.ExtendedContext)

import array
import urllib
import hashlib
import operator

from sqlalchemy import orm, func, select, and_, or_, join
from sqlalchemy.orm.exc import NoResultFound

from idl import app, bbcode
from idl.cache import cache
from idl.saadmin import ModelAdmin, integer
from idl.database import idl_session, forum_session, idl_db_engine, stats

from ZDStack.ZDSModels import *

class ForumMember(object):

    Admin = ModelAdmin(get_session = lambda self: forum_session)

    def __unicode__(self):
        return self.member_name

    __str__ = __unicode__

    def authenticate(self, raw_password):
        pw = None
        for x, y in [('&gt;', '>'), ('&lt;', '<'), ('&#039;', "'"),
                     ('&quot;', '"'), ('&amp;', '&')]:
            pw = pw and pw.replace(x, y) or raw_password.replace(x, y)
        hash = hashlib.sha1()
        hash.update(self.member_name.lower())
        hash.update(pw)
        return hash.hexdigest() == self.passwd

    @property
    def member_id(self):
        return self.id_member

    @property
    def player(self):
        q = idl_session.query(ForumMembersAndPlayers)
        return q.filter_by(member_id=self.id_member).one().player

    @property
    def is_admin(self):
        return self.member_name.lower() in app.config['ADMINS'].lower()

class ForumBoard(object):

    Admin = ModelAdmin(get_session = lambda self: forum_session)

    def __unicode__(self):
        return u'ForumBoard(%s: %s)' % (self.id_board, self.name)

    __str__ = __unicode__

class ForumTopic(object):

    Admin = ModelAdmin(get_session = lambda self: forum_session)

    def __unicode__(self):
        return u'ForumTopic(%s.%s.%s)' % (
            self.id_board, self.id_topic, self.id_first_msg
        )

    __str__ = __unicode__

class ForumMessage(object):

    Admin = ModelAdmin(get_session = lambda self: forum_session)

    def __unicode__(self):
        return u'ForumMessage(%s)' % (self.subject)

    __str__ = __unicode__

    def render_html(self):
        return bbcode.render(self.body)

class Administrator(object):

    def __unicode__(self):
        return u'%s -  %s' % (self.name, self.position)

    __str__ = __unicode__

class Server(object):

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

class Contributor(object):

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

class Demo(object):

    def __unicode__(self):
        player_name = self.player.name
        if player_name.endswith(u's'):
            display_name = player_name + u"'"
        else:
            display_name = player_name + u"'s"
        return u"%s demo for %s" % (display_name, self.game)

    __str__ = __unicode__

    @property
    def absolute_url(self):
        return u'/'.join([app.config['DEMO_FILES_URL'], self.file_name])

class MapScreenShot(object):

    def __unicode__(self):
        return u'Screenshot for %s' % (self.map)

    @property
    def absolute_url(self):
        return '/'.join([
            app.config['MAP_SCREENSHOTS_URL'],
            urllib.quote(self.map.wad_name),
            urllib.quote(self.file_name)
        ])

    @property
    def absolute_thumbnail_url(self):
        if not self.thumbnail_file_name:
            return self.absolute_url
        return '/'.join([
            app.config['MAP_SCREENSHOTS_URL'],
            urllib.quote(self.map.wad_name),
            urllib.quote(self.thumbnail_file_name)
        ])

class Quote(object):

    def __unicode__(self):
        if len(self.body) > 100:
            return self.body[:100] + u'...'
        else:
            return self.body

    def get_display(self):
        s = self.body
        if len(s) > 75:
            s = s[:75] + u'...'
        return s

    Admin = ModelAdmin(get_display = lambda x, y: y.get_display())

    __str__ = __unicode__

    @property
    def is_oneliner(self):
        return self.body.count('\n') < 1

class NewsItem(object):

    def __unicode__(self):
        return '%s (%s)' % (
            self.title,
            self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )

    __str__ = __unicode__

class Log(object):

    def __unicode__(self):
        return u'Log for %s' % (self.game)

    __str__ = __unicode__

    @property
    def absolute_url(self):
        return '/'.join([app.config['LOG_FILES_URL'], self.file_name])

class League(object):

    def __unicode__(self):
        return self.name

    @property
    def latest_season(self):
        q = orm.object_session(self).query(Season).with_parent(self)
        return q.order_by(Season.year.desc(), Season.season).first()

    __str__ = __unicode__

class Conference(object):

    def __unicode__(self):
        return self.name

    __repr__ = __str__ = __unicode__

    @property
    def short_name(self):
        return ''.join([x[0] for x in self.name.split()]).upper()

    def get_divisions_for_season(self, season):
        q = idl_session.query(ConferencesAndDivisions)
        q = q.filter_by(conference_id=self.id, season_id=season.id)
        return [mbs.division for mbs in q.all()]

class Division(object):

    def __unicode__(self):
        return self.name

    __repr__ = __str__ = __unicode__

    def get_conference_membership_for_season(self, season):
        q = idl_session.query(ConferencesAndDivisions)
        q = q.filter(ConferencesAndDivisions.date_left==None)
        return q.filter_by(division_id=self.id, season_id=season.id).one()

    def get_conference_for_season(self, season):
        key = cache.generate_key('divisions', 'conference', season.id, self.id)
        cached_conference_id = cache.get(key)
        if not cached_conference_id:
            conf = self.get_conference_membership_for_season(season).conference
            cache.set(key, conf.id)
        else:
            conf = idl_session.query(Conference).get(cached_conference_id)
        return conf

    def get_division_memberships_for_season(self, season):
        q = idl_session.query(DivisionsAndTeams)
        return q.filter_by(division_id=self.id, season_id=season.id).all()

    def get_teams_for_season(self, season):
        q = idl_session.query(DivisionsAndTeams)
        q = q.filter_by(division_id=self.id, season_id=season.id)
        return [mbs.team for mbs in q.all()]

    def get_current_teams_for_season(self, season):
        q = idl_session.query(DivisionsAndTeams)
        q = q.filter_by(
            division_id=self.id, season_id=season.id, date_left=None
        )
        return [mbs.team for mbs in q.all()]

    @property
    def current_teams(self):
        q = idl_session.query(DivisionsAndTeams)
        q = q.filter_by(division_id=self.id, date_left=None)
        return [mbs.team for mbs in q.all()]

class Team(object):

    def __unicode__(self):
        return self.name

    __repr__ = __str__ = __unicode__

    def _process_games(self, games):
        streak_type = u''
        streak_length = wins = losses = ties = 0
        number_of_games = decimal.Decimal(0)
        for g in games:
            if not g.has_been_played:
                continue
            elif not g.winner:
                new_streak_type = u'T'
                ties += 1
            elif g.winner == self:
                new_streak_type = u'W'
                wins += 1
            else:
                new_streak_type = u'L'
                losses += 1
            if new_streak_type != streak_type:
                streak_type = new_streak_type
                streak_length = 0
            number_of_games += decimal.Decimal(1)
            streak_length += 1
        streak = u'%d%s' % (streak_length, streak_type)
        if number_of_games > 0:
            wins_and_ties = decimal.Decimal(wins) + \
                            (decimal.Decimal(ties) * decimal.Decimal('.5'))
            win_percentage = u'%0.3f' % (wins_and_ties / number_of_games)
        else:
            win_percentage = u'-'
        return {
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "streak": streak,
            "win_percentage": win_percentage
        }

    def get_regular_season_info(self, season):
        key = cache.generate_key(
            'teams', 'regular_season_info', season.id, self.id
        )
        regular_season_info = cache.get(key)
        if not regular_season_info:
            regular_season_info = self._process_games(
                self.get_regular_season_games_for_season(season)
            )
            cache.set(key, regular_season_info)
        return regular_season_info

    def get_conference_record(self, season, conference=None, division=None):
        division = division or self.get_division_for_season(season)
        conference = conference or division.get_conference_for_season(season)
        key = cache.generate_key(
            'teams',
            'conference_record',
            season.id,
            conference.id,
            division.id,
            self.id
        )
        results = cache.get(key)
        if not results:
            results = self._process_games(self.get_conference_games_for_season(
                season, conference, division
            ))
            cache.set(key, results)
        return (results['wins'], results['losses'], results['ties'])

    def get_division_record(self, season, division=None):
        division = division or self.get_division_for_season(season)
        key = cache.generate_key(
            'teams', 'division_record', season.id, division.id, self.id
        )
        results = cache.get(key)
        if not results:
            results = self._process_games(
                self.get_division_games_for_season(season, division)
            )
            cache.set(key, results)
        return (results['wins'], results['losses'], results['ties'])

    def get_playoff_seed_for_season(self, season):
        return self.get_division_membership_for_season(season).playoff_seed

    def get_homefield_for_season(self, season):
        return self.get_division_membership_for_season(season).homefield_map

    def get_division_rivals_for_season(self, season, division=None):
        division = division or self.get_division_for_season(season)
        teams = division.get_teams_for_season(season)
        return [t for t in teams if t != self]

    def get_conference_rivals_for_season(self, season, conference=None,
                                                       division=None):
        if not conference:
            conference = division.get_conference_for_season(season)
        if not division:
            division = self.get_division_for_season(season)
        conf_divs = conference.get_divisions_for_season(season)
        div_teams = division.get_teams_for_season(season)
        out = [t for t in div_teams if t != self]
        for x in [x for x in conf_divs if x != division]:
            for t in x.get_teams_for_season(season):
                if t not in out:
                    out.append(t)
        return out

    def _get_current_division_membership_query(self):
        q = idl_session.query(DivisionsAndTeams)
        q.filter(DivisionAndTeams.date_left==None)
        return q.filter_by(team_id=self.id)

    def _get_division_membership_query_for_season(self, season):
        q = idl_session.query(DivisionsAndTeams)
        return q.filter_by(season_id=season.id, team_id=self.id)

    def get_conference_membership_for_season(self, season):
        div = self.get_division_for_season(season)
        return div.get_conference_membership_for_season(season)

    def get_division_membership_for_season(self, season):
        return self._get_division_membership_query_for_season(season).one()

    def get_conference_for_season(self, season):
        div = self.get_division_for_season(season)
        return div.get_conference_for_season(season)

    def get_division_for_season(self, season):
        key = cache.generate_key('teams', 'division', season.id, self.id)
        cached_division_id = cache.get(key)
        if not cached_division_id:
            division = self.get_division_membership_for_season(season).division
            cache.set(key, division.id)
        else:
            division = idl_session.query(Division).get(cached_division_id)
        return division

    def clinched_playoffs_for_season(self, season):
        mbs = self.get_division_membership_for_season(season)
        return mbs.clinched_playoffs

    def clinched_division_for_season(self, season):
        mbs = self.get_division_membership_for_season(season)
        return mbs.clinched_division

    def clinched_homefield_for_season(self, season):
        mbs = self.get_division_membership_for_season(season)
        return mbs.clinched_homefield

    def _get_games_query_for_season(self, season):
        q = idl_session.query(Game).filter_by(season_id=season.id)
        q = q.filter(or_(Game.team_one_id==self.id,
                         Game.team_two_id==self.id))
        return q.order_by(Game.scheduled_for)

    def _get_regular_season_games_query_for_season(self, season):
        q = self._get_games_query_for_season(season)
        return q.filter(and_(Week.id==Game.week_id, Week.number < 10))

    def _get_playoff_games_query_for_season(self, season):
        q = self._get_games_query_for_season(season)
        return q.filter(Week.id==Game.week_id, Week.number > 9)

    def get_regular_season_games_for_season(self, season):
        return self._get_regular_season_games_query_for_season(season).all()

    def get_playoff_games_for_season(self, season):
        return self._get_playoff_games_query_for_season(season).all()

    def get_conference_games_for_season(self, season, conference=None,
                                                      division=None):
        conference_rivals = \
            self.get_conference_rivals_for_season(season, conference, division)
        conference_rival_ids = [x.id for x in conference_rivals]
        q = self._get_regular_season_games_query_for_season(season)
        return q.filter(or_(and_(Game.team_one_id==self.id,
                                 Game.team_two_id.in_(conference_rival_ids)),
                            and_(Game.team_one_id.in_(conference_rival_ids),
                                 Game.team_two_id==self.id))).all()

    def get_division_games_for_season(self, season, division=None):
        division_rivals = self.get_division_rivals_for_season(season, division)
        division_rival_ids = [x.id for x in division_rivals]
        q = self._get_regular_season_games_query_for_season(season)
        return q.filter(or_(and_(Game.team_one_id==self.id,
                                 Game.team_two_id.in_(division_rival_ids)),
                            and_(Game.team_one_id.in_(division_rival_ids),
                                 Game.team_two_id==self.id))).all()

    def get_players_for_season(self, season):
        q = idl_session.query(TeamsAndPlayers).filter_by(team_id=self.id)
        q = q.filter(and_(TeamsAndPlayers.season_id==season.id,
                          TeamsAndPlayers.date_left==None))
        q = q.order_by('as_captain', 'date_left').limit(4)
        return [mbs.player for mbs in q.all()]

    def get_captain_for_season(self, season):
        q = idl_session.query(TeamsAndPlayers).filter_by(team_id=self.id)
        q = q.filter_by(season_id=season.id, as_captain=True)
        row = q.order_by(TeamsAndPlayers.date_left.desc()).first()
        if row is None:
            return None
        return row.player

    def get_players_for_game(self, game):
        q = idl_session.query(TeamsAndPlayers)
        q = q.filter_by(team_id=self.id, season_id=game.season_id)
        # [CG] Not all games have entries for their "scheduled_for" column,
        #      so this filter will error.  Right now we just list all players
        #      with no date_left value.  What we should probably do is figure
        #      out what the start dates for the seasons were and then offset
        #      each cutoff from there.
        if game.scheduled_for is None:
            q = q.filter(TeamsAndPlayers.date_left==None)
        else:
            q = q.filter(or_(
                TeamsAndPlayers.date_left==None,
                TeamsAndPlayers.date_left > game.scheduled_for
            ))
        q = q.order_by(TeamsAndPlayers.as_captain.desc())
        players_at_the_time = [x.player for x in q.all()]
        return [p for p in players_at_the_time if p in game.players]

    def get_players_for_round(self, round):
        game_players = self.get_players_for_game(round.game[0])
        round_aliases = [a for a in round.aliases if a.stored_player_name]
        round_players = [a.stored_player for a in round_aliases]
        return [p for p in game_players if p in round_players]

    @property
    def current_players(self):
        q = idl_session.query(TeamsAndPlayers).filter_by(team_id=self.id)
        q = q.filter(TeamsAndPlayers.date_left==None)
        return [x.player for x in q.all()]

    @property
    def current_captain(self):
        q = idl_session.query(TeamsAndPlayers).filter_by(team_id=self.id)
        q = q.filter(and_(TeamsAndPlayers.date_left==None,
                          TeamsAndPlayers.as_captain==True))
        try:
            return q.one().player
        except NoResultFound:
            return None

    @property
    def logo(self):
        if self.logo_file is None:
            return u'/'.join((
                app.config['STATIC_URL'], 'images', 'classiclogo.png'
            ))
        return u'/'.join((app.config['LOGOS_URL'], self.logo_file))

class Season(object):

    Admin = ModelAdmin(column_attributes={
        ###
        # Stuff you can specify
        #
        # 'season': {
        #     'choices': (
        #         (u'Winter', u'Winter),
        #         (u'Summer', u'Summer),
        #     )
        # },
        # 'year': {
        #     'max_length': 4
        # }
        # 'clinched_division': {
        #     'label': u'Division Champions'
        # }
        # 'team_id': {
        #     'label':       u'Team'
        #     'blank_value': u'Free Agent'
        # }
        ###
        'season': {
            'get_choices': lambda self_: [
                (u'Winter', u'Winter'),
                (u'Summer', u'Summer'),
            ]
        },
        'year': {
            'max_length': 4
        }
    })

    def __unicode__(self):
        return self.season + u' ' + unicode(self.year)

    __str__ = __unicode__

    @property
    def short_name(self):
        return self.season[:1] + unicode(self.year)

    @property
    def masterbowl(self):
        masterbowl_weeks = [x for x in self.weeks if x.name == 'MasterBowl']
        if not masterbowl_weeks:
            return None
        masterbowl_week = masterbowl_weeks[0]
        games = [g for g in masterbowl_week.games if g.season_id == self.id]
        if not games:
            return None
        return games[0]

    @property
    def champion(self):
        mb = self.masterbowl
        if mb:
            return self.masterbowl.winner
        return None

    @property
    def name(self):
        return self.season[0].capitalize() + unicode(self.year)

    @property
    def regular_season_weeks(self):
        return [x for x in self.weeks if x.number < 10]

    @property
    def playoff_weeks(self):
        return [x for x in self.weeks if x.number > 9]

    def get_regular_season_games(self, league):
        lid = league.id
        return [
            g for g in self.games if g.week.number < 10 and g.league_id == lid
        ]

    def get_playoff_games(self, league):
        lid = league.id
        return [
            g for g in self.games if g.week.number > 9 and g.league_id == lid
        ]

    def get_regular_season_rounds(self, league):
        out = set()
        for g in self.get_regular_season_games(league):
            out.update(g.rounds)
        return list(out)

    def get_playoff_season_rounds(self, league):
        out = set()
        for g in self.get_playoff_games(league):
            out.update(g.rounds)
        return list(out)

    def get_regular_season_stats(self, league):
        return stats.get_base_player_stats([
            r.id for r in self.get_regular_season_rounds(league)
        ])

    def get_playoff_season_stats(self, league):
        return stats.get_base_player_stats([
            r.id for r in self.get_playoff_season_rounds(league)
        ])

    def get_regular_season_leaders(self, league):
        labels = (
            'captures_per_round',
            'pick_captures_per_round',
            'touches_per_round',
            'picks_per_round',
            'flag_ratio',
            'pick_ratio',
            'touches',
            'picks',
            'captures',
            'pick_captures',
            'frags_per_round',
            'returns_per_round',
            'frag_ratio',
            'return_ratio',
            'frags',
            'returns'
        )
        season_stats = self.get_regular_season_stats(league)
        leaders = (
            stats.get_flag_captures_per_round_leaders(season_stats),
            stats.get_pick_captures_per_round_leaders(season_stats),
            stats.get_flag_touches_per_round_leaders(season_stats),
            stats.get_flag_picks_per_round_leaders(season_stats),
            stats.get_flag_ratio_leaders(season_stats),
            stats.get_pick_ratio_leaders(season_stats),
            stats.get_flag_touch_leaders(season_stats),
            stats.get_flag_pick_leaders(season_stats),
            stats.get_flag_capture_leaders(season_stats),
            stats.get_flag_pick_capture_leaders(season_stats),
            stats.get_frags_per_round_leaders(season_stats),
            stats.get_flag_returns_per_round_leaders(season_stats),
            stats.get_frag_ratio_leaders(season_stats),
            stats.get_flag_return_ratio_leaders(season_stats),
            stats.get_frag_leaders(season_stats),
            stats.get_flag_return_leaders(season_stats)
        )
        return dict(zip(labels, leaders))

class Week(object):

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    @property
    def demo_name(self):
        if self.number in (1, 2, 3, 4, 5, 6, 7, 8, 9):
            return u'week%d' % (self.number)
        else:
            tokens = self.name.split(u' ')
            if len(tokens) > 1:
                return tokens[0].lower()
            else:
                return self.name.lower()

    @property
    def is_playoff_season(self):
        return self.number > 9

    @property
    def is_regular_season(self):
        return self.number < 10

    def get_map_for_season(self, season):
        try:
            return idl_session.query(SeasonsAndWeeks).filter_by(
                week_id=self.id,
                season_id=season.id
            ).one().map
        except NoResultFound:
            return None

    def get_map_screenshot_for_season(self, season):
        m = self.get_map_for_season(season)
        if not m:
            if self.is_playoff_season:
                return app.config['LOGO_URL']
            else:
                return app.config['NO_SCREENSHOT_URL']
        shots = m.screenshot
        if not len(shots):
            return app.config['NO_SCREENSHOT_URL']
        else:
            return shots[0].absolute_url

    def get_games_for_league_and_season(self, league, season, conference=None,
                                              sort_by_time=False):
        q = idl_session.query(Game).filter(and_(Game.league_id==league.id,
                                                Game.season_id==season.id,
                                                Game.week_id==self.id))
        if sort_by_time:
            q = q.order_by('scheduled_for')
        if not conference:
            return q.all()
        result = q.all()
        games = []
        for game in result:
            team_one, team_two = (game.team_one, game.team_two)
            team_one_conference = team_one.get_conference_for_season(season)
            team_two_conference = team_two.get_conference_for_season(season)
            if team_one_conference == team_two_conference == conference:
                games.append(game)
        return games

class Game(object):

    Admin = ModelAdmin(
        column_attributes = {
            'team_one_id': {
                'get_label': lambda game: u'Team One'
            },
            'team_two_id': {
                'get_label': lambda game: u'Team Two'
            },
            'forfeiting_team_id': {
                'get_label': lambda game: u'Forfeiting Team',
                'parser': integer
            },
            'forced_winner_id': {
                'get_label': lambda game: u'Force Winner To',
                'parser': integer
            }
        }
    )

    def __unicode__(self):
        return u'%s - %s: %s vs. %s' % (
            self.season.short_name,
            self.week.name,
            self.team_one.tag,
            self.team_two.tag
        )

    __str__ = __unicode__

    @property
    def map(self):
        week = self.week
        season = self.season
        team_one = self.team_one
        team_two = self.team_two
        if week.is_regular_season or week.number == 12:
            return week.get_map_for_season(season)
        else:
            team_one_seed = team_one.get_playoff_seed_for_season(season)
            team_two_seed = team_two.get_playoff_seed_for_season(season)
            if team_one_seed < team_two_seed:
                return team_one.get_homefield_for_season(season)
            else:
                return team_two.get_homefield_for_season(season)

    @property
    def map_screenshot(self):
        m = self.map
        if not m:
            return app.config['NO_SCREENSHOT_URL']
        shots = m.screenshot
        if not len(shots):
            return app.config['NO_SCREENSHOT_URL']
        else:
            return shots[0].absolute_url

    def get_players_for_team(self, team):
        return team.get_players_for_game(self)

    def get_players_for_round(self, team):
        return team.get_players_for_game(self)

    @property
    def players(self):
        s = set()
        for round in self.rounds:
            for alias in round.aliases:
                s.add(alias.stored_player)
        return [x for x in s if x]

    @property
    def players_missing_demos(self):
        player_names = [d.player.name for d in self.demos]
        return [p for p in self.players if p.name not in player_names]

    @property
    def flag_touches(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        q = q.filter(FlagTouch.was_picked==False)
        return q.order_by(FlagTouch.round_id, FlagTouch.loss_time).all()

    @property
    def flag_picks(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        q = q.filter(FlagTouch.was_picked==True)
        return q.order_by(FlagTouch.round_id, FlagTouch.loss_time).all()

    @property
    def flag_captures(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        q = q.filter(FlagTouch.was_picked==False)
        q = q.filter(FlagTouch.resulted_in_score==True)
        return q.order_by(FlagTouch.round_id, FlagTouch.loss_time).all()

    @property
    def total_flag_captures(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        q = q.filter(FlagTouch.resulted_in_score==True)
        return q.order_by(FlagTouch.round_id, FlagTouch.loss_time).all()

    @property
    def flag_pick_captures(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        q = q.filter(FlagTouch.was_picked==True)
        q = q.filter(FlagTouch.resulted_in_score==True)
        return q.order_by(FlagTouch.round_id, FlagTouch.loss_time).all()

    @property
    def flag_losses(self):
        q = idl_session.query(FlagTouch).filter_by(resulted_in_score=False)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        return q.order_by(FlagTouch.round_id, FlagTouch.loss_time).all()

    @property
    def flag_drops(self):
        q = idl_session.query(Frag)
        q = q.filter(and_(
            Frag.round_id.in_(self.round_ids),
            Frag.fraggee_was_holding_flag == True,
            Frag.fragger_id != Frag.fraggee_id
        ))
        return q.order_by(Frag.round_id, Frag.timestamp).all()

    @property
    def flag_returns(self):
        q = idl_session.query(FlagReturn)
        q = q.filter(FlagReturn.round_id.in_(self.round_ids))
        return q.order_by(FlagReturn.round_id, FlagReturn.timestamp).all()

    @property
    def frags(self):
        q = idl_session.query(Frag)
        q = q.filter(and_(
            Frag.round_id.in_(self.round_ids),
            Frag.fragger_id != Frag.fraggee_id
        ))
        return q.order_by(Frag.round_id, Frag.timestamp).all()

    @property
    def deaths(self):
        q = idl_session.query(Frag)
        q = q.filter(Frag.round_id.in_(self.round_ids))
        return q.order_by(Frag.round_id, Frag.timestamp).all()

    def _by_round(self, x):
        out = []
        mbsq = idl_session.query(GamesAndRounds).filter_by(game_id=self.id)
        for mbs in mbsq.order_by(GamesAndRounds.round_id).all():
            out.append([y for y in x if y.round_id == mbs.round_id])
        return out

    def _by_round_and_team(self, m, q=None, cc=None):
        out = []
        if not q:
            q = idl_session.query(m).order_by(m.round_id, m.timestamp)
        cc = cc or m.player_team_color_name
        mbsq = idl_session.query(GamesAndRounds).filter_by(game_id=self.id)
        for mbs in mbsq.order_by(GamesAndRounds.round_id).all():
            rq = q.filter(m.round_id==mbs.round_id)
            t1cq = rq.filter(cc==mbs.team_one_color_name)
            t2cq = rq.filter(cc==mbs.team_two_color_name)
            out.append((t1cq.all(), t2cq.all()))
        return out

    def _counts_by_team(self, m, q=None, cc=None):
        out = [0, 0]
        q = q or idl_session.query(m).filter(m.round_id.in_(self.round_ids))
        cc = cc or m.player_team_color_name
        mbsq = idl_session.query(GamesAndRounds).filter_by(game_id=self.id)
        for mbs in mbsq.order_by(GamesAndRounds.round_id).all():
            rq = q.filter(m.round_id==mbs.round_id)
            out[0] += rq.filter(cc==mbs.team_one_color_name).count()
            out[0] += rq.filter(cc==mbs.team_two_color_name).count()
        return out

    def _counts_by_round_and_team(self, m, q=None, cc=None):
        out = []
        if not q:
            q = idl_session.query(m).order_by(m.round_id, m.timestamp)
        cc = cc or m.player_team_color_name
        mbsq = idl_session.query(GamesAndRounds).filter_by(game_id=self.id)
        for mbs in mbsq.order_by(GamesAndRounds.round_id).all():
            rq = q.filter(m.round_id==mbs.round_id)
            t1cq = rq.filter(cc==mbs.team_one_color_name)
            t2cq = rq.filter(cc==mbs.team_two_color_name)
            out.append((t1cq.count(), t2cq.count()))
        return out

    @property
    def flag_touches_by_round(self):
        return self._by_round(self.flag_touches)

    @property
    def flag_picks_by_round(self):
        return self._by_round(self.flag_picks)

    @property
    def flag_captures_by_round(self):
        return self._by_round(self.flag_captures)

    @property
    def total_flag_captures_by_round(self):
        return self._by_round(self.total_flag_captures)

    @property
    def flag_losses_by_round(self):
        return self._by_round(self.flag_losses)

    @property
    def flag_drops_by_round(self):
        return self._by_round(self.flag_drops)

    @property
    def flag_returns_by_round(self):
        return self._by_round(self.flag_returns)

    @property
    def frags_by_round(self):
        return self._by_round(self.frags)

    @property
    def deaths_by_round(self):
        return self._by_round(self.deaths)

    @property
    def flag_touches_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.was_picked==False)
        q = q.order_by(FlagTouch.round_id, FlagTouch.touch_time)
        return self._by_round_and_team(FlagTouch, q)

    @property
    def flag_picks_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.was_picked==True)
        q = q.order_by(FlagTouch.round_id, FlagTouch.touch_time)
        return self._by_round_and_team(FlagTouch, q)

    @property
    def flag_captures_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.was_picked==False)
        q = q.filter(FlagTouch.resulted_in_score==True)
        q = q.order_by(FlagTouch.round_id, FlagTouch.loss_time)
        return self._by_round_and_team(FlagTouch, q)

    @property
    def total_flag_captures_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.resulted_in_score==True)
        q = q.order_by(FlagTouch.round_id, FlagTouch.loss_time)
        return self._by_round_and_team(FlagTouch, q)

    @property
    def flag_pick_captures_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.was_picked==True)
        q = q.filter(FlagTouch.resulted_in_score==True)
        q = q.order_by(FlagTouch.round_id, FlagTouch.loss_time)
        return self._by_round_and_team(FlagTouch, q)

    @property
    def flag_losses_by_round_and_team(self):
        q = idl_session.query(FlagTouch).filter_by(resulted_in_score=False)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        q = q.order_by(FlagTouch.round_id, FlagTouch.loss_time)
        return self._by_round_and_team(FlagTouch, q)

    @property
    def flag_drops_by_round_and_team(self):
        q = idl_session.query(Frag)
        q = q.filter(and_(
            Frag.round_id.in_(self.round_ids),
            Frag.fraggee_was_holding_flag == True,
            Frag.fragger_id != Frag.fraggee_id
        ))
        q = q.order_by(Frag.round_id, Frag.timestamp)
        return self._by_round_and_team(Frag, q, cc=Frag.fragger_team_color_name)

    @property
    def flag_returns_by_round_and_team(self):
        return self._by_round_and_team(FlagReturn)

    @property
    def frags_by_round_and_team(self):
        q = idl_session.query(Frag).filter(Frag.fragger_id != Frag.fraggee_id)
        return self._by_round_and_team(Frag, q, cc=Frag.fragger_team_color_name)

    @property
    def deaths_by_round_and_team(self):
        return self._by_round_and_team(Frag, cc=Frag.fraggee_team_color_name)

    @property
    def flag_touch_counts_by_team(self):
        q = idl_session.query(FlagTouch).filter(FlagTouch.was_picked==False)
        return self._counts_by_team(FlagTouch, q)

    @property
    def flag_pick_counts_by_team(self):
        q = idl_session.query(FlagTouch).filter(FlagTouch.was_picked==True)
        return self._counts_by_team(FlagTouch, q)

    @property
    def flag_capture_counts_by_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.resulted_in_score==True)
        q = q.filter(FlagTouch.was_picked==False)
        return self._counts_by_team(FlagTouch, q)

    @property
    def flag_pick_capture_counts_by_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.resulted_in_score==True)
        q = q.filter(FlagTouch.was_picked==True)
        return self._counts_by_team(FlagTouch, q)

    @property
    def total_flag_capture_counts_by_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.resulted_in_score==True)
        return self._counts_by_team(FlagTouch, q)

    @property
    def flag_loss_counts_by_team(self):
        q = idl_session.query(FlagTouch).filter_by(resulted_in_score=False)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        return self._counts_by_team(FlagTouch, q)

    @property
    def flag_drop_counts_by_team(self):
        q = idl_session.query(Frag).filter(and_(
            Frag.fraggee_was_holding_flag==True,
            Frag.fragger_id != Frag.fraggee_id
        ))
        return self._counts_by_team(Frag, q, cc=Frag.fragger_team_color_name)

    @property
    def flag_return_counts_by_team(self):
        return self._counts_by_team(FlagReturn)

    @property
    def frag_counts_by_team(self):
        q = idl_session.query(Frag).filter(Frag.fragger_id!=Frag.fraggee_id)
        cc = Frag.fragger_team_color_name
        return self._counts_by_team(Frag, q, cc)

    @property
    def death_counts_by_team(self):
        return self._counts_by_team(Frag, cc=Frag.fraggee_team_color_name)

    @property
    def flag_touch_counts_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.was_picked==False)
        q = q.order_by(FlagTouch.round_id, FlagTouch.touch_time)
        return self._counts_by_round_and_team(FlagTouch, q)

    @property
    def flag_pick_counts_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.was_picked==True)
        q = q.order_by(FlagTouch.round_id, FlagTouch.touch_time)
        return self._counts_by_round_and_team(FlagTouch, q)

    @property
    def flag_capture_counts_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.resulted_in_score==True)
        q = q.filter(FlagTouch.was_picked==False)
        q = q.order_by(FlagTouch.round_id, FlagTouch.loss_time)
        return self._counts_by_round_and_team(FlagTouch, q)

    @property
    def flag_pick_capture_counts_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.resulted_in_score==True)
        q = q.filter(FlagTouch.was_picked==True)
        q = q.order_by(FlagTouch.round_id, FlagTouch.loss_time)
        return self._counts_by_round_and_team(FlagTouch, q)

    @property
    def total_flag_capture_counts_by_round_and_team(self):
        q = idl_session.query(FlagTouch)
        q = q.filter(FlagTouch.resulted_in_score==True)
        q = q.order_by(FlagTouch.round_id, FlagTouch.loss_time)
        return self._counts_by_round_and_team(FlagTouch, q)

    @property
    def flag_loss_counts_by_round_and_team(self):
        q = idl_session.query(FlagTouch).filter_by(resulted_in_score=False)
        q = q.filter(FlagTouch.round_id.in_(self.round_ids))
        q = q.order_by(FlagTouch.round_id, FlagTouch.loss_time)
        return self._counts_by_round_and_team(FlagTouch, q)

    @property
    def flag_drop_counts_by_round_and_team(self):
        q = idl_session.query(Frag)
        q = q.filter(and_(
            Frag.round_id.in_(self.round_ids),
            Frag.fraggee_was_holding_flag == True,
            Frag.fragger_id != Frag.fraggee_id
        ))
        q = q.order_by(Frag.round_id, Frag.timestamp)
        cc = Frag.fragger_team_color_name
        return self._counts_by_round_and_team(Frag, q, cc)

    @property
    def flag_return_counts_by_round_and_team(self):
        return self._counts_by_round_and_team(FlagReturn)

    @property
    def frag_counts_by_round_and_team(self):
        q = idl_session.query(Frag).filter(Frag.fragger_id != Frag.fraggee_id)
        cc = Frag.fragger_team_color_name
        return self._counts_by_round_and_team(Frag, q, cc)

    @property
    def death_counts_by_round_and_team(self):
        cc = Frag.fraggee_team_color_name
        return self._counts_by_round_and_team(Frag, cc=cc)

    @property
    def round_counts(self):
        t1_wins, t2_wins = (0, 0)
        for t1c, t2c in self.round_flag_capture_counts:
            if t1c > t2c:
                t1_wins += 1
            elif t2c > t1c:
                t2_wins += 1
        return (t1_wins, t2_wins)

    @property
    def round_ids(self):
        rounds = sorted(self.rounds, key=operator.attrgetter('start_time'))
        return [r.id for r in rounds]

    @property
    def winner(self):
        if self.forfeiting_team is None:
            t1_wins, t2_wins = self.round_counts
            if t1_wins > t2_wins:
                return self.team_one
            elif t2_wins > t1_wins:
                return self.team_two
            else:
                return None
        else:
            if self.team_one_id == self.forfeiting_team.id:
                return self.team_two
            else:
                return self.team_one

    @property
    def name(self):
        return unicode(self)

    @property
    def rivalry(self):
        if self.team_one.get_division_for_season(self.season) == \
           self.team_two.get_division_for_season(self.season):
            return u'div'
        if self.team_one.get_conference_for_season(self.season) == \
           self.team_two.get_conference_for_season(self.season):
            return u'conf'
        return u'int'

    @property
    def team_colors(self):
        out = []
        q = idl_session.query(GamesAndRounds)
        q = q.filter(GamesAndRounds.game_id==self.id)
        for gar in q.order_by(GamesAndRounds.round_id).all():
            out.append((gar.team_one_color_name, gar.team_two_color_name))
        return out

    @property
    def round_flag_capture_counts(self):
        counts = []
        q = idl_session.query(FlagTouch).filter_by(resulted_in_score=True)
        mbsq = idl_session.query(GamesAndRounds).filter_by(game_id=self.id)
        for mbs in mbsq.all():
            rq = q.filter(FlagTouch.round_id==mbs.round_id)
            t1cq = rq.filter_by(player_team_color_name=mbs.team_one_color_name)
            t2cq = rq.filter_by(player_team_color_name=mbs.team_two_color_name)
            counts.append((t1cq.count(), t2cq.count()))
        return counts

    @property
    def stars(self):
        key = cache.generate_key('games', 'stars', self.id)

        cached_stars = cache.get(key)
        if cached_stars:
            return cached_stars

        if not self.has_been_played or not self.rounds:
            return {
                'flag_count': {'names': [], 'stat': ''},
                'frag_count': {'names': [], 'stat': ''},
                'flag_ratio': {'names': [], 'stat': ''},
                'frag_ratio': {'names': [], 'stat': ''}
            }

        top_flaggers = None
        top_fraggers = None
        most_successful_flaggers = None
        most_successful_fraggers = None
        round_ids = ', '.join([str(int(x)) for x in self.round_ids])
        round_ids = round_ids.join(['(', ')'])
        d = {}
        ###
        # I *KNOW* this is bad.  But fuck it heh.
        ###
        s = idl_db_engine.text("""\
SELECT COUNT(*) AS cnt, player_id, resulted_in_score\
  FROM flag_touches WHERE round_id IN %s\
  GROUP BY player_id, resulted_in_score\
  ORDER BY cnt DESC, player_id, resulted_in_score DESC\
""" % (round_ids))
        rows = s.execute().fetchall()
        for count, player_id, resulted_in_score in rows:
            if player_id not in d:
                d[player_id] = {'caps': 0, 'totals': 0, 'frags': 0, 'deaths': 0}
            d[player_id]['totals'] += count
            if resulted_in_score:
                d[player_id]['caps'] += count

        s = idl_db_engine.text("""\
SELECT COUNT(*) AS cnt, fragger_id, fraggee_id\
  FROM frags WHERE round_id IN %s\
  GROUP BY fragger_id, fraggee_id\
""" % (round_ids))
        rows = s.execute().fetchall()
        for count, fragger_id, fraggee_id in rows:
            if fragger_id not in d:
                d[fragger_id] = \
                            {'caps': 0, 'totals': 0, 'frags': 0, 'deaths': 0}
            if fraggee_id not in d:
                d[fraggee_id] = \
                            {'caps': 0, 'totals': 0, 'frags': 0, 'deaths': 0}
            d[fraggee_id]['deaths'] += count
            if fragger_id != fraggee_id:
                ###
                # Suicides don't count as frags, but they don't count as
                # negative frags either.
                ###
                d[fragger_id]['frags'] += count

        for player_id in d:
            flag_ratio = decimal.Decimal(d[player_id]['caps']) / \
                         decimal.Decimal(d[player_id]['totals'])
            frag_ratio = decimal.Decimal(d[player_id]['frags']) / \
                         decimal.Decimal(d[player_id]['deaths'])
            if not top_flaggers or d[player_id]['caps'] > top_flaggers[1]:
                top_flaggers = ([player_id], d[player_id]['caps'])
            elif d[player_id]['caps'] == top_flaggers[1]:
                top_flaggers[0].append(player_id)
            if not most_successful_flaggers \
                or flag_ratio > most_successful_flaggers[1]:
                most_successful_flaggers = ([player_id], flag_ratio)
            elif flag_ratio == most_successful_flaggers[1]:
                most_successful_flaggers[0].append(player_id)
            if not top_fraggers or d[player_id]['frags'] > top_fraggers[1]:
                top_fraggers = ([player_id], d[player_id]['frags'])
            elif d[player_id]['frags'] == top_fraggers[1]:
                top_fraggers[0].append(player_id)
            if not most_successful_fraggers \
                or frag_ratio > most_successful_fraggers[1]:
                most_successful_fraggers = ([player_id], frag_ratio)
            elif frag_ratio == most_successful_fraggers[1]:
                most_successful_fraggers[0].append(player_id)

        stars = (top_flaggers, top_fraggers, most_successful_flaggers,
                 most_successful_fraggers)
        star_ids = list(set(top_flaggers[0] + top_fraggers[0] + \
                             most_successful_flaggers[0] + \
                             most_successful_fraggers[0]))
        star_players = [idl_session.query(Alias).get(x) for x in star_ids]
        star_players = dict(zip(star_ids, star_players))

        def associate_stars(stars):
            d = {'names': [], 'stat': ''}
            stars, stat = ([star_players[x] for x in stars[0]], stars[1])
            for star in stars:
                if star.stored_player_name:
                    d['names'].append(star.stored_player_name)
                else:
                    d['names'].append(star.name)
                if isinstance(stat, decimal.Decimal):
                    if stat == decimal.Decimal('inf'):
                        d['stat'] = u'&#8734;'
                    else:
                        d['stat'] = u'%3.2f%%' % (stat * decimal.Decimal(100))
                else:
                    d['stat'] = stat
            return d

        result = {
            'flag_count': associate_stars(top_flaggers),
            'frag_count': associate_stars(top_fraggers),
            'flag_ratio': associate_stars(most_successful_flaggers),
            'frag_ratio': associate_stars(most_successful_fraggers)
        }

        cache.set(key, result)

        return result

class LeaguesAndConferences(object):

    def __unicode__(self):
        return u'%s of %s - %s' % (
            self.conference.name,
            self.league.name,
            self.season.short_name
        )

    __str__ = __unicode__

class ConferencesAndDivisions(object):

    def __unicode__(self):
        return u'%s %s - %s' % (self.conference.short_name,
                                self.division.name,
                                self.season.short_name)

    __str__ = __unicode__

class DivisionsAndTeams(object):

    Admin = ModelAdmin(column_attributes={
        'homefield_map_id': {'get_label': lambda self_: u'Homefield Map'}
    })

    def __unicode__(self):
        return u'%s of the %s Division - %s' % (self.team.name,
                                                self.division.name,
                                                self.season.short_name)

    __str__ = __unicode__

class TeamsAndPlayers(object):

    def __unicode__(self):
        if self.player and self.team:
            return u'%s of the %s - %s' % (self.player.name,
                                           self.team.name,
                                           self.season.short_name)
        elif self.player:
            return u'%s (Free Agent)' % (self.player.name)
        elif self.team:
            return u'Opening on %s' % (self.team.name)
        else:
            return u'Unnamed'

    __str__ = __unicode__

class LeaguesAndSeasons(object):

    def __unicode__(self):
        return u'Season %s of the %s' % (self.season.name, self.league.name)

    __str__ = __unicode__

class SeasonsAndWeeks(object):

    def __unicode__(self):
        return u'%s of %s' % (unicode(self.week), unicode(self.season))

    __str__ = __unicode__

class GamesAndRounds(object):

    Admin = ModelAdmin(column_attributes={
        'team_one_color_name': {
            'get_label': lambda game_and_round: u'Team One Color'
        },
        'team_two_color_name': {
            'get_label': lambda game_and_round: u'Team Two Color'
        },
    })

    def __unicode__(self):
        return u'Round #%s of Game %s' % (self.round.id, self.game)

    __str__ = __unicode__

class ForumMembersAndPlayers(object):

    def __unicode__(self):
        return u'Forum Member #%s: %s' % (self.member_id, self.player_name)

    __str__ = __unicode__

    @property
    def member(self):
        q = forum_session.query(ForumMember)
        try:
            return q.filter(ForumMember.id_member==self.member_id).one()
        except NoResultFound:
            return None

    @property
    def member_name(self):
        return self.member.member_name

    @property
    def current_team(self):
        try:
            return idl_session.query(TeamsAndPlayers).filter(and_(
                TeamsAndPlayers.player_name==self.player_name,
                TeamsAndPlayers.date_left==None
            )).one().team
        except NoResultFound:
            return None

###
# Past here are some convenience functions.
###

def administrators():
    return idl_session.query(Administrator).order_by(Administrator.name)

def aliases():
    return idl_session.query(Alias).order_by(Alias.name)

def conferences_and_divisions():
    return idl_session.query(ConferencesAndDivisions)

def conferences():
    return idl_session.query(Conference)

def contributors():
    return idl_session.query(Contributor).order_by(Contributor.name)

def demos():
    return idl_session.query(Demo).order_by(
        Demo.game_id.asc(),
        Demo.team_id.asc(),
        Demo.player_name.asc()
    ).filter(Demo.is_missing==False)

def divisions_and_teams():
    return idl_session.query(DivisionsAndTeams)

def divisions():
    return idl_session.query(Division)

def flag_returns():
    return idl_session.query(FlagReturn)

def flag_touches():
    return idl_session.query(FlagTouch)

def forum_members_and_players():
    return idl_session.query(ForumMembersAndPlayers)

def forum_members():
    return forum_session.query(ForumMember).order_by(ForumMember.member_name)

def frags():
    return idl_session.query(Frag).order_by(Frag.timestamp.desc())

def games_and_rounds():
    return idl_session.query(GamesAndRounds)

def games():
    q = idl_session.query(Game)
    return q.order_by(Game.season_id.desc(), Game.week_id.asc())

def leagues_and_conferences():
    return idl_session.query(LeaguesAndConferences)

def leagues_and_season():
    return idl_session.query(LeaguesAndSeasons)

def leagues():
    return idl_session.query(League).order_by(League.name)

def logs():
    return idl_session.query(Log)

def map_screenshots():
    return idl_session.query(MapScreenShot)

def maps():
    q = idl_session.query(Map).filter(Map.wad_name!=None)
    return q.order_by(Map.wad_name.asc(), Map.number.asc())

def news_items():
    return idl_session.query(NewsItem).order_by(NewsItem.timestamp.desc())

def players():
    return idl_session.query(StoredPlayer).order_by(StoredPlayer.name)

def quotes():
    return idl_session.query(Quote).order_by(Quote.id.desc())

def rcon_accesses():
    return idl_session.query(RCONAccess).order_by(RCONAccess.timestamp.desc())

def rcon_actions():
    return idl_session.query(RCONAction).order_by(RCONAction.timestamp.desc())

def rcon_denials():
    return idl_session.query(RCONDenial).order_by(RCONDenial.timestamp.desc())

def rounds():
    return idl_session.query(Round).order_by(Round.id.asc())

def seasons_and_weeks():
    return idl_session.query(SeasonsAndWeeks)

def seasons():
    q = idl_session.query(Season)
    return q.order_by(Season.year, Season.season.desc())

def servers():
    return idl_session.query(Server).order_by(Server.name, Server.address)

def team_colors():
    return idl_session.query(TeamColor).order_by(TeamColor.color)

def teams_and_players():
    q = idl_session.query(TeamsAndPlayers)
    # Alpha then by season
    return q.order_by(TeamsAndPlayers.player_name, TeamsAndPlayers.season_id)

def teams():
    return idl_session.query(Team).order_by(Team.name)

def wads():
    return idl_session.query(Wad).order_by(Wad.name)

def weapons():
    return idl_session.query(Weapon).order_by(Weapon.name)

def weeks():
    return idl_session.query(Week).order_by(Week.number)

