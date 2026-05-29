# 🍯 Python Multi-Service Honeypot with Live Dashboard

> A custom-built cybersecurity honeypot that deploys fake SSH, HTTP, and FTP servers to attract, trap, and log attacker behaviour in real time.

---

## 📌 Project Overview

This project simulates a vulnerable server environment to lure cyber attackers and silently record everything they do — credentials attempted, commands executed, and paths probed. Built entirely from scratch in Python without relying on pre-built tools like Cowrie.

**Academic Context:** MDC-CS-601 Project | B.Tech CSE (Cybersecurity) | MIET Jammu | 2023–2027

---

## 🧩 Features

| Service | Port | What It Captures |
|---|---|---|
| 🔐 SSH Honeypot | 2222 | Usernames, passwords, shell commands |
| 🌐 HTTP Honeypot | 8080 | Login credentials, path probing (/wp-admin, /.env, /phpmyadmin) |
| 📁 FTP Honeypot | 2121 | Login attempts, file access requests |
| 📊 Live Dashboard | 9999 | Real-time attack table, auto-refreshes every 5 seconds |
| 📋 JSON Logger | — | Centralized structured log of all events |

---

## 🛠️ Technologies Used

- **Python 3** — Core language
- **Paramiko** — SSH protocol handling & key exchange
- **Flask + Jinja2** — HTTP honeypot & live dashboard
- **Socket (stdlib)** — Raw TCP for FTP server
- **Threading (stdlib)** — Parallel execution of all services
- **JSON** — Structured attack log storage

---

## 📂 Project Structure

honeypot_project/
│
├── main.py              # Entry point — starts all services in parallel
├── logger.py            # Centralized JSON logging module
├── ssh_honeypot.py      # Fake SSH server (Paramiko)
├── http_honeypot.py     # Fake HTTP admin login page (Flask)
├── ftp_honeypot.py      # Fake FTP server (Socket)
├── dashboard.py         # Live web dashboard (Flask)
└── logs/
└── honeypot_logs.json   # Attack log output file
---

## ⚙️ Setup & Run

### 1. Clone the Repository
```bash
git clone https://github.com/ManojLasgotra/honeypot-project.git
cd honeypot-project
```

### 2. Create Virtual Environment
```bash
python3 -m venv ~/myenv
source ~/myenv/bin/activate
pip install paramiko flask
```

### 3. Start the Honeypot
```bash
python3 main.py
```

---

## 🧪 Testing the Honeypot

### SSH Attack Simulation
```bash
ssh -p 2222 root@localhost
# Password: 1234
# Then try: ls, whoami, cat secret.txt
```

### HTTP Attack Simulation
```bash
curl -X POST http://127.0.0.1:8080/login -d "username=admin&password=1234"
curl http://127.0.0.1:8080/wp-admin
curl http://127.0.0.1:8080/.env
```

### FTP Attack Simulation
```bash
ftp localhost 2121
# Username: admin | Password: 1234
```

---

## 🌐 Dashboard

- **HTTP Login Page (Honeypot):** http://127.0.0.1:8080
- **Live Attack Dashboard:** http://127.0.0.1:9999

---

## ⚠️ Disclaimer

> This project is built strictly for **educational and research purposes**. Tested in an isolated VirtualBox lab environment. Do NOT deploy on public-facing servers without proper legal authorization.

---

## 👨‍💻 Author

- **Manoj Lasgotra** (2023A7RO48) — [GitHub](https://github.com/ManojLasgotra)

B.Tech CSE (Cybersecurity) | Model Institute of Engineering & Technology, Jammu
