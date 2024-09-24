from django.shortcuts import render
from django.http import HttpResponse
import json
def all_users(request):
    data={
            "event": "user_list",
            "users": [
                {
                    "id": "USR123",
                    "name": "Shubham",
                    "age": 20,
                    "projects": ["project1", "project2", "project3"]
                },
                {
                    "id": "USR333",
                    "name": "John",
                    "age": 32,
                    "projects": ["project3"]
                }
            ],
            "message_id": "abc123",
            "correlation_id": "txn456",
            "status": "pending",
            "error_details": None,
            "retry_count": 0,
            "created_at": "2024-09-24T12:34:56Z",
            "processed_at": None,
            "service_name": "user_service",
            "payload_version": "1.0"
        }

    return HttpResponse(json.dumps(data),content_type="application/json")