#!/bin/bash
set -e

# Set default configuration
SERVICE_NAME="craft-ptp-demo"
REGION="us-central1"
PROJECT_ID="ninghai-ccai"

# Increment version
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
python3 "$SCRIPT_DIR/increment_version.py"

echo ">>> Deploying Craft PTP interactive frontend + backend to Google Cloud Run..."

gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --port 8000 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,VAIS_LOCATION=global,VAIS_DATASTORE_ID=ptp-docs-store"

echo ">>> Deployment Trigger Completed!"
