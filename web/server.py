
import hvac
import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask
import pickle
from config import get_config
c = get_config()
from flask import Flask, request, jsonify

app = Flask(__name__)
app.secret_key = c.FLASK_SECRET
vault_client = hvac.Client(
    url=c.VAULT_ADDR,
    token=c.VAULT_TOKEN,
)


@app.route('/auth', methods=['POST'])
def auth():
    try:
        data = request.json()
    except Exception as e:
        print(e)
        return b'failure', 400
    flask.session['user'] = user
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )
    flask.session['state'] = state
    return jsonify(authorization_url)


@app.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    flow = get_flow(state=flask.session['state'])
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    store(flow.credentials)
    return b'success'


def revoke(creds):
    rep = requests.post(
        'https://accounts.google.com/o/oauth2/revoke',
        params={'token': creds.token},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )
    return rep


def get_flow(scopes, state=None):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        c.CLIENT_SECRETS_FILE,
        scopes,
        state=state
    )
    flow.redirect_uri = c.OAUTH2_REDIRECT
    flow.code_verifier = c.CODE_VERIFIER
    return flow


def store(user, creds):
    rep = vault_client.secrets.kv.v2.create_or_update_secret(
        path=f'gpc/user/{user}/oauth2credentials',
        secret=dict(
            access_token=creds.token,
            refresh_token=creds.refresh_token,
        )
    )
    return rep


def read(user):
    rep = vault_client.secrets.kv.read_secret_version(
        path=f'gpc/user/{user}/oauth2credentials',
    )
    return rep  # ['data']['data']
