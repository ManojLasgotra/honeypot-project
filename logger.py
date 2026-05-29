import json
import os
from datetime import datetime

LOG_FILE = "logs/honeypot_logs.json"

def init_logger():
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def log_event(service, attacker_ip, attacker_port, event_type, data):
    init_logger()
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": service,
        "attacker_ip": attacker_ip,
        "attacker_port": attacker_port,
        "event_type": event_type,
        "data": data
    }
    
    # Console alert
    print(f"\n🚨 ALERT [{entry['timestamp']}]")
    print(f"   Service  : {service}")
    print(f"   Attacker : {attacker_ip}:{attacker_port}")
    print(f"   Event    : {event_type}")
    print(f"   Data     : {data}")
    print(f"{'='*50}")
    
    # Save to JSON
    with open(LOG_FILE, "r+") as f:
        logs = json.load(f)
        logs.append(entry)
        f.seek(0)
        json.dump(logs, f, indent=2)
    
    return entry
