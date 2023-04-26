import requests
import json

# Enter your API key here


# Specify the endpoint and parameters for the NewsAPI request
endpoint = 'https://bhagavadgitaapi.in/slok'
params = {
    'q': 'dogecoin',
    'from': '2023-03-30'
#     'to': '2023-03-31',
#     'sortBy': 'relevancy',
#     'apiKey': api_key
}

# Send the request and get the response
response = requests.get(endpoint)

# Convert the response to JSON format
data = json.loads(response.text)
print(data)
