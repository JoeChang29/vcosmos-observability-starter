# 這裡是readme的答案區

## 如何啟動環境
```bash
docker compose up --build
```

## 如何產生測試流量 如何觸發異常
```bash

```

## Grafana 與 trace UI 的位置
### Grafana
```text
http://localhost:3000
#set data source to http://prometheus:9090
#user:pwd is admin:admin for convenience
```

### trace UI
```text
http://localhost:16686
```

## 如何驗證成果


## 已知限制
1. 在docker-compose.yml裡面api-service, inventory-service如果有debug需求可以將參數OTEL_LOG_LEVEL調整為為debug,console, console參數，但是可能導致log過於龐大，不建議長時間開啟或者爆量測試
