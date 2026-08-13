import os
from flask import Flask
from app.config import Config
from app.extensions import db, login_manager
import logging
import watchtower

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "..", "logs"), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth_bp
    from app.documents.routes import documents_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(documents_bp)

    from app.utils.logger import setup_logger
    setup_logger(app)

    with app.app_context():
        db.create_all()

    return app
