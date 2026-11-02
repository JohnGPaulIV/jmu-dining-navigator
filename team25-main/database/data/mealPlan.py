import requests
import json
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import re

# ====== CONFIGURE THESE ======
CAMPUS_URL_KEY = "campus"
LOCATION_URL_KEY = "bistro-1908"
DATE = "2025-11-01"
MEAL_PERIOD = 16
VIEW_TYPE = "MONTHLY"
# =============================

word_replacements = {}


def clean_html(html: str) -> str:
    """Strip HTML to plain text and normalize whitespace."""
    text = BeautifulSoup(html, "html.parser").get_text(" ")

    # Replace non-breaking spaces
    text = text.replace("\u00a0", " ")

    # Collapse multiple spaces/newlines into one space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_wording(text: str) -> str:
    """
    Post-process wording:
    - Special handling around 'spring'
    - Apply word_replacements mapping
    """
    finished = text
    txt_list = text.split(" ")

    if len(txt_list) > 1:
        finished = ""
        for word in range(len(txt_list)):
            if txt_list[word].lower() == "spring":
                prev = word if word == 0 else word - 1
                next = word + 1 if word + 1 < len(txt_list) else word
                same = prev == word or next == word
                if not same:
                    if txt_list[prev].lower() == "the":
                        if len(txt_list[next]) >= 8 and not txt_list[next][0:8].lower() == "semester":
                            print(f"{txt_list[next][0:8]}")
                            finished += "semester"
                            if len(txt_list[next]) > 8:
                                finished += txt_list[next][8:len(txt_list[next])]
                    if txt_list[next] == "2026":
                        txt_list[next] = " "
                    if txt_list[prev].lower() == "during":
                        finished += "the semester"
                continue

            if txt_list[word] in word_replacements.keys():
                finished += word_replacements[txt_list[word]]
                continue

            if not txt_list[word] == " ":
                finished += txt_list[word]
                if word != len(txt_list) - 1:
                    finished += " "

    return finished


url = "https://api.elevate-dxp.com/api/mesh/c087f756-cc72-4649-a36f-3a41b700c519/graphql"
no_menu = []

# ====== GRAPHQL QUERY (Search Meal Plans) ======
query = """
query SearchProductsQuery(
  $filter: [Search_SearchClauseInput!]
  $sort: [Search_ProductSearchSortInput!]
) {
  Search_productSearch(
    filter: $filter
    sort: $sort
    phrase: ""
    current_page: 1
    page_size: 500
  ) {
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
}
"""

# ====== REQUEST HEADERS ======
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

# ====== FILTERS FOR MEAL PLANS ======
variables = {
    "filter": [
        {
            "attribute": "categoryPath",
            "in": [
                "collegiatehospitalityus-jamesmadisonuniversity/campus/mealplanproductgroup/on-campus-residents",
                "collegiatehospitalityus-jamesmadisonuniversity/campus/mealplanproductgroup/off-campus-residents",
                "collegiatehospitalityus-jamesmadisonuniversity/campus/mealplanproductgroup/jmu-grace-street-apartment-residents",
                "collegiatehospitalityus-jamesmadisonuniversity/campus/mealplanproductgroup/full-time-faculty-staff-and-affiliates"
            ]
        },
        {
            "attribute": "visibility",
            "in": ["Catalog", "Catalog, Search"]
        },
        {
            "attribute": "aramark_visible",
            "in": ["1"]
        }
    ],
    "sort": []
}

# Final request params
params = {
    "query": query,
    "operationName": "SearchProductsQuery",
    "variables": json.dumps(variables),
}

# ====== EXECUTE REQUEST ======
resp = requests.get(url, headers=headers, params=params)
resp.raise_for_status()
data = resp.json()

meal_plans = {}

# Mapping of internal attribute names to our keys
needed_attributes = {
    "names": {
        "db_amount_included": "dining_dollars",
        "good_to_know": "additional_info",
        "meal_plan_type": "type",
        "meals_cycle": "total_punches"
    },
    "attributes": [],
    "records": {
        "3": "duke_deals_per_day",
        "4": "guest_punches",
        "2": "extra_info"
    }
}

start_plans = data["data"]["Search_productSearch"]["items"]

# ====== EXTRACT PLAN DATA ======
for plan in start_plans:
    sku = plan["product"]["sku"]

    meal_plans.setdefault(sku, {})
    meal_plans[sku]["description"] = clean_wording(
        clean_html(plan["product"]["short_description"]["html"])
    )
    meal_plans[sku]["price"] = plan["product"]["price_range"]["maximum_price"]["regular_price"]["value"]

    attributes = plan["productView"]["attributes"]
    meal_plans[sku]["name"] = plan["product"]["name"]

    atts = []

    for attribute in attributes:
        if attribute["name"] == "product_descriptions":
            v = attribute["value"]
            v_d = json.loads(v)
            for record in v_d:
                if record["record_id"] in list(needed_attributes["records"].keys()):
                    primary = record["primary"]
                    primary = "0" if not primary.strip() else primary
                    primary = primary.split()[0] if record["record_id"] == "3" and len(primary) > 0 else primary
                    primary = clean_wording(clean_html(primary))
                    atts.append((needed_attributes["records"][record["record_id"]], primary))
            continue

        if attribute["name"] in needed_attributes["names"]:
            atts.append(
                (
                    needed_attributes["names"][attribute["name"]],
                    clean_wording(clean_html(attribute["value"]))
                )
            )

    # Attach parsed attributes to this meal plan
    for att in atts:
        meal_plans[sku][att[0]] = att[1]

# ====== WRITE OUTPUT FILE ======
with open("meal_plans.json", "w") as f:
    json.dump(meal_plans, f, indent=2)
