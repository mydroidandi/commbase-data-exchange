import requests
import json

# Define the API endpoint
api_url = 'http://127.0.0.1:5000/api/save_json'

# Sample JSON payload
sample_json_data = {
    "name": "John Doe",
    "age": 30,
    "city": "Example City"
}

try:
    # Send a POST request to the API endpoint with JSON payload
    response = requests.post(api_url, json=sample_json_data)

    # Check the response status
    if response.status_code == 200:
        print("JSON data saved successfully.")
        print("Response:", response.json())
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.json())

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
