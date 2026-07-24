import asyncio
import os
import random
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# inventory-service
#
# Simulates a small inventory backend that answers stock lookups by SKU.
# A "database lookup" is emulated with a small base latency.
#
# The service can be put into a degraded state at runtime through
# POST /admin/chaos. In the degraded state a fraction of lookups take a long
# time, which is the fault scenario used in this assignment.
#
# NOTE: this service intentionally ships WITHOUT metrics or tracing. Adding
# observability is part of the assignment.
# ---------------------------------------------------------------------------

# --- OpenTelemetry 模組導入 ---
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# 定義 Service Name，會在 Jaeger/Grafana 中識別此服務
resource = Resource.create({"service.name": "inventory-service"})

# 設定 Tracing Provider 與 Export 到 OTEL Collector (預設埠號 4317 gRPC)
OTEL_COLLECTOR_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")

tracer_provider = TracerProvider(resource=resource)
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_COLLECTOR_ENDPOINT, insecure=True))
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

# 設定 Metrics Provider 與 Export 到 OTEL Collector
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=OTEL_COLLECTOR_ENDPOINT, insecure=True)
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

BASE_LATENCY_MS = int(os.getenv("INVENTORY_BASE_LATENCY_MS", "15"))


class Degradation:
    """Runtime-controllable fault state."""

    def __init__(self) -> None:
        self.enabled = os.getenv("INVENTORY_DEGRADED", "false").lower() == "true"
        self.latency_ms = int(os.getenv("INVENTORY_DEGRADED_LATENCY_MS", "2000"))
        self.probability = float(os.getenv("INVENTORY_DEGRADED_PROBABILITY", "0.3"))


state = Degradation()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="inventory-service", lifespan=lifespan)

# --- 為 FastAPI 自動捕捉傳入的 HTTP Tracing 與 Metrics ---
FastAPIInstrumentor.instrument_app(app)

def _stock_for(sku: str) -> int:
    # Deterministic pseudo-stock so repeated lookups of the same SKU are stable.
    rng = random.Random(sku)
    return rng.randint(0, 500)


class ChaosConfig(BaseModel):
    enabled: bool
    latency_ms: Optional[int] = None
    probability: Optional[float] = None


@app.get("/health")
async def health():
    return {"status": "ok", "service": "inventory-service"}


@app.get("/stock/{sku}")
async def get_stock(sku: str):
    # Normal "database" lookup latency.
    await asyncio.sleep(BASE_LATENCY_MS / 1000.0 + random.uniform(0, 0.01))

    # In the degraded state, a fraction of lookups hit a slow path.
    if state.enabled and random.random() < state.probability:
        await asyncio.sleep(state.latency_ms / 1000.0)

    return {"sku": sku, "quantity": _stock_for(sku), "warehouse": "TPE-1"}


@app.get("/admin/chaos")
async def get_chaos():
    return {
        "enabled": state.enabled,
        "latency_ms": state.latency_ms,
        "probability": state.probability,
    }


@app.post("/admin/chaos")
async def set_chaos(cfg: ChaosConfig):
    state.enabled = cfg.enabled
    if cfg.latency_ms is not None:
        state.latency_ms = cfg.latency_ms
    if cfg.probability is not None:
        state.probability = cfg.probability
    return {
        "enabled": state.enabled,
        "latency_ms": state.latency_ms,
        "probability": state.probability,
    }
