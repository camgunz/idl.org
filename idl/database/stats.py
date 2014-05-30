import array
import decimal
import operator

from sqlalchemy import func, select, and_

from idl.database import idl_session

from idl.database.tables import aliases_table, flag_touches_table, \
                                flag_returns_table, frags_table, \
                                rounds_and_aliases

def get_team_stats_for_league_and_season(teams, league, season):
    stat_dict = {}
    for game in season.games:
        valid_teams = enumerate((game.team_one, game.team_two))
        valid_teams = [(n, t) for n, t in valid_teams if t in teams]
        if not valid_teams:
            continue
        frag_counts = game.frag_counts_by_team
        flag_capture_counts = game.flag_capture_counts_by_team
        flag_pick_capture_counts = game.flag_pick_capture_counts_by_team
        flag_drop_counts = game.flag_drop_counts_by_team
        flag_return_counts = game.flag_return_counts_by_team
        flag_touch_counts = game.flag_touch_counts_by_team
        flag_pick_counts = game.flag_pick_counts_by_team
        flag_loss_counts = game.flag_loss_counts_by_team
        death_counts = game.death_counts_by_team
        round_count = len(game.rounds)
        for n, team in valid_teams:
            if team not in stat_dict:
                stat_dict[team] = {
                    'frags': 0,
                    'captures': 0,
                    'pick_captures': 0,
                    'drops': 0,
                    'returns': 0,
                    'touches': 0,
                    'picks': 0,
                    'touches_allowed': 0,
                    'losses': 0,
                    'deaths': 0,
                    'rounds': 0
                }
            if n == 0:
                i, j = (0, 1)
            else:
                i, j = (1, 0)
            stat_dict[team]['frags'] += frag_counts[i]
            stat_dict[team]['captures'] += flag_capture_counts[i]
            stat_dict[team]['pick_captures'] += flag_pick_capture_counts[i]
            stat_dict[team]['drops'] += flag_drop_counts[i]
            stat_dict[team]['returns'] += flag_return_counts[i]
            stat_dict[team]['touches'] += flag_touch_counts[i]
            stat_dict[team]['picks'] += flag_pick_counts[i]
            stat_dict[team]['touches_allowed'] += flag_touch_counts[j]
            stat_dict[team]['losses'] += flag_loss_counts[i]
            stat_dict[team]['deaths'] += death_counts[i]
            stat_dict[team]['rounds'] += round_count
    stats = []
    for team, d in stat_dict.items():
        d['name'] = team.tag
        d['flag_ratio'] = (d['captures'], d['touches'])
        d['pick_ratio'] = (d['pick_captures'], d['picks'])
        d['frag_ratio'] = (d['frags'], d['deaths'])
        d['return_ratio'] = (d['returns'], d['drops'])
        d['captures_per_round'] = (d['captures'], d['rounds'])
        d['pick_captures_per_round'] = (d['pick_captures'], d['rounds'])
        d['touches_per_round'] = (d['touches'], d['rounds'])
        d['picks_per_round'] = (d['picks'], d['rounds'])
        d['frags_per_round'] = (d['frags'], d['rounds'])
        d['returns_per_round'] = (d['returns'], d['rounds'])
        stats.append(d)
    return stats

def get_base_player_stats(round_ids):
    fls = select([
        aliases_table.c.stored_player_name,
        func.count(flag_touches_table.c.id)
    ])
    # Flag Touches
    flts = fls.where(and_(
        aliases_table.c.id==flag_touches_table.c.player_id,
        flag_touches_table.c.round_id.in_(round_ids),
        flag_touches_table.c.was_picked==False
    ))
    # Flag Captures
    flcs = fls.where(and_(
        aliases_table.c.id==flag_touches_table.c.player_id,
        flag_touches_table.c.round_id.in_(round_ids),
        flag_touches_table.c.was_picked==False,
        flag_touches_table.c.resulted_in_score==True
    ))
    # Flag Touches
    fpts = fls.where(and_(
        aliases_table.c.id==flag_touches_table.c.player_id,
        flag_touches_table.c.round_id.in_(round_ids),
        flag_touches_table.c.was_picked==True
    ))
    # Flag Captures
    fpcs = fls.where(and_(
        aliases_table.c.id==flag_touches_table.c.player_id,
        flag_touches_table.c.round_id.in_(round_ids),
        flag_touches_table.c.was_picked==True,
        flag_touches_table.c.resulted_in_score==True
    ))
    # Flag Returns
    flrs = select([
        aliases_table.c.stored_player_name,
        func.count(flag_returns_table.c.id)
    ])
    flrs = flrs.where(and_(
        aliases_table.c.id==flag_returns_table.c.player_id,
        flag_returns_table.c.round_id.in_(round_ids)
    ))
    # Frags, Deaths & Drops
    fdrs = select([
        aliases_table.c.stored_player_name,
        func.count(frags_table.c.id)
    ])
    # Frags
    frs = fdrs.where(and_(
        aliases_table.c.id==frags_table.c.fragger_id,
        frags_table.c.round_id.in_(round_ids)
    ))
    # Deaths
    ds = fdrs.where(and_(
        aliases_table.c.id==frags_table.c.fraggee_id,
        frags_table.c.round_id.in_(round_ids)
    ))
    # Drops
    flds = frs.where(frags_table.c.fraggee_was_holding_flag==True)
    # Rounds
    rs = select([
        aliases_table.c.stored_player_name,
        func.count(rounds_and_aliases.c.id)
    ])
    rs = rs.where(and_(
        aliases_table.c.id==rounds_and_aliases.c.alias_id,
        rounds_and_aliases.c.round_id.in_(round_ids)
    ))
    labels = [
        'touches', 'captures', 'picks', 'pick_captures', 'returns',
        'frags', 'deaths', 'drops', 'rounds'
    ]
    indices = range(len(labels))
    sl = dict(zip(labels, [
        flts, flcs, fpts, fpcs, flrs, frs, ds, flds, rs
    ]))
    il = dict(zip(labels, indices))
    stats = dict()
    for label, s in sl.items():
        s = s.group_by(aliases_table.c.stored_player_name)
        s = s.order_by(aliases_table.c.stored_player_name.desc())
        for name, stat in idl_session.connection().execute(s).fetchall():
            if name not in stats:
                stats[name] = array.array('I')
                stats[name].extend([0, 0, 0, 0, 0, 0, 0, 0, 0])
            stats[name][il[label]] = stat
    out = []
    final_labels = ['name'] + labels
    for name, stat_row in stats.items():
        d = dict(zip(final_labels, [name] + list(stat_row)))
        d['flag_ratio'] = (d['captures'], d['touches'])
        d['pick_ratio'] = (d['pick_captures'], d['picks'])
        d['frag_ratio'] = (d['frags'], d['deaths'])
        d['return_ratio'] = (d['returns'], d['drops'])
        d['captures_per_round'] = (d['captures'], d['rounds'])
        d['pick_captures_per_round'] = (d['pick_captures'], d['rounds'])
        d['touches_per_round'] = (d['touches'], d['rounds'])
        d['picks_per_round'] = (d['picks'], d['rounds'])
        d['frags_per_round'] = (d['frags'], d['rounds'])
        d['returns_per_round'] = (d['returns'], d['rounds'])
        out.append(d)
    return out

def _get_stat_key_func(k):
    def stat_key_func(x):
        decimal.setcontext(decimal.ExtendedContext)
        v = x.__getitem__(k)
        if isinstance(v, tuple):
            return decimal.Decimal(v[0]) / decimal.Decimal(v[1])
        return decimal.Decimal(v)
    return stat_key_func

def _get_leaders(base_stats, column):
    return [(x['name'], x[column]) for x in reversed(sorted(
        base_stats, key=_get_stat_key_func(column)
    ))]

def get_flag_captures_per_round_leaders(base_stats):
    return _get_leaders(base_stats, 'captures_per_round')

def get_pick_captures_per_round_leaders(base_stats):
    return _get_leaders(base_stats, 'pick_captures_per_round')

def get_flag_touches_per_round_leaders(base_stats):
    return _get_leaders(base_stats, 'touches_per_round')

def get_flag_picks_per_round_leaders(base_stats):
    return _get_leaders(base_stats, 'picks_per_round')

def get_flag_ratio_leaders(base_stats):
    return _get_leaders(base_stats, 'flag_ratio')

def get_pick_ratio_leaders(base_stats):
    return _get_leaders(base_stats, 'pick_ratio')

def get_flag_touch_leaders(base_stats):
    return _get_leaders(base_stats, 'touches')

def get_flag_pick_leaders(base_stats):
    return _get_leaders(base_stats, 'picks')

def get_flag_capture_leaders(base_stats):
    return _get_leaders(base_stats, 'captures')

def get_flag_pick_capture_leaders(base_stats):
    return _get_leaders(base_stats, 'pick_captures')

def get_frags_per_round_leaders(base_stats):
    return _get_leaders(base_stats, 'frags_per_round')

def get_flag_returns_per_round_leaders(base_stats):
    return _get_leaders(base_stats, 'returns_per_round')

def get_frag_ratio_leaders(base_stats):
    return _get_leaders(base_stats, 'frag_ratio')

def get_flag_return_ratio_leaders(base_stats):
    return _get_leaders(base_stats, 'return_ratio')

def get_frag_leaders(base_stats):
    return _get_leaders(base_stats, 'frags')

def get_flag_return_leaders(base_stats):
    return _get_leaders(base_stats, 'returns')

