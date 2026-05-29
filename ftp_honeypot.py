import socket
import threading
from logger import log_event

def handle_ftp_client(client_sock, client_addr):
    client_ip, client_port = client_addr
    print(f"[FTP] Connection from {client_ip}:{client_port}")
    try:
        client_sock.send(b"220 Welcome to Company FTP Server (vsftpd 3.0.5)\r\n")
        username = ""
        while True:
            data = client_sock.recv(1024).decode(errors="ignore").strip()
            if not data:
                break
            print(f"[FTP] {client_ip} >> {data}")
            if data.upper().startswith("USER"):
                username = data.split(" ", 1)[1] if " " in data else ""
                client_sock.send(b"331 Please specify the password.\r\n")
            elif data.upper().startswith("PASS"):
                password = data.split(" ", 1)[1] if " " in data else ""
                log_event(
                    service="FTP",
                    attacker_ip=client_ip,
                    attacker_port=client_port,
                    event_type="LOGIN_ATTEMPT",
                    data={"username": username, "password": password}
                )
                client_sock.send(b"230 Login successful.\r\n")
            elif data.upper() == "LIST" or data.upper() == "NLST":
                client_sock.send(b"150 Here comes the directory listing.\r\n")
                client_sock.send(b"226 Directory send OK.\r\n")
            elif data.upper().startswith("RETR"):
                filename = data.split(" ", 1)[1] if " " in data else ""
                log_event(
                    service="FTP",
                    attacker_ip=client_ip,
                    attacker_port=client_port,
                    event_type="FILE_ACCESS_ATTEMPT",
                    data={"filename": filename}
                )
                client_sock.send(b"550 Failed to open file.\r\n")
            elif data.upper() == "QUIT":
                client_sock.send(b"221 Goodbye.\r\n")
                break
            else:
                client_sock.send(b"200 OK.\r\n")
    except Exception as e:
        print(f"[FTP] Error: {e}")
    finally:
        client_sock.close()

def start_ftp_honeypot(port=2121):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", port))
    server_sock.listen(5)
    print(f"[FTP Honeypot] Listening on port {port}...")
    while True:
        client_sock, client_addr = server_sock.accept()
        t = threading.Thread(target=handle_ftp_client, args=(client_sock, client_addr))
        t.daemon = True
        t.start()
