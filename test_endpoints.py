#!/usr/bin/env python3.11

import requests

# Archon API configuration
ARCHON_API_BASE = "http://localhost:8181/api"
PROJECT_ID = "e8c8b8eb-78f9-4b08-84bd-57a73bda5705"
TASK_ID = "393118bc-941d-4861-92ef-d8e1c1afb3b3"

def test_endpoints():
    print("🔍 Testing different endpoint patterns...")
    
    endpoints = [
        f"/projects/{PROJECT_ID}/tasks/{TASK_ID}",
        f"/tasks/{TASK_ID}",
        f"/projects/{PROJECT_ID}/tasks/{TASK_ID}/update",
        f"/task/{TASK_ID}",
    ]
    
    for endpoint in endpoints:
        url = f"{ARCHON_API_BASE}{endpoint}"
        print(f"\n🌐 Testing GET: {url}")
        
        try:
            response = requests.get(url)
            print(f"📊 Status: {response.status_code}")
            if response.status_code != 404:
                print(f"📄 Response: {response.text[:200]}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_update_methods():
    print("\n🔄 Testing different update methods...")
    
    update_data = {"status": "review"}
    base_url = f"{ARCHON_API_BASE}/projects/{PROJECT_ID}/tasks/{TASK_ID}"
    
    methods = ["PUT", "PATCH", "POST"]
    
    for method in methods:
        print(f"\n🌐 Testing {method}: {base_url}")
        
        try:
            if method == "PUT":
                response = requests.put(base_url, json=update_data)
            elif method == "PATCH":
                response = requests.patch(base_url, json=update_data)
            elif method == "POST":
                response = requests.post(base_url, json=update_data)
                
            print(f"📊 Status: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_endpoints()
    test_update_methods()
