from flask import flash, g, redirect
from app import db
import models
from models import DiningUser
from flask_appbuilder import ModelView
from flask_appbuilder.actions import action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.filters import BaseFilter

# Filter dietary restrictions
# class FilterMenuItemSafeForUser(BaseFilter):
#     """
#     Filter: only menu items that do NOT conflict with the
#     current user's dietary restrictions (via ingredients).
#     Used as a 'search' option on Menu items.
#     """
#     name = "Safe for my restrictions"

#     def apply(self, query, value):
#         fab_user = g.user
#         dining_user = db.session.get(DiningUser, fab_user.id)

#         if dining_user is None or not dining_user.dietary_restrictions:
#             return query

#         restriction_ids = [r.dietary_restriction_id for r in dining_user.dietary_restrictions]

#         bad_ingredient_subq = (
#             db.session.query(models.Ingredient.ingredient_id)
#             .filter(models.Ingredient.dietary_restriction_id.in_(restriction_ids))
#             .subquery()
#         )

#         bad_item_exists = (
#             db.session.query(models.t_menu_item_ingredient.c.menu_item_id)
#             .filter(
#                 models.t_menu_item_ingredient.c.menu_item_id == models.MenuItem.menu_item_id,
#                 models.t_menu_item_ingredient.c.ingredient_id.in_(bad_ingredient_subq),
#             )
#             .exists()
#         )

#         return query.filter(~bad_item_exists)

# ---------------------------------------------------------------
# Tables
# ---------------------------------------------------------------

class Web_logModelView(ModelView):
    datamodel = SQLAInterface(models.WebLog)
    route_base = '/web_log'
    list_title = 'Web Logs'
    list_columns = ['location_id', 'timestamp', 'current_capacity']

    label_columns = {
        'location_id': 'Location',
        'timestamp': 'Timestamp',
        'current_capacity': 'Current Capacity',
    }


class Location_hoursModelView(ModelView):
    datamodel = SQLAInterface(models.LocationHours)
    route_base = '/location_hours'
    list_title = 'Location Hours'

    # Show the time fields in the list
    list_columns = ['location_id', 'day', 'open_time', 'close_time']

    # Only search on columns FAB understands cleanly
    search_columns = ['location_id', 'day']
    add_exclude_columns = edit_exclude_columns = show_exclude_columns = ['open_time', 'close_time']

    label_columns = {
        'location_id': 'Location',
        'day': 'Day',
        'open_time': 'Open Time',
        'close_time': 'Close Time',
    }


class ScheduleModelView(ModelView):
    datamodel = SQLAInterface(models.Schedule)
    route_base = '/schedule'
    list_title = 'Schedules'

    # Show time fields in the table
    list_columns = ['location_id', 'date', 'meal_type', 'beg_time', 'end_time', 'notes']

    # Do NOT include beg_time / end_time in search
    search_columns = ['location_id', 'date', 'meal_type', 'notes']
    add_exclude_columns = edit_exclude_columns = show_exclude_columns = ['beg_time', 'end_time']
    label_columns = {
        'location_id': 'Location',
        'date': 'Date',
        'meal_type': 'Meal Type',
        'beg_time': 'Begin Time',
        'end_time': 'End Time',
        'notes': 'Notes',
    }


class LocationModelView(ModelView):
    datamodel = SQLAInterface(models.Location)
    route_base = '/location'
    list_title = 'Locations'

    list_columns = [
        'location_id',
        'hall_name',
        'address',
        'directions',
        'description',
        'payment_method',
        'capacity_limit',
    ]

    add_exclude_columns = edit_exclude_columns = show_exclude_columns = [
        'location_hours',
        'schedules',
        'web_logs',
    ]

    related_views = [Location_hoursModelView, ScheduleModelView, Web_logModelView]

    label_columns = {
        'location_id': 'Location ID',
        'hall_name': 'Hall Name',
        'address': 'Address',
        'directions': 'Directions',
        'description': 'Description',
        'payment_method': 'Payment Method',
        'capacity_limit': 'Capacity Limit',
    }


class IngredientModelView(ModelView):
    datamodel = SQLAInterface(models.Ingredient)
    route_base = '/ingredient'
    list_title = 'Ingredients'

    list_columns = ['ingredient_id', 'ingredient_name', 'dietary_restriction']
    add_exclude_columns = edit_exclude_columns = show_exclude_columns = ['menu_items']

    label_columns = {
        'ingredient_id': 'Ingredient ID',
        'ingredient_name': 'Ingredient Name',
        'dietary_restriction': 'Dietary Restriction',
    }


class Menu_itemModelView(ModelView):
    datamodel = SQLAInterface(models.MenuItem)
    route_base = '/menu_item'
    list_title = 'Menu Items'

    list_columns = ['menu_item_id', 'item_name', 'description', 'duke_deal']

    label_columns = {
        'menu_item_id': 'Menu Item ID',
        'item_name': 'Item Name',
        'description': 'Description',
        'duke_deal': 'Duke Deal',
    }

    # Filter dietary restrictions
    # search_columns = ['item_name', 'description']

    # search_filters = {
    #     'menu_item_id': [FilterMenuItemSafeForUser]
    # }

    @action("favorite", "Add to Favorites", "Add selected menu item(s) to your favorites?", "fa-star")
    def add_to_favorites(self, items):
        if not isinstance(items, list):
            items = [items]

        # get current logged-in user
        fab_user = g.user
        dining_user = db.session.get(DiningUser, fab_user.id)

        if dining_user is None:
            flash("Error: No DiningUser profile found for current user.", "danger")
            return redirect(self.get_redirect())

        added = 0
        for item in items:
            if item not in dining_user.favorite_items:
                dining_user.favorite_items.append(item)
                added += 1

        db.session.commit()
        flash(f"Added {added} item(s) to your favorites!", "success")
        return redirect(self.get_redirect())


class Dietary_restrictionModelView(ModelView):
    datamodel = SQLAInterface(models.DietaryRestriction)
    route_base = '/dietary_restriction'
    list_title = 'Dietary Restrictions'

    list_columns = ['dietary_restriction_id', 'name', 'description']

    label_columns = {
        'dietary_restriction_id': 'Restriction ID',
        'name': 'Name',
        'description': 'Description',
    }


class Meal_planModelView(ModelView):
    datamodel = SQLAInterface(models.MealPlan)
    route_base = '/meal_plan'
    list_title = 'Meal Plans'

    list_columns = ['plan_id', 'swipes', 'meal_plan']

    label_columns = {
        'plan_id': 'Plan ID',
        'swipes': 'Swipes',
        'meal_plan': 'Meal Plan',
    }


class DiningUserModelView(ModelView):
    datamodel = SQLAInterface(models.DiningUser)
    route_base = '/user'
    list_title = 'Users'

    list_columns = ['user_id', 'name', 'email', 'phone', 'dining_balance']

    add_exclude_columns = edit_exclude_columns = show_exclude_columns = [
        'dietary_restrictions',
        'meal_plans',
        'locations',
    ]

    label_columns = {
        'user_id': 'User ID',
        'name': 'Name',
        'email': 'Email',
        'phone': 'Phone',
        'dining_balance': 'Dining Balance',
    }


class TicketModelView(ModelView):
    datamodel = SQLAInterface(models.Ticket)
    route_base = '/ticket'
    list_title = 'Support Tickets'

    list_columns = ['ticket_id', 'user.name', 'message', 'created_at']

    label_columns = {
        'ticket_id': 'Ticket ID',
        'user.name': 'User',
        'message': 'Message',
        'created_at': 'Created At',
    }

    add_exclude_columns = ['created_at']
    edit_exclude_columns = ['created_at']


# ---------------------------------------------------------------
# Query / View-Only Models
# ---------------------------------------------------------------

class MenuTodayModelView(ModelView):
    datamodel = SQLAInterface(models.VMenuToday)
    list_title = "Today's Menu"

    list_columns = [
        'hall_name',
        'date',
        'meal_type',
        'item_name',
        'description',
        'duke_deal',
    ]

    base_permissions = ['can_list']

    label_columns = {
        'hall_name': 'Hall Name',
        'date': 'Date',
        'meal_type': 'Meal Type',
        'item_name': 'Item Name',
        'description': 'Description',
        'duke_deal': 'Duke Deal',
    }


class DukeDealsTodayModelView(ModelView):
    datamodel = SQLAInterface(models.VDukeDealsToday)
    list_title = "Today's Duke Deals"

    list_columns = [
        'hall_name',
        'date',
        'meal_type',
        'item_name',
        'description',
    ]

    base_permissions = ['can_list']

    label_columns = {
        'hall_name': 'Hall Name',
        'date': 'Date',
        'meal_type': 'Meal Type',
        'item_name': 'Item Name',
        'description': 'Description',
    }


class LocationOpenNowModelView(ModelView):
    datamodel = SQLAInterface(models.VLocationOpenNow)
    list_title = "Locations Open Now"

    list_columns = ['hall_name', 'is_open_now']

    base_permissions = ['can_list']

    label_columns = {
        'hall_name': 'Hall Name',
        'is_open_now': 'Is Open Now',
    }


class LocationCapacityLatestModelView(ModelView):
    datamodel = SQLAInterface(models.VLocationCapacityLatest)
    list_title = "Latest Capacity by Location"

    list_columns = [
        'hall_name',
        'timestamp',
        'current_capacity',
        'capacity_limit',
        'capacity_pct',
    ]

    base_permissions = ['can_list']

    label_columns = {
        'hall_name': 'Hall Name',
        'timestamp': 'Timestamp',
        'current_capacity': 'Current Capacity',
        'capacity_limit': 'Capacity Limit',
        'capacity_pct': 'Capacity %',
    }