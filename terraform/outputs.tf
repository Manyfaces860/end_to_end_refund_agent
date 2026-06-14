output "backend_url" {
  value       = google_cloud_run_v2_service.backend.uri
  description = "The public URL of your backend service"
}

output "frontend_url" {
  value       = google_cloud_run_v2_service.frontend.uri
  description = "The public URL of your frontend service"
}