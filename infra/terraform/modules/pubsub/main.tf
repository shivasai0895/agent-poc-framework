resource "google_project_service" "pubsub" {
  project            = var.project_id
  service            = "pubsub.googleapis.com"
  disable_on_destroy = false
}

resource "google_pubsub_topic" "topic" {
  project = var.project_id
  name    = var.topic_name

  depends_on = [google_project_service.pubsub]
}

resource "google_pubsub_subscription" "subscription" {
  project = var.project_id
  name    = coalesce(var.subscription_name, "${var.topic_name}-sub")
  topic   = google_pubsub_topic.topic.name

  ack_deadline_seconds = 20
}

resource "google_pubsub_topic_iam_member" "agent_publisher" {
  project = var.project_id
  topic   = google_pubsub_topic.topic.name
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:adk-agent@${var.project_id}.iam.gserviceaccount.com"
}
