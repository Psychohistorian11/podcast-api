variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Ambiente de despliegue"
  type        = string
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
}

variable "key_name" {
  description = "Nombre del Key Pair para SSH"
  type        = string
}

variable "security_group_id" {
  description = "ID del Security Group para el EC2"
  type        = string
}

variable "db_username" {
  description = "Usuario de la base de datos"
  type        = string
}

variable "db_password" {
  description = "Password de la base de datos"
  type        = string
  sensitive   = true
}

variable "db_endpoint" {
  description = "Endpoint de la base de datos RDS"
  type        = string
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
}

variable "simon_api_url" {
  description = "URL de la API de Simón"
  type        = string
}

variable "jose_pablo_api_url" {
  description = "URL de la API de José Pablo"
  type        = string
  default     = ""
}
