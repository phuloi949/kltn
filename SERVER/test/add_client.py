import requests
import json

# Dictionary with the data
data = {
    "client_id": "client1",
    "client_ip": "192.168.168.22",
    "client_status": "online",
    "model": "CNN"
}
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjY2ZDk0Y2NhNjY2NTYxZThlZGY3MzAxIn0.KCzs2hl0MGow_qRo0TYnMnTIbwxvHPxcmbYymvNBfS8"
headers = {
    'Authorization': jwt_token
}

# URL of the endpoint
# url = "http://localhost:5000/add_user"
url = "http://localhost:5000/add_client"

# Make the POST request with the dictionary as JSON payload
# response = requests.post(url, json=data)
response = requests.post(url, json=data, headers=headers)
# print(data)

# Print the response from the server
print(response.text)