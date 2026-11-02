"""Generate fake data for the Team25 database."""

import csv
import faker
import psycopg
import random 
import datetime

NUM_USERS = 100
NUM_DIETARY = 5
NUM_MEAL_PLANS = 4
NUM_LOCATIONS = 10
NUM_MENU_ITEMS = 40
NUM_INGREDIENTS = 30
DAYS_OF_OPERATION = 365
NUM_WEB_LOGS_PER_LOC = 5

# Connect to the database
con = psycopg.connect(host="localhost", port="5432", user="team25", dbname="team25")
cur = con.cursor()

fake = faker.Faker()
random.seed(0)

#ENUMS 
payment_methods = ['card', 'cash', 'dining_dollars', 'flex', 'swipe', 'duke_deal']
meal_types = ['breakfast', 'lunch', 'dinner']

def main():
    #dietary_restriction
    print("dietary_restrictions")
    restriction_names = ["Vegetarian", "Vegan", "Gluten-Free", "Nut Allergy", "Lactose Intolerant"]
    for i, name in enumerate(restriction_names):
        cur.execute(
            'INSERT INTO dietary_restriction VALUES (%s, %s, %s)',
            (i + 1, name, fake.sentence())
        )
    con.commit()

    # user
    print("user")
    users = []
    for i in range(NUM_USERS):
        person = (
            i + 1,
            fake.name(),
            fake.email(),
            fake.phone_number(),
            random.choice(restriction_names),
            round(random.uniform(20, 150), 2)
        )
        cur.execute(
            'INSERT INTO "user" VALUES (%s, %s, %s, %s, %s, %s)',
            person
        )
        users.append(person[0])
    con.commit()

    # meal_plan
    # MUST CHANGE THIS TO FIT REAL MEAL PLANS AND VALUES
    meal_plan_names = ["Bronze", "Silver", "Gold", "Platinum"]
    print("meal_plan")
    for i in range(NUM_MEAL_PLANS):
        cur.execute(
            'INSERT INTO meal_plan VALUES (%s, %s, %s)',
            (i + 1, random.randint(50, 250), meal_plan_names[i])
        )
    con.commit()

    #user_meal_plan
    print("user_meal_plan")
    for u in users:
        if random.random() < 0.7:
            plan_id = random.randint(1, NUM_MEAL_PLANS)
            cur.execute(
                'INSERT INTO user_meal_plan VALUES (%s, %s)',
                (u, plan_id)
            )
    con.commit()

    #user_dietary_restriction
    print("user_dietary_restrictions")
    for u in users:
        if random.random() < 0.2:
            restriction_id = random.randint(1, NUM_DIETARY)
            cur.execute(
                'INSERT INTO user_dietary_restriction VALUES (%s, %s)',
                (u, restriction_id)
            )
    con.commit()

    #location
    locations = []
    print("location")
    for i in range(NUM_LOCATIONS):
        manager_id = random.choice(users)
        hall = fake.company() + " Dining Hall"
        cur.execute(
            '''INSERT INTO location
            (location_id, manager_id, hall_name, address, directions, description, payment_method, capacity_limit)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
            (
                i + 1,
                manager_id,
                hall,
                fake.address().replace("\n", ", "),
                fake.sentence(),
                fake.text(max_nb_chars=50),
                random.choice(payment_methods), #THIS WILL BE A PROBLEM
                #WE NEED TO MAKE IT SO THAT THERE CAN BE MULTIPLE PAYMENT METHODS BUT FIRST WE NEED TO CHANGE CREATE
                random.randint(100, 500)
            )
        )
        locations.append(i + 1)
    con.commit()

    #location_hours
    #make a row for each DAY_OF_OPERATION that will be unique to the date
    #This still needs to be adjusted, for example right now open and close times are random, so the same location will have different times for monday and tuesday.
    today = datetime.date.today()
    location_hours = []
    print("location_hours")

    # Prepare data in memory first
    location_hours_data = []
    for loc_id in locations:
        for d in range(DAYS_OF_OPERATION):
            day = today + datetime.timedelta(days=d)
            open_hour = random.randint(7, 9)
            close_hour = random.randint(19, 22)
            open_time = datetime.time(open_hour, 0)
            close_time = datetime.time(close_hour, 0)
            location_hours.append((loc_id, day, open_hour, close_hour))
            location_hours_data.append((loc_id, day, open_time, close_time))

    # One bulk insert instead of 3,650 single ones
    cur.executemany(
        'INSERT INTO location_hours VALUES (%s, %s, %s, %s)',
        location_hours_data
    )
    con.commit()

    # menu_item
    menu_items = []
    print("menu_item")
    for i in range(NUM_MENU_ITEMS):
        cur.execute(
            'INSERT INTO menu_item VALUES (%s, %s, %s, %s)',
            (i + 1, fake.word().capitalize(), fake.sentence(), random.choice([True, False]))
        )
        menu_items.append(i + 1)
    con.commit()

    #ingredient
    print("ingredient")
    ingredients = []
    for i in range(NUM_INGREDIENTS):
        dr = random.randint(1, NUM_DIETARY)
        cur.execute(
            'INSERT INTO ingredient VALUES (%s, %s, %s)',
            (i + 1, fake.word(), dr)
        )
        ingredients.append(i + 1)
    con.commit()

    #menu_item_ingredient
    print("menu_item_ingredient")
    for item in menu_items:
        k = random.randint(3, min(8, len(ingredients)))
        for ing in random.sample(ingredients, k=k):  # unique picks
            cur.execute(
                'INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (%s, %s)',
                (item, ing)
            )
    con.commit()

    #menu
    print("menu")
    for loc_id in locations:
        for _ in range(random.randint(3, 7)):
            item = random.choice(menu_items)
            date = today + datetime.timedelta(days=random.randint(0, DAYS_OF_OPERATION - 1))
            meal = random.choice(meal_types)
            cur.execute(
                'INSERT INTO menu VALUES (%s, %s, %s, %s)',
                (loc_id, item, date, meal)
            )
    con.commit()

    #schedule
    print("schedule")
    schedule_data = []
    for loc_id in locations:
        for d in range(DAYS_OF_OPERATION):
            date = today + datetime.timedelta(days=d)
            for meal in meal_types:
                beg_t = datetime.time(random.randint(7, 10), 0)
                end_t = datetime.time(random.randint(11, 22), 0)
                schedule_data.append((loc_id, date, meal, beg_t, end_t, fake.sentence()))

    cur.executemany(
        'INSERT INTO schedule VALUES (%s, %s, %s, %s, %s, %s)',
        schedule_data
    )
    con.commit()

    # web_log
    print("Generating web logs...")
    web_log_data = []

    for (loc_id, day, open_hour, close_hour) in location_hours:
        open_dt = datetime.datetime.combine(day, datetime.time(open_hour, 0))
        close_dt = datetime.datetime.combine(day, datetime.time(close_hour, 0))

        current = open_dt
        capacity_limit = random.randint(200, 500)
        while current <= close_dt:
            current_capacity = int(capacity_limit * random.uniform(0.2, 1.0))
            web_log_data.append((loc_id, current, current_capacity))
            current += datetime.timedelta(minutes=15)

    # bulk insert once
    cur.executemany(
        'INSERT INTO web_log VALUES (%s, %s, %s)',
        web_log_data
    )
    con.commit()
if __name__ == "__main__":
    main()
    con.close()