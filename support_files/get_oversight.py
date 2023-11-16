import requests

def get_oversight(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

# Replace with your actual FastAPI endpoint URL
api_endpoint = "http://localhost:8010/scrape"
data = get_oversight(api_endpoint)

if data is not None:
    print(data)
