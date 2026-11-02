-- Gets all available menu items at the specified dining hall
SELECT mi.item_name, mi.description
FROM menu_item mi
JOIN menu_item_at_hall mh ON mi.menu_item_id = mh.menu_item_id
WHERE mh.hall_id = (some hall id) AND mh.avaliability = TRUE;

-- Gets all dietary restrictions for the specified user
SELECT dr.name, dr.description
FROM dietary_restriction dr
JOIN user_dietary_restriction udr ON dr.dietary_restriction_id = udr.dietary_restriction_id
WHERE udr.user_id = (some user id);

--Get all info from a user
SELECT * 
FROM user
WHERE user_id = 114868541;

--Get the meal plan ID for the specified user ID
SELECT plan_id
FROM user_meal_plan
JOIN user ON user_meal_plan.user_id = user.user_id
WHERE user.user_id = 114868541;
