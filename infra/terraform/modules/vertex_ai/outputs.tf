output "service_account_email" {
  description = "Email of the ADK agent service account"
  value       = google_service_account.agent_sa.email
}
