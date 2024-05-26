import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from snep_ai.controllers import (
    AuthController, DashboardController, UserController, ChatbotController, InformationValidationController, InformationCategoryController, InformationListController
)
from flask_login import LoginManager, current_user
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor

from waitress import serve

import snep_ai.services.UserService as svc_user

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'images')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db = SQLAlchemy()
    db.init_app(app)

    ckeditor = CKEditor(app)

    # Import All Models
    from snep_ai.models import User, InformationCategory, InformationList, PromptLog, ChatLog
    with app.app_context():
        # Create tables based on the Models
        # Cannot create the existing table
        db.create_all()

    # Flask Login Config
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        user, error = svc_user.get_by_id(user_id)
        return user

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    app.register_blueprint(AuthController.auth)
    app.register_blueprint(DashboardController.dashboard)
    app.register_blueprint(UserController.users, url_prefix="/users")
    app.register_blueprint(InformationCategoryController.informationCategory)
    app.register_blueprint(InformationValidationController.informationValidation)
    app.register_blueprint(InformationListController.informationLists, url_prefix="/informationLists")
    app.register_blueprint(ChatbotController.chatbot)


    # If we run this file directly
    # if __name__ == '__main__':
    #     # Then run the web server
    #     # debug=True => if there are any changes, then automatically re-run the web server
    #     # Need to turn the debug off on production
    #     # app.run(debug=False)
    #     serve(snep_ai, listen='*:8080')

    return app