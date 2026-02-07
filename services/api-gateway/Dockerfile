# ========== STAGE 1: Build ==========
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

# ========== STAGE 2: Runtime ==========
FROM python:3.11-slim AS runtime

WORKDIR /app

# Cria usuário não-root
RUN useradd --no-create-home --shell /bin/false appuser

# Copia dependências do stage anterior
COPY --from=builder /app/dependencies /usr/local/lib/python3.11/site-packages/

# Copia código
COPY app.py .

# Segurança: roda sem root
USER appuser

# Porta
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Start
CMD ["python", "app.py"]
