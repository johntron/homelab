# Consider using https://registry.terraform.io/providers/hashicorp/cloudinit/latest/docs

resource "terraform_data" "cloudinit_server" {
  provisioner "local-exec" {
    working_dir = path.module
#    interpreter = ["python3"]
    command     = "python3 serve-create.py daemon"
  }
}