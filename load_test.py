# load_test.py
import requests
import random
import time

TRANSACTION_URL = "http://localhost:8000/transaction/"
NUM_TRANSACTIONS = 1000
ACCOUNT_IDS = [f"acc{i}" for i in range(1, 11)]
TRANSACTION_TYPES = ["deposit", "withdrawal"]

for i in range(NUM_TRANSACTIONS):
    payload = {
        "account_id": random.choice(ACCOUNT_IDS),
        "type": random.choice(TRANSACTION_TYPES),
        "amount": round(random.uniform(1, 1000), 2)
    }
    start = time.time()
    try:
        response = requests.post(TRANSACTION_URL, json=payload)
        latency = time.time() - start
        if response.status_code != 200:
            print(f"[{i+1}] Failed: {response.status_code} - {response.text}")
        else:
            print(f"[{i+1}] Success in {latency:.4f}s: {payload}")
    except Exception as e:
        print(f"[{i+1}] Error: {e}")
    time.sleep(0.01)
