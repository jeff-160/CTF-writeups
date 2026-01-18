from flask import session, redirect, abort, flash, url_for
from functools import wraps
from hashlib import sha256

class auth():

    @staticmethod
    def verify(password : str, hashed_password : str) -> bool:
        return auth.hash(password) == hashed_password
    
    @staticmethod
    def _hash(password : str) -> str:
        m = sha256(password.encode())

        return m.hexdigest()

    @staticmethod
    def hash(password : str) -> str:
        hashed_password = password

        # super safe!
        for _ in range(256):
            hashed_password = auth._hash(hashed_password)

        return hashed_password

class access():
    def login_required(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if session.get('logined', False):
                return view(*args, **kwargs)
            flash("login first !")
            return redirect(url_for("login"))

        return wrapped_view

    def admin_only(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if session.get('username', False) == 'admin':
                return view(*args, **kwargs)
            return redirect(url_for("index"))

        return wrapped_view
    
def validate(val, _type=str, min_max = (0, 64)):
    if type(val) != _type:
        return False

    if _type == str and min_max:
        _min, _max = min_max
        return _min <= len(val) <= _max
    
    return True


def set(obj, prop, value):
    prop_chain = prop.split('.')
    for i in range(0,len(prop_chain)-1):
        if isinstance(obj, dict): 
            if not prop_chain[i+1]: obj[prop_chain[i]] = value;return
            else:
                obj = obj.setdefault(prop_chain[i], {})
        else:
            if prop_chain[i] and not hasattr(obj, prop_chain[i]): setattr(obj, prop_chain[i], {})
            if not prop_chain[i+1]:
                return setattr(obj, prop_chain[i], value) 
            obj = getattr(obj, prop_chain[i])
    if isinstance(obj, dict): obj[prop_chain[-1]] = value
    else: setattr(obj, prop_chain[-1], value)
    