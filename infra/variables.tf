variable "aws_region" {
  description = "AWS region where the application will be deployed."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used for AWS resource names."
  type        = string
  default     = "serverless-task-api"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}
