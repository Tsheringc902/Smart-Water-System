SMART WATER COMPONENT-WISE PROJECT
===================================

Database: MySQL 8.0+

Setup:
1. Start a MySQL server and note its host, port, user and password.
2. Set the connection details (defaults: localhost, port 3306, user root,
   empty password, database smart_water):
       SMART_WATER_DB_HOST, SMART_WATER_DB_PORT, SMART_WATER_DB_USER,
       SMART_WATER_DB_PASSWORD, SMART_WATER_DB_NAME
   Or edit the DB_* values in config.py.
3. Optional: load database/schema.sql to create tables by hand. The app
   also creates the database, tables, buildings and demo data itself.
4. Install requirements:  pip install -r requirements.txt
5. Put all Python files in the same folder, open the terminal there, run:
       python main.py

Demo login accounts:
Student:
    username: student
    password: Student123

Maintenance:
    username: maintenance
    password: Maintenance123

Admin:
    username: admin
    password: Admin123

Optional Excel export:
    pip install openpyxl

Components:
- main.py: Starts the application and connects modules.
- config.py: Shared constants, colours, buildings and issue types.
- database.py: MySQL tables and database operations.
- login.py: Login screen.
- dashboard.py: Dashboard and building status.
- complaints.py: Complaint form, details, tracking and admin management.
- maintenance.py: Maintenance schedule CRUD.
- analytics.py: Statistics and building status.
- exports.py: CSV and Excel export.
- ui_helpers.py: Shared buttons, cards and tables.

Important:
- The application is a local desktop prototype.
- Building status is based on unresolved complaints, not real sensors.
- The database and tables are created automatically on first run.
- Do not drop the database if you need to keep your records.

Documentation (docs/): use_case_diagram.png and erd_diagram.png.
Schema: database/schema.sql.
