variable "project_id" {
  type        = string
  description = "The GCP Project ID where resources will be deployed"
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "The target geographic region for deployment"
}

variable "backend_image" {
  type        = string
  description = "The fully qualified Artifact Registry path for the backend image"
}

variable "frontend_image" {
  type        = string
  description = "The fully qualified Artifact Registry path for the frontend image"
}
gen-lang-client-0916506621