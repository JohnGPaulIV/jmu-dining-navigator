import pprint
import requests
import json


def remove_empty(d):
    """Recursively remove empty dictionaries."""
    if not isinstance(d, dict):
        return d

    cleaned = {}
    for key, value in d.items():
        if isinstance(value, dict):
            cleaned_value = remove_empty(value)
            # keep only non-empty dicts
            if cleaned_value:
                cleaned[key] = cleaned_value
        else:
            cleaned[key] = value

    return cleaned


# All possible meal periods we care about
meal_periods = [
    'Morning Snack',
    'Snack',
    'Break',
    'Breakfast',
    'Brunch',
    'Lunch',
    'Afternoon Snack',
    'ASSP (After School Snack Program)',
    'Limited Dinner',
    'Dinner',
    'Evening Snack',
    'Overnight',
    'All Day'
]

# Map short day codes -> full day names
DAYS = {
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "Sa": "Saturday",
    "Su": "Sunday"
}

# Elevate GraphQL endpoint
url = "https://api.elevate-dxp.com/api/mesh/c087f756-cc72-4649-a36f-3a41b700c519/graphql"

# GraphQL query (decoded from URL)
query = """
query getLocations(
  $campus_url_key: String!
  $location_category: [String]
  $limit: Int
  $isFeatured: Boolean
) {
  getLocations(
    campusUrlKey: $campus_url_key
    locationCategory: $location_category
    limit: $limit
    isFeatured: $isFeatured
    sort: "featuredPriority DESC, name"
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
      longitude
      latitude
      location_category_ids
      __typename
    }
    aemAttributes {
      name
      wayfindingInstructions
      featuredLocation
      featuredPriority
      teaserAssetRef {
        ... on AEM_ImageRef {
          _dynamicUrl
          width
          height
          __typename
        }
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

# Only parameter we need here
variables = {
    "campus_url_key": "campus"
}

# Headers to mimic browser + auth context
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

# Request payload
params = {
    "query": query,
    "operationName": "getLocations",
    "variables": json.dumps(variables)
}

# Call API
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

print(response.json())
print(response.status_code)

location_data = response.json()["data"]["getLocations"]

# Final structure: slug -> hours/schedule + basic address info
hours = {}

for loc_base in location_data:
    aem = loc_base.get("aemAttributes") or {}
    commerce = loc_base.get("commerceAttributes") or {}

    slug = commerce.get("url_key")
    if not slug:
        # Skip locations with no URL slug
        continue

    hours_of_op = aem.get("hoursOfOperation")
    if not hours_of_op:
        continue

    schedules = hours_of_op.get("schedule") or []
    if not isinstance(schedules, list):
        continue

    # Initialize entry for this location slug
    hours.setdefault(slug, {})
    hours[slug].setdefault("schedule", {})

    # Basic address/location fields
    hours[slug]["address"] = commerce.get("address_line_1")
    hours[slug]["city_locality"] = commerce.get("city_locality")
    hours[slug]["latitude"] = commerce.get("latitude")
    hours[slug]["longitude"] = commerce.get("longitude")
    hours[slug]["postal_code"] = commerce.get("postal_code")
    hours[slug]["state_province"] = commerce.get("state_province")

    # Parse each schedule block
    for sched in schedules:
        curr_name = sched.get("name") or "Default"

        # Dict for this schedule under this slug
        hours[slug]["schedule"].setdefault(curr_name, {})
        curr_hours = hours[slug]["schedule"][curr_name]

        meal_period_list = sched.get("meal_periods") or []
        for curr_period in meal_period_list:
            period_name = curr_period.get("meal_period")
            if not period_name:
                continue

            # Optionally filter to known meal periods
            if period_name not in meal_periods:
                # Currently just keep everything
                pass

            full_hours = curr_period.get("opening_hours") or ""
            if full_hours.strip() == "":
                continue

            # Dict for this meal period
            curr_hours.setdefault(period_name, {})
            curr_period_type = curr_hours[period_name]

            # Example string: "Mo-Fr 07:00-19:00; Sa 08:00-14:00"
            for hrs_str in full_hours.split(";"):
                hrs_str = hrs_str.strip()
                if not hrs_str:
                    continue

                parts = hrs_str.split()
                if len(parts) < 2:
                    continue

                days_part, time_part = parts[0], parts[1]
                days_split = days_part.split("-")

                time_parts = time_part.split("-")
                if len(time_parts) != 2:
                    continue

                open_time, close_time = time_parts[0], time_parts[1]

                start_code = days_split[0]
                end_code = days_split[-1]

                found = False
                for day_abb, day_full in DAYS.items():
                    if day_abb == start_code:
                        found = True
                    if not found:
                        continue

                    curr_day = curr_period_type.setdefault(day_full, {})
                    curr_day["open"] = open_time
                    curr_day["close"] = close_time

                    if day_abb == end_code:
                        break

# Strip out any empty dicts from the structure
hours = remove_empty(hours)

# Write to locations.json
with open("locations.json", 'w') as f:
    json.dump(hours, f, indent=2)

# pprint.pprint(hours)
