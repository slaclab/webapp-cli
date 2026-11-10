#!/usr/bin/env bash
# Delete all deployed resources. Leaves the namespace in place by default.
# Pass --namespace to also remove the namespace.

set -euo pipefail
cd "$(dirname "$0")"
source ./config.sh

echo "==> kubectl delete -f manifests/service.yaml --ignore-not-found"
kubectl delete -f manifests/service.yaml --ignore-not-found

echo "==> kubectl delete -f manifests/deployment.yaml --ignore-not-found"
kubectl delete -f manifests/deployment.yaml --ignore-not-found

echo "==> kubectl -n ${NAMESPACE} delete secret app-secrets --ignore-not-found"
kubectl -n "${NAMESPACE}" delete secret app-secrets --ignore-not-found

if [[ "${1:-}" == "--namespace" ]]; then
  echo "==> kubectl delete -f manifests/namespace.yaml --ignore-not-found"
  kubectl delete -f manifests/namespace.yaml --ignore-not-found
else
  echo "Namespace ${NAMESPACE} kept. Pass --namespace to this script to remove it too."
fi
