"""Configure application settings such as the database URI, secret key, etc."""

import socket

TEAM = "team25"

# Determine whether connecting from on/off campus
try:
    socket.gethostbyname("data.cs.jmu.edu")
    HOST = "data.cs.jmu.edu"
except socket.gaierror:
    HOST = "localhost"


# See https://flask-appbuilder.readthedocs.io/en/latest/config.html

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{TEAM}@{HOST}:5432/{TEAM}"

SECRET_KEY = "3d65d589adf57bfdf51549e5dbeceb5c20f8cd298d4b6cba79b72cd37676f3a7"

AUTH_TYPE = 1  # Database style (user/password)

APP_NAME = "JMU Dining Navigator"

# APP_THEME = "readable.css"

APP_THEME = "flatly.css"
