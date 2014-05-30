import decimal
import operator

from flask import abort

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from idl import app
from idl.database import idl_session
from idl.database.models import Game, MapScreenShot
from idl.views.utils import render_template

def build_stars(game):
    ###
    # [CG] This should probably go in the template.
    ###
    star_categories = (
        'Top Runners', 'Top Fraggers', 'Most Eff. Runners',
        'Most Eff. Fraggers'
    )
    star_units = ('Caps', 'Frags', 'Cap Ratio', 'Frag Ratio')
    star_keys = ('flag_count', 'frag_count', 'flag_ratio', 'frag_ratio')
    _game_stars = game.stars
    game_stars = [
        (star_categories[i], star_units[i], _game_stars[star_keys[i]])
        for i in range(len(_game_stars))
    ]

def build_frag_chart(frags):
    ids_to_names = {}
    frag_count_chart = {}
    for frag in frags:
        if frag.fragger_id == frag.fraggee_id:
            continue
        if frag.fragger_id not in ids_to_names:
            ids_to_names[frag.fragger_id] = frag.fragger.stored_player.name
        if frag.fraggee_id not in ids_to_names:
            ids_to_names[frag.fraggee_id] = frag.fraggee.stored_player.name
        fragger = ids_to_names[frag.fragger_id]
        fraggee = ids_to_names[frag.fraggee_id]
        if fragger not in frag_count_chart:
            frag_count_chart[fragger] = {fraggee: 1}
        elif fraggee not in frag_count_chart[fragger]:
            frag_count_chart[fragger][fraggee] = 1
        else:
            frag_count_chart[fragger][fraggee] += 1
    names = set()
    for fragger in frag_count_chart:
        for fraggee in frag_count_chart[fragger]:
            names.add(fraggee)
        names.add(fragger)
    return frag_count_chart

def build_stats(game):
    frag_counts = game.frag_counts_by_round_and_team
    flag_pick_capture_counts = game.flag_pick_capture_counts_by_round_and_team
    flag_capture_counts = game.flag_capture_counts_by_round_and_team
    flag_drop_counts = game.flag_drop_counts_by_round_and_team
    flag_return_counts = game.flag_return_counts_by_round_and_team
    flag_touch_counts = game.flag_touch_counts_by_round_and_team
    flag_pick_counts = game.flag_pick_counts_by_round_and_team
    flag_loss_counts = game.flag_loss_counts_by_round_and_team
    death_counts = game.death_counts_by_round_and_team
    round_counts = game.round_counts
    round_count = len(game.rounds)
    game_result = u'%s %d - %s %d' % (game.team_one.tag, round_counts[0],
                                      game.team_two.tag, round_counts[1])
    game_overview = []
    getters = [(operator.itemgetter(0), operator.itemgetter(1)),
               (operator.itemgetter(1), operator.itemgetter(0))]
    for f, of in getters:
        game_overview.append({
            'frags': sum([f(x) for x in frag_counts]),
            'flag_captures': sum([f(x) for x in flag_capture_counts]),
            'flag_pick_captures': sum([f(x) for x in flag_pick_capture_counts]),
            'flag_drops': sum([f(x) for x in flag_drop_counts]),
            'flag_returns': sum([f(x) for x in flag_return_counts]),
            'flag_touches': sum([f(x) for x in flag_touch_counts]),
            'flag_picks': sum([f(x) for x in flag_pick_counts]),
            'touches_allowed': sum([of(x) for x in flag_touch_counts]),
            'flag_losses': sum([f(x) for x in flag_loss_counts]),
            'deaths': sum([f(x) for x in death_counts])
        })
    round_overviews = []
    for n, round in enumerate(game.rounds):
        team_overviews = []
        for f, of in getters:
            team_overviews.append({
                'frags': f(frag_counts[n]),
                'flag_captures': f(flag_capture_counts[n]),
                'flag_pick_captures': f(flag_pick_capture_counts[n]),
                'flag_drops': f(flag_drop_counts[n]),
                'flag_returns': f(flag_return_counts[n]),
                'flag_touches': f(flag_touch_counts[n]),
                'flag_picks': f(flag_pick_counts[n]),
                'touches_allowed': of(flag_touch_counts[n]),
                'flag_losses': f(flag_loss_counts[n]),
                'deaths': f(death_counts[n])
            })
        round_overviews.append(team_overviews)
    gs = {
        'touches': {},
        'picks': {},
        'captures': {},
        'pick_captures': {},
        'drops': {},
        'returns': {},
        'frags': {},
        'deaths': {},
    } # [CG] "game state", abbreviated to avoid > 80 char lines.
    round_stats = []
    round_frag_charts = []
    ids_to_names = {}
    for round in game.rounds:
        d = {
            'touches': {},
            'picks': {},
            'captures': {},
            'pick_captures': {},
            'drops': {},
            'returns': {},
            'frags': {},
            'deaths': {},
        }
        for frag in round.frags:
            if frag.fragger_id not in ids_to_names:
                ids_to_names[frag.fragger_id] = frag.fragger.stored_player.name
            if frag.fraggee_id not in ids_to_names:
                ids_to_names[frag.fraggee_id] = frag.fraggee.stored_player.name
            if ids_to_names[frag.fragger_id] not in d['frags']:
                d['frags'][ids_to_names[frag.fragger_id]] = 0
            if ids_to_names[frag.fragger_id] not in gs['frags']:
                gs['frags'][ids_to_names[frag.fragger_id]] = 0
            if ids_to_names[frag.fraggee_id] not in d['deaths']:
                d['deaths'][ids_to_names[frag.fraggee_id]] = 0
            if ids_to_names[frag.fraggee_id] not in gs['deaths']:
                gs['deaths'][ids_to_names[frag.fraggee_id]] = 0
            if not frag.fragger_id == frag.fraggee_id:
                d['frags'][ids_to_names[frag.fragger_id]] += 1
                gs['frags'][ids_to_names[frag.fragger_id]] += 1
                if frag.fraggee_was_holding_flag:
                    if ids_to_names[frag.fragger_id] not in d['drops']:
                        d['drops'][ids_to_names[frag.fragger_id]] = 1
                    else:
                        d['drops'][ids_to_names[frag.fragger_id]] += 1
                    if ids_to_names[frag.fragger_id] not in gs['drops']:
                        gs['drops'][ids_to_names[frag.fragger_id]] = 1
                    else:
                        gs['drops'][ids_to_names[frag.fragger_id]] += 1
            d['deaths'][ids_to_names[frag.fraggee_id]] += 1
            gs['deaths'][ids_to_names[frag.fraggee_id]] += 1
        for flag_touch in round.flag_touches:
            if flag_touch.player_id not in ids_to_names:
                ids_to_names[flag_touch.player_id] = \
                    flag_touch.alias.stored_player.name
            if flag_touch.was_picked:
                k = 'picks'
                ck = 'pick_captures'
            else:
                k = 'touches'
                ck = 'captures'
            if ids_to_names[flag_touch.player_id] not in d[k]:
                d[k][ids_to_names[flag_touch.player_id]] = 1
            else:
                d[k][ids_to_names[flag_touch.player_id]] += 1
            if ids_to_names[flag_touch.player_id] not in gs[k]:
                gs[k][ids_to_names[flag_touch.player_id]] = 1
            else:
                gs[k][ids_to_names[flag_touch.player_id]] += 1
            if flag_touch.resulted_in_score:
                if ids_to_names[flag_touch.player_id] not in d[ck]:
                    d[ck][ids_to_names[flag_touch.player_id]] = 1
                else:
                    d[ck][ids_to_names[flag_touch.player_id]] += 1
                if ids_to_names[flag_touch.player_id] not in gs[ck]:
                    gs[ck][ids_to_names[flag_touch.player_id]] = 1
                else:
                    gs[ck][ids_to_names[flag_touch.player_id]] += 1
        for flag_return in round.flag_returns:
            if flag_return.player_id not in ids_to_names:
                ids_to_names[flag_return.player_id] = \
                    flag_return.alias.stored_player.name
            if ids_to_names[flag_return.player_id] not in d['returns']:
                d['returns'][ids_to_names[flag_return.player_id]] = 1
            else:
                d['returns'][ids_to_names[flag_return.player_id]] += 1
            if ids_to_names[flag_return.player_id] not in gs['returns']:
                gs['returns'][ids_to_names[flag_return.player_id]] = 1
            else:
                gs['returns'][ids_to_names[flag_return.player_id]] += 1
        round_stats.append(d)
        round_frag_charts.append(build_frag_chart(round.frags))

    return (
        ids_to_names.values(), game_overview, round_overviews, gs, round_stats,
        build_frag_chart(game.frags), round_frag_charts
    ) # [CG] Whew!

@app.route('/season/games/<int:game_id>')
def game_results(game_id):
    try:
        game = idl_session.query(Game).filter(Game.id==game_id).one()
    except (MultipleResultsFound, NoResultFound), e:
        print 'Exception 1'
        abort(404)

    decimal.prec = 4
    decimal.setcontext(decimal.ExtendedContext)

    stars = build_stars(game)
    (names, game_overview, round_overviews, game_stats, round_stats,
     game_frag_charts, round_frag_charts) = build_stats(game)

    return render_template('game_results.mako', **{
        'section': 'season',
        'subsection': 'games',
        'game': game,
        'stars': stars,
        'names': names,
        'team_colors': game.team_colors,
        'round_counts': game.round_counts,
        'flag_captures': game.total_flag_captures_by_round,
        'flag_capture_counts': game.flag_capture_counts_by_round_and_team,
        'total_flag_capture_counts':
            game.total_flag_capture_counts_by_round_and_team,
        'game_overview': game_overview,
        'round_overviews': round_overviews,
        'game_stats': game_stats,
        'round_stats': round_stats,
        'game_frag_charts': game_frag_charts,
        'round_frag_charts': round_frag_charts
    })

