terraform {
  required_providers {
    kind = {
      source = "justenwalker/kind"
      version = "0.17.0"
    }
  }
}
provider "kind" {
  provider   = "podman"
  kubeconfig = pathexpand("~/.kube/kind-config")
}
resource "kind_cluster" "new" {
  name = "test"
  config = <<-EOF
        apiVersion: kind.x-k8s.io/v1alpha4
        kind: Cluster
    EOF
}