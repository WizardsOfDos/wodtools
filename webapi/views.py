from flask import render_template, request
from flgproc.collector.demo import inpython_collector
from flgproc.exceptions import FlagException

from webapi import app
from webapi.view_filters import acceptable_content_types


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/flag', methods=['POST'])
@acceptable_content_types(['text/plain', 'application/x-www-form-urlencoded'])
def submit_flag():
    flags = {}
    if request.headers['Content-Type'] == 'text/plain':
        flags = request.data.decode().strip().split('\n')
    elif request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        flags = [request.form['flag']]
    flag_parameters = request.args.to_dict(True)
    results = []
    for flag in flags:
        try:
            inpython_collector(flag, **flag_parameters)
            results.append((flag, 'OK'))
        except FlagException as e:
            results.append((flag, e.reason))
    return render_template('submit_results.html', results=results)
