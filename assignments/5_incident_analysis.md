# Starter incident analysis

## 使用者看到的症狀
部分請求回應速度明顯變慢

## Metrics 顯示了什麼
prometheus>graph
sum by (service_name) (increase(http_server_duration_milliseconds_count[2h])) - sum by (service_name) (increase(http_server_duration_milliseconds_bucket{le="100.0"}[2h]))
可以看到當chaos開啟，會呈現直線上升

## Trace 顯示了什麼
顯示在api-service訪問inventory-service的GET /stock/{sku}耗時至少2s(2000ms)

## 判斷的 root cause
在inventory-service的app.py裡面設定了/admin/chaos的路徑可以提供特殊功能，如果開啟可以讓整個inventory service的/stock/{sku}依照輸入參數進入指定睡眠秒數

## Immediate mitigation
修改chaos參數，將LATENCY_MS, PROBABILITY調低，可以透過scripts/trigger_incident.sh修改

## Long-term improvement
在不影響原有功能下，inventory, api, loadgen新增一段@app.get("/stock/clean/{sku}")
