# vCosmos Take-home：使用可觀測性定位微服務效能問題

## 背景

隨附的 starter project 可在本機執行，包含兩個 Python FastAPI 服務：

```text
api-service → inventory-service
```

專案中包含兩個微服務、Docker Compose、一個簡單的流量產生工具，以及一個可觸發的異常情境。

目前系統缺少足夠的可觀測性：當異常發生時，只能知道 API 變慢，無法快速判斷問題位於哪一個服務。

## 任務目標

請加入基本的 metrics 與 distributed tracing，並利用觀測到的資料找出異常原因。

- 作業期限：**收到題目後三天內**

---

## 必要成果

### 1. 一個指令即可啟動

啟動完整環境時，應能使用：

```bash
docker compose up --build
```

不需要部署到 Kubernetes、AWS 或 GCP。

### 2. Metrics

至少提供以下三項指標：

- Request rate
- Error rate
- p95 latency

並建立一個 Grafana dashboard 顯示這三項資訊。不要求大量 dashboard，一個能協助判斷問題的即可。

### 3. Distributed tracing

使用 OpenTelemetry，讓一次 request 經過 `api-service → inventory-service` 時，可以在**同一條 trace** 中看到兩個服務的 spans。

Trace backend 可自行選擇（例如 Jaeger、Grafana Tempo 或其他合理的開源方案）。

**Trace telemetry 必須經過 OpenTelemetry Collector。** Metrics 則可自行選擇走 Prometheus scrape，或一併經過 Collector。

### 4. 一個告警

建立一個和使用者影響有關的告警（例如 error rate 過高或 p95 latency 過高）。請在 README 中簡短說明：

- 為什麼選擇這個指標
- Threshold 如何決定
- 如何避免短暫波動造成過多告警

### 5. Incident 分析

觸發 starter project 中的異常情境，並提交一份不超過一頁的 `INCIDENT.md`，內容包含：

- 使用者看到的症狀
- Metrics 顯示了什麼
- Trace 顯示了什麼
- 判斷的 root cause
- Immediate mitigation
- Long-term improvement

答案必須引用 metrics 或 traces 作為證據，不能只根據 source code 判斷。

### 6. README

README 至少包含：如何啟動環境、如何產生測試流量、如何觸發異常、Grafana 與 trace UI 的位置、如何驗證成果、已知限制。

---

## AI 工具使用

可以並且鼓勵使用 AI 工具。請另外提交簡短的 `AI_USAGE.md`，說明：

- 使用了哪些 AI 工具
- AI 協助完成哪些部分
- 如何驗證 AI 產生的設定或程式碼
- 至少一項你修改或沒有採用的 AI 建議

不需要提供完整 prompt 或聊天紀錄。後續面試會請你說明提交內容，並現場完成一項小修改，以確認你理解整體設計。

---

## 加分項目（皆非必要，完成一至兩項即可）

1. **Logs 與 Trace 關聯**：讓 application log 包含 `trace_id`，可從 trace 找到 log，或從 log 回查 trace。透過結構化 stdout log 展示即可，不需部署 Loki。
2. **基本 CI**：使用 GitHub Actions 或其他 CI 工具執行 application test、Docker build、Docker Compose configuration validation。
3. **Production 思考**：在 README 中以不超過半頁篇幅說明——若這套設計要部署到 EKS，OpenTelemetry Collector、權限、High Availability 與成本控制會如何調整。
4. **更好的告警設計**：例如使用時間窗口而非單點數值、使用 SLO 或 burn-rate 概念、附上簡單的處理步驟。

---

## 提交內容

```text
README.md
INCIDENT.md
AI_USAGE.md
docker-compose.yml
應用程式與 observability 相關設定
Grafana dashboard 定義
Alert rule
```

可以提交 Git repository，或提供壓縮檔。

## 不需要完成的內容

為控制作業時間，以下不在要求範圍內：Kubernetes manifests、Terraform、AWS／GCP 部署、完整 Production HA、完整 log aggregation platform、大量 dashboard、精美 UI、複雜業務功能。

評估重點不是程式碼數量，而是能否建立一條清楚的調查路徑：

```text
發現異常 → 查看指標 → 找到異常 request → 使用 trace 定位問題
```

---

## 如何開始

請先閱讀 `README.md`，它說明如何啟動環境、產生流量與觸發異常。祝順利！
