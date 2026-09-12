output "api_url" {
  description = "Base URL of the deployed HTTP API."
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}

output "tasks_table_name" {
  description = "DynamoDB table used by the API."
  value       = aws_dynamodb_table.tasks.name
}
