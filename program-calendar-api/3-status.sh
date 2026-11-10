#!/usr/bin/env bash
# Show what's running.

set -euo pipefail
cd "$(dirname "$0")"
source ./config.sh

echo "==> kubectl -n ${NAMESPACE} get deployment,pod,service"
kubectl -n "${NAMESPACE}" get deployment,pod,service -l "app=${APP_NAME}" -o wide

echo
echo "==> recent events"
kubectl -n "${NAMESPACE}" get events --sort-by=.lastTimestamp | tail -10
