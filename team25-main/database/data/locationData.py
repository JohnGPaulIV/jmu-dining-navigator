import requests
import json
import pprint

from images import download_image

# ========= CONFIG =========
CAMPUS_URL_KEY = "campus"
LOCATION_URL_KEY = "d-hall"
# ==========================


payment_types = {
    "Meal Plan Swipes": "swipe",
    "Meal Punches": "swipe",
    "Dining Dollars Gold": "dining_dollars_gold",
    "mealSwipes": "swipe",
    "Dining Plan Swipes": "swipe",
    "Credit/Debit": "card",
    "GOLD": "dining_dollars_gold",
    "Flex": "flex",
    "Panera gift cards": "panera_gift_card",
    "Debit Card": "card",
    "Dining Dollars": "dining_dollars",
    "FLEX": "flex",
    "Cash": "cash",
    "creditCard": "card",
    "diningDollars": "dining_dollars",
    "Duke Deals": "duke_deal",
}

# Base GraphQL endpoint
url = "https://api.elevate-dxp.com/api/mesh/c087f756-cc72-4649-a36f-3a41b700c519/graphql"

# GraphQL query for location data
query = """
query getLocation($campus_url_key: String!, $location_url_key: String!) {
  getLocation(
    campusUrlKey: $campus_url_key
    locationUrlKey: $location_url_key
  ) {
    commerceAttributes {
      uid
      url_key
      address_line_1
      address_line_2
      city_locality
      state_province
      postal_code
      timezone
      display_menu_type
      display_in_menu_highlights
      display_favorite_recipes
      display_meal_calculator
      display_nutrition_information
      display_nml_oml
      display_minimized_recipes
      display_ingredients
      stations
      longitude
      latitude
      menu_preferences
      maxMenusDate
      is_display_price_on_the_menu
      is_display_price_zero
      is_display_product_images_on_the_menu
      hasActiveMenus
      children {
        id
        name
        description
        image
        position
        meal_period_overrides {
          meal_period_id
          name
          description
          __typename
        }
        __typename
      }
      allergens_intolerances
      menu_preferences
      meal_periods {
        id
        name
        position
        __typename
      }
      __typename
    }
    aemAttributes {
      name
      featuredLocation
      teaserAssetRef {
        ... on AEM_ImageRef {
          _dynamicUrl
          width
          height
          __typename
        }
        __typename
      }
      mainAssetRef {
        ... on AEM_ImageRef {
          _dynamicUrl
          width
          height
          __typename
        }
        __typename
      }
      logoAssetRef {
        ... on AEM_ImageRef {
          _dynamicUrl
          width
          height
          __typename
        }
        __typename
      }
      globalPaymentMethods
      globalMobileOrderingMethods
      additionalMobileOrderingMethods
      additionalPaymentMethods
      mobileOrderingLink
      additionalInfo {
        html
        __typename
      }
      goodToKnow {
        name
        description {
          html
          __typename
        }
        _path
        __typename
      }
      wayfindingInstructions
      voc
      contacts {
        firstName
        lastName
        email
        jobTitle
        phone
        __typename
      }
      description {
        html
        plaintext
        __typename
      }
      announcement {
        html
        __typename
      }
      hoursOfOperation {
        _path
        schedule
        __typename
      }
      _path
      __typename
    }
    __typename
  }
}
"""

# Standard headers needed to mimic browser + auth context
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

# Load base locations list
with open("database/pgsql/locations.json", "r", encoding="utf-8") as f:
    location_full_data = json.load(f)
    locations = [loc for loc in location_full_data.keys()]

location_data = dict()

# Iterate over each location and pull full metadata
for loc in locations:
    location_data.setdefault(loc, {})

    variables = {
        "campus_url_key": CAMPUS_URL_KEY,
        "location_url_key": loc,
    }

    params = {
        "query": query,
        "operationName": "getLocation",
        "variables": json.dumps(variables),
    }

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    base_data = data["data"]["getLocation"]["aemAttributes"]
    base_children_data = data["data"]["getLocation"]["commerceAttributes"]["children"]
    has_children = len(base_children_data) > 0

    contacts = base_data["contacts"]

    # Initialize per-location structure
    location_data[loc].setdefault("managers", {})
    location_data[loc].setdefault("payment", set())
    location_data[loc].setdefault("description", "")
    location_data[loc].setdefault("image_from", "")
    location_data[loc].setdefault("image_write", "")
    location_data[loc].setdefault("image_id", "")
    location_data[loc].setdefault("image_name", "")
    location_data[loc].setdefault("stations", {})
    location_data[loc].setdefault("periods_active", [])
    location_data[loc].setdefault("directions", "")

    location_data[loc]["directions"] = base_data["wayfindingInstructions"]
    base_image_url_write = "webapp/static/images/future"

    periods_at = data["data"]["getLocation"]["commerceAttributes"]["meal_periods"]
    location_data[loc].setdefault("stations", {})

    # Station display names
    if has_children:
        for child in base_children_data:
            location_data[loc]["stations"][child["id"]] = child["name"]

    # Track which meal periods are active
    for p in periods_at:
        location_data[loc]["periods_active"].append(p["id"])

    # Manager contact info
    for idx, contact in enumerate(contacts):
        f_name = contact["firstName"]
        l_name = contact["lastName"]
        email = contact["email"]
        phone = contact["phone"]

        location_data[loc]["managers"][idx] = {
            "first_name": f_name,
            "last_name": l_name,
            "email": email,
            "phone": phone,
        }

    # Plain text description from AEM
    location_data[loc]["description"] = base_data["description"]["plaintext"]

    # Payment methods: merge global + additional and map into internal enum
    globalPayment = base_data["globalPaymentMethods"]
    additionalPayment = base_data["additionalPaymentMethods"]

    for payment in (globalPayment + additionalPayment):
        if payment not in payment_types:
            print(loc)
            raise KeyError(f"{payment}")
        location_data[loc]["payment"].add(payment_types[payment])

    # Convert payment set to list for JSON
    location_data[loc]["payment"] = list(location_data[loc]["payment"])

    # Image handling
    location_data[loc]["image_from"] = base_data["mainAssetRef"]["_dynamicUrl"].split("dm-aid--")[1]
    location_data[loc]["image_write"] = base_image_url_write + data["data"]["getLocation"]["commerceAttributes"]["url_key"] + ".jpg"
    location_data[loc]["image_id"] = location_data[loc]["image_from"].split("/")[0]
    location_data[loc]["image_name"] = location_data[loc]["image_from"].split("/")[1]

    # Download and save the image
    download_image(
        location_data[loc]["image_id"],
        location_data[loc]["image_name"],
        location_data[loc]["image_write"],
        True,
    )

# Pretty-print to console
pprint.pprint(location_data)

# Save full location data to JSON
with open("database/pgsql/location_data.json", "w", encoding="utf-8") as f:
    json.dump(location_data, f, ensure_ascii=False, indent=2)

print("Saved JSON to location_d_hall.json")
