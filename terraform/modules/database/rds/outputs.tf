output "endpoint" {
  description = "Endpoint de conexión a RDS (sin puerto)"
  value       = aws_db_instance.main.address
}

output "port" {
  description = "Puerto de RDS"
  value       = aws_db_instance.main.port
}

output "db_name" {
  description = "Nombre de la base de datos"
  value       = aws_db_instance.main.db_name
}
