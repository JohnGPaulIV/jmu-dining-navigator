COMMENT ON TABLE "location" IS 'Contains dining hall details such as name, location, and capacity';

COMMENT ON TABLE "menu_item" IS 'Stores menu items available across dining halls';

COMMENT ON TABLE "menu" IS 'Associates menu items with dining halls and their availability';

COMMENT ON TABLE "dietary_restriction" IS 'Defines dietary restrictions such as vegetarian, vegan, gluten-free';

COMMENT ON TABLE "user" IS 'Contains user information including contact, balance, and role';

COMMENT ON TABLE "user_dietary_restriction" IS 'Maps users to their dietary restrictions';

COMMENT ON TABLE "meal_plan" IS 'Describes a meal plan’s attributes such as swipe allowance';

COMMENT ON TABLE "user_meal_plan" IS 'Associates users with their meal plans';