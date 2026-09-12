import importlib
import json

import boto3
import pytest
from moto import mock_aws


@pytest.fixture()
def handler_module(monkeypatch):
    monkeypatch.setenv("TABLE_NAME", "tasks-test")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")

    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName="tasks-test",
            KeySchema=[{"AttributeName": "task_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "task_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        import handler

        yield importlib.reload(handler)


def test_create_and_get_task(handler_module):
    create_event = {
        "routeKey": "POST /tasks",
        "body": json.dumps({"title": "Learn Terraform", "status": "todo"}),
    }

    create_response = handler_module.lambda_handler(create_event, None)
    assert create_response["statusCode"] == 201

    task = json.loads(create_response["body"])
    get_response = handler_module.lambda_handler(
        {
            "routeKey": "GET /tasks/{task_id}",
            "pathParameters": {"task_id": task["task_id"]},
        },
        None,
    )

    assert get_response["statusCode"] == 200
    assert json.loads(get_response["body"])["title"] == "Learn Terraform"


def test_missing_title_returns_400(handler_module):
    result = handler_module.lambda_handler(
        {"routeKey": "POST /tasks", "body": json.dumps({"status": "todo"})},
        None,
    )

    assert result["statusCode"] == 400
