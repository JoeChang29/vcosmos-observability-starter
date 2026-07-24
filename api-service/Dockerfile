FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 自動安裝可用的 instrumentation 驅動
RUN opentelemetry-bootstrap -a install

COPY app.py .
EXPOSE 8000

# 設定 OpenTelemetry 預設環境變數 (可由 Docker Compose 或 k8s 覆蓋)
ENV OTEL_SERVICE_NAME="api-service"
ENV OTEL_TRACES_EXPORTER="otlp"
ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
# 指向您的 Collector 地址，例如: http://otel-collector:4317
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"

CMD ["opentelemetry-instrument", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
