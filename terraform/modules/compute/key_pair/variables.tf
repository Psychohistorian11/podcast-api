variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Ambiente de despliegue"
  type        = string
}

variable "public_key_path" {
  description = "Ruta al archivo de llave pública (.pub)"
  type        = string
}
