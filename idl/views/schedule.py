from flask import session

from idl import app
from idl.database import idl_session
from idl.database.models import League, seasons
from idl.views.utils import render_template, set_session_defaults

@app.route('/season/schedule')
def schedule():
    set_session_defaults()
    return render_template('schedule.mako', **{
        'section': 'season',
        'subsection': 'schedule',
        'league': idl_session.query(League).filter_by(short_name='IDL').one(),
        'seasons': seasons().all(),
        'schedule_type': 'regular_season',
        'weeks': session["season"].regular_season_weeks
    })

@app.route('/season/playoffs')
def playoffs():
    set_session_defaults()
    return render_template('schedule.mako', **{
        'section': 'season',
        'subsection': 'schedule',
        'league': idl_session.query(League).filter_by(short_name='IDL').one(),
        'seasons': seasons().all(),
        'schedule_type': 'playoffs',
        'weeks': session["season"].playoff_weeks
    })

