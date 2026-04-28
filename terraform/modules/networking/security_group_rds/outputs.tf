output "security_group_id" {
  description = "ID del Security Group del RDS"
  value       = aws_security_group.rds.id
}

output "security_group_name" {
  description = "Nombre del Security Group del RDS"
  value       = aws_security_group.rds.name
}
