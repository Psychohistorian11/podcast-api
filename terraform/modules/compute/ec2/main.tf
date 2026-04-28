//La instancia EC2 es el servidor virtual donde corre la app. Terraform la crea con Ubuntu, la conecta al Security Group correcto y ejecuta un script de instalación automática.

# Buscar la AMI más reciente de Ubuntu 24.04
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [var.security_group_id]

  # Script que se ejecuta automáticamente al crear la instancia
  # Instala Docker, Git, clona el repo y levanta la app
  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get upgrade -y

    # Instalar Docker
    apt-get install -y ca-certificates curl gnupg git
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    usermod -aG docker ubuntu

    cd /home/ubuntu
    git clone https://github.com/Psychohistorian11/podcast-api.git
    cd podcast-api

    cat > .env << 'ENVFILE'
    APP_NAME=podcast-api
    APP_VERSION=3.0.0
    ENVIRONMENT=production
    DATABASE_URL=postgresql://${var.db_username}:${var.db_password}@${var.db_endpoint}:5432/${var.db_name}
    SIMON_API_URL=${var.simon_api_url}
    JOSE_PABLO_API_URL=${var.jose_pablo_api_url}
    ENVFILE

    chown ubuntu:ubuntu .env
    sudo -u ubuntu docker compose up --build -d
  EOF

  tags = {
    Name        = "${var.project_name}-${var.environment}-ec2"
    Project     = var.project_name
    Environment = var.environment
  }
}
