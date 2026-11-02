"""
Data generator for dining management system.

- Loads JSON source data
- Synthesizes locations, menus, users, logs, etc.
- Inserts everything into Postgres.
"""

import datetime
import pprint
import requests
import json
from datetime import date, timedelta
from faker import Faker
import random
import re
from enum import Enum

import psycopg
from psycopg.errors import UniqueViolation


# -------------------------------------------------------------------
# Simple incrementing integer helper (for indexing imported files)
# -------------------------------------------------------------------
class IncInt:
    def __init__(self, value=0):
        self.value = value

    def post_inc(self):
        old = self.value
        self.value += 1
        return old

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


# -------------------------------------------------------------------
# Enums and enum → string maps
# -------------------------------------------------------------------
class PaymentMethod(Enum):
    CARD = "card"
    CASH = "cash"
    DINING_DOLLARS = "dining dollars"
    FLEX = "flex"
    SWIPE = "swipe"
    DUKE_DEAL = "duke deal"
    DINING_DOLLARS_GOLD = "dining dollars gold"
    PANERA_GIFT_CARD = "panera gift card"


class MealType(Enum):
    MORNING_SNACK = "Morning Snack"
    SNACK = "Snack"
    BREAK = "Break"
    BREAKFAST = "Breakfast"
    BRUNCH = "Brunch"
    LUNCH = "Lunch"
    AFTERNOON_SNACK = "Afternoon Snack"
    ASSP = "ASSP (After School Snack Program)"
    LIMITED_DINNER = "Limited Dinner"
    DINNER = "Dinner"
    EVENING_SNACK = "Evening Snack"
    OVERNIGHT = "Overnight"
    ALL_DAY = "All Day"


# Map human-readable meal labels to enum values
meal_type_enum_map = {
    "Morning Snack": MealType.MORNING_SNACK.value,
    "Snack": MealType.SNACK.value,
    "Break": MealType.BREAK.value,
    "Breakfast": MealType.BREAKFAST.value,
    "Brunch": MealType.BRUNCH.value,
    "Lunch": MealType.LUNCH.value,
    "Afternoon Snack": MealType.AFTERNOON_SNACK.value,
    "ASSP (After School Snack Program)": MealType.ASSP.value,
    "Limited Dinner": MealType.LIMITED_DINNER.value,
    "Dinner": MealType.DINNER.value,
    "Evening Snack": MealType.EVENING_SNACK.value,
    "Overnight": MealType.OVERNIGHT.value,
    "All Day": MealType.ALL_DAY.value,
}

# Map JSON payment tags → PaymentMethod enum values
payment_enum_map = {
    "swipe": PaymentMethod.SWIPE.value,
    "dining_dollars_gold": PaymentMethod.DINING_DOLLARS_GOLD.value,
    "card": PaymentMethod.CARD.value,
    "flex": PaymentMethod.FLEX.value,
    "panera_gift_card": PaymentMethod.PANERA_GIFT_CARD.value,
    "dining_dollars": PaymentMethod.DINING_DOLLARS.value,
    "cash": PaymentMethod.CASH.value,
    "duke_deal": PaymentMethod.DUKE_DEAL.value,
}

# -------------------------------------------------------------------
# Special schedules: map specific dates to a named schedule
# -------------------------------------------------------------------
special_schedules = {
    # March 16–20, 2026
    date(2026, 3, 16): "Fall Break 2025",
    date(2026, 3, 17): "Fall Break 2025",
    date(2026, 3, 18): "Fall Break 2025",
    date(2026, 3, 19): "Fall Break 2025",
    date(2026, 3, 20): "Fall Break 2025",

    # October 22–26, 2026
    date(2026, 10, 22): "Fall Break 2025",
    date(2026, 10, 23): "Fall Break 2025",
    date(2026, 10, 24): "Fall Break 2025",
    date(2026, 10, 25): "Fall Break 2025",
    date(2026, 10, 26): "Fall Break 2025",

    # December 30, 2025 – January 18, 2026
    date(2025, 12, 30): "Fall Break 2025",
    date(2025, 12, 31): "Fall Break 2025",
    date(2026, 1, 1): "Fall Break 2025",
    date(2026, 1, 2): "Fall Break 2025",
    date(2026, 1, 3): "Fall Break 2025",
    date(2026, 1, 4): "Fall Break 2025",
    date(2026, 1, 5): "Fall Break 2025",
    date(2026, 1, 6): "Fall Break 2025",
    date(2026, 1, 7): "Fall Break 2025",
    date(2026, 1, 8): "Fall Break 2025",
    date(2026, 1, 9): "Fall Break 2025",
    date(2026, 1, 10): "Fall Break 2025",
    date(2026, 1, 11): "Fall Break 2025",
    date(2026, 1, 12): "Fall Break 2025",
    date(2026, 1, 13): "Fall Break 2025",
    date(2026, 1, 14): "Fall Break 2025",
    date(2026, 1, 15): "Fall Break 2025",
    date(2026, 1, 16): "Fall Break 2025",
    date(2026, 1, 17): "Fall Break 2025",
    date(2026, 1, 18): "Fall Break 2025",
}

# -------------------------------------------------------------------
# DB connection + global setup
# -------------------------------------------------------------------
con = psycopg.connect(host="localhost", port="5432", user="team25", dbname="team25")
cur = con.cursor()

BASE_PATH = "GP/team25/database/data/locations"
fake = Faker()
random.seed(0)

imp_idx = IncInt(0)
EXTRA_RESTRICTIONS = ["Gluten Free", "Vegetarian", "Vegan"]


def n() -> int:
    """Return next incremental index (for imported_files)."""
    return imp_idx.post_inc()


# Map logical file labels to positions in imp_dicts
imported_files = {
    "locations": n(),
    "location_data": n(),
    "menu": n(),
    "allergens": n(),
    "periods": n(),
    "meal_plans": n(),
}

# Load all JSON files into imp_dicts list
imp_dicts = []
for f in imported_files.keys():
    with open(f + ".json", "r") as fi:
        imp_dicts.append(json.load(fi))

# Map location name → numeric location id
loc_ids = {}
loc_id = IncInt(0)
for l in imp_dicts[imported_files["location_data"]].keys():
    loc_ids[l] = loc_id.post_inc()


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def gen_phone():
    """Generate a fake phone number."""
    return f"({fake.random_number(digits=3, fix_len=True)}) {fake.bothify('###')}-{fake.bothify('####')}"


def gen_name():
    """Generate a fake full name."""
    return f"{fake.first_name()} {fake.last_name()}"


# -------------------------------------------------------------------
# location_managers
# -------------------------------------------------------------------
def create_managers(loc_ids: dict):
    """Create location manager rows from location_data.json."""
    managers = []
    man_id = 0

    for l in imp_dicts[imported_files["location_data"]].keys():
        curr_loc_id = loc_ids[l]
        for m in imp_dicts[imported_files["location_data"]][l]["managers"].keys():
            man = imp_dicts[imported_files["location_data"]][l]["managers"][m]
            managers.append(
                (man_id, curr_loc_id, man["first_name"], man["last_name"], man["email"], man["phone"])
            )
            man_id += 1

    return managers


# -------------------------------------------------------------------
# dietary_restriction
# -------------------------------------------------------------------
def create_dietary_restrictions():
    """Create dietary restriction rows from allergens.json."""
    restrictions = []
    idx = 0

    for d in imp_dicts[imported_files["allergens"]]["allergens"].keys():
        restrictions.append(
            (
                idx,
                imp_dicts[imported_files["allergens"]]["allergens"][d]["label"],
                imp_dicts[imported_files["allergens"]]["allergens"][d]["description"],
            )
        )
        idx += 1

    for d in imp_dicts[imported_files["allergens"]]["menuPreferences"].keys():
        if imp_dicts[imported_files["allergens"]]["menuPreferences"][d]["label"] in EXTRA_RESTRICTIONS:
            restrictions.append(
                (
                    idx,
                    imp_dicts[imported_files["allergens"]]["menuPreferences"][d]["label"],
                    imp_dicts[imported_files["allergens"]]["menuPreferences"][d]["description"],
                )
            )
            idx += 1

    return restrictions


# -------------------------------------------------------------------
# meal_plan
# -------------------------------------------------------------------
def create_meal_plans():
    """Create meal plan rows from meal_plans.json."""
    meal_plans = []

    for idx, m in enumerate(imp_dicts[imported_files["meal_plans"]].keys()):
        num_punches = imp_dicts[imported_files["meal_plans"]][m]["total_punches"].strip()
        if num_punches == "":
            num_punches = 0
        else:
            num_punches = int(num_punches)

        meal_plans.append((idx, num_punches, imp_dicts[imported_files["meal_plans"]][m]["name"]))

    return meal_plans


# -------------------------------------------------------------------
# user
# -------------------------------------------------------------------
def create_users(num_fake: int, dietary_restrictions: list):
    """
    Create the fixed Flask/FAB users + additional fake users 
    that include dietary restrictions.
    """

    # --- FIXED REAL USERS (matching your FAB users) ---
    users = [
        # user_id, name, email, phone, dietary_restrictions, dining_balance
        (1, "admin user", "admin@fab.org", gen_phone(), [], round(random.uniform(0, 200), 2)),
        (3, "Joe DiRocco", "joedirocco@gmail.com", gen_phone(), [], round(random.uniform(0, 200), 2)),
        (4, "John Paul", "johnpaul@gmail.com", gen_phone(), [], round(random.uniform(0, 200), 2)),
        (5, "John Henry", "johnhenry@gmail.com", gen_phone(), [], round(random.uniform(0, 200), 2)),
        (6, "Harry Williams", "harrywilliams@gmail.com", gen_phone(), [], round(random.uniform(0, 200), 2)),
        (7, "Lucas Fisher", "lucasfisher@gmail.com", gen_phone(), [], round(random.uniform(0, 200), 2)),
    ]

    # --- STARTING ID FOR GENERATED USERS ---
    next_id = 8

    # --- ADD RANDOM USERS WITH DIETARY RESTRICTIONS ---
    for i in range(num_fake):
        # Pick random dietary restrictions
        d_r = []
        r = random.randint(0, max(0, len(dietary_restrictions) - 3))
        diet = dietary_restrictions.copy()

        for _ in range(r):
            choice = random.choice(diet)
            d_r.append(choice[0])      # store the restriction ID or label
            diet.remove(choice)

        users.append(
            (
                next_id,
                gen_name(),
                fake.email(),
                gen_phone(),
                d_r,
                round(random.uniform(0, 200), 2)
            )
        )
        next_id += 1

    return users


# -------------------------------------------------------------------
# ingredient helpers
# -------------------------------------------------------------------
def dedupe_keep_order(items, nested, lookup=0):
    """Deduplicate list while preserving order."""
    seen = set()
    out = []
    idx = 0

    for x in items:
        if nested:
            product, description, r, l, itemm = x
            key = product.lower().strip()

            if key not in seen:
                seen.add(key)
                out.append((idx, key, description, r, l, itemm))
                idx += 1
        else:
            key = x.lower().strip()
            if key and key not in seen:
                seen.add(key)
                out.append((idx, key))
                idx += 1

    return out


def extract_all_ingredients(text: str):
    """
    Flatten everything: top-level + sub-ingredients from inside parentheses.
    Heuristic but works well for typical ingredient labels.
    """
    t = text

    # Normalize separators
    t = t.replace(";", ",")
    # Turn parentheses into commas so sub-ingredients are split out too
    t = t.replace("(", ",").replace(")", ",")

    # Remove leading phrases like "contains less than 2% of", "may contain one or more of the following:"
    t = re.sub(r"contains\s+less\s+than[^,]*,", ",", t, flags=re.IGNORECASE)
    t = re.sub(r"may\s+contain[^:]*:", "", t, flags=re.IGNORECASE)

    # Split on commas
    raw_parts = [p.strip() for p in t.split(",")]

    ingredients = []
    for p in raw_parts:
        p_clean = p.strip()
        if not p_clean:
            continue

        lower = p_clean.lower()

        # Drop pure connectors
        if lower in {"or", "and"}:
            continue

        # Drop some obvious descriptor fragments
        if lower.startswith("added to "):
            continue
        if lower.startswith("for "):
            continue

        ingredients.append(p_clean)

    return ingredients  # dedupe_keep_order(ingredients)


def create_ingredients():
    """Create master ingredient list + mapping sku → ingredient names."""
    x = []
    z = 0
    menu_items = {}

    for l in imp_dicts[imported_files["menu"]].keys():
        l_dict = imp_dicts[imported_files["menu"]][l]
        for y in l_dict.keys():
            y_dict = l_dict[y]
        for m in y_dict.keys():
            m_dict = y_dict[m]
            for p in m_dict.keys():
                curr_items = m_dict[p]["items"]
                for item in curr_items.keys():
                    curr_item = curr_items[item]
                    if "recipe_ingredients" not in curr_item:
                        menu_items[item] = "no ingredients listed"
                        continue

                    new_addition = extract_all_ingredients(curr_item["recipe_ingredients"])
                    new_addition = [x.lower().strip() for x in new_addition]
                    x.extend(new_addition)
                    menu_items[item] = new_addition

    y = (dedupe_keep_order(x, False), menu_items)
    return y


# -------------------------------------------------------------------
# menu_item
# -------------------------------------------------------------------
def create_menu_item():
    """Create menu items and helper maps for locations and dukedeals."""
    m_items = []
    m_items_all_locations = {}
    m_items_all_no_de = {}

    for l in imp_dicts[imported_files["menu"]].keys():
        l_dict = imp_dicts[imported_files["menu"]][l]
        m_items_all_no_de.setdefault(l, [])
        for y in l_dict.keys():
            y_dict = l_dict[y]
            for m in y_dict.keys():
                m_dict = y_dict[m]
                for p in m_dict.keys():
                    curr_items = m_dict[p]["items"]
                    for idx, item in enumerate(curr_items.keys()):
                        curr_item = curr_items[item]
                        i = curr_item.get("marketing_name", "").lower().strip()
                        d = curr_item.get(
                            "marketing_description", "no description for this product"
                        ).lower().strip()
                        r = curr_item.get("allergens_intolerances", [""])
                        if i:
                            if r == "0":
                                r = [""]
                            m_items.append((i, d, r, l, item))
                            if i in m_items_all_locations:
                                m_items_all_locations[i].append(l)
                            else:
                                m_items_all_locations[i] = [l]
                                continue

    m_items = dedupe_keep_order(m_items, True)
    m_items_all_no_de.setdefault("idx", [])

    for idx, i in enumerate(m_items):
        m_items_all_no_de[i[4]].append(idx)
        if "d-hall" in m_items_all_locations[i[1]] or "e-hall" in m_items_all_locations[i[1]]:
            m_items[idx] += (False,)
        else:
            m_items_all_no_de["idx"].append(idx)
            t = random.random()
            if t > 0.78:
                m_items[idx] += (True,)
            else:
                m_items[idx] += (False,)

    return (m_items, m_items_all_locations, m_items_all_no_de)


# -------------------------------------------------------------------
# location
# -------------------------------------------------------------------
def create_locations():
    """Create location rows + capacity dict."""
    loc_data = {}
    locs = []
    cap_dict = {}

    for l in imp_dicts[imported_files["locations"]].keys():
        loc_data.setdefault(l, {})
        loc_data[l]["address"] = imp_dicts[imported_files["locations"]][l]["address"]

    ld = imp_dicts[imported_files["location_data"]]
    for l in ld.keys():
        loc_data[l]["description"] = ld[l]["description"]
        loc_data[l]["directions"] = ld[l]["directions"]

    for idx, l in enumerate(loc_data.keys()):
        cap = random.randint(250, 1000)
        mod = cap % 10
        cap = cap - mod

        direction = loc_data[l]["directions"]
        address = loc_data[l]["address"]

        if address is None or address.strip() == "":
            address = "No address provided"
        if direction is None or direction.strip() == "":
            direction = "No directions provided"

        locs.append((idx, l, address, direction, loc_data[l]["description"], cap))
        cap_dict[idx] = cap

    return (locs, cap_dict)


# -------------------------------------------------------------------
# location_hours
# -------------------------------------------------------------------
def create_location_hours(num_days):
    """Generate location_hours rows and per-schedule open/close windows."""
    location_hours = []
    hours = {}

    WEEKDAY_NAMES = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    days_ahead = num_days
    start_date = date.today()

    for loc_id, l in enumerate(imp_dicts[imported_files["locations"]].keys()):
        loc_dict = imp_dicts[imported_files["locations"]][l]

        if "schedule" not in loc_dict:
            continue

        schedule = loc_dict["schedule"]
        hours.setdefault(loc_id, {})  # Initialize dictionary for this location

        for offset in range(days_ahead):
            current_day = start_date + timedelta(days=offset)
            weekday_name = WEEKDAY_NAMES[current_day.weekday()]

            # Choose between special schedule and Standard
            schedule_name = special_schedules.get(current_day, "Standard")

            if schedule_name not in schedule:
                continue

            schedule_period = schedule[schedule_name]

            opens = []
            closes = []

            # Loop through meal periods (Breakfast, Lunch, Dinner, etc.)
            for meal_type in schedule_period.keys():
                meal_days = schedule_period[meal_type]

                if weekday_name in meal_days:
                    info = meal_days[weekday_name]
                    opens.append(info["open"])
                    closes.append(info["close"])

            # Closed -- skip this day
            if not opens:
                continue

            open_time = min(opens)
            close_time = max(closes)

            # Format day string
            day_str = current_day.strftime("%Y-%m-%d")

            # Append location_hours entry
            location_hours.append((loc_id, day_str, open_time, close_time))

            # Store per-schedule earliest open + latest close
            if schedule_name not in hours[loc_id]:
                hours[loc_id][schedule_name] = {
                    "open": open_time,
                    "close": close_time,
                }
            else:
                hours[loc_id][schedule_name]["open"] = min(
                    hours[loc_id][schedule_name]["open"], open_time
                )
                hours[loc_id][schedule_name]["close"] = max(
                    hours[loc_id][schedule_name]["close"], close_time
                )

    return (location_hours, hours)


# -------------------------------------------------------------------
# schedule
# -------------------------------------------------------------------
def create_schedule():
    """Generate per-meal schedule rows for each location and date."""
    schedule_rows = []
    WEEKDAY_NAMES = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    days_ahead = 365
    start_date = date.today()

    for loc_id, l in enumerate(imp_dicts[imported_files["locations"]].keys()):
        loc_dict = imp_dicts[imported_files["locations"]][l]

        if "schedule" not in loc_dict:
            continue

        schedule = loc_dict["schedule"]

        for offset in range(days_ahead):
            current_day = start_date + timedelta(days=offset)
            weekday_name = WEEKDAY_NAMES[current_day.weekday()]
            day_str = current_day.strftime("%Y-%m-%d")

            # Pick schedule: special or Standard
            schedule_name = special_schedules.get(current_day, "Standard")
            if schedule_name not in schedule:
                continue

            schedule_period = schedule[schedule_name]

            # For each meal type (Breakfast, Lunch, Dinner, etc.) on this weekday
            for meal_type_name, meal_days in schedule_period.items():
                if weekday_name not in meal_days:
                    continue

                info = meal_days[weekday_name]
                beg_time = info["open"]   # "HH:MM"
                end_time = info["close"]  # "HH:MM"

                meal_type_value = meal_type_name

                if schedule_name == "Standard":
                    notes = "Operating on standard hours"
                else:
                    notes = f"Operating on {schedule_name.lower()} hours"

                schedule_rows.append(
                    (loc_id, day_str, meal_type_value, beg_time, end_time, notes)
                )

    return schedule_rows


# -------------------------------------------------------------------
# web_log
# -------------------------------------------------------------------
def create_web_log(caps: dict, hours: dict):
    """Generate time-series capacity data for each location."""
    web_rows = []

    # Time range: from 2025-11-01 to "now"
    start_ts = datetime.datetime(2025, 11, 1, 0, 0)
    td = datetime.datetime.today()
    end_ts = datetime.datetime(td.year, td.month, td.day, td.hour, td.minute)  # exclusive
    step = datetime.timedelta(minutes=15)

    for loc_id, l in enumerate(imp_dicts[imported_files["locations"]].keys()):
        # Need both a cap and hours for this location
        if loc_id not in caps or loc_id not in hours:
            continue

        max_cap = caps[loc_id]

        ts = start_ts
        last_cap = 0
        was_open = False  # whether we were in an open window on previous tick

        while ts < end_ts:
            current_day = ts.date()

            # Which schedule applies on this day?
            schedule_name = special_schedules.get(current_day, "Standard")

            # If we don't have hours for this schedule at this location, treat as closed
            if schedule_name not in hours[loc_id]:
                curr_cap = 0
                was_open = False
                last_cap = 0
                timestamp_str = ts.strftime("%Y-%m-%d %H:%M:%S")
                web_rows.append((loc_id, timestamp_str, curr_cap))
                ts += step
                continue

            open_str = hours[loc_id][schedule_name]["open"]   # "HH:MM"
            close_str = hours[loc_id][schedule_name]["close"]  # "HH:MM"

            # Parse open/close times to minutes since midnight
            open_h, open_m = map(int, open_str.split(":"))
            close_h, close_m = map(int, close_str.split(":"))

            open_min = open_h * 60 + open_m
            close_min = close_h * 60 + close_m
            close_tail_min = close_min + 30  # 30 minutes after close

            # Current time of day in minutes
            t = ts.time()
            t_min = t.hour * 60 + t.minute

            in_open_window = open_min <= t_min <= close_tail_min

            if not in_open_window:
                # Closed: capacity is zero
                curr_cap = 0
                last_cap = 0
                was_open = False
            else:
                if not was_open:
                    # Just opened: trickle-in, low initial occupancy
                    upper = max(1, int(max_cap * 0.25))
                    curr_cap = random.randint(0, upper)
                else:
                    # Normal operation while open
                    low = max(0, last_cap - 5)
                    high = min(max_cap, last_cap + 45)

                    # In the last 60 minutes before close_tail,
                    # gradually ramp down (factor from 1 → 0).
                    mins_to_close_tail = close_tail_min - t_min
                    if 0 <= mins_to_close_tail <= 60:
                        factor = mins_to_close_tail / 60.0  # 1 at -60, 0 at 0
                        low = int(low * factor)
                        high = int(high * factor)

                    if high < low:
                        high = low

                    curr_cap = random.randint(low, high)

                last_cap = curr_cap
                was_open = True

            timestamp_str = ts.strftime("%Y-%m-%d %H:%M:%S")
            web_rows.append((loc_id, timestamp_str, curr_cap))

            ts += step

    return web_rows


# -------------------------------------------------------------------
# menu
# -------------------------------------------------------------------
def create_menu(menu_items, menu_index_map):
    """Generate menu rows linking locations, items, dates, and meal types."""
    rows = []

    # --- 1. Build mapping from location_name -> location_id ---
    loc_name_to_id = {
        loc_name: loc_id
        for loc_id, loc_name in enumerate(imp_dicts[imported_files["locations"]].keys())
    }

    # --- 2. Build mapping from (location_name, sku) -> menu_item_id and global sku -> menu_item_id ---
    sku_by_loc = {}
    sku_global = {}

    for item in menu_items:
        menu_item_id, name, desc, allergens, item_loc_name, sku, is_duke_deal = item

        if item_loc_name is not None:
            sku_by_loc[(item_loc_name, sku)] = menu_item_id

        if sku not in sku_global:
            sku_global[sku] = menu_item_id

    # --- 3. Build period_id -> meal_type_name map from imp_dicts[periods] ---
    periods = imp_dicts[imported_files["periods"]]
    period_id_to_meal_type = {str(v): k for k, v in periods.items()}

    menu_data = imp_dicts[imported_files["menu"]]

    # Track locations that actually got at least one REAL row
    locations_with_real_rows = set()

    # Fallback pool
    global_fallback_indices = menu_index_map.get("idx", [])

    # --- 4. Use structured menu data (per date/period/sku) ---
    for loc_name, loc_menu in menu_data.items():
        if loc_name not in loc_name_to_id:
            continue

        loc_id = loc_name_to_id[loc_name]

        # Walk year -> month -> period_id -> date_str -> stations
        for year_str, year_dict in loc_menu.items():
            for month_str, month_dict in year_dict.items():
                for period_id_str, dates_dict in month_dict.items():
                    meal_type_name = period_id_to_meal_type.get(period_id_str, "All Day")

                    for date_str, date_info in dates_dict.items():
                        stations = date_info.get("stations", {})
                        used_skus = set()

                        for station_name, station_data in stations.items():
                            offers = station_data.get("offers", [])

                            for sku in offers:
                                if sku in used_skus:
                                    continue
                                used_skus.add(sku)

                                menu_item_id = sku_by_loc.get((loc_name, sku))

                                if menu_item_id is None:
                                    menu_item_id = sku_global.get(sku)

                                if menu_item_id is None:
                                    loc_indices = menu_index_map.get(loc_name, [])
                                    candidate_indices = loc_indices or global_fallback_indices
                                    if candidate_indices:
                                        idx = random.choice(candidate_indices)
                                        if 0 <= idx < len(menu_items):
                                            menu_item_id = menu_items[idx][0]

                                if menu_item_id is None:
                                    continue

                                rows.append((loc_id, menu_item_id, date_str, meal_type_name))
                                locations_with_real_rows.add(loc_id)

    # --- 5. Fallback for locations with *no* real rows at all ---
    today_str = date.today().strftime("%Y-%m-%d")
    default_meal_type = "All Day"

    for loc_id, loc_name in enumerate(imp_dicts[imported_files["locations"]].keys()):
        # Only fallback if this location ended up with ZERO rows above
        if loc_id in locations_with_real_rows:
            continue

        loc_indices = menu_index_map.get(loc_name, [])
        candidate_indices = loc_indices or global_fallback_indices

        if not candidate_indices:
            continue  # nothing we can do

        min_items = 8
        max_items = min(len(candidate_indices), 20)
        k = random.randint(1, max_items)
        if len(candidate_indices) < min_items:
            k = len(candidate_indices)
        else:
            k = random.randint(min_items, max_items)

        chosen_indices = random.sample(candidate_indices, k)

        for idx in chosen_indices:
            if 0 <= idx < len(menu_items):
                menu_item_id = menu_items[idx][0]
                rows.append((loc_id, menu_item_id, today_str, default_meal_type))

    return rows


# -------------------------------------------------------------------
# menu_item_ingredient
# -------------------------------------------------------------------
def create_menu_item_ingredient(ingredients, sku_ingredients, menu_items):
    """Generate mapping rows from menu items to ingredients."""
    rows = []

    # Map normalized ingredient name -> ingredient_id
    ingredient_name_to_id = {}
    for ingredient_id, ingredient_name in ingredients:
        key = ingredient_name.lower().strip()
        ingredient_name_to_id[key] = ingredient_id

    # Map sku -> menu_item_id
    sku_to_menu_item_id = {}
    for menu_item in menu_items:
        menu_item_id = menu_item[0]
        sku = menu_item[5]  # (id, name, desc, allergens, loc, sku, is_duke_deal)
        if sku is not None:
            sku_to_menu_item_id[sku] = menu_item_id

    # Avoid duplicate (menu_item_id, ingredient_id) pairs
    seen_pairs = set()

    # For each SKU, map its ingredient names to IDs and build rows
    for sku, ingr_list in sku_ingredients.items():
        if sku not in sku_to_menu_item_id:
            continue

        menu_item_id = sku_to_menu_item_id[sku]

        for ingr in ingr_list:
            if not ingr:
                continue

            key = str(ingr).lower().strip()
            ingredient_id = ingredient_name_to_id.get(key)

            if ingredient_id is None:
                # No matching ingredient in the ingredient list
                continue

            pair = (menu_item_id, ingredient_id)
            if pair in seen_pairs:
                continue

            seen_pairs.add(pair)
            rows.append(pair)

    return rows


# -------------------------------------------------------------------
# user_dietary_restriction
# -------------------------------------------------------------------
def create_user_dietary_restriction(users, dietary_restrictions):
    """Generate rows mapping users to their dietary restrictions."""
    rows = []

    # Build a set of valid dietary restriction IDs
    valid_restriction_ids = {dr[0] for dr in dietary_restrictions}

    # To avoid duplicates like (user_id, 1) appearing twice
    seen_pairs = set()

    for user in users:
        user_id, name, email, phone, restriction_ids, dining_balance = user

        if not restriction_ids:
            continue

        for rid in restriction_ids:
            if rid not in valid_restriction_ids:
                # Skip invalid / unknown restriction ids
                continue

            pair = (user_id, rid)
            if pair in seen_pairs:
                continue

            seen_pairs.add(pair)
            rows.append(pair)

    return rows


# -------------------------------------------------------------------
# user_meal_plan
# -------------------------------------------------------------------
def create_user_meal_plan(users, meal_plans):
    """Assign each user a random meal plan."""
    rows = []

    valid_plan_ids = [dr[0] for dr in meal_plans]

    for user in users:
        pair = (user[0], random.choice(valid_plan_ids))
        rows.append(pair)

    return rows


# -------------------------------------------------------------------
# location_payment_methods
# -------------------------------------------------------------------
def create_location_payment_methods(locations):
    """Generate rows mapping locations to supported payment methods."""
    rows = []

    loc_data = imp_dicts[imported_files["location_data"]]

    for loc in locations:
        location_id, location_name, address, directions, description, max_capacity = loc

        if location_name not in loc_data:
            continue

        data = loc_data[location_name]
        payments = data.get("payment", [])

        # Dedupe payment types per location
        seen = set()

        for p in payments:
            if not p:
                continue

            payment_type = payment_enum_map[str(p).strip()]

            if payment_type in seen:
                continue

            seen.add(payment_type)
            rows.append((location_id, payment_type))

    return rows


# -------------------------------------------------------------------
# Generic helpers
# -------------------------------------------------------------------
def dedupe_rows(rows):
    """Deduplicate a list of tuples while preserving order."""
    seen = set()
    out = []

    for row in rows:
        if row not in seen:
            seen.add(row)
            out.append(row)

    return out


# -------------------------------------------------------------------
# Main orchestration + DB inserts
# -------------------------------------------------------------------
def main(num_users, num_days):
    # Generate all data sets
    dietary_restrictions = create_dietary_restrictions()  # Entry: NONE, Fields: ALL
    users = create_users(num_users, dietary_restrictions)  # Entry: NONE, Fields: 0,1,2,3,5
    managers = create_managers(loc_ids)  # Entry: NONE, Fields: ALL
    meal_plans = create_meal_plans()  # Entry: NONE, Fields: ALL
    ingredients = create_ingredients()  # Entry: 0, Fields: ALL
    menu_items = create_menu_item()  # Entry: 0, Fields 0,1,2,6
    locations = create_locations()  # Entry: 0, Fields: ALL
    location_hours = create_location_hours(num_days)  # Entry: 0, Fields: ALL
    schedules = create_schedule()  # Entry: NONE, Fields: ALL
    web_log = create_web_log(locations[1], location_hours[1])  # Entry: NONE, Fields: ALL
    menus = create_menu(menu_items[0], menu_items[2])  # Entry: NONE, Fields: ALL
    menu_item_ingredients = create_menu_item_ingredient(
        ingredients[0], ingredients[1], menu_items[0]
    )  # Entry: NONE, Fields: ALL
    user_dietary_restrictions = create_user_dietary_restriction(
        users, dietary_restrictions
    )  # Entry: NONE, Fields: ALL
    user_meal_plans = create_user_meal_plan(users, meal_plans)  # Entry: NONE, Fields: ALL
    location_payment_methods = create_location_payment_methods(
        locations[0]
    )  # Entry: NONE, Fields: ALL

    # Build final insert lists shaped to tables
    user_insert = []
    ingredient_insert = ingredients[0].copy()
    menu_items_insert = []
    locations_insert = locations[0].copy()
    location_hours_insert = location_hours[0].copy()

    for u in users:
        t = (u[0], u[1], u[2], u[3], u[5])
        user_insert.append(t)

    for m in menu_items[0]:
        t = (m[0], m[1], m[2], m[6])
        menu_items_insert.append(t)

    menus = dedupe_rows(menus)

    tables = {
        "location": locations_insert,
        "location_hours": location_hours_insert,
        "menu_item": menu_items_insert,
        "menu": menus,
        "dietary_restriction": dietary_restrictions,
        "user": user_insert,
        "user_dietary_restriction": user_dietary_restrictions,
        "meal_plan": meal_plans,
        "user_meal_plan": user_meal_plans,
        "schedule": schedules,
        "ingredient": ingredient_insert,
        "web_log": web_log,
        "menu_item_ingredient": menu_item_ingredients,
        "location_managers": managers,
        "location_payment_methods": location_payment_methods,
    }

    # Bulk insert into each table
    for k, v in tables.items():
        print(k)
        len_cols = len(v[0])

        vals = "("
        for i in range(len_cols):
            vals += "%s"
            if i != len_cols - 1:
                vals += ", "
        vals += ")"

        cur.executemany(f'INSERT INTO "{k}" VALUES {vals}', v)
        con.commit()


if __name__ == "__main__":
    main(5, 365)
    con.close()
