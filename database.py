import hashlib
import secrets
from datetime import datetime

import mysql.connector

from config import (
    BUILDINGS, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, STATUSES
)


def hash_password(password, salt=None):
    """Create a salted PBKDF2 password hash."""
    salt = salt or secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000
    ).hex()
    return f"{salt}${password_hash}"


def verify_password(password, stored_value):
    """Verify a password against salt$hash format."""
    try:
        salt, saved_hash = stored_value.split("$", 1)
        test_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000
        ).hex()
        return secrets.compare_digest(test_hash, saved_hash)
    except ValueError:
        return False


def password_is_strong(password):
    """Require a reasonably strong password."""
    if len(password) < 8:
        return False
    return (
        any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
    )


# Complaint columns returned with building names and formatted timestamps,
# so the rest of the application can use the same row keys as before.
COMPLAINT_SELECT = """
    SELECT c.id, c.user_id, b.name AS building, c.issue_type, c.priority,
           c.description, c.photo_path, c.status,
           DATE_FORMAT(c.created_at, '%Y-%m-%d %H:%i:%s') AS created_at,
           DATE_FORMAT(c.updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at,
           u.full_name, u.username
    FROM complaints c
    JOIN users u     ON u.id = c.user_id
    JOIN buildings b ON b.id = c.building_id
"""

MAINTENANCE_SELECT = """
    SELECT m.id, m.title, b.name AS building,
           DATE_FORMAT(m.maintenance_date, '%Y-%m-%d') AS maintenance_date,
           m.status
    FROM maintenance m
    JOIN buildings b ON b.id = m.building_id
"""

SCHEMA = [
    """CREATE TABLE IF NOT EXISTS users (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        role ENUM('Student','Maintenance','Admin') NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uq_users_username (username)
    ) ENGINE = InnoDB""",
    """CREATE TABLE IF NOT EXISTS buildings (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE KEY uq_buildings_name (name)
    ) ENGINE = InnoDB""",
    """CREATE TABLE IF NOT EXISTS complaints (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        building_id INT UNSIGNED NOT NULL,
        issue_type ENUM('No Water','Low Pressure','Leakage','Dirty Water','Other') NOT NULL,
        priority ENUM('Low','Medium','High','Critical') NOT NULL,
        description TEXT NOT NULL,
        photo_path VARCHAR(255) NULL,
        status ENUM('Pending','In Progress','Resolved') NOT NULL DEFAULT 'Pending',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY idx_complaints_status (status),
        KEY idx_complaints_building (building_id),
        KEY idx_complaints_user (user_id),
        CONSTRAINT fk_complaints_user FOREIGN KEY (user_id)
            REFERENCES users (id) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_complaints_building FOREIGN KEY (building_id)
            REFERENCES buildings (id) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE = InnoDB""",
    """CREATE TABLE IF NOT EXISTS maintenance (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        title VARCHAR(150) NOT NULL,
        building_id INT UNSIGNED NOT NULL,
        maintenance_date DATE NOT NULL,
        status ENUM('Planned','Completed','Cancelled') NOT NULL DEFAULT 'Planned',
        PRIMARY KEY (id),
        KEY idx_maintenance_date (maintenance_date),
        KEY idx_maintenance_building (building_id),
        CONSTRAINT fk_maintenance_building FOREIGN KEY (building_id)
            REFERENCES buildings (id) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE = InnoDB""",
]


class Database:
    def __init__(self):
        self.ensure_database()
        self.connection = mysql.connector.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER,
            password=DB_PASSWORD, database=DB_NAME,
        )
        self.create_tables()
        self.seed_buildings()
        self.create_demo_accounts()
        self.create_demo_maintenance()

    def cursor(self):
        return self.connection.cursor(dictionary=True)

    def ensure_database(self):
        """Create the schema database if it does not exist yet."""
        conn = mysql.connector.connect(
            host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        cur.close()
        conn.close()

    def create_tables(self):
        cur = self.cursor()
        for statement in SCHEMA:
            cur.execute(statement)
        self.connection.commit()
        cur.close()

    def seed_buildings(self):
        cur = self.cursor()
        cur.executemany(
            "INSERT IGNORE INTO buildings (name) VALUES (%s)",
            [(name,) for name in BUILDINGS]
        )
        self.connection.commit()
        cur.close()

    def building_id(self, cur, name):
        cur.execute("SELECT id FROM buildings WHERE name = %s", (name,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Unknown building: {name}")
        return row["id"]

    def create_demo_accounts(self):
        accounts = [
            ("student", "Student123", "Demo Student", "Student"),
            ("maintenance", "Maintenance123", "Maintenance Officer", "Maintenance"),
            ("admin", "Admin123", "System Administrator", "Admin"),
        ]
        cur = self.cursor()
        for username, password, full_name, role in accounts:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cur.fetchone() is None:
                cur.execute(
                    """INSERT INTO users (username, password_hash, full_name, role)
                       VALUES (%s, %s, %s, %s)""",
                    (username, hash_password(password), full_name, role)
                )
        self.connection.commit()
        cur.close()

    def create_demo_maintenance(self):
        cur = self.cursor()
        cur.execute("SELECT COUNT(*) AS total FROM maintenance")
        if cur.fetchone()["total"] == 0:
            records = [
                ("Water tank inspection", "Academic Block", "2026-10-05", "Planned"),
                ("Pipe checking", "Boys' Hostel", "2026-10-08", "Planned"),
                ("Tank cleaning", "Girls' Hostel", "2026-10-12", "Planned"),
            ]
            for title, building, date, status in records:
                cur.execute(
                    """INSERT INTO maintenance
                       (title, building_id, maintenance_date, status)
                       VALUES (%s, %s, %s, %s)""",
                    (title, self.building_id(cur, building), date, status)
                )
            self.connection.commit()
        cur.close()

    # ---------------- users ----------------
    def authenticate(self, username, password, role):
        cur = self.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = %s AND role = %s",
            (username, role)
        )
        user = cur.fetchone()
        cur.close()
        if user and verify_password(password, user["password_hash"]):
            return user
        return None

    def change_password(self, user_id, old_password, new_password):
        cur = self.cursor()
        cur.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()

        if not user or not verify_password(old_password, user["password_hash"]):
            cur.close()
            return False, "Old password is incorrect."

        if not password_is_strong(new_password):
            cur.close()
            return False, (
                "Password must be at least 8 characters and include "
                "uppercase, lowercase, and a number."
            )

        cur.execute(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (hash_password(new_password), user_id)
        )
        self.connection.commit()
        cur.close()
        return True, "Password changed successfully."

    # ---------------- complaints ----------------
    def add_complaint(self, user_id, building, issue_type, priority,
                      description, photo_path=""):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur = self.cursor()
        cur.execute(
            """INSERT INTO complaints
               (user_id, building_id, issue_type, priority, description,
                photo_path, status, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, 'Pending', %s, %s)""",
            (user_id, self.building_id(cur, building), issue_type, priority,
             description, photo_path or None, now, now)
        )
        self.connection.commit()
        complaint_id = cur.lastrowid
        cur.close()
        return complaint_id

    def get_complaint(self, complaint_id):
        cur = self.cursor()
        cur.execute(COMPLAINT_SELECT + " WHERE c.id = %s", (complaint_id,))
        row = cur.fetchone()
        cur.close()
        return row

    def get_user_complaints(self, user_id):
        cur = self.cursor()
        cur.execute(
            COMPLAINT_SELECT + " WHERE c.user_id = %s ORDER BY c.id DESC",
            (user_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_all_complaints(self, search="", status="All"):
        cur = self.cursor()
        value = f"%{search}%"
        query = COMPLAINT_SELECT + """
            WHERE (
                CAST(c.id AS CHAR) LIKE %s
                OR u.full_name LIKE %s
                OR b.name LIKE %s
                OR c.issue_type LIKE %s
                OR c.priority LIKE %s
            )
        """
        params = [value] * 5
        if status != "All":
            query += " AND c.status = %s"
            params.append(status)
        query += " ORDER BY c.id DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        return rows

    def update_complaint_status(self, complaint_id, status):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur = self.cursor()
        cur.execute(
            "UPDATE complaints SET status = %s, updated_at = %s WHERE id = %s",
            (status, now, complaint_id)
        )
        self.connection.commit()
        cur.close()

    def get_summary(self, user_id=None):
        cur = self.cursor()
        condition = ""
        params = []
        if user_id is not None:
            condition = " WHERE user_id = %s"
            params = [user_id]

        cur.execute(
            f"SELECT COUNT(*) AS total FROM complaints{condition}", params
        )
        result = {"Total": cur.fetchone()["total"]}

        for status in STATUSES:
            query = "SELECT COUNT(*) AS total FROM complaints WHERE status = %s"
            status_params = [status]
            if user_id is not None:
                query += " AND user_id = %s"
                status_params.append(user_id)
            cur.execute(query, status_params)
            result[status] = cur.fetchone()["total"]

        query = """SELECT COUNT(DISTINCT building_id) AS total
                   FROM complaints WHERE status != 'Resolved'"""
        status_params = []
        if user_id is not None:
            query += " AND user_id = %s"
            status_params.append(user_id)
        cur.execute(query, status_params)
        result["Affected Buildings"] = cur.fetchone()["total"]

        cur.close()
        return result

    def get_building_counts(self):
        cur = self.cursor()
        cur.execute("""
            SELECT b.name AS building, COUNT(*) AS total
            FROM complaints c JOIN buildings b ON b.id = c.building_id
            GROUP BY b.name
            ORDER BY total DESC
        """)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_issue_counts(self):
        cur = self.cursor()
        cur.execute("""
            SELECT issue_type, COUNT(*) AS total
            FROM complaints
            GROUP BY issue_type
            ORDER BY total DESC
        """)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_building_statuses(self):
        """Calculate building status from unresolved complaints."""
        cur = self.cursor()
        statuses = {}
        for building in BUILDINGS:
            cur.execute("""
                SELECT c.priority, c.issue_type
                FROM complaints c
                JOIN buildings b ON b.id = c.building_id
                WHERE b.name = %s AND c.status != 'Resolved'
            """, (building,))
            rows = cur.fetchall()

            if any(r["priority"] == "Critical" for r in rows):
                status = "No Water / Critical"
            elif any(r["issue_type"] in ("No Water", "Leakage") for r in rows):
                status = "Low Supply / Issue"
            elif rows:
                status = "Under Review"
            else:
                status = "Normal"
            statuses[building] = status
        cur.close()
        return statuses

    # ---------------- maintenance ----------------
    def get_maintenance(self):
        cur = self.cursor()
        cur.execute(MAINTENANCE_SELECT + " ORDER BY m.maintenance_date, m.id")
        rows = cur.fetchall()
        cur.close()
        return rows

    def add_maintenance(self, title, building, date, status):
        cur = self.cursor()
        cur.execute(
            """INSERT INTO maintenance
               (title, building_id, maintenance_date, status)
               VALUES (%s, %s, %s, %s)""",
            (title, self.building_id(cur, building), date, status)
        )
        self.connection.commit()
        cur.close()

    def update_maintenance(self, record_id, title, building, date, status):
        cur = self.cursor()
        cur.execute(
            """UPDATE maintenance
               SET title = %s, building_id = %s, maintenance_date = %s, status = %s
               WHERE id = %s""",
            (title, self.building_id(cur, building), date, status, record_id)
        )
        self.connection.commit()
        cur.close()

    def delete_maintenance(self, record_id):
        cur = self.cursor()
        cur.execute("DELETE FROM maintenance WHERE id = %s", (record_id,))
        self.connection.commit()
        cur.close()

    def close(self):
        self.connection.close()
