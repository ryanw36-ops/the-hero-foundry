#!/usr/bin/env python3.11
"""
Update Task 1.5 to doing status
"""

import requests

# Task 1.5 ID
TASK_ID = "0eb28309-e10a-4d0d-b4dc-95cfc5874e73"

# Update data
update_data = {
    "status": "doing",
    "description": "Currently implementing ruleset scanning system that loads /rulesets/*/ruleset.json at startup with validation and caching."
}

# Update the task
response = requests.put(
    f"http://localhost:8181/api/tasks/{TASK_ID}",
    json=update_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    print("✅ Task 1.5 updated to 'doing' status")
    print("🚀 Starting: Create Modular Ruleset Framework")
else:
    print(f"❌ Failed to update task: {response.status_code}")
    print(response.text)
