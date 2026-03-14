resource "google_storage_bucket" "bucket" {
  project                     = var.project_id
  name                        = var.bucket_name
  location                    = var.region
  force_destroy               = true  # Set to false for production
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_member" "agent_object_admin" {
  bucket = google_storage_bucket.bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:adk-agent@${var.project_id}.iam.gserviceaccount.com"
}
