from flask import Flask

#Create the app
app = Flask(__name__)

#Load config from config file
app.config.from_object('config')
