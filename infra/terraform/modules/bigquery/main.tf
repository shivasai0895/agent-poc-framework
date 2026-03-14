resource "google_project_service" "bigquery" {
  project            = var.project_id
  service            = "bigquery.googleapis.com"
  disable_on_destroy = false
}

resource "google_bigquery_dataset" "dataset" {
  project     = var.project_id
  dataset_id  = var.dataset_id
  location    = var.region
  description = "Dataset for ADK agent"

  depends_on = [google_project_service.bigquery]
}

# Grant the agent service account read + job access
# Assumes vertex_ai module has already created adk-agent@... SA
resource "google_project_iam_member" "bq_data_viewer" {
  project = var.project_id
  role    = "roles/bigquery.dataViewer"
  member  = "serviceAccount:adk-agent@${var.project_id}.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "bq_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:adk-agent@${var.project_id}.iam.gserviceaccount.com"
}
