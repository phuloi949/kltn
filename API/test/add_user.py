import requests
import json

# Dictionary with the data
data = {
    "username": "kient4",
    "password": "pasdf84bsgdfq34"
}

# URL of the endpoint
# url = "http://localhost:5000/add_user"
url = "http://localhost:5000/login"

# Make the POST request with the dictionary as JSON payload
# response = requests.post(url, json=data)
response = requests.post(url, json=data)
# print(data)

# Print the response from the server
print(response.text)