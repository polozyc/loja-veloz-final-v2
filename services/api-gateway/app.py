from flask import Flask, Response, request
import os
import logging

from prometheus_client import Counter, generate_latest

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

app = Flask(__name__)

# Nome do serviço
SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")

# Métrica Prometheus
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total de requisições HTTP",
    ["service", "method", "endpoint"]
)


# Log + métrica por request
@app.before_request
def before_request():
    REQUEST_COUNT.labels(
        service=SERVICE_NAME,
        method=request.method,
        endpoint=request.path
    ).inc()

    logging.info(
        f"{SERVICE_NAME} | {request.method} {request.path}"
    )


# Healthcheck
@app.route("/health")
def health():
    return {
        "service": SERVICE_NAME,
        "status": "UP"
    }


# Métricas Prometheus
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


# Endpoint raiz
@app.route("/")
def home():
    return f"{SERVICE_NAME} ativo com observabilidade"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
