import os

SECRET_KEY = # REDACTED #
ADMIN_PASSWORD = os.urandom(16).hex()
FLAG  = os.getenv("FLAG", "DH{FAKE_FLAG}")