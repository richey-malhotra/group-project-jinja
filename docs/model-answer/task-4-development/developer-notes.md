# Task 4: Developer Notes

## Development Log & Implementation Commentary

> **📋 Student Scope**
>
> **Core — what you need:** The development environment table (Section 1), an implementation narrative covering your most complex features (Section 2 — focus on authentication and RBAC), and a bug log showing at least 3–4 real bugs you found and fixed (Section 4). These prove you BUILT the system rather than just designed it.
>
> **Stretch — what makes it exceptional:** This document shows the full stretch version: a phased implementation narrative covering all 7 development phases (Section 2), reusable code pattern examples (Section 3), a bug log with root cause analysis (Section 4), a code review checklist (Section 5), and third-party acknowledgements (Section 6). You don't need 7 phases — but you DO need enough narrative to show you understand WHY the code works, not just WHAT it does.

---

### 1. Development Environment Setup

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14.2 | Server-side language |
| Flask | 3.1.0 | Web framework |
| Jinja2 | 3.1.x | Template engine (bundled with Flask) |
| Werkzeug | 3.1.3 | Password hashing (scrypt), WSGI utilities |
| python-dotenv | 1.1.0 | Load .env variables |
| SQLite | 3 (built-in) | Database |
| VS Code | Latest | IDE with Python + SQLite extensions |
| Git | Latest | Version control |

**Setup steps:**
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
python seed_data.py          # Create database + demo data
python app.py                # Start server on port 5001
```

---

### 2. Implementation Narrative

#### Phase 1: Foundation (database.py, app.py)

**Implements:** NFR-MAINT-01

Created the database module first because every other module depends on it. The `get_db()` function creates a new SQLite connection each time it is called, with `row_factory = sqlite3.Row` so columns can be accessed by name (e.g., `row['title']` instead of `row[0]`). Each route is responsible for closing its own connection after use.

Key decision: used `PRAGMA foreign_keys = ON` because SQLite has foreign key support DISABLED by default. Without this pragma, the `client_id` foreign key in the tasks table would accept values that don't exist in the clients table — a silent data integrity failure.

The application factory pattern (`create_app()`) configures the template folder and registers all blueprints. Unlike an API approach where pages are served separately, here the same Flask app serves both routes and templates — there is no separate frontend.

#### Phase 2: Authentication (routes/auth.py)

**Implements:** FR-AUTH-01, FR-AUTH-02, FR-AUTH-03, FR-AUTH-04, FR-AUTH-05

The `login_required` decorator was written first because every other route needs it. It checks for `session["user_id"]` and redirects to the login page with a flash message if missing — unlike an API that would return JSON 401.

The `role_required` decorator takes a list of allowed roles and calls `abort(403)` if the current user's role is not in the list. It is ALWAYS placed AFTER `@login_required` in the decorator stack — this is critical because Python decorators execute bottom-up. If `@role_required` ran before `@login_required`, it would duplicate the login check unnecessarily. Keeping `@login_required` first makes each decorator's responsibility clear: one checks authentication, the other checks authorisation.

```python
# Correct order — login_required runs FIRST (bottom-up)
@login_required
@role_required("admin", "manager")
def create_task():
    ...
```

Password hashing uses Werkzeug's `generate_password_hash()` which produces a scrypt hash with a unique random salt per user. The hash format is: `scrypt:32768:8:1$<salt>$<hash>`.

The login route handles GET (render form) and POST (process credentials) on the same URL — this is the standard server-rendered pattern. On success, it redirects to the dashboard (PRG pattern). On failure, it flashes an error and redirects back to the login page. The error message is deliberately vague ("Invalid username or password") for both "user not found" and "wrong password" — this prevents username enumeration (FR-AUTH-01).

No `/api/users` or `/api/auth/me` endpoint is needed — session data (`session["role"]`, `session["full_name"]`) is available directly in every Jinja2 template via Flask's `session` object.

#### Phase 3: Task Management (routes/tasks.py)

**Implements:** FR-TASK-01 through FR-TASK-07

The task list route builds SQL dynamically based on query parameters submitted via a GET form. Each filter is appended as an AND clause with a parameterised value — never string concatenation. This prevents SQL injection even with user-supplied filter values (NFR-SEC-02).

```python
# Safe — parameterised
query += " AND t.title LIKE ?"
params.append(f"%{search}%")

# NEVER — string concatenation
query += f" AND t.title LIKE '%{search}%'"  # SQL injection vector!
```

The RBAC logic uses two separate routes instead of field whitelisting on a single endpoint (FR-TASK-04). Staff use `POST /tasks/<id>/status` which only accepts the `status` field. Admins and managers use `POST /tasks/<id>/edit` which accepts all fields. This is simpler and more secure than checking which fields were submitted — the route itself defines what can be changed.

Both routes also enforce ownership: a staff member can only update status on tasks assigned to them, not on other users' tasks.

The create route (POST `/tasks/create`) uses `@role_required("admin", "manager")` — staff users receive 403 before the handler code runs (FR-TASK-01).

Search uses SQL `LIKE` with `%` wildcards on title and description, combined with `OR` (FR-TASK-06). Filters (status, priority, department) use exact-match `=` with `AND` (FR-TASK-07). The GET form submits these as query parameters, making filtered views bookmarkable.

#### Phase 4: Client Management (routes/clients.py)

**Implements:** FR-CLIENT-01 through FR-CLIENT-05

Client routes follow the same template-rendering pattern as tasks but with different role restrictions:
- Create and update: admin + manager (FR-CLIENT-01, FR-CLIENT-02)
- Delete: admin ONLY (FR-CLIENT-03)
- Staff: no access — `@role_required("admin", "manager")` on all client routes (FR-CLIENT-05)

The delete route checks for linked tasks BEFORE executing the DELETE (FR-CLIENT-04). If any tasks reference the client, it flashes an error message ("Cannot delete client with 3 linked task(s). Reassign or delete the tasks first.") and redirects back. This is a business rule — not a foreign key constraint — because we want a helpful message rather than a generic database error.

#### Phase 5: Dashboard (routes/dashboard.py)

**Implements:** FR-DASH-01, FR-DASH-02, FR-DASH-03

The dashboard combines summary statistics and chart data into a single `render_template()` call — unlike an API approach that would need separate `/summary` and `/charts` endpoints.

The `_role_filter()` helper function returns a SQL WHERE clause fragment and parameters based on the current user's role:

| Role | Filter | Scope |
|---|---|---|
| Admin | (empty) | Organisation-wide |
| Manager | `WHERE department = ?` | Department-scoped |
| Staff | `WHERE assigned_to = ?` | Personal tasks only |

This filter is applied to ALL dashboard queries — summary stats AND chart aggregations — guaranteeing consistency.

Chart data is passed to JavaScript via Jinja2's `tojson` filter:

```html
<script>
  const chartData = {{ charts | tojson }};
  renderCharts(chartData, "{{ role }}");
</script>
```

The `tojson` filter converts Python dicts to JSON strings safely — Jinja2 auto-escapes the output to prevent XSS even if the data contained malicious strings. This is the standard Flask pattern for passing server data to client-side JavaScript.

The number of charts varies by role: admin gets 4 (status, priority, department, workload), manager gets 3 (no department — already scoped), staff gets 2 (status and priority only). Jinja conditionals control which `<canvas>` elements are rendered in the template (FR-DASH-02).

#### Phase 6: File Attachments (routes/attachments.py)

**Implements:** FR-ATT-01, FR-ATT-02, FR-ATT-03

File security was a priority. Every uploaded file is renamed with a UUID hex string (`uuid.uuid4().hex`) — the original filename is preserved in the database for display but NEVER used on the file system (NFR-SEC-05). This prevents:
- Path traversal attacks (`../../etc/passwd` → harmless UUID)
- Filename collisions (two `report.pdf` files get different UUIDs)
- Information leakage (UUID reveals nothing about content)

The upload form uses `enctype="multipart/form-data"` — the browser sends the file as binary data, not URL-encoded text. Flask makes this available via `request.files` instead of `request.form`.

Deletion permissions follow a hierarchy: the uploader can always delete their own files, admin and manager can delete any file, but a staff member cannot delete another user's file (FR-ATT-03).

#### Phase 7: Templates & Styling (templates/, static/)

**Implements:** Multiple FR and NFR requirements

All templates extend `base.html` using Jinja2 template inheritance:

```html
{% extends "base.html" %}
{% block title %}Task Management{% endblock %}
{% block content %}
  <!-- page-specific content here -->
{% endblock %}
```

The base template provides:
- Navigation bar with role-conditional links (`{% if session.get('role') in ['admin', 'manager'] %}`)
- Flash message rendering using `get_flashed_messages(with_categories=true)`
- Consistent page structure (header, main, footer)
- An empty `{% block scripts %}` placeholder that child templates (like `dashboard.html`) override to load page-specific scripts such as the Chart.js CDN

XSS prevention is automatic — Jinja2 auto-escapes ALL template variables by default (NFR-SEC-03). When a template renders `{{ task.title }}`, Jinja2 converts `<script>alert('xss')</script>` to `&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;`. No manual escaping function is needed.

User feedback uses Flask's `flash()` function. The base template renders flash messages with category-based styling (success/error/warning). After a POST-Redirect-Get cycle, the flash message appears on the redirected page and disappears on the next navigation (NFR-USAB-02).

The only significant JavaScript is `charts.js` for Chart.js rendering — this satisfies the "two programming languages" requirement. Form modals use the HTML `<dialog>` element with a small JS function to populate edit forms. All other interactions are standard HTML forms.

---

### 3. Key Code Patterns

#### 3.1 Parameterised Queries (NFR-SEC-02)

Every SQL query uses `?` placeholders:

```python
# Every query in the codebase follows this pattern
cursor.execute(
    "SELECT * FROM tasks WHERE id = ? AND assigned_to = ?",
    (task_id, user_id)
)
```

This is the ONLY method used. No string concatenation, no f-strings, no `.format()` in any SQL query.

#### 3.2 Consistent Validation (NFR-USAB-01)

All routes collect ALL validation errors before redirecting:

```python
errors = []
if not title:
    errors.append("Title is required")
if not department:
    errors.append("Department is required")
if errors:
    for error in errors:
        flash(error, "error")
    return redirect(url_for("tasks.task_list"))
```

This flashes all issues at once rather than one at a time.

#### 3.3 Jinja2 Auto-Escaping (NFR-SEC-03)

Every piece of user-generated content is automatically escaped by Jinja2:

```html
<!-- Jinja2 auto-escapes this — safe by default -->
<td>{{ task.title }}</td>

<!-- Even if task.title contains <script>alert('xss')</script> -->
<!-- Jinja2 renders: &lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt; -->
```

No manual `escapeHtml()` function is needed. The template engine handles it.

---

### 4. Bugs Encountered and Fixed

| # | Bug | Cause | Fix | Lesson |
|---|---|---|---|---|
| 1 | Port 5000 refused on macOS | AirTunes service uses port 5000 | Changed to port 5001 | Always check for port conflicts on the development machine |
| 2 | Flash messages not appearing | `base.html` was missing `get_flashed_messages()` call | Added flash rendering block to base template | Flash messages are stored in the session but only displayed if the template reads them |
| 3 | Foreign keys not enforced | SQLite disables foreign keys by default | Added `PRAGMA foreign_keys = ON` in `get_db()` | Never assume database features are enabled by default |
| 4 | Staff could see all tasks | No role-based query filtering | Added `WHERE assigned_to = ?` for staff role in task queries | Template hiding is not security — backend must filter data |
| 5 | Double form submission on refresh | Browser re-submits POST on F5 | Applied PRG pattern: POST routes end with `redirect()`, never `render_template()` | POST handlers should always redirect on success — the Post-Redirect-Get pattern prevents duplicate submissions |
| 6 | Manager could delete clients | Delete route only checked `login_required`, not role | Added `@role_required("admin")` to client delete route | Every route needs explicit role checking |
| 7 | `url_for()` generating wrong URL | Blueprint prefix not matching route registration in `app.py` | Aligned `url_prefix` in `register_blueprint()` with template `url_for()` calls | Template URLs must match the exact prefix set during blueprint registration |

---

### 5. Code Review Checklist

Before each commit, the team verified:

- [ ] All SQL queries use parameterised `?` placeholders (NFR-SEC-02)
- [ ] All templates extend `base.html` using template inheritance
- [ ] Every route has `@login_required` (FR-AUTH-04)
- [ ] Restricted routes have `@role_required()` with correct roles (FR-AUTH-03)
- [ ] POST handlers redirect on success (PRG pattern)
- [ ] Validation collects ALL errors before flashing (NFR-USAB-01)
- [ ] New features tested for all three roles (admin, manager, staff)
- [ ] No hard-coded values — configuration in `.env` file

---

### 6. Third-Party Acknowledgements

| Library | Version | Licence | Used For |
|---|---|---|---|
| Flask | 3.1.0 | BSD-3 | Web framework |
| Jinja2 | 3.1.x | BSD-3 | Template engine (bundled with Flask) |
| Werkzeug | 3.1.3 | BSD-3 | Password hashing, request handling |
| python-dotenv | 1.1.0 | BSD-3 | Environment variable loading |
| Chart.js | 4.x | MIT | Dashboard charts |

---

> **📝 Examiner Note:** Developer notes demonstrate the PROCESS of development, not just the end result. The FR-ID and NFR-ID references throughout show traceability from requirements → design → code → testing. The bug log shows that problems were encountered and solved — examiners want to see this because it demonstrates real development experience. The code review checklist shows quality assurance practices. Students who present "everything worked first time" are less credible than those who document issues and solutions.
