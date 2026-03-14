variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

# ── Per-module variables (only needed if that module is enabled) ──────────────

variable "cloud_run_image" {
  description = "Container image URI for Cloud Run (e.g. gcr.io/my-project/agent:latest)"
  type        = string
  default     = ""
}

variable "bigquery_dataset_id" {
  description = "BigQuery dataset ID to create"
  type        = string
  default     = "agent_dataset"
}

variable "bucket_name" {
  description = "Cloud Storage bucket name"
  type        = string
  default     = ""
}

variable "pubsub_topic_name" {
  description = "Pub/Sub topic name"
  type        = string
  default     = "agent-topic"
}

variable "db_name" {
  description = "Cloud SQL database name"
  type        = string
  default     = "agentdb"
}
