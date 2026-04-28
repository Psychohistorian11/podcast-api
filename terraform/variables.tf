//Son los valores que pueden cambiar entre ambientes o que no quieres hardcodear. Como el .env pero para Terraform.

variable "aws_region" {
  description = "Región de AWS donde se desplegará la infraestructura"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto, usado para nombrar todos los recursos"
  type        = string
  default     = "podcast-api"
}

variable "environment" {
  description = "Ambiente de despliegue (dev o prod)"
  type        = string
  default     = "prod"
}

variable "db_username" {
  description = "Usuario de la base de datos PostgreSQL"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Password de la base de datos PostgreSQL"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
  default     = "podcast_db"
}

variable "ec2_instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "rds_instance_class" {
  description = "Tipo de instancia RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "my_ip" {
  description = "IP pública para acceso SSH (formato: x.x.x.x/32)"
  type        = string
}

variable "simon_api_url" {
  description = "URL del API de Simón"
  type        = string
  default     = "http://34.41.107.90"

}

variable "jose_pablo_api_url" {
  description = "URL del API de José Pablo"
  type        = string
  default     = "http://34.21.77.119/api/v2/"
}
