from datetime import timedelta

from flask import abort

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from idl import app
from idl.database import idl_session
from idl.database.models import Wad, Map, Round, Frag, FlagTouch
from idl.views.utils import get_latest_games, render_template

ten_minutes = timedelta(seconds=60 * 10)

def timedelta_to_seconds(td):
    return (td.days * 86400) + td.seconds

def get_map_stats(map):
    rounds = idl_session.query(Round).filter(Round.map==map).all()
    if not rounds:
        return None
    round_ids = [r.id for r in rounds]
    round_count = len(rounds)
    timed_round_count = round_count
    total_round_duration = 0
    for r in rounds:
        if r.start_time is None or r.end_time is None:
            timed_round_count -= 1
            continue
        else:
            total_round_duration += timedelta_to_seconds(
                r.end_time - r.start_time
            )
    q = idl_session.query(Frag).filter(Frag.round_id.in_(round_ids))
    total_frags = q.count()
    total_suicides = q.filter(Frag.fragger_id==Frag.fraggee_id).count()
    q = idl_session.query(FlagTouch).filter(FlagTouch.round_id.in_(round_ids))
    total_flag_touches = q.filter(FlagTouch.was_picked==False).count()
    total_flag_picks = q.filter(FlagTouch.was_picked==True).count()
    q = q.filter(FlagTouch.resulted_in_score==True)
    total_flag_captures = q.filter(FlagTouch.was_picked==False).count()
    total_flag_pick_captures = q.filter(FlagTouch.was_picked==True).count()
    timed_flag_captures = total_flag_captures
    total_flag_run_time = 0
    for flag_capture in q.filter(FlagTouch.was_picked==False).all():
        if not (flag_capture.touch_time and flag_capture.loss_time):
            timed_flag_captures -= 1
            continue
        total_flag_run_time += timedelta_to_seconds(
            flag_capture.loss_time - flag_capture.touch_time
        )
    return {
        'round_count': round_count,
        'timed_round_count': timed_round_count,
        'total_round_duration': total_round_duration,
        'total_frags': total_frags,
        'total_suicides': total_suicides,
        'total_flag_touches': total_flag_touches,
        'total_flag_picks': total_flag_picks,
        'total_flag_captures': total_flag_captures,
        'total_flag_pick_captures': total_flag_pick_captures,
        'timed_flag_captures': timed_flag_captures,
        'total_flag_run_time': total_flag_run_time
    }

@app.route('/profiles/maps')
def map_profiles():
    wads = idl_session.query(Wad).order_by(Wad.name).all()
    if not wads:
        abort(404)
    wad = wads[0]
    maps = idl_session.query(Map).filter_by(wad=wad).order_by(Map.number).all()
    if not maps:
        abort(404)
    map = maps[0]

    return render_template('map_profiles.mako', **{
        'section': 'profiles',
        'subsection': 'maps',
        'wads': wads,
        'wad': wad,
        'map': map,
        'maps': maps,
        'stats': get_map_stats(map)
    })

@app.route('/profiles/maps/<wad_name>')
def wads(wad_name):
    wads = idl_session.query(Wad).order_by(Wad.name).all()
    if not wads:
        abort(404)
    try:
        wad = idl_session.query(Wad).filter_by(name=wad_name).one()
    except (NoResultFound, MultipleResultsFound), e:
        abort(404)
    maps = idl_session.query(Map).filter_by(wad=wad).order_by(Map.number).all()
    if not maps:
        abort(404)
    map = maps[0]

    return render_template('map_profiles.mako', **{
        'section': 'profiles',
        'subsection': 'maps',
        'wads': wads,
        'wad': wad,
        'maps': maps,
        'map': map,
        'stats': get_map_stats(map)
    })

@app.route('/profiles/maps/<wad_name>/<int:map_number>')
def maps(wad_name, map_number):
    wads = idl_session.query(Wad).order_by(Wad.name).all()
    if not wads:
        abort(404)
    try:
        wad = idl_session.query(Wad).filter_by(name=wad_name).one()
    except (NoResultFound, MultipleResultsFound), e:
        abort(404)
    maps = idl_session.query(Map).filter_by(wad=wad).order_by(Map.number).all()
    if not maps:
        abort(404)
    try:
        q = idl_session.query(Map)
        map = q.filter(and_(Map.wad==wad, Map.number==map_number)).one()
    except (NoResultFound, MultipleResultsFound), e:
        abort(404)

    return render_template('map_profiles.mako', **{
        'section': 'profiles',
        'subsection': 'maps',
        'wads': wads,
        'wad': wad,
        'maps': maps,
        'map': map,
        'stats': get_map_stats(map)
    })

