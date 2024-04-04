provider "google" {
  credentials = file(var.credentials_json)
  project     = var.project_id
  region      = var.region
}

data "google_client_config" "default" {}


provider "kubernetes" {
  host                   = "https://${google_container_cluster.main_gke_cluster.endpoint}"
  cluster_ca_certificate = base64decode(google_container_cluster.main_gke_cluster.master_auth[0].cluster_ca_certificate)
  token                  = data.google_client_config.default.access_token
}