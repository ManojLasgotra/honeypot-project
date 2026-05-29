from flask import Flask, request, render_template_string
from logger import log_event

app = Flask(__name__)

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Admin Panel - Company Portal</title></head>
<body style="font-family:Arial; background:#1a1a2e; color:white; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
  <div style="background:#16213e; padding:40px; border-radius:10px; width:300px; text-align:center;">
    <h2>🔐 Admin Login</h2>
    <p style="color:#aaa;">Company Internal Portal</p>
    <form method="POST" action="/login">
      <input name="username" placeholder="Username" style="width:90%; padding:10px; margin:8px 0; border-radius:5px; border:none;"><br>
      <input name="password" type="password" placeholder="Password" style="width:90%; padding:10px; margin:8px 0; border-radius:5px; border:none;"><br>
      <button type="submit" style="width:97%; padding:10px; background:#e94560; border:none; border-radius:5px; color:white; font-size:16px; cursor:pointer;">Login</button>
    </form>
  </div>
</body>
</html>
"""

ERROR_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Admin Panel</title></head>
<body style="font-family:Arial; background:#1a1a2e; color:white; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
  <div style="background:#16213e; padding:40px; border-radius:10px; width:300px; text-align:center;">
    <h2>❌ Invalid Credentials</h2>
    <p style="color:#e94560;">Access Denied. Attempt has been logged.</p>
    <a href="/" style="color:#aaa;">Try Again</a>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    log_event(
        service="HTTP",
        attacker_ip=request.remote_addr,
        attacker_port=request.environ.get("REMOTE_PORT", 0),
        event_type="PAGE_VISIT",
        data={"path": "/", "user_agent": request.headers.get("User-Agent")}
    )
    return LOGIN_PAGE

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    log_event(
        service="HTTP",
        attacker_ip=request.remote_addr,
        attacker_port=request.environ.get("REMOTE_PORT", 0),
        event_type="LOGIN_ATTEMPT",
        data={"username": username, "password": password}
    )
    return ERROR_PAGE

@app.route("/admin")
@app.route("/wp-admin")
@app.route("/phpmyadmin")
@app.route("/.env")
@app.route("/config")
def sensitive_paths():
    log_event(
        service="HTTP",
        attacker_ip=request.remote_addr,
        attacker_port=0,
        event_type="SENSITIVE_PATH_PROBE",
        data={"path": request.path, "user_agent": request.headers.get("User-Agent")}
    )
    return "403 Forbidden", 403

def start_http_honeypot(port=8080):
    print(f"[HTTP Honeypot] Listening on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
