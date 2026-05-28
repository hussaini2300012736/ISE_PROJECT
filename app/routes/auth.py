from flask import Blueprint, redirect, url_for, session, jsonify, send_from_directory
from authlib.integrations.flask_client import OAuth
import os

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

@auth_bp.route('/auth/login')
def login():
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, prompt='select_account')

@auth_bp.route('/auth/callback')
def callback():
    token = oauth.google.authorize_access_token()
    user = token['userinfo']
    session['user'] = {
        'name': user['name'],
        'email': user['email'],
        'picture': user.get('picture', '')
    }
    return redirect('/dashboard')

@auth_bp.route('/auth/user')
def get_user():
    user = session.get('user')
    if user:
        return jsonify(user)
    return jsonify(None)

@auth_bp.route('/auth/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# ── Page routes ──────────────────────────────
FRONTEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend')

@auth_bp.route('/')
def index():
    return send_from_directory(FRONTEND, 'index.html')

@auth_bp.route('/tutors-page')
def tutors_page():
    return send_from_directory(FRONTEND, 'tutors.html')

@auth_bp.route('/dashboard')
def dashboard():
    if not session.get('user'):
        return redirect('/auth/login')
    return send_from_directory(FRONTEND, 'dashboard.html')

@auth_bp.route('/booking-page')
def booking_page():
    if not session.get('user'):
        return redirect('/auth/login')
    return send_from_directory(FRONTEND, 'booking.html')

@auth_bp.route('/payment-page')
def payment_page():
    if not session.get('user'):
        return redirect('/auth/login')
    return send_from_directory(FRONTEND, 'payment.html')