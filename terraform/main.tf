resource "google_storage_bucket" "climateiq_flood_simulation_bucket_set" {
  project = var.project_id

  for_each = toset(var.climateiq_flood_simulation_bucket_set)
  name     = each.value # note: each.key and each.value are the same for a set

  location      = var.location_id
  storage_class = "STANDARD"
  force_destroy = true

  uniform_bucket_level_access = true
}