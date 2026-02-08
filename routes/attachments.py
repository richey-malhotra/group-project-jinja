"""
File Attachment Routes — Upload, download, and delete files linked to tasks.

Attachments use multipart form data for uploads — the only place where
the HTML form encoding differs from standard URL-encoded POST data.
Even so, the pattern remains the same: POST → process → redirect.

Security considerations:
    - Files are renamed with a unique prefix to prevent overwriting
    - Original filename is stored in the database for display
    - Only allowed file extensions are accepted
    - File size is limited by MAX_CONTENT_LENGTH in app config (5MB)
    - Files are stored in uploads/ (not directly web-accessible)
    - send_from_directory prevents path traversal attacks
"""

import os
import uuid
from flask import Blueprint, request, session, redirect, url_for, flash, current_app, send_from_directory
from routes.auth import login_required
from database import get_db

attachments_bp = Blueprint("attachments", __name__)

# Allowed file types — prevents uploading executable files
ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "xls", "xlsx", "csv",
    "txt", "png", "jpg", "jpeg", "gif",
}


def allowed_file(filename):
    """Check if a filename has an allowed extension.

    'report.pdf'.rsplit('.', 1) gives ['report', 'pdf']
    We check the part after the last dot, lowercased.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@attachments_bp.route("/upload/<int:task_id>", methods=["POST"])
@login_required
def upload_file(task_id):
    """Upload a file and attach it to a task.

    The form uses enctype='multipart/form-data' — the browser sends
    the file as binary data, not URL-encoded text. Flask makes this
    available via request.files instead of request.form.
    """
    conn = get_db()
    task = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        conn.close()
        flash("Task not found", "error")
        return redirect(url_for("tasks.task_list"))

    if "file" not in request.files:
        conn.close()
        flash("No file provided", "error")
        return redirect(url_for("tasks.task_detail", task_id=task_id))

    file = request.files["file"]
    if file.filename == "":
        conn.close()
        flash("No file selected", "error")
        return redirect(url_for("tasks.task_detail", task_id=task_id))

    if not allowed_file(file.filename):
        conn.close()
        flash(
            f"File type not allowed. Accepted: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            "error",
        )
        return redirect(url_for("tasks.task_detail", task_id=task_id))

    # Generate unique filename to prevent collisions
    original_filename = file.filename
    extension = original_filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{extension}"

    # Save file to disk
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_filename)
    file.save(filepath)
    file_size = os.path.getsize(filepath)

    # Record in database
    conn.execute(
        """
        INSERT INTO attachments (task_id, filename, original_filename, file_size, uploaded_by)
        VALUES (?, ?, ?, ?, ?)
        """,
        (task_id, unique_filename, original_filename, file_size, session["user_id"]),
    )
    conn.commit()
    conn.close()

    flash("File uploaded successfully", "success")
    return redirect(url_for("tasks.task_detail", task_id=task_id))


@attachments_bp.route("/download/<filename>", methods=["GET"])
@login_required
def download_file(filename):
    """Download an attached file.

    send_from_directory safely serves files from a specific folder,
    preventing path traversal attacks (e.g., '../../../etc/passwd').
    The as_attachment=True header tells the browser to download, not display.
    """
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(upload_folder, filename)

    if not os.path.exists(filepath):
        flash("File not found", "error")
        return redirect(url_for("tasks.task_list"))

    # Look up original filename for the download
    conn = get_db()
    attachment = conn.execute(
        "SELECT original_filename FROM attachments WHERE filename = ?", (filename,)
    ).fetchone()
    conn.close()

    download_name = attachment["original_filename"] if attachment else filename

    return send_from_directory(
        upload_folder,
        filename,
        as_attachment=True,
        download_name=download_name,
    )


@attachments_bp.route("/<int:attachment_id>/delete", methods=["POST"])
@login_required
def delete_attachment(attachment_id):
    """Delete an attachment (file and database record).

    Only the uploader, admins, or managers can delete attachments.
    """
    conn = get_db()
    attachment = conn.execute(
        "SELECT * FROM attachments WHERE id = ?", (attachment_id,)
    ).fetchone()

    if attachment is None:
        conn.close()
        flash("Attachment not found", "error")
        return redirect(url_for("tasks.task_list"))

    # Permission check: uploader, admin, or manager
    if (
        attachment["uploaded_by"] != session["user_id"]
        and session.get("role") not in ("admin", "manager")
    ):
        conn.close()
        flash("Permission denied", "error")
        return redirect(url_for("tasks.task_detail", task_id=attachment["task_id"]))

    # Delete the physical file
    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"], attachment["filename"]
    )
    if os.path.exists(filepath):
        os.remove(filepath)

    # Delete the database record
    conn.execute("DELETE FROM attachments WHERE id = ?", (attachment_id,))
    conn.commit()
    conn.close()

    task_id = attachment["task_id"]

    flash("Attachment deleted successfully", "success")
    return redirect(url_for("tasks.task_detail", task_id=task_id))
