import socket
import threading
import paramiko
from logger import log_event

# Generate RSA key for fake SSH server
HOST_KEY = paramiko.RSAKey.generate(2048)

FAKE_BANNER = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6"

class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip, client_port):
        self.client_ip = client_ip
        self.client_port = client_port
        self.username = ""
        self.password = ""

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        self.username = username
        self.password = password
        log_event(
            service="SSH",
            attacker_ip=self.client_ip,
            attacker_port=self.client_port,
            event_type="LOGIN_ATTEMPT",
            data={"username": username, "password": password}
        )
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def get_allowed_auths(self, username):
        return "password"


def handle_ssh_client(client_sock, client_addr):
    client_ip, client_port = client_addr
    print(f"[SSH] Connection from {client_ip}:{client_port}")

    transport = paramiko.Transport(client_sock)
    transport.local_version = FAKE_BANNER
    transport.add_server_key(HOST_KEY)

    server = FakeSSHServer(client_ip, client_port)

    try:
        transport.start_server(server=server)
        channel = transport.accept(30)

        if channel is None:
            return

        channel.send(b"\r\nWelcome to Ubuntu 22.04.3 LTS\r\n")
        channel.send(b"Last login: Mon May 4 10:23:11 2026 from 192.168.1.5\r\n")
        channel.send(b"root@ubuntu-server:~# ")

        command_buffer = b""

        while True:
            data = channel.recv(1024)
            if not data:
                break

            channel.send(data)

            if data in (b"\r", b"\n", b"\r\n"):
                command = command_buffer.decode(errors="ignore").strip()
                if command:
                    log_event(
                        service="SSH",
                        attacker_ip=client_ip,
                        attacker_port=client_port,
                        event_type="COMMAND_EXECUTED",
                        data={"command": command}
                    )
                    if command == "whoami":
                        channel.send(b"\r\nroot\r\n")
                    elif command == "ls":
                        channel.send(b"\r\npasswd.bak  secret.txt  server.conf  backup/\r\n")
                    elif command == "cat secret.txt":
                        channel.send(b"\r\nDB_PASSWORD=Sup3rS3cur3!\r\nAPI_KEY=sk-xxxxxxxxxxxx\r\n")
                    elif command == "exit":
                        channel.send(b"\r\nlogout\r\n")
                        break
                    else:
                        channel.send(f"\r\nbash: {command}: command not found\r\n".encode())
                    channel.send(b"root@ubuntu-server:~# ")
                command_buffer = b""
            else:
                command_buffer += data

    except Exception as e:
        print(f"[SSH] Error: {e}")
    finally:
        transport.close()
