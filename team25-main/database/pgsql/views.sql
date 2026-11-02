-- makes this file re-runnable during development
DROP VIEW IF EXISTS
    v_duke_deals_today,
    v_menu_today,
    v_location_open_now,
    v_location_hours_today,
    v_location_capacity_latest
CASCADE;

------------------------------------------------------------
-- 1. What’s being served today at each location & meal
------------------------------------------------------------
CREATE VIEW v_menu_today AS
SELECT
    m.location_id,
    l.hall_name,
    m.date,
    m.meal_type,
    m.menu_item_id,
    mi.item_name,
    mi.description,
    mi.duke_deal
FROM menu m
JOIN location l
    ON l.location_id = m.location_id
JOIN menu_item mi
    ON mi.menu_item_id = m.menu_item_id
WHERE m.date = CURRENT_DATE;


------------------------------------------------------------
-- 2. Today's Duke Deals by location/meal
------------------------------------------------------------
CREATE VIEW v_duke_deals_today AS
SELECT
    t.location_id,
    t.hall_name,
    t.date,
    t.meal_type,
    t.menu_item_id,
    t.item_name,
    t.description,
    t.duke_deal
FROM v_menu_today t
WHERE t.duke_deal = TRUE;


------------------------------------------------------------
-- 3. Today's hours for each location
--    (needed by v_location_open_now)
------------------------------------------------------------
CREATE VIEW v_location_hours_today AS
SELECT
    lh.location_id,
    l.hall_name,
    lh.day,
    lh.open_time,
    lh.close_time
FROM location_hours lh
JOIN location l
    ON l.location_id = lh.location_id
WHERE lh.day = CURRENT_DATE;


------------------------------------------------------------
-- 4. Is the location open right now?
------------------------------------------------------------
CREATE VIEW v_location_open_now AS
SELECT
    h.location_id,
    h.hall_name,
    (CURRENT_TIME BETWEEN h.open_time AND h.close_time) AS is_open_now
FROM v_location_hours_today h;


------------------------------------------------------------
-- 5. Latest capacity reading per location
------------------------------------------------------------
CREATE VIEW v_location_capacity_latest AS
SELECT DISTINCT ON (wl.location_id)
    wl.location_id,
    l.hall_name,
    wl.timestamp,
    wl.current_capacity,
    l.capacity_limit,
    ROUND(
        100.0 * wl.current_capacity
        / NULLIF(l.capacity_limit, 0),
        1
    ) AS capacity_pct
FROM web_log wl
JOIN location l
    ON l.location_id = wl.location_id
ORDER BY
    wl.location_id,
    wl.timestamp DESC;
