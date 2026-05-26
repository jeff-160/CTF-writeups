import os

from Crypto.PublicKey import RSA


def rsa_key() -> tuple[bytes, bytes]:
    key = RSA.generate(1024)
    return (
        key.public_key().exportKey(),
        key.exportKey(),
    )


basedir = os.path.abspath(os.path.dirname(__file__))


class Production:
    DEBUG = False
    SECRET_KEY = os.urandom(32)

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    TIMEZONE = "Asia/Seoul"

    AUTH_PUBLIC_KEY, AUTH_PRIVATE_KEY = rsa_key()
    FLAG_SCHOOL = os.environ.get("FLAG_SCHOOL", "드림고등학교")


class Development:
    DEBUG = True
    SECRET_KEY = "💙"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    TIMEZONE = "Asia/Seoul"

    AUTH_PUBLIC_KEY, AUTH_PRIVATE_KEY = rsa_key()
    FLAG_SCHOOL = os.environ.get("FLAG_SCHOOL", "드림고등학교")
