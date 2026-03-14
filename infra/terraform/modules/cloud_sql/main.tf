resource "google_project_service" "cloud_sql" {
  project            = var.project_id
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_sql_database_instance" "instance" {
  project          = var.project_id
  name             = var.instance_name
  region           = var.region
  database_version = "POSTGRES_15"

  settings {
    tier = var.db_tier

    ip_configuration {
      ipv4_enabled = false
      # For private IP, add a VPC network reference here
    }
  }

  deletion_protection = false  # Set to true for production

  depends_on = [google_project_service.cloud_sql]
}

resource "google_sql_database" "database" {
  project  = var.project_id
  name     = var.db_name
  instance = google_sql_database_instance.instance.name
}

resource "google_project_iam_member" "cloud_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:adk-agent@${var.project_id}.iam.gserviceaccount.com"
}
