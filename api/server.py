
import hvac
import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask
from config import get_config
c = get_config()
from flask import Flask, request

app = Flask(__name__)
app.secret_key = c.FLASK_SECRET
vault_client = hvac.Client(
    url=c.VAULT_ADDR,
    token=c.VAULT_TOKEN,
)
code_verifier = 'abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd'

@app.route('/auth', methods=['GET'])
def auth():
    flask.session['user'] = 'bob'
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )
    flask.session['state'] = state
    return flask.redirect(authorization_url)


@app.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    flow = get_flow()
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    path = f'gpc/user/{flask.session["user"]}/oauth2credentials'
    #store(path=path, secret=flow.credentials)
    print(f"I would now store the creds {flow.credentials}")
    return b'success'


def get_flow():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        c.CLIENT_SECRETS_FILE,
        c.OAUTH2_SCOPES,
        state=flask.session['state'],
    )
    flow.redirect_uri = c.OAUTH2_REDIRECT
    flow.code_verifier = code_verifier
    return flow


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
