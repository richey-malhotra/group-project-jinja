"""
Database module — SQLite connection and initialisation.

Why SQLite?
- Zero setup: ships with Python, no server to install
- File-based: the entire database is a single file (mj_limited.db)
- Perfect for prototypes and small-to-medium applications
- SQL skills transfer directly to PostgreSQL/MySQL in production

This module provides helper functions to get a database connection
and to initialise the schema (create tables if they don't exist).
"""

import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "mj_limited.db")


def get_db():
    """Get a database connection with Row factory enabled.

    Row factory lets us access columns by name (row['title'])
    instead of by index (row[0]) — much more readable.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign key enforcement (off by default in SQLite)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't already exist.

    This is safe to call on every app startup — IF NOT EXISTS
    means it won't destroy existing data.
    """
    conn = get_db()
    cursor = conn.cursor()

    # --- Users table ---
    # Stores all staff accounts with hashed passwords and role-based access
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'staff')),
            department TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --- Clients table ---
    # Tracks MJ Limited's external clients (SMEs they provide services to)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            contact_email TEXT NOT NULL,
            contact_phone TEXT,
            industry TEXT,
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --- Tasks table ---
    # Central work tracking — replaces the spreadsheets and email chains
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'in_progress', 'completed', 'cancelled')),
            priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
            department TEXT NOT NULL,
            assigned_to INTEGER,
            client_id INTEGER,
            due_date TEXT,
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES users(id),
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)

    # --- Attachments table ---
    # File uploads linked to tasks — replaces emailing documents around
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            uploaded_by INTEGER NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (uploaded_by) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
