import requests
import json

# Test the inference server
url = "http://localhost:5000/predict"
test_data = {
    "amount": 10000,
    "department": "IT", 
    "category": "Unusual"
}

response = requests.post(url, json=test_data)
print(f"Response: {response.json()}")