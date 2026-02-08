"""
Client Management Routes — CRUD for MJ Limited's external clients.

Same POST-based pattern as tasks:
    GET    /clients              → list all clients
    POST   /clients/create       → create a client
    POST   /clients/<id>/edit    → update a client
    POST   /clients/<id>/delete  → delete a client

Only admins and managers can access client management.
Staff accessing /clients receive 403 Forbidden via @role_required.
"""

from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from routes.auth import login_required, role_required
from database import get_db

clients_bp = Blueprint("clients", __name__)


@clients_bp.route("", methods=["GET"])
@login_required
@role_required("admin", "manager")
def client_list():
    """List all clients with optional search and status filtering."""
    conn = get_db()

    query = "SELECT * FROM clients WHERE 1=1"
    params = []

    if request.args.get("status"):
        query += " AND status = ?"
        params.append(request.args["status"])

    if request.args.get("search"):
        query += " AND (company_name LIKE ? OR contact_name LIKE ? OR contact_email LIKE ?)"
        search_term = f"%{request.args['search']}%"
        params.extend([search_term, search_term, search_term])

    if request.args.get("industry"):
        query += " AND industry = ?"
        params.append(request.args["industry"])

    query += " ORDER BY company_name ASC"

    clients = conn.execute(query, params).fetchall()
    conn.close()

    return render_template(
        "clients.html",
        clients=clients,
        role=session.get("role"),
        filters={
            "search": request.args.get("search", ""),
            "status": request.args.get("status", ""),
            "industry": request.args.get("industry", ""),
        },
    )


@clients_bp.route("/create", methods=["POST"])
@login_required
@role_required("admin", "manager")
def create_client():
    """Create a new client. Admin and manager only."""
    errors = []
    company_name = request.form.get("company_name", "").strip()
    contact_name = request.form.get("contact_name", "").strip()
    contact_email = request.form.get("contact_email", "").strip()

    if not company_name:
        errors.append("Company name is required")
    if not contact_name:
        errors.append("Contact name is required")
    if not contact_email:
        errors.append("Contact email is required")

    status = request.form.get("status", "active")
    if status not in ("active", "inactive"):
        errors.append("Status must be 'active' or 'inactive'")

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("clients.client_list"))

    conn = get_db()
    conn.execute(
        """
        INSERT INTO clients (company_name, contact_name, contact_email,
                            contact_phone, industry, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company_name,
            contact_name,
            contact_email,
            request.form.get("contact_phone", "").strip(),
            request.form.get("industry", "").strip(),
            status,
            request.form.get("notes", "").strip(),
        ),
    )
    conn.commit()
    conn.close()

    flash("Client created successfully", "success")
    return redirect(url_for("clients.client_list"))


@clients_bp.route("/<int:client_id>/edit", methods=["POST"])
@login_required
@role_required("admin", "manager")
def edit_client(client_id):
    """Update an existing client."""
    conn = get_db()
    existing = conn.execute(
        "SELECT * FROM clients WHERE id = ?", (client_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        flash("Client not found", "error")
        return redirect(url_for("clients.client_list"))

    conn.execute(
        """
        UPDATE clients SET company_name=?, contact_name=?, contact_email=?,
               contact_phone=?, industry=?, status=?, notes=?,
               updated_at=CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            request.form.get("company_name", "").strip(),
            request.form.get("contact_name", "").strip(),
            request.form.get("contact_email", "").strip(),
            request.form.get("contact_phone", "").strip(),
            request.form.get("industry", "").strip(),
            request.form.get("status", "active"),
            request.form.get("notes", "").strip(),
            client_id,
        ),
    )
    conn.commit()
    conn.close()

    flash("Client updated successfully", "success")
    return redirect(url_for("clients.client_list"))


@clients_bp.route("/<int:client_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_client(client_id):
    """Delete a client. Admin only.

    Checks for linked tasks before deletion — if this client has tasks
    assigned to them, the delete is blocked with a flash message.
    """
    conn = get_db()
    existing = conn.execute(
        "SELECT * FROM clients WHERE id = ?", (client_id,)
    ).fetchone()
    if existing is None:
        conn.close()
        flash("Client not found", "error")
        return redirect(url_for("clients.client_list"))

    # Check for linked tasks — cannot delete a client with active work
    linked_tasks = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE client_id = ?", (client_id,)
    ).fetchone()[0]
    if linked_tasks > 0:
        conn.close()
        flash(
            f"Cannot delete client with {linked_tasks} linked task(s). "
            "Reassign or delete the tasks first.",
            "error",
        )
        return redirect(url_for("clients.client_list"))

    conn.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

    flash("Client deleted successfully", "success")
    return redirect(url_for("clients.client_list"))
