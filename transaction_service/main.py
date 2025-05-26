
# transaction_service/producer.py
from kafka import KafkaProducer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)

class Transaction(BaseModel):
    account_id: str
    type: str
    amount: float

@app.post("/transaction/")
def create_transaction(txn: Transaction):
    try:
        producer.send('transactions', key=txn.account_id, value=txn.dict())
        return {"status": "sent", "txn": txn}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))