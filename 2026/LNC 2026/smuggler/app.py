import socket
import threading

FLAG = "LNC26{NotTheRealFlag}\n"


def read_chunked_body(conn, buf):
    
    body = b""
    while True:
        # Ensure we have at least one chunk-size line in buf
        while b"\r\n" not in buf:
            more = conn.recv(4096)
            if not more:
                return body, buf
            buf += more

        crlf = buf.index(b"\r\n")
        chunk_size = int(buf[:crlf].split(b";")[0], 16)
        buf = buf[crlf + 2:]

        if chunk_size == 0:
            # Consume trailing \r\n after the zero-chunk
            while len(buf) < 2:
                more = conn.recv(4096)
                if not more:
                    return body, buf
                buf += more
            if buf[:2] == b"\r\n":
                buf = buf[2:]
            return body, buf

        # Read chunk data + trailing \r\n
        while len(buf) < chunk_size + 2:
            more = conn.recv(4096)
            if not more:
                return body, buf
            buf += more

        body += buf[:chunk_size]
        buf = buf[chunk_size + 2:]


def handle_client(conn):
    buf = b""
    while True:
        try:
            # Read until we have a complete header block
            while b"\r\n\r\n" not in buf:
                data = conn.recv(4096)
                if not data:
                    conn.close()
                    return
                buf += data

            headers_end = buf.index(b"\r\n\r\n")
            raw_headers = buf[:headers_end]
            buf = buf[headers_end + 4:]

            header_text = raw_headers.decode("latin-1")
            lines = header_text.split("\r\n")
            request_line = lines[0]
            method, path, _ = request_line.split(" ", 2)

            # Parse headers into a dict
            headers = {}
            for line in lines[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().lower()] = v.strip()

            
            if headers.get("transfer-encoding", "").lower() == "chunked":
                body, buf = read_chunked_body(conn, buf)
            else:
                content_length = int(headers.get("content-length", 0))
                while len(buf) < content_length:
                    data = conn.recv(4096)
                    if not data:
                        conn.close()
                        return
                    buf += data
                body = buf[:content_length]
                buf = buf[content_length:]

            if path == "/":
                response = "Welcome to the secure portal.\n"
            elif path == "/submit_feedback":
                response = "Feedback received successfully!\n"
            elif path == "/get_flag":
                response = FLAG
            else:
                response = "Not found\n"

            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Connection: keep-alive\r\n"
                f"Content-Length: {len(response)}\r\n"
                "\r\n"
                f"{response}"
            )

            conn.sendall(http_response.encode("latin-1"))

        except Exception:
            break

    conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 5000))
    server.listen(5)
    print("Backend server running on port 5000")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    start_server()
