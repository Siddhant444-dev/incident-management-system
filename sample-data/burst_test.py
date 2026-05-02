# Simulates 100 signals in <10 sec (debouncing test)
import requests

API = "http://127.0.0.1:8000/api/signals"

payload = {
    "component_id": "CACHE_CLUSTER_01",
    "component_type": "CACHE",
    "severity": "P2",
    "message": "Cache overload spike",
    "latency_ms": 2500
}

for _ in range(100):
    requests.post(API, json=payload)

print("Sent 100 signals for debouncing test")