from flask import Flask, Response, request
import os
import logging

from prometheus_client import Counter, generate_latest

# Configuração básica de logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Nome do serviço vindo da env
SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")

# Métrica Prometheus
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "method", "endpoint"]
)


# Conta todas as requisições
@app.before_request
def count_requests():
    REQUEST_COUNT.labels(
        service=SERVICE_NAME,
        method=request.method,
        endpoint=request.path
    ).inc()

    logging.info(
        f"Request {request.method} {request.path} - Service: {SERVICE_NAME}"
    )


# Healthcheck (K8s usa isso)
@app.route("/health")
def health():
    return {
        "service": SERVICE_NAME,
        "status": "UP"
    }


# Métricas (Prometheus coleta aqui)
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


# Rota exemplo
@app.route("/")
def home():
    return f"{SERVICE_NAME} rodando!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
