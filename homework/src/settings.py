import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# _CLIENT_SECRETS_FILE_NAME = 'client_secrets.json'
# _CREDENTIALS_FILE_NAME = 'credentials.json'
# _TOKEN_FILE_NAME = 'token.json'
_PROJECT_FILE_NAME = 'myproject-392812-84a5c4556204.json'

# CLIENT_SECRETS_FILE_PATH = os.path.join(STATIC_ROOT, _CLIENT_SECRETS_FILE_NAME)
# CREDENTIALS_FILE_PATH = os.path.join(STATIC_ROOT, _CREDENTIALS_FILE_NAME)
PROJECT_FILE_PATH = os.path.join(STATIC_ROOT, _PROJECT_FILE_NAME)
