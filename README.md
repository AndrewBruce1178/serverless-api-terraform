# Serverless Task API

REST API for task management built with Python, AWS Lambda, API Gateway, DynamoDB, Terraform, and GitHub Actions.

## Architecture

```text
Client
  -> API Gateway HTTP API
  -> AWS Lambda Python handler
  -> DynamoDB tasks table
```

Terraform provisions the AWS infrastructure. Terraform remote state is stored in S3 and locked with DynamoDB.

## API

```text
POST   /tasks
GET    /tasks
GET    /tasks/{task_id}
PUT    /tasks/{task_id}
DELETE /tasks/{task_id}
```

Example task:

```json
{
  "task_id": "uuid",
  "title": "Learn Terraform",
  "description": "Build AWS serverless API",
  "status": "todo",
  "created_at": "2026-09-12T10:00:00+00:00",
  "updated_at": "2026-09-12T10:00:00+00:00"
}
```

## Local tests

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
PYTHONPATH=. pytest
```

On Windows PowerShell:

```powershell
cd app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
$env:PYTHONPATH="."
pytest
```

## Bootstrap Terraform state backend

The main Terraform configuration uses an S3 backend. Create the backend resources once:

```bash
cd infra/bootstrap
terraform init
terraform apply \
  -var="state_bucket_name=your-globally-unique-state-bucket" \
  -var="lock_table_name=serverless-task-api-terraform-locks"
```

For this repository:

```powershell
terraform apply `
  -var="state_bucket_name=andrewbruce1178-serverless-api-terraform-state" `
  -var="lock_table_name=serverless-task-api-terraform-locks"
```

The bootstrap stack also creates a GitHub Actions OIDC role. Copy the `github_actions_role_arn` output and store it as the `AWS_ROLE_TO_ASSUME` GitHub Actions secret.

Then copy the backend example:

```bash
cd ..
cp backend/dev.hcl.example backend/dev.hcl
```

On Windows PowerShell:

```powershell
cd ..
Copy-Item backend/dev.hcl.example backend/dev.hcl
```

Edit `infra/backend/dev.hcl` with the S3 bucket and DynamoDB lock table names from the bootstrap output.

## Deploy

```bash
cd infra
terraform init -backend-config=backend/dev.hcl
terraform plan
terraform apply
```

After apply, Terraform prints `api_url`.

## GitHub Actions

The workflow runs:

- on pull requests: `terraform fmt`, `terraform init`, `terraform validate`, `terraform plan`
- on push to `main`: the same checks plus `terraform apply`

The workflow expects this GitHub secret:
The workflow expects these GitHub secrets:

```text
AWS_ROLE_TO_ASSUME
TF_STATE_BUCKET
TF_LOCK_TABLE
```

Use GitHub OIDC with an AWS IAM role that can manage the resources in this project and access the Terraform state bucket and lock table.

For this repository:

```text
TF_STATE_BUCKET=andrewbruce1178-serverless-api-terraform-state
TF_LOCK_TABLE=serverless-task-api-terraform-locks
```
