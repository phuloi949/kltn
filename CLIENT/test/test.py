import requests

# Example JWT token
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjY2ZWQxYjNkNDExZGZiNDg4ZjRiMDU4In0.fBS0qteWZj_mKVyPT6ubPWv_pynVpJG9Azgk0WTw63o"

# Define your Flask server URL
url = "http://192.168.0.43:5000/zip_file"

# Set the Authorization header with the JWT token
headers = {
    'Authorization': jwt_token
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    
    # Check if the response content type is ZIP
    if response.headers['content-type'] == 'application/zip':
        # Define the filename to save the ZIP file
        filename = 'CLIENT/test/flower-homomorphic_encryption.zip'
        
        # Save the content to a file
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"ZIP file saved as: {filename}")
    else:
        print("Response content is not a ZIP file.")
    
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")