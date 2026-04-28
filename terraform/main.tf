# 1. Security Group EC2
module "security_group_ec2" {
  source = "./modules/networking/security_group_ec2"

  project_name = var.project_name
  environment  = var.environment
  my_ip        = var.my_ip
}

# 2. Security Group RDS
# Depende del SG del EC2 para saber a quién permitirle acceso
module "security_group_rds" {
  source = "./modules/networking/security_group_rds"

  project_name          = var.project_name
  environment           = var.environment
  my_ip                 = var.my_ip
  ec2_security_group_id = module.security_group_ec2.security_group_id
}

# 3. Key Pair
module "key_pair" {
  source = "./modules/compute/key_pair"

  project_name    = var.project_name
  environment     = var.environment
  public_key_path = "/home/psychohistorian/.ssh/podcast-api-key.pub"
}

# 4. RDS
# Se crea antes que el EC2 porque el EC2 necesita el endpoint
module "rds" {
  source = "./modules/database/rds"

  project_name      = var.project_name
  environment       = var.environment
  instance_class    = var.rds_instance_class
  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
  security_group_id = module.security_group_rds.security_group_id
}

# 5. EC2
# Se crea al final porque necesita el endpoint de RDS
module "ec2" {
  source = "./modules/compute/ec2"

  project_name       = var.project_name
  environment        = var.environment
  instance_type      = var.ec2_instance_type
  key_name           = module.key_pair.key_name
  security_group_id  = module.security_group_ec2.security_group_id
  db_username        = var.db_username
  db_password        = var.db_password
  db_endpoint        = module.rds.endpoint
  db_name            = var.db_name
  simon_api_url      = var.simon_api_url
  jose_pablo_api_url = var.jose_pablo_api_url
}
