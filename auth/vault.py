from .base import env
import hvac
import sys

# Vault settings

# Authentication
client = hvac.Client(
    url=env('VAULT_URI'),
    token=env('VAULT_TOKEN')
)
# print(client.token)

# print("is_sealed ", client.sys.is_sealed())
# print(client.is_authenticated())


# Reading a secret
SECRETE_KEY_SERVICE = client.secrets.kv.read_secret_version(
    path=env('VAULT_PATH'))

# SECRETE_DB_SERVICE = client.secrets.database.get_static_credentials(
#     name=env('VAULT_DB_ROLE'),
#     mount_point=env('VAULT_DB_PATH')
# )


# print(SECRETE_DB_SERVICE['data']['password'],
#       SECRETE_DB_SERVICE['data']['username'])
