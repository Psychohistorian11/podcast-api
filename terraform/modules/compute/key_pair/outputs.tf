output "key_name" {
  description = "Nombre del Key Pair en AWS"
  value       = aws_key_pair.main.key_name
}
