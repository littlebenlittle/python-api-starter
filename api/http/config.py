
import os
import sys
from types import SimpleNamespace

_config_vars = [
    'REDIRECT_URI',
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
    return errors

def get_config():
    c = SimpleNamespace()
    for var in _config_vars:
        setattr(c, var, os.environ[var])
    return c