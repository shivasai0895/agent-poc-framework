resource "google_project_service" "cloud_run" {
  project            = var.project_id
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_cloud_run_v2_service" "agent" {
  project  = var.project_id
  name     = var.service_name
  location = var.region

  template {
    containers {
      image = var.image

      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }

      ports {
        container_port = 8080
      }
    }
  }

  depends_on = [google_project_service.cloud_run]
}

# Allow unauthenticated access (remove for production)
resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.agent.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
