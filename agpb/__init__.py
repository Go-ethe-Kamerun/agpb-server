import os

from flask import Flask, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Another secret key will be generated later
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = os.environ.get('TEMPLATES_AUTO_RELOAD')
app.config['UPLOADS'] = os.getcwd() + 'agpb/db/data/trans/'
app.config['SERVER_ADDRESS'] = 'http://3.17.141.122'
app.config['PLAY_AUDIO_ROUTE'] = '/api/v1/play?'

db = SQLAlchemy(app)

# Enble CORS on application
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# we import all our blueprint routes here
from agpb.main.routes import main

# Here we register the various blue_prints of our app
app.register_blueprint(main)