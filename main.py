import threading
from ssh_honeypot import start_ssh_honeypot
from http_honeypot import start_http_honeypot
from ftp_honeypot import start_ftp_honeypot
from dashboard import start_dashboard
from logger import init_logger

if __name__ == "__main__":
    init_logger()
    print("""
    ╔══════════════════════════════════════════╗
    ║     🍯 ADVANCED HONEYPOT SYSTEM v1.0    ║
    ║         Developed by: [Manoj Lasgotra]        ║
    ╠══════════════════════════════════════════╣
    ║  SSH Honeypot   → Port 2222              ║
    ║  HTTP Honeypot  → Port 8080              ║
    ║  FTP Honeypot   → Port 2121              ║
    ║  Dashboard      → Port 9999              ║
    ╚══════════════════════════════════════════╝
    """)
    services = [
        threading.Thread(target=start_ssh_honeypot, args=(2222,)),
        threading.Thread(target=start_http_honeypot, args=(8080,)),
        threading.Thread(target=start_ftp_honeypot, args=(2121,)),
        threading.Thread(target=start_dashboard, args=(9999,)),
    ]
    for s in services:
        s.daemon = True
        s.start()
    print("[*] All honeypot services running! Press Ctrl+C to stop.\n")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[*] Honeypot stopped.")
