import socket
import threading
import random


USERS = ['bob', 'john']
SERVER_PORT = 32029
PASSWORD = 0x41A9CC23

class ProtocolError(Exception):
    pass

def generate_challenge_response():
    challenge = random.randint(0,0xFFFFFFFF)
    response = challenge ^ PASSWORD
    return challenge, response

def server_output(client, msg):
    client.send(msg.encode() + b'\n')

def client_input(client, expected_action, should_have_arg = False):
    # Read until newline
    msg = ''
    while True:
        c = client.recv(1).decode()
        if not c or c == '\n':
            break
        msg += c

    parts = msg.split('|')

    if len(parts) != 1 + int(should_have_arg):
        server_output(client, "ERROR Invalid message")
        raise ProtocolError()

    if parts[0] != expected_action:
        server_output(client, "ERROR Unexpected action")
        raise ProtocolError()

    return parts[1] if should_have_arg else None

def login(client):
    server_output(client, "LOGIN")
    username = client_input(client, "USERNAME", should_have_arg = True)
    if username not in USERS:
        server_output(client, "ERROR Unknown username")
        return None

    challenge, response = generate_challenge_response()
    server_output(client, "CHALLENGE|%d" % challenge)
    client_response = client_input(client, "RESPONSE", should_have_arg = True)
    try:
        if int(client_response) == response:
            return username
        else:
            server_output(client, "ERROR Auth failure")
            return None
    except:
        server_output(client, "ERROR Invalid response")
        return None

def show_songs_for_client(client, username):
    with open('{}.lst'.format(username), 'r') as f:
        inbox = f.read()
        server_output(client, "SONGS\n" + inbox)

def handle(client):
    try:
        client_input(client, "START")
        server_output(client, "BANNER Welcome to Extra Simple Playlist Protocol server! Log in to see your saved list of favorite songs")
        username = login(client)
        if username:
            show_songs_for_client(client, username)
    except ProtocolError as e:
        pass

    client.close()

def main():
    print("* ESPP v2.0 Server started; listening for clients")
    s = socket.socket()
    s.bind(('0.0.0.0', SERVER_PORT))
    s.listen(50)
    while True:
        try:
            k, _ = s.accept()
            print("* Got client connection")
            k.settimeout(3)
            print("Client")
            threading.Thread(target=handle, args=(k,)).start()
        except:
            pass

if __name__ == '__main__':
    main()
