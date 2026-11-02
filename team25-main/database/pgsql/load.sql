-- INSERT INTO dietary_restriction (dietary_restriction_id, name, description)
--   VALUES
--     (1, 'Vegetarian', 'No meat'),
--     (2, 'Vegan', 'No animal products'),
--     (3, 'Gluten-Free', 'No gluten'),
--     (4, 'Nut Allergy', 'No tree nuts'),
--     (5, 'Lactose Intolerant', 'No dairy')
-- ON CONFLICT DO NOTHING;

-- INSERT INTO meal_plan (plan_id, swipes, meal_plan)
--   VALUES
--     (1, 120, 'Bronze'),
--     (2, 200, 'Silver'),
--     (3, 300, 'Gold')
-- ON CONFLICT DO NOTHING;

-- -- A couple of minimal example rows for dev/testing FROM CHATGPT🤑🤑🤑🤑
-- INSERT INTO "user" (user_id, name, email, phone, dietary_restriction, dining_balance)
--   VALUES (1001, 'Test Student', 'test@student.edu', '5551234567', NULL, 75.00)
-- ON CONFLICT DO NOTHING;

-- INSERT INTO "location" (location_id, manager_id, hall_name, address, directions, description, payment_method, capacity_limit)
--   VALUES (1, NULL, 'Commons Dining', '123 Campus Dr', 'Inside Commons', 'Main campus dining hall', 'swipe', 400)
-- ON CONFLICT DO NOTHING;

-- INSERT INTO menu_item (menu_item_id, item_name, description, duke_deal)
--   VALUES (1, 'Cheeseburger', 'Beef patty with cheese', false)
-- ON CONFLICT DO NOTHING;

-- INSERT INTO menu (location_id, menu_item_id, date, meal_type)
--   VALUES (1, 1, CURRENT_DATE, 'lunch')
-- ON CONFLICT DO NOTHING;
