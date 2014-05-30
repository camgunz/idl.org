from flask import redirect

from idl import app
from idl.views.utils import render_template

@app.route('/media')
def media():
    return render_template('media.mako', **{
        'section': 'media',
        'subsection': 'media'
    })

