from flask import Flask

app = Flask(__name__)
app.config.from_object('webapi.config')

import webapi.views
