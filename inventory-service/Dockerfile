FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    opentelemetry-distro \
    opentelemetry-instrumentation \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-fastapi \
    opentelemetry-instrumentation-httpx

# 自動檢測並安裝該環境需要的 instrumentation 套件
RUN opentelemetry-bootstrap -a install

COPY app.py .
EXPOSE 8001

# 設定屬於 inventory-service 的名字
ENV OTEL_SERVICE_NAME="inventory-service"
ENV OTEL_TRACES_EXPORTER="otlp"
ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"

CMD ["opentelemetry-instrument", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
