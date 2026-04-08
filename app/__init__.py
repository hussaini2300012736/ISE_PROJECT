from flask import Flask
from flask_cors import CORS
import sqlite3

def create_app():
    app = Flask(__name__)

    app.config['DATABASE'] = 'database.db'

    CORS(app)

    from app.routes.tutor import tutor_bp
    app.register_blueprint(tutor_bp)

    return app