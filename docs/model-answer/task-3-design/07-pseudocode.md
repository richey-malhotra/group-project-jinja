# Design Artefact 7 — Pseudocode for Key Algorithms

## Overview

Pseudocode describes the logic of complex algorithms in plain language before implementing them in a programming language. It helps the developer (and examiner) verify the logic is correct without getting distracted by syntax. This document covers the most important algorithms in the system — authentication, RBAC enforcement, role-filtered data queries, and input validation.

> **📋 Student Scope**
>
> **Core — what you need:** Three to four algorithms that demonstrate your most complex logic. For this system, that means: password verification (Algorithm 1), the RBAC decorators (Algorithms 2–3), and the staff task update restriction (Algorithm 4). Each one should have a plain-English explanation of WHY the logic works that way.
>
> **Stretch — what makes it exceptional:** Additional algorithms for dashboard aggregation (Algorithm 5) and the remaining operations. The first five algorithms are shown in full below. The remaining three — client deletion, file upload, and input validation — follow the same pattern of "check permissions, validate input, act on data" and are summarised in Section 6 rather than written in full. The examiner values seeing 3–4 algorithms written WELL over 8 algorithms written quickly.

---

## 1. Password Verification (FR-AUTH-01, FR-AUTH-02)

```
FUNCTION login(form_data):
    username ← form_data.username
    password ← form_data.password

    IF username is empty OR password is empty:
        flash("Username and password are required")
        REDIRECT → /login
    END IF

    user ← DATABASE.query("SELECT * FROM users WHERE username = ?", username)

    IF user is NULL:
        flash("Invalid username or password")
        REDIRECT → /login
    END IF

    IF NOT verify_password_hash(user.password, password):
        flash("Invalid username or password")
        REDIRECT → /login
    END IF

    // Note: same error message for both cases — prevents
    // attackers learning which usernames exist

    SESSION.user_id ← user.id
    SESSION.role ← user.role
    SESSION.full_name ← user.full_name
    SESSION.department ← user.department

    REDIRECT → /dashboard
END FUNCTION
```

**Design decision:** The same error message ("Invalid username or password") is returned whether the username doesn't exist OR the password is wrong. This prevents **username enumeration attacks** — an attacker cannot determine which usernames are valid by observing different error messages. The **Post-Redirect-Get** pattern prevents form resubmission on browser refresh.

---

## 2. Login Required Decorator (FR-AUTH-04)

```
FUNCTION login_required(wrapped_function):
    FUNCTION wrapper(request):
        IF "user_id" NOT IN SESSION:
            flash("Please log in to access this page")
            REDIRECT → /login
        END IF
        RETURN wrapped_function(request)
    END FUNCTION
    RETURN wrapper
END FUNCTION
```

**Usage:** Every route (except /login) is wrapped with this decorator. It runs BEFORE the route handler code. Unlike an API that returns 401 JSON, a server-rendered app redirects the user to the login page — a better user experience.

---

## 3. Role Required Decorator (FR-AUTH-03)

```
FUNCTION role_required(allowed_roles...):
    FUNCTION decorator(wrapped_function):
        FUNCTION wrapper(request):
            // login_required has already run, so session exists

            user_role ← SESSION.role

            IF user_role NOT IN allowed_roles:
                RETURN error 403 "Insufficient permissions"
            END IF

            RETURN wrapped_function(request)
        END FUNCTION
        RETURN wrapper
    END FUNCTION
    RETURN decorator
END FUNCTION
```

**Example usage:**
```
@login_required
@role_required("admin", "manager")
FUNCTION create_task(form_data):
    // This code ONLY runs if:
    //   1. User is logged in (login_required passed)
    //   2. User's role is admin OR manager (role_required passed)
    // Staff users get 403 before reaching this line.
    ...
END FUNCTION
```

---

## 4. Staff Task Update — Status-Only Restriction (FR-TASK-04)

This is the most complex RBAC algorithm — it determines not just WHETHER a user can act, but WHAT they can change.

```
FUNCTION update_task_status(task_id, form_data):
    user_id ← SESSION.user_id

    task ← DATABASE.query("SELECT * FROM tasks WHERE id = ?", task_id)

    IF task is NULL:
        RETURN error 404 "Task not found"
    END IF

    // RESTRICTION 1: Staff can only update their own tasks
    IF task.assigned_to ≠ user_id:
        RETURN error 403 "You can only update your own tasks"
    END IF

    // Staff only changes status — this route only accepts status
    new_status ← form_data.status

    DATABASE.execute(
        "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        new_status, task_id
    )

    flash("Task status updated")
    REDIRECT → /tasks
END FUNCTION

FUNCTION update_task_full(task_id, form_data):
    // Admin and manager: separate route, update any fields
    // @role_required("admin", "manager") blocks staff at decorator level

    DATABASE.execute(
        "UPDATE tasks SET title=?, description=?, status=?,
         priority=?, department=?, assigned_to=?, client_id=?,
         due_date=? WHERE id = ?",
        ... all fields from form_data ..., task_id
    )

    flash("Task updated successfully")
    REDIRECT → /tasks
END FUNCTION
```

**Why this matters:** This algorithm demonstrates the difference between **action-level RBAC** (can the user access this route?) and **field-level RBAC** (which fields can the user modify?). In the server-rendered version, we use separate routes for staff status updates vs. full updates — the template only renders the status dropdown for staff, and the route only accepts a status field. This is simpler and more secure than checking which fields were submitted.

---

## 5. Role-Filtered Dashboard Aggregation (FR-DASH-01, FR-DASH-03)

```
FUNCTION dashboard():
    role ← SESSION.role
    user_id ← SESSION.user_id
    department ← SESSION.department

    // Build WHERE clause based on role
    IF role == "admin":
        filter ← ""               // No filter — org-wide
        params ← []
    ELSE IF role == "manager":
        filter ← " AND department = ?"
        params ← [department]
    ELSE:  // staff
        filter ← " AND assigned_to = ?"
        params ← [user_id]
    END IF

    total ← DATABASE.query(
        "SELECT COUNT(*) FROM tasks " + filter, params
    )

    active ← DATABASE.query(
        "SELECT COUNT(*) FROM tasks " + filter +
        " AND status IN ('open', 'in_progress')", params
    )

    overdue ← DATABASE.query(
        "SELECT COUNT(*) FROM tasks " + filter +
        " AND due_date < TODAY AND status NOT IN ('completed', 'cancelled')", params
    )

    stats ← {total, open, in_progress, completed, overdue, urgent}

    // Admin and manager see client counts
    IF role == "admin" OR role == "manager":
        stats.total_clients ← DATABASE.query(
            "SELECT COUNT(*) FROM clients"
        )
        stats.active_clients ← DATABASE.query(
            "SELECT COUNT(*) FROM clients WHERE status = 'active'"
        )
    END IF

    // Build chart data (role-filtered GROUP BY queries)
    charts ← build_chart_data(role, filter, params)

    RETURN render_template("dashboard.html",
        stats=stats,
        charts=charts,
        role=role
    )
END FUNCTION
```

**Design decision:** The filter is built ONCE and applied to ALL queries. This guarantees consistency — if a manager sees "4 total tasks", the active/overdue counts are also scoped to those same 4 tasks, not to the whole organisation. The template receives the computed data and renders it — the template itself contains no business logic.

---

## 6. Remaining Algorithms — Summary

The following algorithms follow the same structural pattern shown above: check permissions → validate input → query/mutate data → redirect. Their key logic is summarised here rather than written in full pseudocode.

| Algorithm | Requirements | Key Logic | Design Insight |
|---|---|---|---|
| **Client deletion** | FR-CLIENT-03, FR-CLIENT-04 | Before deleting, query `SELECT COUNT(*) FROM tasks WHERE client_id = ?`. If count > 0, flash error and redirect — the request is valid but violates a business rule (referential integrity). | Shows understanding of referential integrity and user-friendly error handling via flash messages. |
| **File upload validation** | FR-ATT-01, FR-ATT-02 | Check extension against an allowlist (not a blocklist — safer). Flask enforces the 5 MB limit via `MAX_CONTENT_LENGTH`. Rename the file to a **UUID** before saving to prevent path traversal, filename collisions, and content-revealing names. | Three security benefits from one rename. |
| **Input validation** | NFR-USAB-01 | Collect ALL validation errors into a list. Flash each error message. Redirect back to the form — the template re-renders with the error messages visible. | Better UX than showing errors one at a time — the user fixes everything in one pass. |

---

> **📝 Examiner Note:** Pseudocode demonstrates that the developer planned the LOGIC before writing code. The algorithms here are not trivial — they involve conditional branching based on roles, multi-layer security checks, and careful error handling. For the exam, focus on algorithms that show DECISION-MAKING: the staff status-only restriction (Algorithm 4) and the role-filtered dashboard (Algorithm 5) are particularly strong because they demonstrate field-level and data-level access control — concepts many students overlook. Each pseudocode block should have a plain-English explanation of WHY the algorithm works that way.
