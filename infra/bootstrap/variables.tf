variable "aws_region" {
  description = "AWS region for the Terraform backend resources."
  type        = string
  default     = "eu-central-1"
}

variable "state_bucket_name" {
  description = "Globally unique S3 bucket name for Terraform state."
  type        = string
}

variable "lock_table_name" {
  description = "DynamoDB table name for Terraform state locking."
  type        = string
  default     = "serverless-task-api-terraform-locks"
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the deployment role, in owner/name format."
  type        = string
  default     = "AndrewBruce1178/serverless-api-terraform"
}

variable "github_branch" {
  description = "GitHub branch allowed to apply infrastructure changes."
  type        = string
  default     = "main"
}

variable "github_actions_role_name" {
  description = "IAM role name used by GitHub Actions through OIDC."
  type        = string
  default     = "github-actions-serverless-api-terraform"
}
