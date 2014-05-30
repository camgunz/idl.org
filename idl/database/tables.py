import datetime

import sqlalchemy as sa

from idl.database import idl_metadata, forum_metadata

from ZDStack.ZDSTables import *

smf_members_table = sa.Table('idlsmf_members', forum_metadata, autoload=True)
smf_boards_table = sa.Table('idlsmf_boards', forum_metadata, autoload=True)
smf_topics_table = sa.Table('idlsmf_topics', forum_metadata, autoload=True)
smf_messages_table = sa.Table('idlsmf_messages', forum_metadata, autoload=True)

administrators_table = sa.Table('idl_administrators', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('name', sa.Unicode(255), sa.ForeignKey('stored_players.name')),
  sa.Column('position', sa.Unicode(255), nullable=False),
  sa.Column('date_joined', sa.DateTime, default=datetime.datetime.now),
  sa.Column('date_left', sa.DateTime, default=None)
)

servers_table = sa.Table('idl_servers', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('name', sa.Unicode(255), nullable=False),
  sa.Column('address', sa.Unicode(255), nullable=False),
  sa.Column('password', sa.Unicode(255))
)

contributors_table = sa.Table('idl_contributors', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('name', sa.Unicode(255), nullable=False),
  sa.Column('contribution', sa.Unicode(255), nullable=False),
  sa.Column('link', sa.Unicode(255), nullable=True, default=None)
)

demos_table = sa.Table('idl_demos', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('file_name', sa.Unicode(100), nullable=True),
  sa.Column('player_name', sa.Unicode(255),
                           sa.ForeignKey('stored_players.name')),
  sa.Column('team_id', sa.Integer, sa.ForeignKey('idl_teams.id')),
  sa.Column('game_id', sa.Integer, sa.ForeignKey('idl_games.id')),
  sa.Column('timestamp', sa.DateTime, default=datetime.datetime.now),
  sa.Column('is_missing', sa.Boolean, default=False)
)

map_screenshots_table = sa.Table('idl_screenshots', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('file_name', sa.Unicode(100)),
  sa.Column('map_id', sa.Integer, sa.ForeignKey('maps.id')),
  sa.Column('thumbnail_file_name', sa.Unicode(100))
)

quotes_table = sa.Table('idl_quotes', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('body', sa.UnicodeText)
)

news_items_table = sa.Table('idl_news_items', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('title', sa.Unicode(100), nullable=True),
  sa.Column('body', sa.UnicodeText, nullable=True),
  sa.Column('timestamp', sa.DateTime, default=datetime.datetime.now),
  sa.Column('add_to_scroller', sa.Boolean, default=True),
  sa.Column('is_old', sa.Boolean, default=False)
)

logs_table = sa.Table('idl_logs', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('game_id', sa.Integer, sa.ForeignKey('idl_games.id')),
  sa.Column('logtype', sa.String(10))
)

leagues_table = sa.Table('idl_leagues', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('name', sa.Unicode(100), nullable=False, unique=True),
  sa.Column('short_name', sa.String(10), nullable=False, unique=True)
)

conferences_table = sa.Table('idl_conferences', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('name', sa.Unicode(30), nullable=False, unique=True)
)

divisions_table = sa.Table('idl_divisions', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('name', sa.Unicode(30), nullable=False, unique=True)
)

teams_table = sa.Table('idl_teams', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('name', sa.Unicode(100), nullable=False, unique=True),
  sa.Column('tag', sa.Unicode(5)),
  sa.Column('game_tag', sa.Unicode(15)),
  sa.Column('logo_file', sa.Unicode(100), nullable=True)
)

seasons_table = sa.Table('idl_seasons', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('season', sa.Unicode(6), nullable=False),
  sa.Column('year', sa.Integer, nullable=False),
  sa.Column('wad', sa.String(20), sa.ForeignKey('wads.name')),
  sa.UniqueConstraint('season', 'year')
)

weeks_table = sa.Table('idl_weeks', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('number', sa.Integer, nullable=False),
  sa.Column('name', sa.Unicode(40)),
  sa.UniqueConstraint('number', 'name')
)

games_table = sa.Table('idl_games', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('week_id', sa.Integer,
                       sa.ForeignKey('idl_weeks.id'),
                       nullable=False),
  sa.Column('season_id', sa.Integer,
                         sa.ForeignKey('idl_seasons.id'),
                         nullable=False),
  sa.Column('league_id', sa.Integer,
                         sa.ForeignKey('idl_leagues.id'),
                         nullable=False),
  sa.Column('team_one_id', sa.Integer,
                           sa.ForeignKey('idl_teams.id'),
                           nullable=False),
  sa.Column('team_two_id', sa.Integer,
                           sa.ForeignKey('idl_teams.id'),
                           nullable=False),
  sa.Column('scheduled_for', sa.DateTime, nullable=True),
  sa.Column('has_been_played', sa.Boolean, default=False),
  sa.Column('forfeiting_team_id', sa.Integer,
                                  sa.ForeignKey('idl_teams.id'),
                                  default=None,
                                  nullable=True),
  sa.Column('overturned', sa.Boolean, default=False),
  sa.Column('forced_winner_id', sa.Integer,
                                sa.ForeignKey('idl_teams.id'),
                                nullable=True),
)

leagues_and_conferences_table = sa.Table('idl_leagues_and_conferences',
  idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('league_id', sa.Integer, sa.ForeignKey('idl_leagues.id'),
                         nullable=False),
  sa.Column('conference_id', sa.Integer,
                             sa.ForeignKey('idl_conferences.id'),
                             nullable=False),
  sa.Column('season_id', sa.Integer, sa.ForeignKey('idl_seasons.id'),
                         nullable=False),
  sa.Column('date_joined', sa.DateTime, default=datetime.datetime.now),
  sa.Column('date_left', sa.DateTime, nullable=True)
)

conferences_and_divisions_table = sa.Table('idl_conferences_and_divisions',
  idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('conference_id', sa.Integer,
                             sa.ForeignKey('idl_conferences.id'),
                             nullable=False),
  sa.Column('division_id', sa.Integer,
                           sa.ForeignKey('idl_divisions.id'),
                           nullable=False),
  sa.Column('season_id', sa.Integer, sa.ForeignKey('idl_seasons.id'),
                         nullable=False),
  sa.Column('date_joined', sa.DateTime, default=datetime.datetime.now),
  sa.Column('date_left', sa.DateTime, nullable=True)
)

divisions_and_teams_table = sa.Table('idl_divisions_and_teams', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('division_id', sa.Integer,
                           sa.ForeignKey('idl_divisions.id'),
                           nullable=False),
  sa.Column('team_id', sa.Integer, sa.ForeignKey('idl_teams.id'),
                       nullable=False),
  sa.Column('season_id', sa.Integer, sa.ForeignKey('idl_seasons.id'),
                         nullable=False),
  sa.Column('clinched_playoffs', sa.Boolean, default=False),
  sa.Column('clinched_division', sa.Boolean, default=False),
  sa.Column('clinched_homefield', sa.Boolean, default=False),
  sa.Column('playoff_seed', sa.Integer, nullable=True),
  sa.Column('date_joined', sa.DateTime, default=datetime.datetime.now),
  sa.Column('date_left', sa.DateTime, nullable=True),
  sa.Column('homefield_map_id', sa.Integer, sa.ForeignKey('maps.id'),
                                nullable=True)
)

teams_and_players_table = sa.Table('idl_teams_and_players', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('team_id', sa.Integer, sa.ForeignKey('idl_teams.id'),
                       nullable=False),
  sa.Column('player_name', sa.Unicode(255),
                           sa.ForeignKey('stored_players.name'),
                           nullable=False),
  sa.Column('season_id', sa.Integer, sa.ForeignKey('idl_seasons.id'),
                         nullable=False),
  sa.Column('as_captain', sa.Boolean, default=False),
  sa.Column('date_joined', sa.DateTime, default=datetime.datetime.now),
  sa.Column('date_left', sa.DateTime, nullable=True)
)

leagues_and_seasons_table = sa.Table('idl_leagues_and_seasons', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('league_id', sa.Integer, sa.ForeignKey('idl_leagues.id'),
                         nullable=False),
  sa.Column('season_id', sa.Integer, sa.ForeignKey('idl_seasons.id'),
                         nullable=False)
)

seasons_and_weeks_table = sa.Table('idl_seasons_and_weeks', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('season_id', sa.Integer, sa.ForeignKey('idl_seasons.id'),
                         nullable=False),
  sa.Column('week_id', sa.Integer, sa.ForeignKey('idl_weeks.id'),
                       nullable=False),
  sa.Column('map_id', sa.Integer, sa.ForeignKey('maps.id'), nullable=True),
  sa.Column('date_joined', sa.DateTime, default=datetime.datetime.now),
  sa.Column('date_left', sa.DateTime, nullable=True)
)

games_and_rounds_table = sa.Table('idl_games_and_rounds', idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('game_id', sa.Integer, sa.ForeignKey('idl_games.id'),
                       nullable=False),
  sa.Column('round_id', sa.Integer, sa.ForeignKey('rounds.id'),
                        nullable=False),
  sa.Column('team_one_color_name', sa.String(10),
                                   sa.ForeignKey('team_colors.color'),
                                   nullable=False),
  sa.Column('team_two_color_name', sa.String(10),
                                   sa.ForeignKey('team_colors.color'),
                                   nullable=False)
)

forum_members_and_players_table = sa.Table('idl_forum_members_and_players',
  idl_metadata,
  sa.Column('id', sa.Integer, primary_key=True),
  sa.Column('member_id', sa.Integer, nullable=False),
  sa.Column('player_name', sa.Unicode(255),
                           sa.ForeignKey('stored_players.name'),
                           nullable=False),
  sa.UniqueConstraint('member_id', 'player_name')
)

