import subprocess

with open("tokens.txt", "r") as f:
    tokens = f.read().strip().split("\n")

subprocess.run(['python', 'jwt_forgery.py', *tokens])