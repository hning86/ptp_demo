#!/bin/bash
set -e

# Set default configuration
SERVICE_NAME="craft-ptp-demo-v2"
REGION="us-central1"
PROJECT_ID="ninghai-ccai"

# Increment version
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
python3 "$SCRIPT_DIR/increment_version.py"

# Commit the version increment change to git
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"
VERSION=$(python3 -c "import json; print(json.load(open('$ROOT_DIR/frontend/version.json'))['version'])")
git -C "$ROOT_DIR" add frontend/version.json
git -C "$ROOT_DIR" commit -m "Bump version to v$VERSION"

echo ">>> Deploying Craft PTP interactive frontend + backend to Google Cloud Run..."

gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --port 8000 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,VAIS_LOCATION=global,VAIS_DATASTORE_ID=ptp-docs-store"

echo ">>> Deployment Trigger Completed!"
