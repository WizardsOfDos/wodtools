from flask import render_template, request

from webapi import app
from flgproc.collector.demo import inpython_collector
from flgproc.exceptions import FlagException


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/flag', methods=['POST'])
def submit_flag():
    flags = request.data.decode().strip().split('\n')
    flag_parameters = request.args.to_dict(True)
    results = []
    for flag in flags:
        try:
            inpython_collector(flag, **flag_parameters)
            results.append((flag, 'OK'))
        except FlagException as e:
            results.append((flag, e.reason))
    return render_template('submit_results.html', results=results)
