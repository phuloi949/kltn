import requests

# Example JWT token
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjY2ZDk0Y2NhNjY2NTYxZThlZGY3MzAxIn0.KCzs2hl0MGow_qRo0TYnMnTIbwxvHPxcmbYymvNBfS8"

# Define your Flask server URL
url = "http://localhost:5000/hello"

# Set the Authorization header with the JWT token
headers = {
    'Authorization': jwt_token
}

# Send GET request to the protected endpoint
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Response:", response.json())
elif response.status_code == 401:
    print("Authentication failed:", response.json()['message'])
else:
    print("Failed to fetch data. Status code:", response.status_code)
    print(response.text)