APP_TITLE = "Smart Water Issue Monitoring and Management System"
# MySQL connection settings (override with environment variables)
import os
DB_HOST = os.getenv("SMART_WATER_DB_HOST", "localhost")
DB_PORT = int(os.getenv("SMART_WATER_DB_PORT", "3306"))
DB_USER = os.getenv("SMART_WATER_DB_USER", "root")
DB_PASSWORD = os.getenv("SMART_WATER_DB_PASSWORD", "")
DB_NAME = os.getenv("SMART_WATER_DB_NAME", "smart_water")

COLORS = {
    "navy": "#12355B",
    "blue": "#1976D2",
    "light_blue": "#EAF4FF",
    "green": "#2E8B57",
    "yellow": "#F4B400",
    "red": "#D64545",
    "purple": "#6A5ACD",
    "dark": "#263238",
    "light": "#F5F7FA",
    "white": "#FFFFFF",
    "gray": "#607D8B"
}

BUILDINGS = [
    "Academic Block",
    "Boys' Hostel",
    "Girls' Hostel",
    "Library",
    "Administration Block",
    "Science Block"
]

ISSUE_TYPES = [
    "No Water",
    "Low Pressure",
    "Leakage",
    "Dirty Water",
    "Other"
]

PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Pending", "In Progress", "Resolved"]
ROLES = ["Student", "Maintenance", "Admin"]
MAINTENANCE_STATUSES = ["Planned", "Completed", "Cancelled"]
