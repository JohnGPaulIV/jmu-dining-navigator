"""Base views that expose specific routes."""

from app import db
from flask_appbuilder import BaseView, expose
from markdown import markdown
from models import Location
from pathlib import Path
from sqlalchemy import text


def md_to_html(filename: str) -> str:
    """Render a markdown file as html."""
    path = Path("templates") / filename
    text = path.read_text(encoding="utf-8")
    return markdown(text, extensions=["attr_list"])


class AboutView(BaseView):
    route_base = "/about"

    @expose("/")
    def about(self):
        return self.render_template("about.jinja", content=md_to_html("about.md"))

class HelpView(BaseView):
    route_base = "/help"

    @expose("/")
    def help_page(self):
        help_text = """
        <h2>Help & Support</h2>
        <p>If you have any issues, please contact one of the following:</p>

        <h4>For dining related questions:</h4>
        <ul>
            <li>Email: dining@jmu.edu</li>
            <li>Call: 540-568-6751</li>
        </ul>

        <h4>For IT help:</h4>
        <ul>
            <li>Email: helpdesk@jmu.edu</li>
            <li>Call: (540) 568-3555</li>
        </ul>

        <h4>For technology security or abuse incidents:</h4>
        <ul>
            <li>Email: abuse@jmu.edu</li>
        </ul>

        <h4>For questions about IT advising:</h4>
        <ul>
            <li>Email: it.advising@jmu.edu</li>
        </ul>
        """
        return self.render_template("help.jinja", help_txt=help_text)


class MapView(BaseView):
    route_base = "/map"

    @expose("/")
    def map_page(self):
        return self.render_template("map.jinja")

class PlaceView(BaseView):
    route_base = "/place"

    @expose("/<location_slug>")
    def show_location(self, location_slug):
        location = db.session.execute(
            db.select(Location).where(
                Location.hall_name == location_slug
            )
        ).scalar_one_or_none()

        if location is None:
            return "Location not found", 404

        location_id = location.location_id

        # Custom SQL query
        sql = text("""
            SELECT
                mi.menu_item_id,
                mi.item_name,
                mi.description,
                mi.duke_deal,
                m.meal_type,
                m.date
            FROM menu m
            JOIN menu_item mi
                ON mi.menu_item_id = m.menu_item_id
            WHERE m.location_id = :loc AND m.date = CURRENT_DATE
            ORDER BY m.meal_type, mi.item_name;
        """)

        menu_items = db.session.execute(sql, {"loc": location_id}).fetchall()

        return self.render_template(
            "place.jinja",
            location=location,
            menu_items=menu_items
        )

class popPage(BaseView):
    route = "/chart"

    @expose("/")
    def genPop(self):
        all_current_pop = db.session.execute("""
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
        """).fetchall()

        return self.render_template("chart.jinja", all_current_pop = all_current_pop)

class GraphView(BaseView):
    route_base = "/graph"

    @expose("/")
    def graph_page(self):
        d_hall = db.session.execute(
            db.select(Location).where(Location.hall_name == "d-hall")
        ).scalar_one_or_none()

        e_hall = db.session.execute(
            db.select(Location).where(Location.hall_name == "e-hall")
        ).scalar_one_or_none()

        if d_hall is None or e_hall is None:
            return "Dining hall data is missing. Import locations first.", 404
        hall_id = d_hall.location_id  # fixed hall for demo
        hall_id2 = e_hall.location_id
        #generates


        sql = text("""
    SELECT
        LPAD(EXTRACT(HOUR FROM w.timestamp)::text, 2, '0') || ':' ||
        LPAD(
            (EXTRACT(MINUTE FROM w.timestamp)::int - (EXTRACT(MINUTE FROM w.timestamp)::int % 15))::text,
            2, '0'
        ) AS time_block,
        AVG(w.current_capacity) AS avg_capacity
    FROM web_log w
    INNER JOIN schedule s
        ON s.location_id = w.location_id
       AND s.date = DATE(w.timestamp)
       AND w.timestamp::time BETWEEN s.beg_time AND s.end_time
    WHERE w.location_id = :hall_id
    GROUP BY time_block
    ORDER BY time_block
""")

        avg_rows = db.session.execute(sql, {"hall_id": hall_id}).fetchall()
        avg_rows2 = db.session.execute(sql, {"hall_id": hall_id2}).fetchall()

        """
            avg_rows = db.session.execute(
            SELECT time_block, avg_capacity
            FROM avg_capacity_by_time
            WHERE location_id = :hall_id
            ORDER BY time_block;
        , {"hall_id": hall_id}).fetchall()
        """

        avg_data = [{"time_block": r[0], "avg_capacity": r[1]} for r in avg_rows]
        avg_data2 = [{"time_block": r[0], "avg_capacity": r[1]} for r in avg_rows2]

        #most recent weblog pop
        sql2 = text("""
            SELECT current_capacity, timestamp
            FROM web_log
            WHERE location_id = :hall_id
            ORDER BY timestamp DESC
            LIMIT 1;
        """)
        live_row = db.session.execute(sql2, {"hall_id": hall_id}).fetchone()
        live_row2 = db.session.execute(sql2, {"hall_id": hall_id2}).fetchone()

        #cap limit for graph
        sql3 = text("""
            SELECT capacity_limit
            FROM location
            WHERE location_id = :hall_id;
        """)

        cap_row = db.session.execute(sql3, {"hall_id": hall_id}).fetchone()
        cap_row2 = db.session.execute(sql3, {"hall_id": hall_id2}).fetchone()

        live_capacity = {
            "current_capacity": live_row[0],
            "timestamp": live_row[1].strftime("%Y-%m-%d %H:%M:%S"),
            "capacity_limit": cap_row[0]
        }

        live_capacity2 = {
            "current_capacity": live_row2[0],
            "timestamp": live_row2[1].strftime("%Y-%m-%d %H:%M:%S"),
            "capacity_limit": cap_row2[0]
        }

        #jinja
        return self.render_template(
            "graph.jinja",
            avg_data=avg_data,
            avg_data2=avg_data2,
            live_capacity=live_capacity,
            live_capacity2=live_capacity2
        )
