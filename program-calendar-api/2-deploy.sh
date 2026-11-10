#!/usr/bin/env bash
# Apply all Kubernetes manifests + create the Secret from local files.
#
# Reads the three gitignored files from $APP_SRC and publishes them as
# the Kubernetes Secret "app-secrets" in $NAMESPACE.

set -euo pipefail
cd "$(dirname "$0")"
source ./config.sh

echo "==> kubectl apply -f manifests/namespace.yaml"
kubectl apply -f manifests/namespace.yaml

echo "==> creating Secret app-secrets from local files"
secret_args=()
for f in "${SECRET_FILES[@]}"; do
  if [[ ! -f "${f}" ]]; then
    echo "ERROR: ${f} not found in $(pwd). Generate it locally (run the app once)" >&2
    echo "       and place it here. It will NOT be committed (see .gitignore)." >&2
    exit 1
  fi
  secret_args+=(--from-file="${f}")
done
kubectl -n "${NAMESPACE}" create secret generic app-secrets \
  "${secret_args[@]}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> kubectl apply -f manifests/deployment.yaml"
kubectl apply -f manifests/deployment.yaml

echo "==> kubectl apply -f manifests/service.yaml"
kubectl apply -f manifests/service.yaml

echo "==> waiting for rollout..."
kubectl -n "${NAMESPACE}" rollout status "deployment/${APP_NAME}" --timeout=120s

echo "Done. Try: ./3-status.sh   or   kubectl -n ${NAMESPACE} port-forward svc/${APP_NAME} 8080:80"
