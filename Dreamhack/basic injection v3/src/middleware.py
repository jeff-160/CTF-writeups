import os

def load_env():
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def check(username):
    load_env()
    middleware = os.getenv('MIDDLEWARE', 'true').lower()
    
    if middleware == 'true' and username == 'admin':
        return False
    return True