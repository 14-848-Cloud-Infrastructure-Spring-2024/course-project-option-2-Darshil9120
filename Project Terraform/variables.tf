variable "project_id" {
  type        = string
  description = "The Project ID in GCP."
}

variable "region" {
  type        = string
  description = "The region where resources will be created."
}


variable "credentials_json" {
  type        = string
  description = "Path to the GCP credentials file."
}

variable "cluster_name" {
  type        = string
  description = "server name."

}
