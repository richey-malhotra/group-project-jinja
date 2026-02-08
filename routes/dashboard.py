"""
Dashboard Routes — Role-aware statistics and chart data.

Unlike the v1 API which had two separate endpoints (/summary and /charts),
the server-rendered version combines everything into one route that passes
all data to the template in a single render_template() call.

RBAC on the dashboard:
    Admin:   sees the ENTIRE organisation — all tasks, all departments
    Manager: sees their OWN DEPARTMENT — tasks and workload scoped to team
    Staff:   sees only THEIR OWN tasks — a personal overview

Why different views per role?
    A staff member has no business seeing the CEO's workload or org-wide
    overdue counts. Managers need their department's picture, not data
    from departments they don't manage. This is the "Principle of Least
    Privilege" — show people only what they need.
"""

from flask import Blueprint, session, render_template
from routes.auth import login_required
from database import get_db

dashboard_bp = Blueprint("dashboard", __name__)


def _role_filter():
    """Build WHERE clause fragments based on the current user's role.

    Returns (where_clause, params) tuple that can be appended to any
    query against the tasks table (aliased as 't').

    Why a helper function?
    - Summary stats and chart data both need the same role-based filter
    - DRY principle: define the logic once, use it everywhere
    - If roles change later, we only update one place
    """
    role = session.get("role")
    user_id = session.get("user_id")
    department = session.get("department")

    if role == "staff":
        return " AND t.assigned_to = ?", [user_id]
    elif role == "manager":
        return " AND t.department = ?", [department]
    else:
        return "", []


@dashboard_bp.route("", methods=["GET"])
@login_required
def dashboard():
    """Render the dashboard with summary stats and chart data.

    Everything is computed server-side and passed to the template.
    Chart.js receives its data via {{ chart_data | tojson }} in a
    <script> block — this is the standard Flask pattern for passing
    Python data to JavaScript.
    """
    conn = get_db()
    role = session.get("role")
    where, params = _role_filter()

    # --- Summary statistics ---
    summary = {
        "total_tasks": conn.execute(
            f"SELECT COUNT(*) FROM tasks t WHERE 1=1{where}", params
        ).fetchone()[0],
        "open_tasks": conn.execute(
            f"SELECT COUNT(*) FROM tasks t WHERE status = 'open'{where}", params
        ).fetchone()[0],
        "in_progress_tasks": conn.execute(
            f"SELECT COUNT(*) FROM tasks t WHERE status = 'in_progress'{where}", params
        ).fetchone()[0],
        "completed_tasks": conn.execute(
            f"SELECT COUNT(*) FROM tasks t WHERE status = 'completed'{where}", params
        ).fetchone()[0],
        "overdue_tasks": conn.execute(
            f"SELECT COUNT(*) FROM tasks t WHERE due_date < DATE('now') AND status NOT IN ('completed', 'cancelled'){where}",
            params,
        ).fetchone()[0],
        "urgent_tasks": conn.execute(
            f"SELECT COUNT(*) FROM tasks t WHERE priority = 'urgent' AND status NOT IN ('completed', 'cancelled'){where}",
            params,
        ).fetchone()[0],
    }

    # Only admin/manager see organisation-level metrics
    if role in ("admin", "manager"):
        summary["total_clients"] = conn.execute(
            "SELECT COUNT(*) FROM clients"
        ).fetchone()[0]
        summary["active_clients"] = conn.execute(
            "SELECT COUNT(*) FROM clients WHERE status = 'active'"
        ).fetchone()[0]

    if role == "admin":
        summary["total_staff"] = conn.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

    # --- Chart data ---
    # Structured to match what Chart.js expects: labels, data, backgroundColor
    charts = {}

    # Tasks by status (all roles)
    status_data = conn.execute(
        f"SELECT status, COUNT(*) as count FROM tasks t WHERE 1=1{where} GROUP BY status ORDER BY status",
        params,
    ).fetchall()
    status_colours = {
        "open": "#4895ef", "in_progress": "#f9a825",
        "completed": "#4caf50", "cancelled": "#9e9e9e",
    }
    charts["tasks_by_status"] = {
        "labels": [r["status"].replace("_", " ").title() for r in status_data],
        "data": [r["count"] for r in status_data],
        "backgroundColor": [status_colours.get(r["status"], "#999") for r in status_data],
    }

    # Tasks by priority (all roles)
    priority_data = conn.execute(
        f"""SELECT priority, COUNT(*) as count FROM tasks t WHERE 1=1{where}
            GROUP BY priority ORDER BY CASE priority
            WHEN 'urgent' THEN 1 WHEN 'high' THEN 2
            WHEN 'medium' THEN 3 WHEN 'low' THEN 4 END""",
        params,
    ).fetchall()
    priority_colours = {
        "urgent": "#d32f2f", "high": "#f57c00",
        "medium": "#fbc02d", "low": "#66bb6a",
    }
    charts["tasks_by_priority"] = {
        "labels": [r["priority"].title() for r in priority_data],
        "data": [r["count"] for r in priority_data],
        "backgroundColor": [priority_colours.get(r["priority"], "#999") for r in priority_data],
    }

    # Tasks by department (admin only)
    if role == "admin":
        dept_data = conn.execute(
            "SELECT department, COUNT(*) as count FROM tasks GROUP BY department ORDER BY department"
        ).fetchall()
        charts["tasks_by_department"] = {
            "labels": [r["department"] for r in dept_data],
            "data": [r["count"] for r in dept_data],
            "backgroundColor": ["#4895ef", "#f9a825", "#4caf50", "#e91e63", "#9c27b0", "#00bcd4"][:len(dept_data)],
        }

    # Workload by user (admin sees all, manager sees their dept)
    if role == "admin":
        workload_data = conn.execute(
            """SELECT u.full_name, COUNT(t.id) as task_count
               FROM users u LEFT JOIN tasks t ON u.id = t.assigned_to AND t.status != 'completed'
               GROUP BY u.id HAVING task_count > 0 ORDER BY task_count DESC"""
        ).fetchall()
        charts["workload_by_user"] = {
            "labels": [r["full_name"] for r in workload_data],
            "data": [r["task_count"] for r in workload_data],
            "backgroundColor": "#4895ef",
        }
    elif role == "manager":
        department = session.get("department")
        workload_data = conn.execute(
            """SELECT u.full_name, COUNT(t.id) as task_count
               FROM users u LEFT JOIN tasks t ON u.id = t.assigned_to AND t.status != 'completed'
               WHERE u.department = ? GROUP BY u.id HAVING task_count > 0 ORDER BY task_count DESC""",
            (department,),
        ).fetchall()
        charts["workload_by_user"] = {
            "labels": [r["full_name"] for r in workload_data],
            "data": [r["task_count"] for r in workload_data],
            "backgroundColor": "#4895ef",
        }

    conn.close()

    return render_template(
        "dashboard.html",
        summary=summary,
        charts=charts,
        role=role,
    )
