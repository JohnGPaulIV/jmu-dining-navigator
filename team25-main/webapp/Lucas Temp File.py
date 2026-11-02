#Current Capacity For Specific Dining Hall
SELECT *
FROM web_log
WHERE location_id = ?
ORDER BY timestamp DESC
LIMIT 1;

#Show All Current Capacities
SELECT wl.location_id,
       wl.current_capacity,
       wl.timestamp
FROM web_log wl
JOIN (
    SELECT location_id, MAX(timestamp) AS latest_timestamp
    FROM web_log
    GROUP BY location_id
) AS latest
ON wl.location_id = latest.location_id
AND wl.timestamp = latest.latest_timestamp
ORDER BY wl.location_id;

class GraphView(BaseView):
    route_base = "/graph"

    @expose("/")
    def graph_page(self):

        hall_id = 1  # fixed hall for demo

        #generates 
        avg_rows = db.session.execute("""
            SELECT time_block, avg_capacity
            FROM avg_capacity_by_time
            WHERE location_id = :hall_id
            ORDER BY time_block;
        """, {"hall_id": hall_id}).fetchall()

        avg_data = [{"time_block": r[0], "avg_capacity": r[1]} for r in avg_rows]

        #most recent weblog pop
        live_row = db.session.execute("""
            SELECT current_capacity, timestamp
            FROM web_log
            WHERE location_id = :hall_id
            ORDER BY timestamp DESC
            LIMIT 1;
        """, {"hall_id": hall_id}).fetchone()

        #cap limit for graph
        cap_row = db.session.execute("""
            SELECT capacity_limit
            FROM location
            WHERE location_id = :hall_id;
        """, {"hall_id": hall_id}).fetchone()

        live_capacity = {
            "current_capacity": live_row[0],
            "timestamp": live_row[1].strftime("%Y-%m-%d %H:%M:%S"),
            "capacity_limit": cap_row[0]
        }

        #jinja
        return self.render_template(
            "graph.jinja",
            avg_data=avg_data,
            live_capacity=live_capacity
        )
