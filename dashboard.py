from flask import Flask, jsonify, render_template_string
import json, os

dash_app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>🍯 Honeypot Dashboard</title>
  <meta http-equiv="refresh" content="5">
  <style>
    body { font-family: monospace; background: #0d1117; color: #58a6ff; margin: 0; padding: 20px; }
    h1 { color: #f0883e; text-align: center; }
    .stats { display: flex; gap: 20px; justify-content: center; margin: 20px 0; }
    .stat-box { background: #161b22; padding: 20px 30px; border-radius: 8px; text-align: center; border: 1px solid #30363d; }
    .stat-box h2 { margin: 0; font-size: 2em; color: #e94560; }
    .stat-box p { margin: 5px 0 0; color: #aaa; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th { background: #161b22; padding: 12px; text-align: left; border: 1px solid #30363d; color: #f0883e; }
    td { padding: 10px 12px; border: 1px solid #21262d; font-size: 0.9em; }
    tr:nth-child(even) { background: #161b22; }
    tr:hover { background: #1f2937; }
    .badge-ssh { color: #58a6ff; }
    .badge-http { color: #3fb950; }
    .badge-ftp { color: #f0883e; }
  </style>
</head>
<body>
  <h1>🍯 Advanced Honeypot — Live Dashboard</h1>
  <div class="stats">
    <div class="stat-box"><h2>{{ total }}</h2><p>Total Events</p></div>
    <div class="stat-box"><h2>{{ unique_ips }}</h2><p>Unique Attackers</p></div>
    <div class="stat-box"><h2>{{ ssh_count }}</h2><p>SSH Attacks</p></div>
    <div class="stat-box"><h2>{{ http_count }}</h2><p>HTTP Attacks</p></div>
    <div class="stat-box"><h2>{{ ftp_count }}</h2><p>FTP Attacks</p></div>
  </div>
  <table>
    <tr>
      <th>#</th><th>Timestamp</th><th>Service</th>
      <th>Attacker IP</th><th>Event Type</th><th>Data</th>
    </tr>
    {% for i, log in logs %}
    <tr>
      <td>{{ i }}</td>
      <td>{{ log.timestamp }}</td>
      <td class="badge-{{ log.service|lower }}">{{ log.service }}</td>
      <td>{{ log.attacker_ip }}</td>
      <td>{{ log.event_type }}</td>
      <td>{{ log.data }}</td>
    </tr>
    {% endfor %}
  </table>
  <p style="text-align:center; color:#555; margin-top:20px;">Auto-refresh every 5 seconds</p>
</body>
</html>
"""

@dash_app.route("/")
def dashboard():
    logs = []
    if os.path.exists("logs/honeypot_logs.json"):
        with open("logs/honeypot_logs.json") as f:
            logs = json.load(f)
    logs_reversed = list(enumerate(reversed(logs), 1))
    services = [l["service"] for l in logs]
    return render_template_string(
        DASHBOARD_HTML,
        logs=logs_reversed,
        total=len(logs),
        unique_ips=len(set(l["attacker_ip"] for l in logs)),
        ssh_count=services.count("SSH"),
        http_count=services.count("HTTP"),
        ftp_count=services.count("FTP")
    )

def start_dashboard(port=9999):
    print(f"[Dashboard] Running at http://0.0.0.0:{port}")
    dash_app.run(host="0.0.0.0", port=9999, debug=False, use_reloader=False)
