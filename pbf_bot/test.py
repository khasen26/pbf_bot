import requests
import json

# Define the API endpoint
url = "https://api.pbf.kz/api"

# Make a GET request to the API
response = requests.get(url)

# Check the response status code
assert response.status_code == 200

# Parse the JSON data
data = json.loads(response.text)

# Check if the data contains the expected series of numbers
assert data == [1, 2, 3, 4, 5]

print("API test passed successfully!")