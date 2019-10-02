
import os
import sys

bind = '0.0.0.0:80'
workers = 4
loglevel = 'info'
errorlog = '-'
accesslog = '-'
certfile = os.environ.get('TLSCERT')
keyfile = os.environ.get('TLSKEY')

def on_starting(server):
    from config import validate
    errors = validate()
    if errors:
        for err in errors:
            print(err)
        if os.environ.get('DEBUG'):
            sys.exit(1)
