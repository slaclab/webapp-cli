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

missing=()
for f in "${SECRET_FILES[@]}"; do
  [[ -f "${f}" ]] || missing+=("${f}")
done
if [[ ${#missing[@]} -eq 0 ]]; then
  echo "==> creating Secret app-secrets from local files"
  secret_args=()
  for f in "${SECRET_FILES[@]}"; do
    secret_args+=(--from-file="${f}")
  done
  kubectl -n "${NAMESPACE}" create secret generic app-secrets \
    "${secret_args[@]}" \
    --dry-run=client -o yaml | kubectl apply -f -
else
  echo "==> skipping Secret: missing ${missing[*]}"
  echo "    Pod will still start. /docs will render. Event endpoints will"
  echo "    error until you drop these files in and re-run ./2-deploy.sh."
  kubectl -n "${NAMESPACE}" delete secret app-secrets --ignore-not-found >/dev/null
fi

echo "==> kubectl apply -f manifests/deployment.yaml"
kubectl apply -f manifests/deployment.yaml

echo "==> kubectl apply -f manifests/service.yaml"
kubectl apply -f manifests/service.yaml

echo "==> waiting for rollout..."
kubectl -n "${NAMESPACE}" rollout status "deployment/${APP_NAME}" --timeout=120s

echo "Done. Try: ./3-status.sh   or   kubectl -n ${NAMESPACE} port-forward svc/${APP_NAME} 8080:80"
