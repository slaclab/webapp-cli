# Shared variables sourced by every script in this directory.
# Edit here if you fork for a different app or namespace.

APP_NAME="program-calendar-api"
NAMESPACE="program-calendar-dev"
IMAGE="ghcr.io/slaclab/program-calendar-api"
TAG="dev"

# Gitignored files that become the Kubernetes Secret. Place these next to
# this script before running 2-deploy.sh. They never get committed.
SECRET_FILES=(credentials.json token.json config.json)
