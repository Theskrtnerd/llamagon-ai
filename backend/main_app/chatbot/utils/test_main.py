import os
import requests

# Define the API URL
api_url = "http://127.0.0.1:8004/chat-with-context/"

# Define the test data
context = "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France."
question = "What is the Eiffel Tower?"

# Prepare the data to send in the POST request
data = {
    "context": context,
    "question": question
}

# Send the POST request
response = requests.post(api_url, json=data)

# Print the status code and response content
print(f"Status Code: {response.status_code}")
print("Response Content:")
print(response.json())
