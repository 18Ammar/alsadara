from flask import Flask,Blueprint
import os
import dotenv
from flask_compress import Compress
from flask_cors import CORS
from shared.database import db
from controller.defaults import create_default
from account import AccountBlueprint
dotenv.load_dotenv(".env")


def create_app():
    app = Flask(__name__)
    Compress(app)
    CORS(app, resources={r"/api/*":{"origins":"*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = "10ifv942jsdf&&&kjadw29iujkjefg0933fjij"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/alsadara"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    db.init_app(app)
    MainBlueprint = Blueprint('main','main','static')
    MainBlueprint.register_blueprint(AccountBlueprint,url_prefix='/account')

    with app.app_context():
        db.create_all()
        create_default()

    app.register_blueprint(MainBlueprint, url_prefix="/api")

    return app