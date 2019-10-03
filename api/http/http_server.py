
import flask
from config import get_config
c = get_config()

app = flask.Flask(__name__)


@app.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    api.submitRedirectUrl(flask.request.url)
    return flask.redirect(c.REDIRECT_URL)
