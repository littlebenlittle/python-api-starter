
import os
import sys
import google_auth_oauthlib.flow
from types import SimpleNamespace

_config_vars = [
    'VAULT_ADDR',
    'VAULT_TOKEN',
    'CLIENT_SECRETS_FILE',
    'OAUTH2_SCOPES',
    'FLASK_SECRET',
    'OAUTH2_REDIRECT',
    'TLSCERT',
    'TLSKEY',
]

def validate():
    errors = []
    missing = []
    for var in _config_vars:
        if not os.environ.get(var):
            missing.append(var)
    if any(missing):
        err = 'Missing environment variables:\n'
        for var in missing:
            err += f' - {var}\n'
        errors.append(err)
    try:
        _ = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            os.environ.get('CLIENT_SECRETS_FILE'),
            os.environ.get('OAUTH2_SCOPES'),
        )
    except (IsADirectoryError, FileNotFoundError):
        err = 'CLIENT_SECRETS_FILE has invalid value:\n' \
            + f'"{os.environ.get("CLIENT_SECRETS_FILE")}" is not a file.'
        errors.append(err)
    except Exception as e:
        print('Unhandled error with google oauth flow')
        raise(e)
    return errors

def get_config():
    c = SimpleNamespace()
    for var in _config_vars:
        setattr(c, var, os.environ[var])
    c.OAUTH2_SCOPES = c.OAUTH2_SCOPES.split(',')

    # NOTE: !!! 64 bits of ENTROPY, not 64 characters !!!
    c.CODE_VERIFIER = os.urandom(64)

    return c
