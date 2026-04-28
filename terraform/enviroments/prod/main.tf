# Ambiente de producción
# Usa los mismos módulos del raíz pero con valores de producción

module "podcast_api_prod" {
  source = "../../"

  aws_region         = "us-east-1"
  project_name       = "podcast-api"
  environment        = "prod"
  db_username        = "postgres"
  db_password        = var.db_password
  db_name            = "podcast_db"
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
