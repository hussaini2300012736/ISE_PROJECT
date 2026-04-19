from flask import Blueprint, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth

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
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/auth/callback')
def callback():
    token = oauth.google.authorize_access_token()
    user = token['userinfo']
    session['user'] = {
        'name': user['name'],
        'email': user['email']
    }
    return redirect('http://127.0.0.1:5000/auth/user')

@auth_bp.route('/auth/user')
def user():
    user = session.get('user')
    if user:
        return f"Logged in as {user['name']} ({user['email']})"
    return "Not logged in"

@auth_bp.route('/auth/logout')
def logout():
    session.pop('user', None)
    return redirect('/')