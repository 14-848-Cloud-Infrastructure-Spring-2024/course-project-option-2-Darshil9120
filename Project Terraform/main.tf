resource "google_container_cluster" "main_gke_cluster" {
  name     = var.cluster_name
  location = var.region
  project = var.project_id
  remove_default_node_pool = true
  initial_node_count = 1
  deletion_protection = false
  
  workload_identity_config {
		workload_pool =  "${var.project_id}.svc.id.goog"
  }
   
}

resource "google_container_node_pool" "main_node_pool" {
  name       = "main-node-pool"
  location   = var.region
  cluster    = google_container_cluster.main_gke_cluster.name
  node_count = 1

  node_config {
    preemptible  = false
    disk_size_gb = 100
  }
}

resource "null_resource" "deploy_backend" {
  depends_on = [
    google_container_node_pool.main_node_pool
  ]

  provisioner "local-exec" {
    command = "gcloud container clusters get-credentials ${google_container_cluster.main_gke_cluster.name} --region=${google_container_cluster.main_gke_cluster.location}"
  }
  
  provisioner "local-exec" {
    command = "kubectl apply -f service-pro-backend-lb.yaml"
  }


  provisioner "local-exec" {
    command = "kubectl apply -f pro-backend-deployment.yaml"
  }
 
}


 