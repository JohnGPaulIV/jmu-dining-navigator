-- UPDATED ENUM TYPES (as requested)

CREATE TYPE payment_method AS ENUM (
  'card',
  'cash',
  'dining dollars',
  'flex',
  'swipe',
  'duke deal',
  'dining dollars gold',
  'panera gift card'
);

CREATE TYPE meal_type AS ENUM (
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
);

--------------------------------------------------
-- TABLES FROM SECOND SCHEMA
--------------------------------------------------

CREATE TABLE "location" (
  "location_id" int PRIMARY KEY,
  "hall_name" text,
  "address" text,
  "directions" text,
  "description" text,
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
  "location_id" int,
  "menu_item_id" int,
  "date" date,
  "meal_type" meal_type,
  PRIMARY KEY ("location_id", "menu_item_id", "date", "meal_type")
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
  "phone" text,
  "dining_balance" float
);

CREATE TABLE "user_dietary_restriction" (
  "user_id" int,
  "dietary_restriction_id" int,
  PRIMARY KEY ("user_id", "dietary_restriction_id")
);

CREATE TABLE "meal_plan" (
  "plan_id" int PRIMARY KEY,
  "swipes" int,
  "meal_plan" text
);

CREATE TABLE "user_meal_plan" (
  "user_id" int,
  "plan_id" int,
  PRIMARY KEY ("user_id", "plan_id")
);

CREATE TABLE "schedule" (
  "location_id" int,
  "date" date,
  "meal_type" meal_type,
  "beg_time" time,
  "end_time" time,
  "notes" text,
  PRIMARY KEY ("location_id", "date", "meal_type")
);

CREATE TABLE "ingredient" (
  "ingredient_id" int PRIMARY KEY,
  "ingredient_name" text
);

CREATE TABLE "web_log" (
  "location_id" int,
  "timestamp" timestamp,
  "current_capacity" int,
  PRIMARY KEY ("location_id", "timestamp")
);

CREATE TABLE "menu_item_ingredient" (
  "menu_item_id" int,
  "ingredient_id" int,
  PRIMARY KEY ("menu_item_id", "ingredient_id")
);

CREATE TABLE "location_managers" (
  "manager_id" int PRIMARY KEY,
  "location_id" int,
  "first_name" text,
  "last_name" text,
  "email" text,
  "phone" text
);

CREATE TABLE "location_payment_methods" (
  "location_id" int,
  "payment_type" payment_method,
  PRIMARY KEY ("location_id", "payment_type")
);

--------------------------------------------------
-- EXTRA TABLES FROM FIRST SCHEMA
--------------------------------------------------

CREATE TABLE "user_favorite_item" (
  "user_id" int,
  "menu_item_id" int,
  PRIMARY KEY ("user_id", "menu_item_id")
);

CREATE TABLE "ticket" (
  "ticket_id" serial PRIMARY KEY,
  "user_id" int REFERENCES "user"("user_id"),
  "message" text NOT NULL,
  "created_at" timestamp DEFAULT CURRENT_TIMESTAMP
);
