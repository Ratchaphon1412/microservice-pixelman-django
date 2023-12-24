from .base import env
import hvac
import sys

# Vault settings

# Authentication
client = hvac.Client(
    url=env('VAULT_URI'),
    token=env('VAULT_TOKEN'),
)

# Reading a secret
SECRETE_KEY_SERVICE = client.secrets.kv.read_secret_version(
    path=env('VAULT_PATH'))
