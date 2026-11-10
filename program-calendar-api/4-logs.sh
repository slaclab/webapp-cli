#!/usr/bin/env bash
# Tail logs. Pass -f to follow.

set -euo pipefail
cd "$(dirname "$0")"
source ./config.sh

echo "==> kubectl -n ${NAMESPACE} logs -l app=${APP_NAME} $*"
kubectl -n "${NAMESPACE}" logs -l "app=${APP_NAME}" --tail=200 --prefix=true "$@"
