"""
Seed Data Script — Populates the database with realistic sample data.

Run this once after setting up the project:
    python seed_data.py

This creates sample users, clients, and tasks so the application
has meaningful data to display from the start. All passwords are
hashed using Werkzeug's security functions — never stored in plain text.

The seed data reflects MJ Limited's department structure from the fact file.
"""

from werkzeug.security import generate_password_hash
from database import get_db, init_db


def seed():
    """Insert sample data into all tables."""

    # Ensure tables exist
    init_db()

    conn = get_db()
    cursor = conn.cursor()

    # Check if data already exists (don't duplicate on re-run)
    existing = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        print("Database already contains data. Skipping seed.")
        conn.close()
        return

    # --- Users ---
    # Passwords are hashed — the plain text is shown here only for reference
    # In production, users would set their own passwords
    users = [
        # Admin users (IT & Management)
        ("admin", generate_password_hash("admin123"), "Sarah Mitchell",
         "s.mitchell@mjlimited.co.uk", "admin", "Management & Strategy"),
        # Manager users
        ("m.jones", generate_password_hash("manager123"), "Michael Jones",
         "m.jones@mjlimited.co.uk", "manager", "Client Services"),
        ("l.chen", generate_password_hash("manager123"), "Lisa Chen",
         "l.chen@mjlimited.co.uk", "manager", "Finance"),
        ("r.patel", generate_password_hash("manager123"), "Raj Patel",
         "r.patel@mjlimited.co.uk", "manager", "Administration"),
        # Staff users
        ("j.smith", generate_password_hash("staff123"), "James Smith",
         "j.smith@mjlimited.co.uk", "staff", "Client Services"),
        ("e.williams", generate_password_hash("staff123"), "Emma Williams",
         "e.williams@mjlimited.co.uk", "staff", "Finance"),
        ("d.brown", generate_password_hash("staff123"), "David Brown",
         "d.brown@mjlimited.co.uk", "staff", "Administration"),
        ("a.taylor", generate_password_hash("staff123"), "Amy Taylor",
         "a.taylor@mjlimited.co.uk", "staff", "HR"),
    ]

    cursor.executemany(
        "INSERT INTO users (username, password_hash, full_name, email, role, department) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        users,
    )

    # --- Clients ---
    clients = [
        ("Westfield Accountants", "John Westfield", "john@westfieldacc.co.uk",
         "0121 456 7890", "Accounting", "active",
         "Long-standing client since 2020. Monthly financial reporting required."),
        ("GreenLeaf Marketing", "Sophie Green", "sophie@greenleaf.co.uk",
         "0121 234 5678", "Marketing", "active",
         "New client. Requires admin support and client coordination."),
        ("BridgePoint Legal", "Mark Bridge", "mark@bridgepointlegal.co.uk",
         "0121 987 6543", "Legal", "active",
         "Requires document management and compliance tracking."),
        ("TechForward Solutions", "Priya Sharma", "priya@techforward.co.uk",
         "0121 111 2222", "Technology", "active",
         "IT consultancy client. Complex project tracking needs."),
        ("Midlands Property Group", "Tom Harris", "tom@midlandsproperty.co.uk",
         "0121 333 4444", "Real Estate", "inactive",
         "Contract paused — to be reviewed Q2 2026."),
    ]

    cursor.executemany(
        "INSERT INTO clients (company_name, contact_name, contact_email, "
        "contact_phone, industry, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        clients,
    )

    # --- Tasks ---
    tasks = [
        ("Prepare monthly financial report", "Compile and verify the monthly financial "
         "report for Westfield Accountants including P&L and balance sheet.",
         "in_progress", "high", "Finance", 6, 1, "2026-02-14", 3),
        ("Update client contact database", "Review and update all client contact "
         "information to ensure records are current and accurate.",
         "open", "medium", "Administration", 7, None, "2026-02-21", 4),
        ("Schedule quarterly review meetings", "Arrange Q1 review meetings with all "
         "active clients. Send calendar invites and prepare agendas.",
         "open", "medium", "Client Services", 5, None, "2026-02-28", 2),
        ("Onboard new starter — Marketing Dept", "Complete onboarding checklist for "
         "new marketing coordinator. Set up accounts, arrange induction.",
         "in_progress", "high", "HR", 8, None, "2026-02-10", 1),
        ("Process GreenLeaf invoices", "Process outstanding invoices for GreenLeaf "
         "Marketing for January services.",
         "open", "urgent", "Finance", 6, 2, "2026-02-07", 3),
        ("Prepare compliance documentation", "Gather and organise compliance documents "
         "for BridgePoint Legal's annual review.",
         "open", "high", "Client Services", 5, 3, "2026-02-18", 2),
        ("IT equipment audit", "Conduct inventory check of all IT equipment across "
         "departments. Record serial numbers and conditions.",
         "completed", "low", "Administration", 7, None, "2026-01-31", 1),
        ("Draft staff training plan", "Create a training needs analysis and development "
         "plan for Q1-Q2 2026 across all departments.",
         "open", "medium", "HR", 8, None, "2026-03-01", 1),
        ("TechForward project status update", "Compile progress report on all active "
         "workstreams for TechForward Solutions.",
         "in_progress", "high", "Client Services", 2, 4, "2026-02-12", 2),
        ("Archive inactive client files", "Move Midlands Property Group files to "
         "archive storage following contract pause.",
         "open", "low", "Administration", 7, 5, "2026-03-15", 4),
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, description, status, priority, department, "
        "assigned_to, client_id, due_date, created_by) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        tasks,
    )

    conn.commit()
    conn.close()
    print("✅ Database seeded successfully with sample data.")
    print("   Users: 8 (1 admin, 3 managers, 4 staff)")
    print("   Clients: 5 (4 active, 1 inactive)")
    print("   Tasks: 10 (various statuses and priorities)")
    print()
    print("   Login credentials:")
    print("   Admin:   admin / admin123")
    print("   Manager: m.jones / manager123")
    print("   Staff:   j.smith / staff123")


if __name__ == "__main__":
    seed()
