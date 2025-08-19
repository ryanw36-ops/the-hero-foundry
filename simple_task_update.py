#!/usr/bin/env python3.11

import requests

# Archon API configuration
ARCHON_API_BASE = "http://localhost:8181/api"
PROJECT_ID = "e8c8b8eb-78f9-4b08-84bd-57a73bda5705"
TASK_ID = "393118bc-941d-4861-92ef-d8e1c1afb3b3"

def main():
    print("🔄 Updating Task 1.6 to review status...")
    
    update_data = {
        "status": "review",
        "description": "Task 1.6: Implement File-Based Storage System - COMPLETED\n\nImplementation includes:\n1. File storage service with save/load/delete operations\n2. React hook for state management\n3. Settings page with backup/restore functionality\n4. Characters page with full CRUD operations\n5. Comprehensive logging and error handling\n\nThe file-based storage system is fully functional and ready for review."
    }
    
    url = f"{ARCHON_API_BASE}/projects/{PROJECT_ID}/tasks/{TASK_ID}"
    
    print(f"🌐 Making request to: {url}")
    
    try:
        response = requests.put(url, json=update_data)
        print(f"📊 Response status: {response.status_code}")
        print(f"📄 Response text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Task 1.6 successfully updated to 'review' status!")
        else:
            print(f"❌ Failed to update task: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error making request: {e}")

if __name__ == "__main__":
    main()
