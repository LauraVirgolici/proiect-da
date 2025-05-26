import requests
import random
import time
import csv
import sys
import os
import json

# Use command-line argument for number of transactions
if len(sys.argv) != 2:
    print("Usage: python script.py <number_of_transactions>")
    sys.exit(1)

NUM_TRANSACTIONS = int(sys.argv[1])
TRANSACTION_URL = "http://localhost:8000/transaction/"
ACCOUNT_URL = "http://localhost:8002/accounts"
ACCOUNT_IDS = [f"acc{i}" for i in range(1, 11)]
TRANSACTION_TYPES = ["deposit", "withdrawal"]

latencies = []

# Prepare output directory
output_dir = "./data"
os.makedirs(output_dir, exist_ok=True)

# Capture start time
start_total = time.time()

# Submit transactions
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
        latencies.append(latency)
        if response.status_code != 200:
            print(f"[{i+1}] Failed: {response.status_code} - {response.text}")
        else:
            print(f"[{i+1}] Success in {latency:.4f}s")
    except Exception as e:
        print(f"[{i+1}] Error: {e}")
    time.sleep(0.01)

# Capture total time
end_total = time.time()
total_time = end_total - start_total
avg_latency = sum(latencies) / len(latencies) if latencies else 0
throughput = NUM_TRANSACTIONS / total_time if total_time > 0 else 0

# Fetch final balances
try:
    final_balances = requests.get(ACCOUNT_URL).json()
except Exception as e:
    final_balances = {"error": str(e)}

# Save to CSV
csv_filename = os.path.join(output_dir, f"experiment_summary-{NUM_TRANSACTIONS}.csv")
csv_data = [["Transaction Count", "Avg Latency (s)", "Throughput (txn/sec)", "Total Time (s)"],
            [NUM_TRANSACTIONS, round(avg_latency, 4), round(throughput, 2), round(total_time, 2)]]

with open(csv_filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

# Save final balances
json_filename = os.path.join(output_dir, f"final_balances-{NUM_TRANSACTIONS}.json")
with open(json_filename, "w") as f:
    json.dump(final_balances, f, indent=2)

(csv_filename, json_filename, latencies[:5], avg_latency, throughput, total_time)