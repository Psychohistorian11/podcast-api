//La instancia RDS es la base de datos PostgreSQL administrada por AWS. Terraform la crea con todos los parámetros necesarios.

# Subnet group — le dice a RDS en qué subnets puede vivir
data "aws_subnets" "default" {
  filter {
    name   = "default-for-az"
    values = ["true"]
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name        = "${var.project_name}-${var.environment}-subnet-group"
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-${var.environment}-db"

  # Motor de base de datos
  engine         = "postgres"
  engine_version = "15"
  instance_class = var.instance_class

  # Configuración de la DB
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  # Almacenamiento
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"

  # Red
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.security_group_id]
  publicly_accessible    = true # necesario para conectarse via SSH

  # Backups
  backup_retention_period = 0
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  # Al hacer terraform destroy, elimina la DB sin snapshot final
  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    Name        = "${var.project_name}-${var.environment}-db"
    Project     = var.project_name
    Environment = var.environment
  }
}
