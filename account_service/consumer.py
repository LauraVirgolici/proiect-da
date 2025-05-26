# account_service/consumer.py
from kafka import KafkaConsumer
import json
import time
import threading

balances = {}
lock = threading.Lock()

def process_transaction(transaction):
    account_id = transaction['account_id']
    txn_type = transaction['type']
    amount = transaction['amount']
    with lock:
        current = balances.get(account_id, 0)
        if txn_type == 'deposit':
            balances[account_id] = current + amount
        elif txn_type == 'withdrawal':
            balances[account_id] = current - amount
        print(f"Updated {account_id}: {balances[account_id]}")

def start_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                'transactions',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id=f'account-service-group-{int(time.time())}',  # Unique ID each time
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                key_deserializer=lambda x: x.decode('utf-8') if x else None
            )
            for message in consumer:
                process_transaction(message.value)
        except Exception as e:
            print(f"Kafka error: {e}, retrying in 5s...")
            time.sleep(5)

def get_balances():
    with lock:
        return dict(balances)
