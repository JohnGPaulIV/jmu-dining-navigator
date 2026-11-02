import requests
import json
import pprint

# ========== API ENDPOINT ==========
url = "https://api.elevate-dxp.com/api/mesh/c087f756-cc72-4649-a36f-3a41b700c519/graphql"

# ========== GRAPHQL QUERY (decoded from your URL) ==========
# Fetches store config including allergens and menu preferences
query = """
{
  Commerce_storeConfig {
    client_code
    website_code
    marketing_email_communication {
      automatic_enrollment_at_checkout
      __typename
    }
    converge_is_demo
    website_name
    customer_default_group_id
    store_group_code
    low_balance_alert_enabled
    weekly_balance_summary_enabled
    aramark_catalog_time_format
    store_code
    store_name
    aramark_consumer_sso
    aramark_sso_active
    default_country
    locale
    base_currency_code
    braintree_paypal_active
    default_display_currency_code
    timezone
    secure_base_url
    secure_base_media_url
    aramark_customer_groups
    aramark_long_acquisition_form_show_class_year_field_for_roles
    aramark_long_acquisition_form_show_residence_field_for_roles
    aramark_number_id_is_required
    aramark_number_id_is_show
    countries_with_required_state
    is_student_id_active
    is_pms_enabled
    marketing_communication {
      fyf_enabled
      joining_rewards_enabled
      checkout_enrollment_enabled
      account_create_enabled
      account_update_enabled
      account_update_method
      __typename
    }
    is_guest_checkout_enabled
    is_enable_refer_friend
    is_enable_send_a_family_link
    is_allow_fulfillment_instructions_on_order_enabled
    is_allow_gift_message_on_order_enabled
    allergens_intolerances {
      is_active
      label
      sort_order
      value
      __typename
    }
    allergens_is_display
    menu_preferences {
      description
      icon
      title
      value
      is_active
      label
      sort_order
      __typename
    }
    eat_to_excel_icons {
      icon
      label
      value
      __typename
    }
    preferences_is_display
    location_category_filter_enabled
    location_category
    accepted_credit_cards {
      name
      __typename
    }
    active_payment_methods
    default_country
    is_enable_sort_locations_by_distance
    measurement_system
    line_of_business {
      value
      title
      __typename
    }
    default_delivery_hours_of_operations {
      closed_temporarily_from
      closed_temporarily_to
      display_date_time
      standard_hours {
        day_of_week
        from
        is_closed_all_day
        to
        __typename
      }
      time_increment
      __typename
    }
    is_delivery_service_charge_enabled
    is_pickup_service_charge_enabled
    recaptcha_v3_config {
      forms
      is_enabled
      language_code
      website_key
      __typename
    }
    __typename
  }
}
"""

# Empty variables
variables = {}

# ========== HEADERS ==========
# Mimic browser + required auth / store headers
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

# ========== SEND REQUEST ==========
# Use GET with query + variables in params
params = {
    "query": query,
    "variables": json.dumps(variables)
}

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()  # Raise if HTTP error

data = response.json()

# ========== EXTRACT ALLERGENS + MENU PREFERENCES ==========
allergens = dict()

print(data["data"]["Commerce_storeConfig"]["allergens_intolerances"])
allergen_list = data["data"]["Commerce_storeConfig"]["allergens_intolerances"]

# Initialize top-level structure
allergens.setdefault("allergens", {})
allergens.setdefault("menuPreferences", {})

# Build allergens section
for allergen in allergen_list:
    al_val = allergen["value"]
    allergens["allergens"].setdefault(al_val, {})

    allergens["allergens"][al_val]["label"] = allergen["label"]
    description = ""

    # Manually map value -> human description
    match al_val:
        case "39":
            description = "Contains eggs or egg based product(s)"
        case "42":
            description = "Contains fish or fish based product(s)"
        case "45":
            description = "Contains milk or milk based product(s)"
        case "48":
            description = "Contains peanuts or peanut based product(s)"
        case "51":
            description = "Contains sesame or sesame based product(s)"
        case "54":
            description = "Contains shellfish or shellfish based product(s)"
        case "57":
            description = "Contains soy or soy based product(s)"
        case "60":
            description = "Contains tree nuts or tree nut based product(s)"
        case "63":
            description = "Contains wheat or wheat based product(s)"

    allergens["allergens"][al_val]["description"] = description

# Build menuPreferences section
preferences = data["data"]["Commerce_storeConfig"]["menu_preferences"]
for preference in preferences:
    allergens["menuPreferences"].setdefault(preference["value"], {})
    allergens["menuPreferences"][preference["value"]]["description"] = preference["description"]
    allergens["menuPreferences"][preference["value"]]["label"] = preference["label"]
    allergens["menuPreferences"][preference["value"]]["title"] = preference["title"]

# Pretty-print the final structure
pprint.pprint(allergens)

# ========== WRITE TO FILE ==========
with open("allergens.json", "w", encoding="utf-8") as f:
    json.dump(allergens, f, ensure_ascii=False, indent=2)

print("Saved store_config.json")
