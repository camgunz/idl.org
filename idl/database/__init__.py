from sqlalchemy import create_engine, orm, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from idl import app

idl_db_engine   = create_engine(app.config['IDL_DB_URI'])
forum_db_engine = create_engine(app.config['FORUM_DB_URI'])
idl_session     = scoped_session(sessionmaker(bind=idl_db_engine))
forum_session   = scoped_session(sessionmaker(bind=forum_db_engine))
idl_metadata    = MetaData(bind=idl_db_engine)
forum_metadata  = MetaData(bind=forum_db_engine)

import ZDStack
ZDStack.DB_ENGINE = idl_db_engine
ZDStack.DB_METADATA = idl_metadata
ZDStack.DB_AUTOFLUSH = True
ZDStack.DB_AUTOCOMMIT = True
ZDStack.initialize_database()

from models import *
from tables import *
from ZDStack.ZDSModels import TeamColor, Map, StoredPlayer, Round

_pc = 'save-update, delete, delete-orphan'

orm.mapper(ForumMember, smf_members_table)

orm.mapper(ForumBoard, smf_boards_table, properties={
    'topics': orm.relation(
        ForumTopic,
        primaryjoin=smf_boards_table.c.id_board==smf_topics_table.c.id_board,
        foreign_keys=[smf_topics_table.c.id_board],
        backref='board'
    )
})

orm.mapper(ForumTopic, smf_topics_table, properties={
    'messages': orm.relation(
        ForumMessage,
        primaryjoin=smf_topics_table.c.id_topic==smf_messages_table.c.id_topic,
        foreign_keys=[smf_messages_table.c.id_topic],
        backref='topic'
    )
})

orm.mapper(ForumMessage, smf_messages_table)

orm.mapper(Team, teams_table, properties={
    'players': orm.relation(StoredPlayer, backref='teams',
                            secondary=teams_and_players_table),
    'seasons': orm.relation(Season, backref='teams',
                            secondary=teams_and_players_table)
})

orm.mapper(Administrator, administrators_table, properties={
    'player': orm.relation(StoredPlayer, backref='administrator')
})

orm.mapper(Server, servers_table)

orm.mapper(Contributor, contributors_table)

orm.mapper(Demo, demos_table, properties={
    'player': orm.relation(StoredPlayer, backref='demos'),
    'team': orm.relation(Team, backref='demos'),
    'game': orm.relation(Game, backref='demos')
})

orm.mapper(MapScreenShot, map_screenshots_table, properties={
    'map': orm.relation(Map, backref='screenshot')
})

orm.mapper(Quote, quotes_table)

orm.mapper(NewsItem, news_items_table)

orm.mapper(Log, logs_table, properties ={
    'game': orm.relation(Game, backref='log')
})

orm.mapper(League, leagues_table, properties={
    'conferences': orm.relation(Conference, backref='leagues',
                                secondary=leagues_and_conferences_table),
    'seasons': orm.relation(Season, backref='leagues',
                            secondary=leagues_and_seasons_table)
})

orm.mapper(Conference, conferences_table, properties={
    'divisions': orm.relation(Division, backref='conferences',
                              secondary=conferences_and_divisions_table),
    'seasons': orm.relation(Season, backref='conferences',
                            secondary=conferences_and_divisions_table)
})

orm.mapper(Division, divisions_table, properties={
    'teams': orm.relation(Team, backref='divisions',
                          secondary=divisions_and_teams_table),
    'seasons': orm.relation(Season, backref='divisions',
                            secondary=divisions_and_teams_table)
})

orm.mapper(Season, seasons_table, properties={
    'weeks': orm.relation(Week,
        backref='seasons',
        order_by=weeks_table.c.number.asc(),
        secondary=seasons_and_weeks_table
    ),
    'maps': orm.relation(Map,
        backref='seasons',
        secondary=seasons_and_weeks_table
    )
})

orm.mapper(Week, weeks_table, properties={
    'maps': orm.relation(Map, backref='weeks',
                         secondary=seasons_and_weeks_table)
})

orm.mapper(Game, games_table, properties={
    'week': orm.relation(Week, backref='games'),
    'season': orm.relation(Season, backref='games'),
    'league': orm.relation(League, backref='games'),
    'rounds': orm.relation(Round, backref='game',
                           secondary=games_and_rounds_table,
                           order_by=rounds_table.c.start_time),
    'team_one': orm.relation(Team,
      primaryjoin=games_table.c.team_one_id==teams_table.c.id),
    'team_two': orm.relation(Team,
      primaryjoin=games_table.c.team_two_id==teams_table.c.id),
    'forfeiting_team': orm.relation(Team,
      primaryjoin=games_table.c.forfeiting_team_id==teams_table.c.id),
    'forced_winner': orm.relation(Team,
      primaryjoin=games_table.c.forced_winner_id==teams_table.c.id)
})

orm.mapper(LeaguesAndConferences, leagues_and_conferences_table,
    properties={
        'league': orm.relation(League),
        'conference': orm.relation(Conference),
        'season': orm.relation(Season)
    }
)

orm.mapper(ConferencesAndDivisions, conferences_and_divisions_table,
    properties={
        'conference': orm.relation(Conference),
        'division': orm.relation(Division),
        'season': orm.relation(Season)
    }
)

orm.mapper(DivisionsAndTeams, divisions_and_teams_table, properties={
    'division': orm.relation(Division),
    'team': orm.relation(Team),
    'season': orm.relation(Season),
    'homefield_map': orm.relation(Map)
})

orm.mapper(TeamsAndPlayers, teams_and_players_table, properties={
    'team': orm.relation(Team),
    'player': orm.relation(StoredPlayer),
    'season': orm.relation(Season)
})

orm.mapper(LeaguesAndSeasons, leagues_and_seasons_table, properties={
    'league': orm.relation(League),
    'season': orm.relation(Season)
})

orm.mapper(SeasonsAndWeeks, seasons_and_weeks_table, properties={
    'season': orm.relation(Season),
    'week': orm.relation(Week),
    'map': orm.relation(Map)
})

orm.mapper(GamesAndRounds, games_and_rounds_table, properties={
    'round': orm.relation(Round),
    'game': orm.relation(Game),
    'team_one_color': orm.relation(TeamColor,
      primaryjoin=games_and_rounds_table.c.team_one_color_name==\
                  team_colors_table.c.color),
    'team_two_color': orm.relation(TeamColor,
      primaryjoin=games_and_rounds_table.c.team_two_color_name==\
                  team_colors_table.c.color)
})

orm.mapper(ForumMembersAndPlayers, forum_members_and_players_table,
    properties={
        'player': orm.relation(StoredPlayer, backref='forum_membership')
    }
)

admin_models = [
    models.Administrator,
    models.Alias,
    models.ConferencesAndDivisions,
    models.Conference,
    models.Contributor,
    models.Demo,
    models.DivisionsAndTeams,
    models.Division,
    models.FlagReturn,
    models.FlagTouch,
    models.ForumMembersAndPlayers,
    models.ForumMember,
    models.Frag,
    models.GamesAndRounds,
    models.Game,
    models.LeaguesAndConferences,
    models.LeaguesAndSeasons,
    models.League,
    models.Log,
    models.MapScreenShot,
    models.Map,
    models.NewsItem,
    models.Quote,
    models.RCONAccess,
    models.RCONAction,
    models.RCONDenial,
    models.Round,
    models.SeasonsAndWeeks,
    models.Season,
    models.Server,
    models.StoredPlayer,
    models.TeamColor,
    models.TeamsAndPlayers,
    models.Team,
    models.Wad,
    models.Weapon,
    models.Week
]

admin_getters = [
    lambda self: models.administrators(),
    lambda self: models.aliases(),
    lambda self: models.conferences_and_divisions(),
    lambda self: models.conferences(),
    lambda self: models.contributors(),
    lambda self: models.demos(),
    lambda self: models.divisions_and_teams(),
    lambda self: models.divisions(),
    lambda self: models.flag_returns(),
    lambda self: models.flag_touches(),
    lambda self: models.forum_members_and_players(),
    lambda self: models.forum_members(),
    lambda self: models.frags(),
    lambda self: models.games_and_rounds(),
    lambda self: models.games(),
    lambda self: models.leagues_and_conferences(),
    lambda self: models.leagues_and_season(),
    lambda self: models.leagues(),
    lambda self: models.logs(),
    lambda self: models.map_screenshots(),
    lambda self: models.maps(),
    lambda self: models.news_items(),
    lambda self: models.quotes(),
    lambda self: models.rcon_accesses(),
    lambda self: models.rcon_actions(),
    lambda self: models.rcon_denials(),
    lambda self: models.rounds(),
    lambda self: models.seasons_and_weeks(),
    lambda self: models.seasons(),
    lambda self: models.servers(),
    lambda self: models.players(),
    lambda self: models.team_colors(),
    lambda self: models.teams_and_players(),
    lambda self: models.teams(),
    lambda self: models.wads(),
    lambda self: models.weapons(),
    lambda self: models.weeks()
]

def _old_display_map(map, max=15):
    if len(map.name) > max:
        map_name = map.name[:max].rstrip() + u'...'
    else:
        map_name = map.name
    if map.wad and map.wad.short_name and map.wad.prefix and map.number:
        if map.wad.prefix == map.wad.short_name:
            temp = u'%s - MAP%s: %s'
            return temp % (map.wad_name, unicode(map.number).zfill(2),
                           map_name)
        else:
            return u'%s: %s' % (map.short_name, map_name)
    elif map.number:
        return u'MAP%s' % (unicode(map.number).zfill(2))
    else:
        return u''

def _display_map(map, max=15):
    if map.wad and map.wad.short_name and map.wad.prefix and map.number:
        if map.wad.prefix == map.wad.short_name:
            temp = u'%s - MAP%s: %s'
            out = temp % (map.wad_name, unicode(map.number).zfill(2),
                          map.name)
        else:
            out = u'%s: %s' % (map.short_name, map.name)
    elif map.number:
        out = u'MAP%s' % (unicode(map.number).zfill(2))
    else:
        out = u''
    if len(out) > 40:
        out = out[:40] + u'...'
    return out

def display_map(self, map):
    return _display_map(map)

def display_round(self, round):
    ts_format = '%Y-%m-%d %H:%M'
    if round.map.wad_name:
        temp = u'Round %d: MAP%s of %s at %s'
        return temp % (round.id, round.map.number, round.map.wad_name,
                       round.start_time.strftime(ts_format))
    else:
        temp = u'Round %d: MAP%s (%s) at %s'
        if len(round.map.name) > 18:
            map_name = round.map.name[:18] + u'...'
        else:
            map_name = round.map.name
        return temp % (round.id, round.map.number, map_name,
                       round.start_time.strftime(ts_format))

def display_map_screenshot(self, ss):
    return u'Screenshot for %s' % (_display_map(ss.map, max=22))

display_models = (models.Alias, models.Map, models.Round,
                  models.MapScreenShot, models.StoredPlayer, models.Weapon,
                  models.TeamColor)
# models.ConferenceAndDivisions
# lambda self, x: u'%s, member of %s' % (x.division, x.conference),
display_funcs = (
    lambda self, x: u'%s (%s)' % (x.name, x.ip_address),
    display_map,
    display_round,
    display_map_screenshot,
    lambda self, x: x.name,
    lambda self, x: x.name,
    lambda self, x: x.color
)

###
# Setup admin features
###
from idl import saadmin
saadmin.ColumnTypes.add_postgres_column_types()
saadmin.set_global_session(idl_session)
saadmin.set_models(admin_models)
for model, getter in zip(admin_models, admin_getters):
    saadmin.set_getter(model, getter)
for model, display in zip(display_models, display_funcs):
    saadmin.set_display(model, display)
saadmin.activate_all()
