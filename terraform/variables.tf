variable "project_id" {
  description = "The GCP project id."
  type        = string
}

variable "location_id" {
  description = "The GCP location id."
  default     = "us-central1"
}

variable "env" {
  description = "The environment (local|dev|prod)."
  type        = string
}

variable "climateiq_flood_simulation_bucket_set" {
  description = "A set of GCS bucket names for the flood simulation."
  type        = list(string)
}