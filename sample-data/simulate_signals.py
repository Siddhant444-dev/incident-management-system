import requests
import time
import random

API = "http://127.0.0.1:8000/api/signals"

components = [
    ("CACHE_CLUSTER_01", "CACHE", "P2", "Cache latency spike"),
    ("API_GATEWAY", "API", "P1", "High error rate"),
    ("RDBMS_PRIMARY", "DATABASE", "P0", "DB connection timeout"),
]

def send_signal(component):
    payload = {
        "component_id": component[0],
        "component_type": component[1],
        "severity": component[2],
        "message": component[3],
        "latency_ms": random.randint(100, 3000)
    }

    try:
        requests.post(API, json=payload)
    except:
        pass

if __name__ == "__main__":
    print("Simulating signals...")

    for _ in range(200):  # burst traffic
        comp = random.choice(components)
        send_signal(comp)
        time.sleep(0.05)  # simulate load