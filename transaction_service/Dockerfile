# transaction_service/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY producer.py .
RUN pip install kafka-python fastapi uvicorn
CMD ["uvicorn", "producer:app", "--host", "0.0.0.0", "--port", "8000"]