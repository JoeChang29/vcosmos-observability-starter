# vCosmos Observability Take-home — Starter

一個可在本機執行的最小環境，包含兩個 Python FastAPI 微服務：

```text
api-service  →  inventory-service
```

`api-service` 對外提供產品查詢，每次查詢會呼叫 `inventory-service` 取得庫存。

> ⚠️ 這個 starter **刻意沒有任何 metrics 或 tracing**。加入可觀測性、dashboard 與告警，正是這份作業的內容。你需要延伸這個專案（包含 `docker-compose.yml`）。

---

## 需求

- Docker / Docker Compose

## 啟動環境

```bash
docker compose up --build
```

啟動後：

- api-service：<http://localhost:8000>（`GET /products/{sku}`、`GET /health`）
- inventory-service：<http://localhost:8001>（`GET /stock/{sku}`、`GET /health`）

快速驗證：

```bash
curl http://localhost:8000/products/sku-1
# {"sku":"sku-1","name":"Product 1","price":5.99,"quantity":...,"in_stock":true}
```

## 產生測試流量

流量產生器放在獨立的 compose profile，`docker compose up` 不會自動啟動它。要送流量時：

```bash
docker compose --profile loadgen up loadgen
```

可用環境變數調整（在 `docker-compose.yml` 或指令中設定）：`RPS`（預設 10）、`TARGET_URL`。

不想用容器的話，也可以用簡單的迴圈：

```bash
while true; do curl -s http://localhost:8000/products/sku-$((RANDOM%20+1)) > /dev/null; sleep 0.1; done
```

## 觸發異常情境

在有流量的情況下觸發故障：

```bash
./scripts/trigger_incident.sh
```

觸發後，一段時間內 API 會明顯變慢。請透過你加入的 metrics 與 traces 觀察並定位問題。

關閉故障：

```bash
./scripts/resolve_incident.sh
```

（兩個 script 都是呼叫 inventory-service 的 admin 端點，可用 `INVENTORY_ADMIN_URL`、`LATENCY_MS`、`PROBABILITY` 覆寫參數。）

## 服務端點

| 服務 | 方法 | 路徑 | 說明 |
|---|---|---|---|
| api-service | GET | `/products/{sku}` | 查詢產品，內部呼叫 inventory-service |
| api-service | GET | `/health` | 健康檢查 |
| inventory-service | GET | `/stock/{sku}` | 查詢庫存 |
| inventory-service | GET | `/health` | 健康檢查 |
| inventory-service | GET/POST | `/admin/chaos` | 查詢／控制故障狀態（由 script 使用） |

SKU 範圍為 `sku-1` ～ `sku-20`。

## 已知限制

- 沒有 metrics、tracing、logging 之外的標準輸出。
- 沒有持久化儲存；庫存為記憶體內的模擬資料。
- 僅供本機評估使用，非 production 設定。
