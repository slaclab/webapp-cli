# Shared variables sourced by every script in this directory.
# Edit here if you fork for a different app or namespace.

APP_NAME="program-calendar-api"
NAMESPACE="program-calendar-dev"
IMAGE="ghcr.io/slaclab/program-calendar-api"
TAG="dev"

# Optional gitignored files that become the Kubernetes Secret "app-secrets".
# Place next to this script to enable live Google Calendar access; otherwise
# the deployment runs without a Secret (/docs works, /events/* will error).
SECRET_FILES=(credentials.json token.json config.json)
