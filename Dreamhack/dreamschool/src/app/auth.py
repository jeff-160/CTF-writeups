from functools import wraps
import hashlib
import datetime

from flask import abort, request
import jwt

from models import User, School
from typings import UserNotFoundError


class JwtAuthenticator:
    def generate(self, user: User) -> str:
        return (
            jwt.encode(
                {
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                    "username": user.username,
                    "school": user.school_name,
                },
                self.private_key,
                algorithm="RS256",
            )
        ).decode()

    def decode(self, token: str) -> tuple[str, str]:
        payload = jwt.decode(token, self.public_key, options={"verify_signature": True})
        return str(payload["username"]), str(payload["school"])

    def verify(self, token: str) -> tuple[User, School]:
        username, school_name = self.decode(token)
        user, school = (
            User.query.filter(User.username == username).first(),
            School.query.filter(School.name == school_name).first(),
        )

        if user is None or school is None:
            raise UserNotFoundError

        return user, school

    def authorize(self, is_abort: bool = True):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if "token" not in request.cookies:
                    abort(401)

                user, school = None, None

                try:
                    user, school = self.verify(request.cookies.get("token"))
                except UserNotFoundError as e:
                    _ = abort(401) if is_abort else None
                except jwt.ExpiredSignatureError as e:
                    _ = abort(401) if is_abort else None
                except jwt.DecodeError as e:
                    _ = abort(401) if is_abort else None
                except Exception as e:
                    _ = abort(401) if is_abort else None

                return f(user, school, *args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def hash(password: str):
        return hashlib.sha3_256(password.encode()).hexdigest()

    def __init__(self, public_key: str, private_key: str):
        self.public_key = public_key
        self.private_key = private_key
