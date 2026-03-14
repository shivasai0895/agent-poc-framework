output "connection_name" {
  description = "Cloud SQL connection name (use with Cloud SQL Auth Proxy)"
  value       = google_sql_database_instance.instance.connection_name
}

output "database_name" {
  value = google_sql_database.database.name
}
