#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-searxng}"
ROTATOR_DEPLOY="${ROTATOR_DEPLOY:-searxng-vpn-rotator}"
EGRESS_CRONJOB="${EGRESS_CRONJOB:-searxng-egress-check}"
METRICS_PORT="${METRICS_PORT:-9090}"
HEALTH_PATH="${HEALTH_PATH:-/healthz}"
METRICS_PATH="${METRICS_PATH:-/metrics}"
TIMEOUT="${TIMEOUT:-120}"

command -v kubectl >/dev/null || { echo "kubectl not found" >&2; exit 1; }
command -v curl >/dev/null || { echo "curl not found" >&2; exit 1; }

RG_BIN="rg"
if ! command -v rg >/dev/null; then
  RG_BIN="grep -E"
fi

echo "[searxng-rotation] checking rotator pod..."
kubectl -n "$NAMESPACE" get pods -l app.kubernetes.io/name="$ROTATOR_DEPLOY"

echo "[searxng-rotation] starting port-forward for metrics..."
kubectl -n "$NAMESPACE" port-forward "deploy/${ROTATOR_DEPLOY}" "${METRICS_PORT}:${METRICS_PORT}" >/tmp/searxng-rotator-pf.log 2>&1 &
PF_PID=$!
cleanup() {
  kill "$PF_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT
sleep 1

echo "[searxng-rotation] health check..."
curl -s "http://localhost:${METRICS_PORT}${HEALTH_PATH}" || true
echo
echo "[searxng-rotation] metrics snapshot..."
curl -s "http://localhost:${METRICS_PORT}${METRICS_PATH}" | ${RG_BIN} "searxng_vpn_rotator_" || true
echo

JOB_NAME="searxng-egress-check-manual-$(date +%s)"
echo "[searxng-rotation] running egress check job ${JOB_NAME}..."
kubectl -n "$NAMESPACE" create job --from=cronjob/"${EGRESS_CRONJOB}" "${JOB_NAME}"
kubectl -n "$NAMESPACE" wait --for=condition=complete "job/${JOB_NAME}" --timeout="${TIMEOUT}s" || true
kubectl -n "$NAMESPACE" logs "job/${JOB_NAME}" || true

echo "[searxng-rotation] triggering manual rotation..."
if ! kubectl -n "$NAMESPACE" exec "deploy/${ROTATOR_DEPLOY}" -- env METRICS_ENABLED=false ACTIVE_POOL_SWAP_COOLDOWN_S=0 python3 /app/rotator.py --swap-only; then
  echo "[searxng-rotation] swap-only failed, rotating all VPN endpoints..."
  kubectl -n "$NAMESPACE" exec "deploy/${ROTATOR_DEPLOY}" -- env METRICS_ENABLED=false python3 /app/rotator.py --rotate-now
fi

echo "[searxng-rotation] recent rotator logs..."
kubectl -n "$NAMESPACE" logs "deploy/${ROTATOR_DEPLOY}" --tail=50 || true
