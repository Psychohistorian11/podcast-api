output "security_group_id" {
  description = "ID del Security Group del EC2"
  value       = aws_security_group.ec2.id
}

output "security_group_name" {
  description = "Nombre del Security Group del EC2"
  value       = aws_security_group.ec2.name
}
