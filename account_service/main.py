# account_service/main.py
from fastapi import FastAPI
import threading
from consumer import start_consumer, get_balances

app = FastAPI()

# Start Kafka consumer in a background thread
threading.Thread(target=start_consumer, daemon=True).start()

@app.get("/accounts")
def accounts():
    return get_balances()