"""SQLAlchemy model classes for the dining management system."""

import datetime
from typing import Optional

from flask_appbuilder import Model
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Double,
    Enum,
    ForeignKeyConstraint,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    Table,
    Text,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


# ---------------------------------------------------------------
# Association Tables
# ---------------------------------------------------------------

# Track users' favorite menu items
t_user_favorite_item = Table(
    "user_favorite_item",
    Model.metadata,
    Column("user_id", Integer, primary_key=True),
    Column("menu_item_id", Integer, primary_key=True),
    ForeignKeyConstraint(["user_id"], ["user.user_id"], name="user_favorite_item_user_id_fkey"),
    ForeignKeyConstraint(
        ["menu_item_id"],
        ["menu_item.menu_item_id"],
        name="user_favorite_item_menu_item_id_fkey",
    ),
    PrimaryKeyConstraint("user_id", "menu_item_id", name="user_favorite_item_pkey"),
    comment="User favorited menu items",
)

t_menu_item_ingredient = Table(
    "menu_item_ingredient",
    Model.metadata,
    Column("menu_item_id", Integer, primary_key=True),
    Column("ingredient_id", Integer, primary_key=True),
    ForeignKeyConstraint(
        ["ingredient_id"],
        ["ingredient.ingredient_id"],
        name="menu_item_ingredient_ingredient_id_fkey",
    ),
    ForeignKeyConstraint(
        ["menu_item_id"],
        ["menu_item.menu_item_id"],
        name="menu_item_ingredient_menu_item_id_fkey",
    ),
    PrimaryKeyConstraint("menu_item_id", "ingredient_id", name="menu_item_ingredient_pkey"),
)

t_user_dietary_restriction = Table(
    "user_dietary_restriction",
    Model.metadata,
    Column("user_id", Integer, primary_key=True),
    Column("dietary_restriction_id", Integer, primary_key=True),
    ForeignKeyConstraint(
        ["dietary_restriction_id"],
        ["dietary_restriction.dietary_restriction_id"],
        name="user_dietary_restriction_dietary_restriction_id_fkey",
    ),
    ForeignKeyConstraint(
        ["user_id"], ["user.user_id"], name="user_dietary_restriction_user_id_fkey"
    ),
    PrimaryKeyConstraint("user_id", "dietary_restriction_id", name="user_dietary_restriction_pkey"),
    comment="Maps users to their dietary restrictions",
)

t_user_meal_plan = Table(
    "user_meal_plan",
    Model.metadata,
    Column("user_id", Integer, primary_key=True),
    Column("plan_id", Integer, primary_key=True),
    ForeignKeyConstraint(["plan_id"], ["meal_plan.plan_id"], name="user_meal_plan_plan_id_fkey"),
    ForeignKeyConstraint(["user_id"], ["user.user_id"], name="user_meal_plan_user_id_fkey"),
    PrimaryKeyConstraint("user_id", "plan_id", name="user_meal_plan_pkey"),
    comment="Associates users with their meal plans",
)

t_menu = Table(
    "menu",
    Model.metadata,
    Column("location_id", Integer),
    Column("menu_item_id", Integer),
    Column("date", Date),
    Column(
        "meal_type",
        Enum(
            "Morning Snack",
            "Snack",
            "Break",
            "Breakfast",
            "Brunch",
            "Lunch",
            "Afternoon Snack",
            "ASSP (After School Snack Program)",
            "Limited Dinner",
            "Dinner",
            "Evening Snack",
            "Overnight",
            "All Day",
            name="meal_type",
        ),
    ),
    ForeignKeyConstraint(["location_id"], ["location.location_id"], name="menu_location_id_fkey"),
    ForeignKeyConstraint(
        ["menu_item_id"], ["menu_item.menu_item_id"], name="menu_menu_item_id_fkey"
    ),
    PrimaryKeyConstraint("location_id", "menu_item_id", "date", "meal_type", name="menu_pkey"),
    comment="Associates menu items with dining halls and their availability",
)


# ---------------------------------------------------------------
# Core Models
# ---------------------------------------------------------------


class WebLog(Model):
    __tablename__ = "web_log"
    __table_args__ = (
        ForeignKeyConstraint(["location_id"], ["location.location_id"], name="web_log_location_id_fkey"),
        PrimaryKeyConstraint("location_id", "timestamp", name="web_log_pkey"),
    )

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    current_capacity: Mapped[Optional[int]] = mapped_column(Integer)

    location: Mapped["Location"] = relationship("Location", back_populates="web_logs")

    def __repr__(self) -> str:
        return f"WebLog(location_id={self.location_id}, timestamp={self.timestamp})"


class LocationHours(Model):
    __tablename__ = "location_hours"
    __table_args__ = (
        ForeignKeyConstraint(
            ["location_id"], ["location.location_id"], name="location_hours_location_id_fkey"
        ),
        PrimaryKeyConstraint("location_id", "day", name="location_hours_pkey"),
    )

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    open_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    close_time: Mapped[Optional[datetime.time]] = mapped_column(Time)

    location: Mapped["Location"] = relationship("Location", back_populates="location_hours")

    def __repr__(self) -> str:
        return f"LocationHours(location_id={self.location_id}, day={self.day})"


class Schedule(Model):
    __tablename__ = "schedule"
    __table_args__ = (
        ForeignKeyConstraint(
            ["location_id"], ["location.location_id"], name="schedule_location_id_fkey"
        ),
        PrimaryKeyConstraint("location_id", "date", "meal_type", name="schedule_pkey"),
    )

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    meal_type: Mapped[str] = mapped_column(
        Enum(
            "Morning Snack",
            "Snack",
            "Break",
            "Breakfast",
            "Brunch",
            "Lunch",
            "Afternoon Snack",
            "ASSP (After School Snack Program)",
            "Limited Dinner",
            "Dinner",
            "Evening Snack",
            "Overnight",
            "All Day",
            name="meal_type",
        ),
        primary_key=True,
    )
    beg_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    location: Mapped["Location"] = relationship("Location", back_populates="schedules")

    def __repr__(self) -> str:
        return f"Schedule(location_id={self.location_id}, date={self.date}, meal_type={self.meal_type})"


class Location(Model):
    __tablename__ = "location"
    __table_args__ = (
        PrimaryKeyConstraint("location_id", name="location_pkey"),
        {"comment": "Contains dining hall details such as name, location, and capacity"},
    )

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hall_name: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    directions: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    capacity_limit: Mapped[Optional[int]] = mapped_column(Integer)

    location_hours: Mapped[list["LocationHours"]] = relationship(
        "LocationHours", back_populates="location"
    )
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="location")
    web_logs: Mapped[list["WebLog"]] = relationship("WebLog", back_populates="location")
    managers: Mapped[list["LocationManager"]] = relationship(
        "LocationManager", back_populates="location"
    )
    payment_methods: Mapped[list["LocationPaymentMethod"]] = relationship(
        "LocationPaymentMethod", back_populates="location"
    )

    def __repr__(self) -> str:
        return f"{self.hall_name or 'Unnamed Location'}"


class LocationManager(Model):
    __tablename__ = "location_managers"
    __table_args__ = (
        ForeignKeyConstraint(
            ["location_id"],
            ["location.location_id"],
            name="location_managers_location_id_fkey",
        ),
        PrimaryKeyConstraint("manager_id", name="location_managers_pkey"),
    )

    manager_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_id: Mapped[int] = mapped_column(Integer)
    first_name: Mapped[Optional[str]] = mapped_column(Text)
    last_name: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(Text)

    location: Mapped["Location"] = relationship("Location", back_populates="managers")

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} (Location {self.location_id})"


class LocationPaymentMethod(Model):
    __tablename__ = "location_payment_methods"
    __table_args__ = (
        ForeignKeyConstraint(
            ["location_id"],
            ["location.location_id"],
            name="location_payment_methods_location_id_fkey",
        ),
        PrimaryKeyConstraint("location_id", "payment_type", name="location_payment_methods_pkey"),
    )

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_type: Mapped[str] = mapped_column(
        Enum(
            "card",
            "cash",
            "dining dollars",
            "flex",
            "swipe",
            "duke deal",
            "dining dollars gold",
            "panera gift card",
            name="payment_method",
        ),
        primary_key=True,
    )

    location: Mapped["Location"] = relationship("Location", back_populates="payment_methods")

    def __repr__(self) -> str:
        return f"{self.payment_type}"


class Ingredient(Model):
    __tablename__ = "ingredient"
    __table_args__ = (
        PrimaryKeyConstraint("ingredient_id", name="ingredient_pkey"),
    )

    ingredient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient_name: Mapped[Optional[str]] = mapped_column(Text)

    menu_items: Mapped[list["MenuItem"]] = relationship(
        "MenuItem",
        secondary="menu_item_ingredient",
        back_populates="ingredients",
    )

    def __repr__(self) -> str:
        return f"{self.ingredient_name or 'Unnamed Ingredient'}"


class MenuItem(Model):
    __tablename__ = "menu_item"
    __table_args__ = (
        PrimaryKeyConstraint("menu_item_id", name="menu_item_pkey"),
        {"comment": "Stores menu items available across dining halls"},
    )

    menu_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    duke_deal: Mapped[Optional[bool]] = mapped_column(Boolean)

    favorited_by: Mapped[list["DiningUser"]] = relationship(
        "DiningUser",
        secondary="user_favorite_item",
        back_populates="favorite_items",
    )
    ingredients: Mapped[list["Ingredient"]] = relationship(
        "Ingredient",
        secondary="menu_item_ingredient",
        back_populates="menu_items",
    )

    def __repr__(self) -> str:
        return f"{self.item_name or 'Unnamed Item'}"


class DietaryRestriction(Model):
    __tablename__ = "dietary_restriction"
    __table_args__ = (
        PrimaryKeyConstraint("dietary_restriction_id", name="dietary_restriction_pkey"),
        {"comment": "Defines dietary restrictions such as vegetarian, vegan, gluten-free"},
    )

    dietary_restriction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)

    users: Mapped[list["DiningUser"]] = relationship(
        "DiningUser",
        secondary="user_dietary_restriction",
        back_populates="dietary_restrictions",
    )

    def __repr__(self) -> str:
        return f"{self.name or 'Unnamed Restriction'}"


class MealPlan(Model):
    __tablename__ = "meal_plan"
    __table_args__ = (
        PrimaryKeyConstraint("plan_id", name="meal_plan_pkey"),
        {"comment": "Describes a meal plan’s attributes such as swipe allowance"},
    )

    plan_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    swipes: Mapped[Optional[int]] = mapped_column(Integer)
    meal_plan: Mapped[Optional[str]] = mapped_column(Text)

    users: Mapped[list["DiningUser"]] = relationship(
        "DiningUser",
        secondary="user_meal_plan",
        back_populates="meal_plans",
    )

    def __repr__(self) -> str:
        return f"{self.meal_plan or 'Unnamed Plan'}"


class DiningUser(Model):
    __tablename__ = "user"

    # Primary key is a foreign key to FAB's ab_user.id
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ab_user.id"),
        primary_key=True,
    )

    # Relationship to FAB User
    fab_user: Mapped[User] = relationship("User", backref="dining_user", uselist=False)

    name: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(Text)
    dining_balance: Mapped[Optional[float]] = mapped_column(Double(53))

    dietary_restrictions: Mapped[list["DietaryRestriction"]] = relationship(
        "DietaryRestriction",
        secondary="user_dietary_restriction",
        back_populates="users",
    )
    meal_plans: Mapped[list["MealPlan"]] = relationship(
        "MealPlan",
        secondary="user_meal_plan",
        back_populates="users",
    )
    favorite_items: Mapped[list["MenuItem"]] = relationship(
        "MenuItem",
        secondary="user_favorite_item",
        back_populates="favorited_by",
    )

    def __repr__(self) -> str:
        return f"{self.name or 'Unnamed User'} ({self.email or 'no email'})"


class Ticket(Model):
    __tablename__ = "ticket"

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.user_id"))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )

    user: Mapped["DiningUser"] = relationship("DiningUser")

    def __repr__(self) -> str:
        return f"Ticket({self.ticket_id} - {self.user.name})"


# ---------------------------------------------------------------
# View Models (read-only)
# ---------------------------------------------------------------


class VMenuToday(Model):
    __tablename__ = "v_menu_today"

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    meal_type: Mapped[str] = mapped_column(
        Enum(
            "Morning Snack",
            "Snack",
            "Break",
            "Breakfast",
            "Brunch",
            "Lunch",
            "Afternoon Snack",
            "ASSP (After School Snack Program)",
            "Limited Dinner",
            "Dinner",
            "Evening Snack",
            "Overnight",
            "All Day",
            name="meal_type",
        ),
        primary_key=True,
    )

    hall_name: Mapped[Optional[str]] = mapped_column(Text)
    item_name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    duke_deal: Mapped[Optional[bool]] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"{self.hall_name} - {self.meal_type} - {self.item_name}"


class VDukeDealsToday(Model):
    __tablename__ = "v_duke_deals_today"

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    meal_type: Mapped[str] = mapped_column(
        Enum(
            "Morning Snack",
            "Snack",
            "Break",
            "Breakfast",
            "Brunch",
            "Lunch",
            "Afternoon Snack",
            "ASSP (After School Snack Program)",
            "Limited Dinner",
            "Dinner",
            "Evening Snack",
            "Overnight",
            "All Day",
            name="meal_type",
        ),
        primary_key=True,
    )

    hall_name: Mapped[Optional[str]] = mapped_column(Text)
    item_name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    duke_deal: Mapped[Optional[bool]] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return (
            f"{self.hall_name} - {self.meal_type} - "
            f"{self.item_name} (Duke Deal)"
        )


class VLocationOpenNow(Model):
    __tablename__ = "v_location_open_now"

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hall_name: Mapped[Optional[str]] = mapped_column(Text)
    is_open_now: Mapped[Optional[bool]] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"{self.hall_name} ({'Open' if self.is_open_now else 'Closed'})"


class VLocationCapacityLatest(Model):
    __tablename__ = "v_location_capacity_latest"

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hall_name: Mapped[Optional[str]] = mapped_column(Text)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)
    current_capacity: Mapped[Optional[int]] = mapped_column(Integer)
    capacity_limit: Mapped[Optional[int]] = mapped_column(Integer)
    capacity_pct: Mapped[Optional[float]] = mapped_column(Double)

    def __repr__(self) -> str:
        return f"{self.hall_name} - {self.capacity_pct}% full"


# TODO: Add model class for v_location_hours_today if/when you create that view
