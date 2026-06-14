variable "project_id" {
  type        = string
  default     = "gen-lang-client-0916506621"
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

# === Non-Sensitive Variables ===
variable "langfuse_base_url" { type = string }
variable "base_url"          { type = string }
variable "mongo_db_name"     { type = string }

# === Sensitive Secrets ===
variable "langfuse_public_key" { type = string; sensitive = true }
variable "langfuse_secret_key" { type = string; sensitive = true }
variable "vdb_key"             { type = string; sensitive = true }
variable "redis_api_key"       { type = string; sensitive = true }
variable "redis_url"           { type = string; sensitive = true }
variable "mongo_uri"           { type = string; sensitive = true }