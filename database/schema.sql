-- =====================================================================
-- Smart Water Issue Monitoring and Management System
-- MySQL 8.0+ schema (converted from the SQLite version in database.py)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS smart_water
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE smart_water;

-- Drop in dependency order so the script can be re-run
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS maintenance;
DROP TABLE IF EXISTS buildings;
DROP TABLE IF EXISTS users;

-- ---------------------------------------------------------------------
-- users: login accounts for Students, Maintenance officers and Admins
-- ---------------------------------------------------------------------
CREATE TABLE users (
    id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username      VARCHAR(50)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,          -- salt$pbkdf2_hash
    full_name     VARCHAR(100) NOT NULL,
    role          ENUM('Student', 'Maintenance', 'Admin') NOT NULL,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- buildings: campus buildings (normalised from config.BUILDINGS)
-- ---------------------------------------------------------------------
CREATE TABLE buildings (
    id   INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_buildings_name (name)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- complaints: water issues reported by users
-- ---------------------------------------------------------------------
CREATE TABLE complaints (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id     INT UNSIGNED NOT NULL,
    building_id INT UNSIGNED NOT NULL,
    issue_type  ENUM('No Water', 'Low Pressure', 'Leakage', 'Dirty Water', 'Other')
                NOT NULL,
    priority    ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL,
    description TEXT         NOT NULL,
    photo_path  VARCHAR(255) NULL,
    status      ENUM('Pending', 'In Progress', 'Resolved')
                NOT NULL DEFAULT 'Pending',
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                             ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_complaints_status (status),
    KEY idx_complaints_building (building_id),
    KEY idx_complaints_user (user_id),
    CONSTRAINT fk_complaints_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_complaints_building
        FOREIGN KEY (building_id) REFERENCES buildings (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- maintenance: scheduled maintenance work per building
-- ---------------------------------------------------------------------
CREATE TABLE maintenance (
    id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
    title            VARCHAR(150) NOT NULL,
    building_id      INT UNSIGNED NOT NULL,
    maintenance_date DATE         NOT NULL,
    status           ENUM('Planned', 'Completed', 'Cancelled')
                     NOT NULL DEFAULT 'Planned',
    PRIMARY KEY (id),
    KEY idx_maintenance_date (maintenance_date),
    KEY idx_maintenance_building (building_id),
    CONSTRAINT fk_maintenance_building
        FOREIGN KEY (building_id) REFERENCES buildings (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Seed data
-- ---------------------------------------------------------------------
INSERT INTO buildings (name) VALUES
    ('Academic Block'),
    ('Boys'' Hostel'),
    ('Girls'' Hostel'),
    ('Library'),
    ('Administration Block'),
    ('Science Block');

INSERT INTO maintenance (title, building_id, maintenance_date, status) VALUES
    ('Water tank inspection', 1, '2026-10-05', 'Planned'),
    ('Pipe checking',         2, '2026-10-08', 'Planned'),
    ('Tank cleaning',         3, '2026-10-12', 'Planned');

-- ---------------------------------------------------------------------
-- Useful views (replace the building-status logic in database.py)
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW v_complaint_details AS
SELECT c.id, c.created_at, c.updated_at, c.issue_type, c.priority,
       c.status, c.description, c.photo_path,
       b.name AS building, u.username, u.full_name
FROM complaints c
JOIN users     u ON u.id = c.user_id
JOIN buildings b ON b.id = c.building_id;

CREATE OR REPLACE VIEW v_building_status AS
SELECT b.name AS building,
       CASE
           WHEN SUM(c.priority = 'Critical') > 0 THEN 'No Water / Critical'
           WHEN SUM(c.issue_type IN ('No Water', 'Leakage')) > 0
                THEN 'Low Supply / Issue'
           WHEN COUNT(c.id) > 0 THEN 'Under Review'
           ELSE 'Normal'
       END AS status
FROM buildings b
LEFT JOIN complaints c
       ON c.building_id = b.id AND c.status <> 'Resolved'
GROUP BY b.id, b.name;
