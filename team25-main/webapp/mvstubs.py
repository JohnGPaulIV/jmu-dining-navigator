"""Generate a basic ModelView class for each table in the database."""

import psycopg
import os

# try:
#     socket.gethostbyname("data.cs.jmu.edu")
#     HOST = "data.cs.jmu.edu"
# except socket.gaierror:
#     HOST = "localhost"

HOST = os.environ.get("HUNGRY_HOST")
PASSWORD = os.environ.get("HUNGRY_PASSWORD")
TEAM = os.environ.get("HUNGRY_TEAM")


# Get all tables and their columns
with psycopg.connect(host=HOST, user=TEAM, dbname=TEAM, password=PASSWORD) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name NOT LIKE 'ab_%'
            ORDER BY table_name, ordinal_position;
        """)
        schema = cur.fetchall()

# Build a dictionary of results by table
tables: dict[str, list[str]] = {}
for table_name, column_name in schema:
    tables.setdefault(table_name, []).append(column_name)

# Generate Flask-AppBuilder ModelView classes
for table, columns in tables.items():
    name = table.capitalize()
    print(f"class {name}ModelView(ModelView):")
    print(f"    datamodel = SQLAInterface(models.{name})")
    print(f"    route_base = '/{table}'")
    print(f"    list_title = '{name}s'")
    print(f"    list_columns = {columns}")
    print()

# Generate code to add each view to the app
for table in tables:
    name = table.capitalize()
    print('appbuilder.add_view(')
    print(f'    {name}ModelView,')
    print(f'    "{name}s",')
    print('    icon="fa-database",')
    print('    category="Admin",')
    print(')')
    print()