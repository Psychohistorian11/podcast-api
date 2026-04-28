//El Key Pair es la llave SSH que permite conectarte al EC2 de forma segura. 
//Terraform la registra en AWS usando tu llave pública.

resource "aws_key_pair" "main" {
  key_name   = "${var.project_name}-${var.environment}-key"
  public_key = file(var.public_key_path)

  tags = {
    Name        = "${var.project_name}-${var.environment}-key"
    Project     = var.project_name
    Environment = var.environment
  }
}
