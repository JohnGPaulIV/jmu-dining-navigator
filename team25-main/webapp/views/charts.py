"""Chart views that visualize complex database queries."""

from flask_appbuilder.charts.views import DirectByChartView, GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from models import queries


# ------------------------------------------------------------------------------
# Chart Views
# ------------------------------------------------------------------------------


class Workshop_Department_Chart(GroupByChartView):
    datamodel = SQLAInterface(queries.Workshop_Department)
    chart_title = "Workshop Leaders"
    definitions = [
        {
            "group": "college_code",
            "series": [
                (aggregate_count, "leader"),
            ]
        },
        {
            "group": "department_code",
            "series": [
                (aggregate_count, "leader"),
            ]
        },
    ]