variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Ambiente de despliegue"
  type        = string
}

variable "my_ip" {
  description = "IP pública para acceso directo a RDS"
  type        = string
}

variable "ec2_security_group_id" {
  description = "ID del Security Group del EC2 para permitir acceso a RDS"
  type        = string
}
