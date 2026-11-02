import requests
import json
from datetime import date
from dateutil.relativedelta import relativedelta

# ====== CONFIGURE THESE ======
CAMPUS_URL_KEY = "campus"
LOCATION_URL_KEY = "bistro-1908"
DATE = "2025-11-01"
MEAL_PERIOD = 16
VIEW_TYPE = "MONTHLY"
# =============================

# Debug helpers / config
i_check = []
attributes = [
    "allergen_statement",
    "allergens_intolerances",
    "calcium",
    "calories",
    "calories_from_fat",
    "cholesterol",
    "configurable_option_attributes",
    "dietary_fiber",
    "includes_added_sugars",
    "iron",
    "marketing_description",
    "marketing_name",
    "protein",
    "recipe_attributes",
    "recipe_ingredients",
    "saturated_fat",
    "sodium",
    "sugars",
    "total_carbohydrates",
    "total_fat",
    "trans_fat",
    "vitamin_a",
    "vitamin_c",
]

months = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]

# ========== GRAPHQL SETUP ==========
url = "https://api.elevate-dxp.com/api/mesh/c087f756-cc72-4649-a36f-3a41b700c519/graphql"
no_menu = []

# Decoded GraphQL query for location recipes
query = """
query getLocationRecipes(
  $campusUrlKey: String!
  $locationUrlKey: String!
  $date: String!
  $mealPeriod: Int
  $viewType: Commerce_MenuViewType!
) {
  getLocationRecipes(
    campusUrlKey: $campusUrlKey
    locationUrlKey: $locationUrlKey
    date: $date
    mealPeriod: $mealPeriod
    viewType: $viewType
  ) {
    locationRecipesMap {
      skus
      stationSkuMap {
        id
        skus
        __typename
      }
      dateSkuMap {
        date
        stations {
          id
          skus {
            simple
            configurable {
              sku
              variants
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    products {
      items {
        product {
          attribute_set_id
          sku
          add_to_cart_allowed
          canonical_url
          created_at
          custom_attributes {
            code
            value
            __typename
          }
          description {
            html
            __typename
          }
          gift_message_available
          uid
          meta_description
          meta_keyword
          meta_title
          name
          new_from_date
          new_to_date
          price_range {
            maximum_price {
              discount {
                amount_off
                percent_off
                __typename
              }
              final_price {
                currency
                value
                __typename
              }
              fixed_product_taxes {
                amount {
                  currency
                  value
                  __typename
                }
                label
                __typename
              }
              regular_price {
                currency
                value
                __typename
              }
              __typename
            }
            minimum_price {
              discount {
                amount_off
                percent_off
                __typename
              }
              final_price {
                currency
                value
                __typename
              }
              fixed_product_taxes {
                amount {
                  currency
                  value
                  __typename
                }
                label
                __typename
              }
              regular_price {
                currency
                value
                __typename
              }
              __typename
            }
            __typename
          }
          short_description {
            html
            __typename
          }
          small_image {
            disabled
            label
            position
            url
            __typename
          }
          thumbnail {
            disabled
            label
            position
            url
            __typename
          }
          updated_at
          __typename
        }
        productView {
          sku
          images {
            label
            roles
            url
            __typename
          }
          attributes {
            name
            value
            __typename
          }
          ... on Search_ComplexProductView {
            attributes {
              name
              value
              __typename
            }
            options {
              title
              values {
                id
                title
                ... on Search_ProductViewOptionValueProduct {
                  product {
                    name
                    sku
                    attributes {
                      name
                      value
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      page_info {
        current_page
        page_size
        total_pages
        __typename
      }
      total_count
      __typename
    }
    __typename
  }
}
"""

# ========== LOAD PREVIOUSLY-SAVED SUPPORTING DATA ==========
with open("locations.json", "r") as f:
    locs = [l for l in json.load(f).keys()]

with open("location_data.json", "r") as f:
    periods = json.load(f)

# ========== REQUEST HEADERS ==========
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

# ========== MAIN SCRAPE / BUILD STRUCTURE ==========
today = date.today()
menu = dict()
not_processed = []

for l in locs:
    d = date(today.year, today.month, 1)
    not_none = True
    menu.setdefault(l, {})

    if l == "d-hall":
        print(f"periods:  {periods[l]["periods_active"]}")

    if periods[l]["periods_active"] == []:
        not_processed.append(l)
        continue

    while not_none:
        
        check = 0

        for p in periods[l]["periods_active"]:
            # Build GraphQL variables per location / date / period
            variables = {
                "campusUrlKey": CAMPUS_URL_KEY,
                "locationUrlKey": l,           #
                "date": d.strftime("%Y-%m-%d"),  #
                "mealPeriod": p,               #
                "viewType": VIEW_TYPE,
            }

            params = {
                "query": query,
                "operationName": "getLocationRecipes",
                "variables": json.dumps(variables),
            }

            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()

            data = resp.json()

            first_base_check = data["data"]
            if (first_base_check is None):
                not_none = False
                continue

            check_base = data["data"]["getLocationRecipes"]

            if check_base["locationRecipesMap"] is None or check_base["locationRecipesMap"] is {} or check_base["locationRecipesMap"] is [] or check_base["products"] is None or check_base["products"] is {} or check_base["products"] is []:
                
                not_none = False
                continue

            base_menu_items = data["data"]["getLocationRecipes"]["products"]["items"]

            curr_month = months[d.month - 1]
            menu[l].setdefault(d.year, {})
            menu[l][d.year].setdefault(curr_month, {})
            menu[l][d.year][curr_month].setdefault(p, {})
            
            items = []
           
            for item in base_menu_items:
                
                menu[l][d.year][curr_month][p].setdefault("items", {})
                curr_item = item["product"]["sku"]

                if curr_item in menu[l][d.year][curr_month][p]["items"]:
                    continue

                menu[l][d.year][curr_month][p]["items"].setdefault(curr_item, {})
                menu[l][d.year][curr_month][p]["items"][curr_item]["name"] = item["product"]["name"]

                item_info = item["productView"]["attributes"]
                curr_item_dict = menu[l][d.year][curr_month][p]["items"][curr_item]
                attrs = item["productView"]["attributes"]

                for attr in attrs:
                    if attr["name"] in attributes:
                        
                        curr_item_dict[attr["name"]] = attr["value"]

            base_menu = data["data"]["getLocationRecipes"]["locationRecipesMap"]["dateSkuMap"]

            if len(base_menu) > 0:
                for day in base_menu:
                    curr_day = day["date"]
                    curr_day_parts = [int(x) for x in curr_day.split("-")]

                    if d.year == curr_day_parts[0] or d.month == curr_day_parts[1]:
                        menu[l][d.year][curr_month][p].setdefault(curr_day, {})
                        menu[l][d.year][curr_month][p][curr_day].setdefault("stations", {})
                        stations = day["stations"]

                        for s in stations:
                            food_items = []
                            menu[l][d.year][curr_month][p][curr_day]["stations"].setdefault(s["id"], {})

                            for config in s["skus"]["configurable"]:
                                food_items.append(config["sku"])

                            for simple in s["skus"]["simple"]:
                                food_items.append(simple)

                            menu[l][d.year][curr_month][p][curr_day]["stations"][s["id"]]["offers"] = food_items

        if not_none is False:
            break

        d = d + relativedelta(months=1)


# Debug output + write to file
print(len(i_check))
print(not_processed)

with open("menu.json", "w") as f:
    json.dump(menu, f, indent=2)
    