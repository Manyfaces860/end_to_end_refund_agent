terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "worknoon-terraform-state-bucket"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "iam.googleapis.com"
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "my_repo" {
  repository_id = "worknoon-repo"
  location      = var.region
  description   = "Docker repository for Frontend and Backend images"
  format        = "DOCKER"

  depends_on = [google_project_service.required_apis]
}

resource "google_cloud_run_v2_service" "backend" {
  name     = "worknoon-backend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.backend_image
      ports {
        container_port = 8000
      }

      env {
        name  = "FRONTEND_URL"
        value = google_cloud_run_v2_service.frontend.uri
      }

      env {
        name  = "LANGFUSE_BASE_URL"
        value = var.langfuse_base_url
      }
      env {
        name  = "BASE_URL"
        value = var.base_url
      }
      env {
        name  = "MONGO_DB_NAME"
        value = var.mongo_db_name
      }
      env {
        name  = "LANGFUSE_PUBLIC_KEY"
        value = var.langfuse_public_key
      }
      env {
        name  = "LANGFUSE_SECRET_KEY"
        value = var.langfuse_secret_key
      }
      env {
        name  = "VDB_KEY"
        value = var.vdb_key
      }
      env {
        name  = "REDIS_API_KEY"
        value = var.redis_api_key
      }
      env {
        name  = "REDIS_URL"
        value = var.redis_url
      }
      env {
        name  = "MONGO_URI"
        value = var.mongo_uri
      }

      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
    }
  }

  depends_on = [
    google_project_service.required_apis,
    google_artifact_registry_repository.my_repo,
    google_cloud_run_v2_service.frontend
  ]
}

resource "google_cloud_run_v2_service_iam_member" "backend_public" {
  name     = google_cloud_run_v2_service.backend.name
  location = google_cloud_run_v2_service.backend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_v2_service" "frontend" {
  name     = "worknoon-frontend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.frontend_image
    }
  }

  depends_on = [
    google_project_service.required_apis,
    google_artifact_registry_repository.my_repo
  ]
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  name     = google_cloud_run_v2_service.frontend.name
  location = google_cloud_run_v2_service.frontend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}