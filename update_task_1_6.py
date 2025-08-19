#!/usr/bin/env python3.11
"""
Update Task 1.6 to doing status
"""

import requests

# Task 1.6 ID
TASK_ID = "393118bc-941d-4861-92ef-d8e1c1afb3b3"

# Update data
update_data = {
    "status": "doing",
    "description": "Currently implementing file system operations for local storage in user documents folder with character data persistence and backup capabilities."
}

# Update the task
response = requests.put(
    f"http://localhost:8181/api/tasks/{TASK_ID}",
    json=update_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    print("✅ Task 1.6 updated to 'doing' status")
    print("🚀 Starting: Implement File-Based Storage System")
else:
    print(f"❌ Failed to update task: {response.status_code}")
    print(response.text)
