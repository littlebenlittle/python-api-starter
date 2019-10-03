
import flask
import pickle
from config import get_config
c = get_config()

app = flask.Flask(__name__)


@app.route('/auth', methods=['GET'])
def auth():
    authUrl = api.getAuthUrl(
        request=pb.Request(
            scopes=c.SCOPES
        )
    )
    return flask.redirect(authUrl.url)


@app.route('/redirect', methods=['GET'])
def redirect():
    return b'<h1>flow redirect page</h1>'


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
