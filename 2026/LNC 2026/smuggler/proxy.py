import socket
import threading
from urllib.parse import unquote

BACKEND_HOST = "web"
BACKEND_PORT = 5000


def recv_until(sock, delimiter):
    buf = b""
    while not buf.endswith(delimiter):
        byte = sock.recv(1)
        if not byte:
            return None
        buf += byte
    return buf


def read_body(sock, length):
    body = b""
    while len(body) < length:
        chunk = sock.recv(length - len(body))
        if not chunk:
            break
        body += chunk
    return body


def forward_request(client_sock, backend_sock):
    # Read raw request headers
    raw_headers = recv_until(client_sock, b"\r\n\r\n")
    if raw_headers is None:
        return False

    header_text = raw_headers[:-4].decode("latin-1")
    lines = header_text.split("\r\n")
    request_line = lines[0]

    try:
        method, path, version = request_line.split(" ", 2)
    except ValueError:
        return False

    # block direct access to /get_flag
    if unquote(path).lower().startswith("/get_flag"):
        client_sock.sendall(
            b"HTTP/1.1 403 Forbidden\r\n"
            b"Content-Length: 9\r\n"
            b"Connection: close\r\n"
            b"\r\n"
            b"Forbidden"
        )
        return False

    # Parse request the read body
    content_length = 0
    for line in lines[1:]:
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())
            break

    
    body = read_body(client_sock, content_length)

    # Forward raw request (headers + body) to backend
    backend_sock.sendall(raw_headers + body)

    # Read response headers from backend
    response_headers = recv_until(backend_sock, b"\r\n\r\n")
    if response_headers is None:
        return False

    # Parse response to read body
    resp_lines = response_headers[:-4].decode("latin-1").split("\r\n")
    resp_cl = 0
    for line in resp_lines[1:]:
        if line.lower().startswith("content-length:"):
            resp_cl = int(line.split(":", 1)[1].strip())
            break

    resp_body = read_body(backend_sock, resp_cl)
    client_sock.sendall(response_headers + resp_body)
    return True


def handle_client(client_sock):
    backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        backend_sock.connect((BACKEND_HOST, BACKEND_PORT))
        while True:
            if not forward_request(client_sock, backend_sock):
                break
    except Exception:
        pass
    finally:
        try:
            backend_sock.close()
        except Exception:
            pass
        try:
            client_sock.close()
        except Exception:
            pass


def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 80))
    server.listen(10)
    print("Proxy running on port 80")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    start_proxy()
