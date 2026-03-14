terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ── Always required ───────────────────────────────────────────────────────────

module "vertex_ai" {
  source     = "./modules/vertex_ai"
  project_id = var.project_id
  region     = var.region
}

# ── Uncomment the modules this client needs ───────────────────────────────────

# module "cloud_run" {
#   source      = "./modules/cloud_run"
#   project_id  = var.project_id
#   region      = var.region
#   image       = var.cloud_run_image
# }

# module "bigquery" {
#   source     = "./modules/bigquery"
#   project_id = var.project_id
#   region     = var.region
#   dataset_id = var.bigquery_dataset_id
# }

# module "cloud_sql" {
#   source     = "./modules/cloud_sql"
#   project_id = var.project_id
#   region     = var.region
#   db_name    = var.db_name
# }

# module "cloud_storage" {
#   source      = "./modules/cloud_storage"
#   project_id  = var.project_id
#   region      = var.region
#   bucket_name = var.bucket_name
# }

# module "pubsub" {
#   source      = "./modules/pubsub"
#   project_id  = var.project_id
#   topic_name  = var.pubsub_topic_name
# }
