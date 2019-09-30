
import hvac
import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask
from config import c
from flask import Flask, request

app = Flask(__name__)
app.secret_key = c.FLASK_SECRET
vault_client = hvac.Client(
    url=c.VAULT_ADDR,
    token=c.VAULT_TOKEN,
)


@app.route('/auth', methods=['GET'])
def auth():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        c.CLIENT_SECRETS_FILE,
        c.OAUTH2_SCOPES,
    )
    flow.redirect_uri = c.OAUTH2_REDIRECT
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )
    flask.session['state'] = state
    return flask.redirect(authorization_url)


@app.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        c.CLIENT_SECRETS_FILE,
        c.OAUTH2_SCOPES,
        state=flask.session['state']
    )
    flow.redirect_uri = c.OAUTH2_REDIRECT
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    path = f'gpc/user/{flask.session["user"]}/oauth2credentials'
    store(path=path, secret=flow.credentials)


def store(path, secret):
    rep = vault_client.secrets.kv.v2.create_or_update_secret(
        path=path,
        secret=secret,
    )


def read(path):
    rep = vault_client.secrets.kv.read_secret_version(
        path=path
    )
    return rep['data']['data']
