CREATE TYPE "payment_method" AS ENUM (
  'card',
  'cash',
  'dining_dollars',
  'flex',
  'swipe',
  'duke_deal'
);

CREATE TYPE "meal_type" AS ENUM (
  'breakfast',
  'lunch',
  'dinner'
);

CREATE TABLE "location" (
  "location_id" int PRIMARY KEY,
  "manager_id" int,
  "hall_name" text,
  "address" text,
  "directions" text,
  "description" text,
  "payment_method" enum,
  "capacity_limit" int
);

CREATE TABLE "location_hours" (
  "location_id" int,
  "day" date,
  "open_time" time,
  "close_time" time,
  PRIMARY KEY ("location_id", "day")
);

CREATE TABLE "menu_item" (
  "menu_item_id" int PRIMARY KEY,
  "item_name" text,
  "description" text,
  "duke_deal" bool
);

CREATE TABLE "menu" (
  "location_id" int PRIMARY KEY,
  "menu_item_id" int,
  "date" date,
  "meal_type" enum
);

CREATE TABLE "dietary_restriction" (
  "dietary_restriction_id" int PRIMARY KEY,
  "name" text,
  "description" text
);

CREATE TABLE "user" (
  "user_id" int PRIMARY KEY,
  "name" text,
  "email" text,
  "phone" int,
  "dietary_restriction" text,
  "dining_balance" float
);

CREATE TABLE "user_dietary_restriction" (
  "user_id" int,
  "dietary_restriction_id" int,
  PRIMARY KEY ("user_id", "dietary_restriction_id")
);

CREATE TABLE "meal_plan" (
  "plan_id" INT PRIMARY KEY,
  "swipes" INT,
  "meal_plan" TEXT
);

CREATE TABLE "user_meal_plan" (
  "user_id" int,
  "plan_id" int,
  PRIMARY KEY ("user_id", "plan_id")
);

CREATE TABLE "schedule" (
  "location_id" int,
  "date" date,
  "meal_type" enum,
  "beg_time" time,
  "end_time" time,
  "notes" text,
  PRIMARY KEY ("location_id", "date", "meal_type")
);

CREATE TABLE "ingredient" (
  "ingredient_id" int PRIMARY KEY,
  "ingredient_name" text,
  "dietary_restriction" int
);

CREATE TABLE "web_log" (
  "location_id" int,
  "timestamp" datetime,
  "current_capacity" int,
  PRIMARY KEY ("location_id", "timestamp")
);

CREATE TABLE "menu_item_ingredient" (
  "menu_item_id" int,
  "ingredient_id" int,
  PRIMARY KEY ("menu_item_id", "ingredient_id")
);

COMMENT ON TABLE "location" IS 'Contains dining hall details such as name, location, and capacity';

COMMENT ON TABLE "menu_item" IS 'Stores menu items available across dining halls';

COMMENT ON TABLE "menu" IS 'Associates menu items with dining halls and their availability';

COMMENT ON TABLE "dietary_restriction" IS 'Defines dietary restrictions such as vegetarian, vegan, gluten-free';

COMMENT ON TABLE "user" IS 'Contains user information including contact, balance, and role';

COMMENT ON TABLE "user_dietary_restriction" IS 'Maps users to their dietary restrictions';

COMMENT ON TABLE "meal_plan" IS 'Describes a meal plan’s attributes such as swipe allowance';

COMMENT ON TABLE "user_meal_plan" IS 'Associates users with their meal plans';

ALTER TABLE "location" ADD FOREIGN KEY ("manager_id") REFERENCES "user" ("user_id");

ALTER TABLE "menu" ADD FOREIGN KEY ("meal_type") REFERENCES "schedule" ("meal_type");

ALTER TABLE "schedule" ADD FOREIGN KEY ("date") REFERENCES "menu" ("date");

ALTER TABLE "location_hours" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("location_id");

ALTER TABLE "menu_item_ingredient" ADD FOREIGN KEY ("menu_item_id") REFERENCES "menu_item" ("menu_item_id");

ALTER TABLE "ingredient" ADD FOREIGN KEY ("ingredient_id") REFERENCES "menu_item_ingredient" ("ingredient_id");

ALTER TABLE "ingredient" ADD FOREIGN KEY ("dietary_restriction") REFERENCES "dietary_restriction" ("dietary_restriction_id");

ALTER TABLE "web_log" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("location_id");

ALTER TABLE "schedule" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("location_id");

ALTER TABLE "menu" ADD FOREIGN KEY ("location_id") REFERENCES "schedule" ("location_id");

ALTER TABLE "menu_item" ADD FOREIGN KEY ("menu_item_id") REFERENCES "menu" ("menu_item_id");

ALTER TABLE "user_dietary_restriction" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "user_dietary_restriction" ADD FOREIGN KEY ("dietary_restriction_id") REFERENCES "dietary_restriction" ("dietary_restriction_id");

ALTER TABLE "user_meal_plan" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "user_meal_plan" ADD FOREIGN KEY ("user_id") REFERENCES "meal_plan" ("plan_id");
