-- location.manager_id no longer exists → this one is removed
-- ALTER TABLE "location" ADD FOREIGN KEY ("manager_id") REFERENCES "user" ("user_id");

ALTER TABLE "location_hours"
  ADD FOREIGN KEY ("location_id") REFERENCES "location" ("location_id");

ALTER TABLE "menu_item_ingredient"
  ADD FOREIGN KEY ("menu_item_id") REFERENCES "menu_item" ("menu_item_id");

ALTER TABLE "menu_item_ingredient"
  ADD FOREIGN KEY ("ingredient_id") REFERENCES "ingredient" ("ingredient_id");

-- ingredient.dietary_restriction no longer exists in the new schema → remove this
-- ALTER TABLE "ingredient" ADD FOREIGN KEY ("dietary_restriction") REFERENCES "dietary_restriction" ("dietary_restriction_id");

ALTER TABLE "web_log"
  ADD FOREIGN KEY ("location_id") REFERENCES "location" ("location_id");

ALTER TABLE "schedule"
  ADD FOREIGN KEY ("location_id") REFERENCES "location" ("location_id");

ALTER TABLE "menu"
  ADD FOREIGN KEY ("location_id") REFERENCES "location" ("location_id");

ALTER TABLE "menu"
  ADD FOREIGN KEY ("menu_item_id") REFERENCES "menu_item" ("menu_item_id");

ALTER TABLE "user_dietary_restriction"
  ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "user_dietary_restriction"
  ADD FOREIGN KEY ("dietary_restriction_id") REFERENCES "dietary_restriction" ("dietary_restriction_id");

ALTER TABLE "user_meal_plan"
  ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");

ALTER TABLE "user_meal_plan"
  ADD FOREIGN KEY ("plan_id") REFERENCES "meal_plan" ("plan_id");

ALTER TABLE "user_favorite_item"
  ADD FOREIGN KEY ("user_id") REFERENCES "user"("user_id");

ALTER TABLE "user_favorite_item"
  ADD FOREIGN KEY ("menu_item_id") REFERENCES "menu_item"("menu_item_id");

-- New tables in the merged schema:

ALTER TABLE "location_managers"
  ADD FOREIGN KEY ("location_id") REFERENCES "location"("location_id");

ALTER TABLE "location_payment_methods"
  ADD FOREIGN KEY ("location_id") REFERENCES "location"("location_id");

-- Ticket already has its FK inline in the CREATE TABLE:
-- "user_id" int REFERENCES "user"("user_id")
-- so no extra ALTER needed.
