//Es el puente entre Terraform y AWS. Le dice a Terraform qué nube va a usar, en qué región, y cómo autenticarse.
//Sin el provider, Terraform no sabe con quién hablar.

terraform {
  required_version = ">= 1.0" //versión de terraform, sencillito

  required_providers { //Declaración de plugins, en este caso el de AWS, se descargan con el init
    aws = {
      source  = "hashicorp/aws" //plugin oficial de aws
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
