from flask import Flask
from flask_cors import CORS
from app.routes.auth import auth_bp, init_oauth

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    CORS(app)

    from app.routes.tutor import tutor_bp
    app.register_blueprint(tutor_bp)

    from app.routes.booking import booking_bp
    app.register_blueprint(booking_bp)

    app.register_blueprint(auth_bp)
    init_oauth(app)

    from app.routes.payment import payment_bp
    app.register_blueprint(payment_bp)

    from app.tasks import start_workers
    start_workers()

    return app