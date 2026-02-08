"""
Task Management Routes — CRUD operations for work items.

CRUD = Create, Read, Update, Delete — the four basic database operations.
Every data-driven application needs these. This module implements them
as Flask routes that render Jinja2 templates.

Server-rendered route conventions:
    GET    /tasks              → list all tasks (renders tasks.html)
    POST   /tasks/create       → create a task (redirects to /tasks)
    POST   /tasks/<id>/edit    → update a task (redirects to /tasks)
    POST   /tasks/<id>/status  → update status only — staff (redirects to /tasks)
    POST   /tasks/<id>/delete  → delete a task (redirects to /tasks)

Why POST for everything?
    HTML forms only support GET and POST. Unlike a REST API where we use
    PUT and DELETE, server-rendered apps use POST with descriptive URLs.
    This is the standard approach in Django, Rails, Flask, and Laravel.
"""

from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from routes.auth import login_required, role_required
from database import get_db

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("", methods=["GET"])
@login_required
def task_list():
    """List all tasks, with optional filtering via query parameters.

    Query parameters (submitted via GET form, all optional):
        ?status=open
        ?priority=high
        ?department=Finance
        ?search=invoice

    Staff users only see tasks assigned to them.
    Managers and admins see all tasks.

    The template receives the tasks, users, clients, and current filters
    as context — it renders everything server-side.
    """
    conn = get_db()

    # Start building the query
    query = """
        SELECT t.*, u.full_name AS assigned_name, c.company_name AS client_name
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to = u.id
        LEFT JOIN clients c ON t.client_id = c.id
        WHERE 1=1
    """
    params = []

    # Role-based filtering: staff only see their own tasks
    if session.get("role") == "staff":
        query += " AND t.assigned_to = ?"
        params.append(session["user_id"])

    # Apply optional filters from query string
    if request.args.get("status"):
        query += " AND t.status = ?"
        params.append(request.args["status"])

    if request.args.get("priority"):
        query += " AND t.priority = ?"
        params.append(request.args["priority"])

    if request.args.get("department"):
        query += " AND t.department = ?"
        params.append(request.args["department"])

    # Search across title and description
    if request.args.get("search"):
        query += " AND (t.title LIKE ? OR t.description LIKE ?)"
        search_term = f"%{request.args['search']}%"
        params.extend([search_term, search_term])

    query += " ORDER BY t.created_at DESC"

    tasks = conn.execute(query, params).fetchall()

    # For admin/manager: fetch users and clients for dropdowns
    users = []
    clients = []
    if session.get("role") in ("admin", "manager"):
        users = conn.execute(
            "SELECT id, full_name, role, department FROM users ORDER BY full_name"
        ).fetchall()
        clients = conn.execute(
            "SELECT id, company_name FROM clients WHERE status = 'active' ORDER BY company_name"
        ).fetchall()

    conn.close()

    return render_template(
        "tasks.html",
        tasks=tasks,
        users=users,
        clients=clients,
        role=session.get("role"),
        filters={
            "search": request.args.get("search", ""),
            "status": request.args.get("status", ""),
            "priority": request.args.get("priority", ""),
            "department": request.args.get("department", ""),
        },
    )


@tasks_bp.route("/create", methods=["POST"])
@login_required
@role_required("admin", "manager")
def create_task():
    """Create a new task. Only admins and managers can create tasks.

    Why restrict task creation?
    - In MJ Limited, staff RECEIVE work — they don't assign it
    - Managers allocate tasks to their team based on capacity
    - This mirrors real workplaces: your line manager assigns work,
      you don't create your own tasks and assign them to colleagues

    Server-side validation ensures data integrity.
    POST-Redirect-Get pattern prevents double submission on refresh.
    """
    # --- Validation ---
    errors = []
    title = request.form.get("title", "").strip()
    department = request.form.get("department", "").strip()

    if not title:
        errors.append("Title is required")
    if not department:
        errors.append("Department is required")

    valid_statuses = ["open", "in_progress", "completed", "cancelled"]
    status = request.form.get("status", "open")
    if status not in valid_statuses:
        errors.append(f"Status must be one of: {', '.join(valid_statuses)}")

    valid_priorities = ["low", "medium", "high", "urgent"]
    priority = request.form.get("priority", "medium")
    if priority not in valid_priorities:
        errors.append(f"Priority must be one of: {', '.join(valid_priorities)}")

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("tasks.task_list"))

    # --- Insert into database ---
    conn = get_db()
    conn.execute(
        """
        INSERT INTO tasks (title, description, status, priority, department,
                          assigned_to, client_id, due_date, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            request.form.get("description", "").strip(),
            status,
            priority,
            department,
            request.form.get("assigned_to") or None,
            request.form.get("client_id") or None,
            request.form.get("due_date") or None,
            session["user_id"],
        ),
    )
    conn.commit()
    conn.close()

    flash("Task created successfully", "success")
    return redirect(url_for("tasks.task_list"))


@tasks_bp.route("/<int:task_id>/edit", methods=["POST"])
@login_required
@role_required("admin", "manager")
def edit_task(task_id):
    """Update all fields on a task. Admin and manager only.

    Staff use the separate /status route which only allows status changes.
    """
    conn = get_db()

    # Check task exists
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        conn.close()
        flash("Task not found", "error")
        return redirect(url_for("tasks.task_list"))

    conn.execute(
        """
        UPDATE tasks SET title=?, description=?, status=?, priority=?,
               department=?, assigned_to=?, client_id=?, due_date=?,
               updated_at=CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            request.form.get("title", "").strip(),
            request.form.get("description", "").strip(),
            request.form.get("status", "open"),
            request.form.get("priority", "medium"),
            request.form.get("department", "").strip(),
            request.form.get("assigned_to") or None,
            request.form.get("client_id") or None,
            request.form.get("due_date") or None,
            task_id,
        ),
    )
    conn.commit()
    conn.close()

    flash("Task updated successfully", "success")
    return redirect(url_for("tasks.task_list"))


@tasks_bp.route("/<int:task_id>/status", methods=["POST"])
@login_required
def update_task_status(task_id):
    """Update ONLY the status of a task — staff can use this on their own tasks.

    Why a separate route?
    - Staff should be able to mark tasks as "in progress" or "completed"
    - But they should NOT change title, priority, assignment, etc.
    - Using a separate route (instead of field whitelisting) is simpler
      and more secure — the form only has a status dropdown
    """
    conn = get_db()

    # Check task exists
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        conn.close()
        flash("Task not found", "error")
        return redirect(url_for("tasks.task_list"))

    # Staff can only update tasks assigned to them
    if session.get("role") == "staff" and existing["assigned_to"] != session.get("user_id"):
        conn.close()
        flash("You can only update tasks assigned to you", "error")
        return redirect(url_for("tasks.task_list"))

    new_status = request.form.get("status", "")
    valid_statuses = ["open", "in_progress", "completed", "cancelled"]
    if new_status not in valid_statuses:
        conn.close()
        flash("Invalid status value", "error")
        return redirect(url_for("tasks.task_list"))

    conn.execute(
        "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (new_status, task_id),
    )
    conn.commit()
    conn.close()

    flash("Task status updated", "success")
    return redirect(url_for("tasks.task_list"))


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
@role_required("admin", "manager")
def delete_task(task_id):
    """Delete a task and its attachments. Admin and manager only."""
    conn = get_db()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        conn.close()
        flash("Task not found", "error")
        return redirect(url_for("tasks.task_list"))

    # Delete attachments first (cascade), then the task
    conn.execute("DELETE FROM attachments WHERE task_id = ?", (task_id,))
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    flash("Task deleted successfully", "success")
    return redirect(url_for("tasks.task_list"))
