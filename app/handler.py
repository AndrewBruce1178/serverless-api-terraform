import json
import os
import uuid
from datetime import datetime, timezone

import boto3


TABLE_NAME = os.environ["TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    route_key = event.get("routeKey", "")
    path_parameters = event.get("pathParameters") or {}

    try:
        if route_key == "POST /tasks":
            return create_task(event)
        if route_key == "GET /tasks":
            return list_tasks()
        if route_key == "GET /tasks/{task_id}":
            return get_task(path_parameters["task_id"])
        if route_key == "PUT /tasks/{task_id}":
            return update_task(path_parameters["task_id"], event)
        if route_key == "DELETE /tasks/{task_id}":
            return delete_task(path_parameters["task_id"])

        return response(404, {"message": "Route not found"})
    except KeyError as exc:
        return response(400, {"message": f"Missing required field: {exc.args[0]}"})
    except json.JSONDecodeError:
        return response(400, {"message": "Request body must be valid JSON"})


def create_task(event):
    body = parse_body(event)
    now = utc_now()
    task = {
        "task_id": str(uuid.uuid4()),
        "title": body["title"],
        "description": body.get("description", ""),
        "status": body.get("status", "todo"),
        "created_at": now,
        "updated_at": now,
    }

    table.put_item(Item=task)
    return response(201, task)


def list_tasks():
    result = table.scan()
    return response(200, {"items": result.get("Items", [])})


def get_task(task_id):
    result = table.get_item(Key={"task_id": task_id})
    item = result.get("Item")
    if not item:
        return response(404, {"message": "Task not found"})

    return response(200, item)


def update_task(task_id, event):
    body = parse_body(event)
    result = table.get_item(Key={"task_id": task_id})
    current = result.get("Item")
    if not current:
        return response(404, {"message": "Task not found"})

    updated = {
        **current,
        "title": body.get("title", current["title"]),
        "description": body.get("description", current.get("description", "")),
        "status": body.get("status", current.get("status", "todo")),
        "updated_at": utc_now(),
    }

    table.put_item(Item=updated)
    return response(200, updated)


def delete_task(task_id):
    table.delete_item(Key={"task_id": task_id})
    return response(204, None)


def parse_body(event):
    body = event.get("body") or "{}"
    return json.loads(body)


def response(status_code, body):
    payload = "" if body is None else json.dumps(body)
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": payload,
    }


def utc_now():
    return datetime.now(timezone.utc).isoformat()
