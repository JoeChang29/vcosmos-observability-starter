#!/usr/bin/env bash
# Trigger the fault scenario in the running environment.
# Enables degraded behaviour in inventory-service via its admin endpoint.
set -euo pipefail

INVENTORY_ADMIN_URL="${INVENTORY_ADMIN_URL:-http://localhost:8001}"
LATENCY_MS="${LATENCY_MS:-2000}"
PROBABILITY="${PROBABILITY:-0.3}"

echo "Enabling fault scenario (latency_ms=${LATENCY_MS}, probability=${PROBABILITY}) ..."
curl -sS -X POST "${INVENTORY_ADMIN_URL}/admin/chaos" \
  -H 'Content-Type: application/json' \
  -d "{\"enabled\": true, \"latency_ms\": ${LATENCY_MS}, \"probability\": ${PROBABILITY}}"
echo
echo "Fault scenario ENABLED. Observe the impact via your dashboards and traces,"
echo "then run scripts/resolve_incident.sh to turn it off."
