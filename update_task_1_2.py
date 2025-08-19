#!/usr/bin/env python3.11
"""
Update Task 1.2 to doing status
"""

import requests

# Task 1.2 ID
TASK_ID = "5cbace57-271d-425e-b373-24527f55642e"

# Update data
update_data = {
    "status": "doing",
    "description": "Currently implementing main App component with routing and basic navigation layout for The Hero Foundry application."
}

# Update the task
response = requests.put(
    f"http://localhost:8181/api/tasks/{TASK_ID}",
    json=update_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    print("✅ Task 1.2 updated to 'doing' status")
    print("🚀 Starting: Create Basic Application Structure")
else:
    print(f"❌ Failed to update task: {response.status_code}")
    print(response.text)
