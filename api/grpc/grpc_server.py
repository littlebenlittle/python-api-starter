

import grpc
import time
import sys
from concurrent import futures
from requests_oauthlib import OAuth2Session
from config import get_config
c = get_config()

sys.path.append(c.PYTHON_PB)
import api_pb2 as pb
import api_pb2_grpc as pb_grpc


class ApiServicer(pb_grpc.ApiServicer):

    session = None
    state = None
    
    def getAuthUrl(self, request, context):
        session = OAuth2Session(
            c.GOOGLE_CLIENT_ID,
            scope=request.scopes,
            redirect_uri=c.REDIRECT_URI,
        )
        auth_url, state = session.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
        )
        set_current_context(session, state)
        return pb.Url(
            url=auth_url,
        )

    def submitRedirectUrl(self, userAndUrl, context):
        session, state = get_current_context()
        tokens = session.fetch_token(
            c.TOKEN_URL,
            client_secret=c.CLIENT_SECRET,
            authorization_response=userAndUrl.url,
        )
        put_tokens(
            userAndUrl.user.name,
            tokens,
        )
        return pb.Emtpy()

    def getToken(self, user, context):
        tokens = get_tokens(user.name)
        access_token = maybe_refresh_tokens(tokens)
        return pb.Token(token=access_token)

    def revokeTokens(self, user, context):
        access_token = self.getToken(user)
        rep = requests.post(
            'https://accounts.google.com/o/oauth2/revoke',
            params={'token': access_token},
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )
        return pb.Emtpy()

    def set_current_context(self, session, state):
        self.session = session
        self.state = state

    def get_current_context(self):
        return self.session, self.state

    def put_tokens(self, username, tokens):
        print("I would now put this in vault:")
        print(userAndUrl.user.name)
        print(tokens)

    def get_tokens(self, username):
        print("get_tokens() not implented")

    def maybe_refresh_tokens(tokens):
        print("maybe_refresh_tokens() not implented")

server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=10)
)
pb_grpc.add_ApiServicer_to_server(
    ApiServicer(),
    server
)
server.add_insecure_port(f'[::]:{RPC_PORT}')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
erver.stop(0)
