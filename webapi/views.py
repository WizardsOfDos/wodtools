from flask import render_template, request, jsonify

from webapi import app
from flgproc.collector.demo import inpython_collector
from flgproc.exceptions import FlagException

@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/submit_flag', methods=['POST'])
def submit_flag():
    flags = request.data.split('\n')
    flag_parameters = request.args.to_dict(True)
    result_map = {}
    for flag in flags:
        try:
            inpython_collector(flag, **flag_parameters)
        except FlagException as e:
            result_map[flag] = e.reason
        result_map[flag] = 'OK'
    return render_template('templates/submit_results.html', results=result_map)
