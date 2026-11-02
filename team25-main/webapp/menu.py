"""Flask-AppBuilder views that provide CRUD web interfaces for the models."""

# See https://fontawesome.com/icons for icon names.

def setup_menu(appbuilder):

    import base
    import views
    from forms import HelpFormView, DietaryPreferencesView

    # Global Home link in the navbar
    appbuilder.add_link(
        "Home",
        href="/",
        icon="fa-home",
        category="",
    )

    appbuilder.add_view_no_menu(base.AboutView())
    appbuilder.add_view_no_menu(base.PlaceView())
    appbuilder.add_view_no_menu(HelpFormView())
    appbuilder.add_view_no_menu(base.MapView())
    appbuilder.add_view_no_menu(base.GraphView())
    appbuilder.add_view_no_menu(base.popPage())



    # --------------------------------------------------------------------------
    # Tables Menu (in an order that makes sense for the GUI)
    # --------------------------------------------------------------------------

    appbuilder.add_view(
        views.Dietary_restrictionModelView,
        "Dietary Restrictions",
        icon="fa-database",
        category="Tables",
    )

    appbuilder.add_view(
        views.IngredientModelView,
        "Ingredients",
        icon="fa-database",
        category="Tables",
    )

    appbuilder.add_view(
        views.LocationModelView,
        "Locations",
        icon="fa-database",
        category="Tables",
    )

    appbuilder.add_view(
        views.Location_hoursModelView,
        "Location Hours",
        icon="fa-database",
        category="Tables",
    )

    appbuilder.add_view(
        views.Meal_planModelView,
        "Meal Plans",
        icon="fa-database",
        category="Tables",
    )

    appbuilder.add_view(
        views.Menu_itemModelView,
        "Menu Items",
        icon="fa-database",
        category="Tables",
    )

    appbuilder.add_view(
        views.ScheduleModelView,
        "Schedules",
        icon="fa-database",
        category="Tables",
    )

    appbuilder.add_view(
        views.DiningUserModelView,
        "Users",
        icon="fa-database",
        category="Tables",
    )

    appbuilder.add_view(
        views.TicketModelView,
        "Support Tickets",
        icon="fa-ticket",
        category="Tables",
    )

    appbuilder.add_view(
        views.Web_logModelView,
        "Web Logs",
        icon="fa-database",
        category="Tables",
    )

    # --------------------------------------------------------------------------
    # Views Menu (in an order that makes sense for the GUI)
    # --------------------------------------------------------------------------

    appbuilder.add_view(
        views.MenuTodayModelView,
        "Today's Menu",
        icon="fa-eye",
        category="Views",
    )

    appbuilder.add_view(
        views.DukeDealsTodayModelView,
        "Today's Duke Deals",
        icon="fa-eye",
        category="Views",
    )

    appbuilder.add_view(
        views.LocationOpenNowModelView,
        "Locations Open Now",
        icon="fa-eye",
        category="Views",
    )

    appbuilder.add_view(
        views.LocationCapacityLatestModelView,
        "Latest Capacity",
        icon="fa-eye",
        category="Views",
    )

    # TODO Add v_location_hours_today to appbuilder

    # --------------------------------------------------------------------------
    # Chart Menu - TODO replace with your own
    # --------------------------------------------------------------------------

    # appbuilder.add_view(
    #     charts.Workshop_Department_Chart,
    #     "Workshop Leaders",
    #     icon="fa-chart-simple",
    #     category="Charts",
    #     category_icon="fa-chart-simple",
    # )

    # appbuilder.add_view(
    #     charts.Volunteer_College_Chart,
    #     "Volunteers by College",
    #     icon="fa-chart-simple",
    #     category="Charts",
    # )

    # --------------------------------------------------------------------------
    # Form Views
    # --------------------------------------------------------------------------


    appbuilder.add_view(
        DietaryPreferencesView,
        "Update Dietary Preferences",
        icon="fa-utensils",
        category="Forms",
        category_icon="fa-table-list",
    )

    # appbuilder.add_view(
    #     forms.ReturningProposerFormView,
    #     "Propose Workshop",
    #     icon="fa-table-list",
    #     label="Propose Workshop (returning faculty)",
    #     category="Forms",
    #     category_icon="fa-table-list",
    # )

    # appbuilder.add_view(
    #    forms.NewProposerFormView,
    #    "Propose Workshop",
    #    icon="fa-table-list",
    #    label='Propose Workshop (new faculty)',
    #    category="Forms",
    #    category_icon="fa-table-list")
