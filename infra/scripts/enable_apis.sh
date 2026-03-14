#!/usr/bin/env bash
# Fallback: manually enable GCP APIs and set up IAM when Terraform isn't available.
# Usage: PROJECT_ID=my-project bash infra/scripts/enable_apis.sh

set -euo pipefail

PROJECT_ID="${PROJECT_ID:?Set PROJECT_ID environment variable}"

echo "Configuring project: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# ── Always required ───────────────────────────────────────────────────────────
echo "Enabling core APIs..."
gcloud services enable \
  aiplatform.googleapis.com \
  iam.googleapis.com

echo "Creating agent service account..."
gcloud iam service-accounts create adk-agent \
  --display-name="ADK Agent Service Account" \
  --project="$PROJECT_ID" || echo "Service account already exists"

SA_EMAIL="adk-agent@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/aiplatform.user"

# ── Uncomment as needed ───────────────────────────────────────────────────────

# Cloud Run
# gcloud services enable run.googleapis.com

# BigQuery
# gcloud services enable bigquery.googleapis.com
# gcloud projects add-iam-policy-binding "$PROJECT_ID" \
#   --member="serviceAccount:${SA_EMAIL}" \
#   --role="roles/bigquery.dataViewer"
# gcloud projects add-iam-policy-binding "$PROJECT_ID" \
#   --member="serviceAccount:${SA_EMAIL}" \
#   --role="roles/bigquery.jobUser"

# Cloud SQL
# gcloud services enable sqladmin.googleapis.com
# gcloud projects add-iam-policy-binding "$PROJECT_ID" \
#   --member="serviceAccount:${SA_EMAIL}" \
#   --role="roles/cloudsql.client"

# Cloud Storage
# gcloud services enable storage.googleapis.com
# gsutil iam ch "serviceAccount:${SA_EMAIL}:roles/storage.objectAdmin" gs://YOUR_BUCKET

# Pub/Sub
# gcloud services enable pubsub.googleapis.com
# gcloud pubsub topics add-iam-policy-binding YOUR_TOPIC \
#   --member="serviceAccount:${SA_EMAIL}" \
#   --role="roles/pubsub.publisher"

echo "Done. SA email: $SA_EMAIL"
