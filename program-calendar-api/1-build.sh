#!/usr/bin/env bash
# Build the Docker image and push it to GHCR.
#
# You usually don't need this: GitHub Actions builds on every push to main.
# Use this only for a quick local iteration before pushing a commit.
#
# Prereqs:
#   - docker daemon running
#   - `docker login ghcr.io` succeeded for your GitHub user
#   - you have push permission on github.com/slaclab packages

set -euo pipefail
cd "$(dirname "$0")"
source ./config.sh

echo "==> docker build -t ${IMAGE}:${TAG} ."
docker build -t "${IMAGE}:${TAG}" .

echo "==> docker push ${IMAGE}:${TAG}"
docker push "${IMAGE}:${TAG}"

echo "Done. Image: ${IMAGE}:${TAG}"
