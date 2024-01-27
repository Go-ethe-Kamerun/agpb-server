import os
import yaml

from flask import Flask, request, session
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_migrate import Migrate

app = Flask(__name__)


# Another secret key will be generated later
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['TEMPLATES_AUTO_RELOAD'] = os.environ.get('TEMPLATES_AUTO_RELOAD')
# app.config['UPLOADS_DIR'] = os.getcwd() + os.environ.get('UPLOADS_DIR')
# app.config['SERVER_ADDRESS'] = os.environ.get('SERVER_ADDRESS')
# app.config['PLAY_AUDIO_ROUTE'] = os.environ.get('PLAY_AUDIO_ROUTE')

config_file = 'config.yaml'

if os.path.isfile(config_file):
    # Load configuration from YAML file
    __dir__ = os.path.dirname(__file__)
    app.config.update(
        yaml.safe_load(open(os.path.join(__dir__, config_file))))
else:
    __dir__ = os.path.dirname(__file__)
    app.config.update(
        yaml.safe_load(open(os.path.join(__dir__, 'test_config.yaml'))))


def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

db = SQLAlchemy(app)

# init db migrate 
migrate = Migrate()
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.home'
login_manager.login_message = 'You Need to Login to Access This Page!'
login_manager.login_message_category = 'danger'


@app.before_request
def before_request():
    try:
        db.session.execute(text("SELECT 1;"))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    # Update session language
    get_locale()


# Enble CORS on application
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# we import all our blueprint routes here
from agpb.main.routes import main
from agpb.users.routes import users


# Here we register the various blue_prints of our app
app.register_blueprint(main)
app.register_blueprint(users)


app.app_context().push()