from flask import Flask,Blueprint,jsonify
import dotenv
from flask_compress import Compress
from flask_cors import CORS
from shared.database import db
from controller.defaults import create_default
from account import AccountBlueprint
from shared.exceptions import NotAuthenticated,NotFound,UnauthorizedAccount,InvalidRequest,NotLoggedIn
from shared.response import messages
import os


dotenv.load_dotenv(".env")
def create_app():
    app = Flask(__name__)
    Compress(app)
    CORS(app, resources={r"/api/*":{"origins":"*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = "10ifv942jsdf&&&kjadw29iujkjefg0933fjij"
    app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://avnadmin:AVNS_oj7KNyeNG1a07-byQ9W@alsadara-alsadara.d.aivencloud.com:13523/defaultdb?sslmode=require"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    db.init_app(app)
    MainBlueprint = Blueprint('main','main','static')
    MainBlueprint.register_blueprint(AccountBlueprint,url_prefix='/account')
    @MainBlueprint.errorhandler(NotAuthenticated)
    @MainBlueprint.errorhandler(NotFound)
    @MainBlueprint.errorhandler(UnauthorizedAccount)
    @MainBlueprint.errorhandler(InvalidRequest)
    @MainBlueprint.errorhandler(NotLoggedIn)
    def error_handler(error):
        response={
            "msg": error.msg,
            "msg_ar": error.msg_ar
        }
        return jsonify(response, error.code)
    
    @app.errorhandler(404)
    def not_found_handler(*args):
        return error_handler(NotFound(messages["Requested URL was not found"]))

    # @app.errorhandler(405)
    # def method_not_allowed_handler(*args):
    #     return error_handler(MethodNotAllowed(messages["Method not allowed"]))

    
    with app.app_context():
        db.create_all()
        create_default()

    app.register_blueprint(MainBlueprint, url_prefix="/api")

    return app
