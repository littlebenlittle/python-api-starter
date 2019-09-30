
import os
import sys
from types import SimpleNamespace

_config_vars = [
    'VAULT_ADDR',
    'VAULT_TOKEN',
    'CLIENT_SECRETS_FILE',
    'OAUTH2_SCOPES',
    'FLASK_SECRET',
    'OAUTH2_REDIRECT',
]

_missing = []
for var in _config_vars:
    if not os.environ.get(var):
        _missing.append(var)

if any(_missing):
    print('Missing environment variables:')
    for var in _missing:
        print(var)
    sys.exit(1)

c = SimpleNamespace()
for var in _config_vars:
    setattr(c, var, os.environ[var])

c.OAUTH2_SCOPES = c.OAUTH2_SCOPES.split(',')
