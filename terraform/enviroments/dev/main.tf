# Ambiente de desarrollo
# Misma estructura pero con nombres diferentes para no pisar producción

module "podcast_api_dev" {
  source = "../../"

  aws_region         = "us-east-1"
  project_name       = "podcast-api"
  environment        = "dev"
  db_username        = "postgres"
  db_password        = var.db_password
  db_name            = "podcast_db_dev"
  ec2_instance_type  = "t3.micro"
  rds_instance_class = "db.t3.micro"
  my_ip              = var.my_ip
  simon_api_url      = "http://34.41.107.90"
  jose_pablo_api_url = ""
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "my_ip" {
  type = string
}
