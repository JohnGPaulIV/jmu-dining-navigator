import requests
import json
import pprint

# Elevate GraphQL endpoint
url = "https://api.elevate-dxp.com/api/mesh/c087f756-cc72-4649-a36f-3a41b700c519/graphql"

# Simple GraphQL query: fetch all meal periods
query = """
{ Commerce_mealPeriods { id name position __typename } }
"""

# No variables needed
variables = {}

# Request headers (browser-like + API keys)
headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://jmu.mydininghub.com",
    "referer": "https://jmu.mydininghub.com/",
    "user-agent": "Mozilla/5.0",
    "x-api-key": "ElevateAPIProd",
    "magento-store-code": "ch_jmu",
    "magento-store-view-code": "ch_jmu_en",
    "magento-website-code": "ch_jmu",
    "store": "ch_jmu_en",
}

# Final request payload
params = {
    "query": query,
    "variables": json.dumps(variables)
}

# Execute request
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

data = response.json()

# Build simple dict: { meal_name: id }
meal_info = {}
period_data = data["data"]["Commerce_mealPeriods"]

for period in period_data:
    meal_info[period["name"]] = period["id"]

# Save to file
with open("periods.json", "w") as f:
    json.dump(meal_info, f, indent=2)

# Print nicely
pprint.pprint(meal_info)
