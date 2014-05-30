from flask import g

from idl import app
from idl.cache.kyoto_tycoon import KyotoTycoonCache
from idl.cache.sqlite import SQLiteCache

cache = None

def init():
    global cache
    if app.config.get('SQLITE_DB_FILE', None):
        cache = SQLiteCache()
    else:
        cache = KyotoTycoonCache()

###
# Models:
#
# Division.get_conference_for_season
#   'divisions', 'conference', season.id, self.id
# Team.get_division_for_season
#   'teams', 'division', season.id, self.id
# Team.get_regular_season_info 
#   'teams', 'regular_season_info', season.id, self.id
# Team.get_conference_record
#   'teams', 'conference_record', season.id, conference.id, division.id, self.id
# Team.get_division_record
#   'teams', 'division_record', season.id, conference.id, division.id, self.id
# Game.stars
#   'games', 'stars', self.id
# 
# Views:
#
# season_stats.py
#   season_player_stats
#     'season', 'stats', 'players', season.id, league.id
#   season_team_stats
#     'season', 'stats', 'teams', season.id, league.id
# player_profiles.py
#   render_player_profile
#     'profiles', 'players', player.name
###

