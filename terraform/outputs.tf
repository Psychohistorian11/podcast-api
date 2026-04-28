output "ec2_public_ip" {
  description = "IP pública del servidor EC2"
  value       = module.ec2.public_ip
}

output "ec2_public_dns" {
  description = "DNS público del servidor EC2"
  value       = module.ec2.public_dns
}

output "rds_endpoint" {
  description = "Endpoint de conexión a la base de datos"
  value       = module.rds.endpoint
}

output "rds_port" {
  description = "Puerto de la base de datos"
  value       = module.rds.port
}

output "ssh_command" {
  description = "Comando para conectarse al EC2 por SSH"
  value       = "ssh -i ~/.ssh/podcast-api-key.pem ubuntu@${module.ec2.public_ip}"
}

output "app_url" {
  description = "URL de la aplicación"
  value       = "http://${module.ec2.public_ip}:8000/docs"
}
