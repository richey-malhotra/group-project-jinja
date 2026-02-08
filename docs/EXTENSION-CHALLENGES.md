# Extension Challenges

These are optional features you can add to the MJ Limited Task Manager. They're ordered from easiest to hardest, and each one builds skills that map directly to the T Level DPDD assessment criteria.

| # | Challenge | Difficulty | What you'll practise |
|---|-----------|------------|----------------------|
| 1 | CSV Data Export | ⭐ Gentle | Python `csv` module, HTTP response headers, role-based UI |
| 2 | Server-Side Sortable Table | ⭐⭐ Moderate | SQL ORDER BY, query parameters, Jinja2 conditional rendering |
| 3 | Audit Logging | ⭐⭐⭐ Challenging | New database table, helper functions, cross-cutting concerns |
| 4 | User Management | ⭐⭐⭐⭐ Substantial | Full CRUD, password hashing, referential integrity, safety checks |

Work through them in order — each challenge assumes you're comfortable with the patterns from the previous one. Don't worry if you can't finish all four. Even completing Challenge 1 gives you something concrete to write about in your reflective report.

---

## Before You Start

### How to debug

When something goes wrong, **look at the terminal** where `python app.py` is running — not the browser. Flask prints the full error traceback there.

**How to read a Python traceback:**
1. Scroll to the **last line** — it tells you the error type and message (e.g., `NameError: name 'csv' is not defined`)
2. Look at the line **just above** it — it shows the exact file path and line number where the error happened
3. Read upwards from there to see the chain of function calls that led to the error

Common error types you'll see:
- `ImportError` / `ModuleNotFoundError` — you forgot an `import` statement or misspelled a module name
- `NameError` — you're using a variable or function that doesn't exist in the current scope (often a missing import)
- `TypeError` — you're passing the wrong number of arguments, or calling a method on the wrong type (e.g., `.lower()` on `None`)
- `IntegrityError` — a database constraint was violated (duplicate username, missing required field)
- `AttributeError` — you're trying to use a method or property that doesn't exist on that object (e.g., calling `.append()` on a string)

If the browser shows "Internal Server Error", the server has hit an exception. Check the terminal first — the answer is almost always there.

### Blueprint starter template

Challenges 3 and 4 ask you to create new route files. Every route file in this project follows the same skeleton. Copy this when starting a new file:

```python
from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from routes.auth import login_required, role_required
from database import get_db

# Change "example" to your feature name (e.g., "users", "audit")
example_bp = Blueprint("example", __name__)


@example_bp.route("/example")
@login_required
def example_list():
    """Fetch and display all records."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM example").fetchall()
    conn.close()
    return render_template("example.html", items=rows)
```

Then register it in `app.py` — add two lines alongside the existing Blueprint registrations:

```python
from routes.example import example_bp
app.register_blueprint(example_bp)
```

You also need a Jinja2 template. Create `templates/example.html`:

```html
{% extends "base.html" %}
{% block content %}
<h1>Example</h1>
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        {% for item in items %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ item.description }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

> **Why `{% extends "base.html" %}`?** This inherits the navigation bar, CSS, and flash message display from the base template. Without it, your new page would have no navigation and no consistent styling. Every template in this project extends `base.html`.

---

## Challenge 1: CSV Data Export

**What you're building:** A button on the tasks page that downloads all visible tasks as a `.csv` file.

> **What you'll learn:**
> - How to create a new route that returns a file instead of a rendered template
> - How HTTP response headers (`Content-Type`, `Content-Disposition`) control what the browser does with a response
> - How to conditionally show a UI element based on the logged-in user's role

**Why it matters:** The reflective report identifies this as FR-EXPORT-01. Managers need to share reports with people who don't have system access. CSV is the universal format — it opens in Excel, Google Sheets, and every data tool. This is the kind of "management asked for it on Friday" feature you'll build in real jobs.

**Study these files first:**
- `routes/tasks.py` — look at the `task_list()` function (the `GET /tasks` route). It already builds the SQL query and returns all the data you need. Your export route will reuse the same query
- `routes/attachments.py` — look at the `download_file()` function. It uses `send_from_directory()` with `as_attachment=True` — this is how Flask tells the browser "download this, don't display it". Your approach will be slightly different (you're building the file in memory, not reading one from disk), but the concept is the same

**Steps:**

1. **New route in `routes/tasks.py`:** Add `GET /tasks/export` that:
   - Requires login and admin or manager role (`@login_required` then `@role_required("admin", "manager")`)
   - Runs the same query as the existing task list but returns CSV instead of a rendered template
   - Sets the response `Content-Type` to `text/csv`
   - Sets `Content-Disposition` to `attachment; filename="tasks-export.csv"` so the browser downloads it

   > **Why two decorators?** `@login_required` checks that someone is logged in. `@role_required` checks they have the right role. You need both — without `@login_required`, an unauthenticated user would hit the role check and crash because there's no session. Look at how `create_task()` in the same file uses both.

2. **Build the CSV in memory:** Python's built-in `csv` module (no `pip install` needed) can write to a `StringIO` object. Think of `StringIO` as a "fake file" — it behaves like a file you opened with `open()`, but it lives in memory instead of on disk. You need:

   ```python
   import csv
   import io
   from flask import Response  # add this to your existing imports at the top
   ```

   Then in your route:

   ```python
   output = io.StringIO()                           # create the fake file
   writer = csv.writer(output)                       # attach a CSV writer to it
   writer.writerow(["Title", "Status", "Priority"])  # write the header row
   for task in tasks:                                # write one row per task
       writer.writerow([task["title"], task["status"], task["priority"]])
   csv_text = output.getvalue()                      # get everything as a string
   ```

   Then return it:
   ```python
   return Response(
       csv_text,
       mimetype="text/csv",
       headers={"Content-Disposition": "attachment; filename=tasks-export.csv"}
   )
   ```

   > **Why `Response()` instead of `render_template()`?** `render_template()` renders an HTML page. Here you're returning CSV text, so you need `Response()` to set the right content type and tell the browser to download it. `Response` is imported from Flask just like `render_template` is.

3. **Button in `templates/tasks.html`:** Add an "Export CSV" link (visible to admin/manager only) that navigates to `/tasks/export`. Look at how other role-conditional elements are shown — you'll follow the same `{% if %}` pattern:

   ```html
   {% if session.role in ["admin", "manager"] %}
       <a href="{{ url_for('tasks.export_tasks') }}" class="btn">Export CSV</a>
   {% endif %}
   ```

   > **Why a plain link instead of a form?** Because this is a GET request that downloads a file. The browser handles it natively — clicking the link triggers the download because the response has `Content-Disposition: attachment`. No JavaScript needed, no form needed. The session cookie is sent automatically because it's a same-origin navigation.

**Common mistakes:**
- Forgetting to add `@login_required` and `@role_required("admin", "manager")` — the route works but anyone can download all the data, which is a security issue the examiner would flag
- Using `render_template()` out of habit instead of `Response(...)` — the browser will try to display CSV text as an HTML page
- Forgetting to `import Response` from Flask — you'll get a `NameError` at runtime
- Writing `writer.writerow(row)` where `row` is a dict — `csv.writer` expects a list, not a dict. Use `writer.writerow([row["title"], row["status"], ...])` or use `csv.DictWriter` instead
- Not including enough columns — add all the useful fields (title, description, status, priority, due date, client name, assigned user). More columns = more useful export

**How to test it:**
1. Log in as `admin` / `admin123`. Navigate to Tasks. Click "Export CSV". A file should download.
2. Open the file in Excel or a text editor — check that all columns are present and data looks correct.
3. Log out. Log in as `j.smith` / `staff123`. The "Export CSV" button should not be visible.
4. While logged in as `j.smith`, try navigating directly to `http://localhost:5001/tasks/export` — you should be redirected away, not get a file download. This proves the backend protection works even if someone types the URL directly.

**You're done when:**
- [ ] Admin/manager can click "Export CSV" and a `.csv` file downloads
- [ ] The file opens correctly in Excel or Google Sheets
- [ ] Staff users cannot see the button or access the route
- [ ] The CSV contains all task fields including assigned user and client name

---

## Challenge 2: Server-Side Sortable Task Table

**What you're building:** Clickable column headers on the tasks page that sort the table ascending/descending, with arrow indicators showing the current direction.

> **What you'll learn:**
> - How SQL `ORDER BY` sorts data at the database level — faster and more reliable than sorting in Python or JavaScript
> - How query parameters in URLs (`?sort=title&dir=asc`) pass user preferences to the server
> - How Jinja2 templates can generate dynamic links with conditional rendering

**Why it matters:** Sorting is something users expect in every data table. In a server-rendered application, the right approach is to sort on the server using SQL — the database is optimised for this. This challenge is entirely server-side (no JavaScript needed), which reinforces the architecture pattern used throughout this project.

**Study these files first:**
- `routes/tasks.py` — look at how the existing `task_list()` function builds a SQL query with optional `WHERE` clauses for filtering. You'll add an `ORDER BY` clause using the same pattern
- `templates/tasks.html` — look at the `<th>` elements in the `<thead>`. You'll make these clickable links that pass sort parameters back to the server

**Steps:**

1. **Read sort parameters from the URL.** In `routes/tasks.py`, inside `task_list()`, read two query parameters:

   ```python
   sort_column = request.args.get("sort", "id")       # default: sort by id
   sort_dir = request.args.get("dir", "asc")           # default: ascending
   ```

   > **Why `request.args` instead of `request.form`?** `request.form` reads data from POST form submissions. `request.args` reads data from the URL query string (the `?key=value` part). Sorting is a GET operation — the user clicks a link, not a form submit. GET parameters appear in the URL, which means the sorted view is bookmarkable and shareable.

2. **Validate the sort parameters.** Never put user input directly into SQL — even for column names. Create an allowlist of sortable columns:

   ```python
   SORTABLE_COLUMNS = {"id", "title", "status", "priority", "due_date", "client_name", "assigned_name"}

   if sort_column not in SORTABLE_COLUMNS:
       sort_column = "id"
   if sort_dir not in ("asc", "desc"):
       sort_dir = "asc"
   ```

   > **Why validate?** Because `sort_column` goes into the SQL query. If you write `ORDER BY {sort_column}`, a malicious user could set `sort=id; DROP TABLE tasks--` in the URL. The allowlist ensures only known column names are accepted. **This is not the same as parameterised queries** — `?` placeholders don't work for column names or `ORDER BY` direction, only for values. Allowlist validation is the correct defence here.

3. **Add ORDER BY to the SQL query.** After building your existing WHERE clause, append the sort:

   ```python
   query += f" ORDER BY {sort_column} {'ASC' if sort_dir == 'asc' else 'DESC'}"
   ```

   This is safe because you validated both values against allowlists in step 2.

4. **Pass sort state to the template.** Add the sort parameters to your `render_template()` call:

   ```python
   return render_template("tasks.html",
       tasks=tasks,
       sort_column=sort_column,
       sort_dir=sort_dir,
       # ... other existing variables ...
   )
   ```

5. **Make column headers clickable.** In `templates/tasks.html`, replace each `<th>` with a link that toggles the sort direction:

   ```html
   <th>
       {% set next_dir = "desc" if sort_column == "title" and sort_dir == "asc" else "asc" %}
       <a href="{{ url_for('tasks.task_list', sort='title', dir=next_dir) }}">
           Title
           {% if sort_column == "title" %}
               {{ "&#9650;" if sort_dir == "asc" else "&#9660;" | safe }}
           {% endif %}
       </a>
   </th>
   ```

   > **What does `{% set %}` do?** It creates a temporary variable inside the template. Here it calculates the *next* sort direction: if you're currently sorting by title ascending, the next click should sort descending (and vice versa). If you're sorting by a different column, clicking title should start with ascending.

   > **What are `&#9650;` and `&#9660;`?** They're HTML entities for the up arrow (&#9650;) and down arrow (&#9660;) characters. The `| safe` filter tells Jinja2 not to escape the HTML entity — without it, you'd see the literal text `&#9650;` instead of the arrow symbol.

   Repeat this pattern for every sortable column: title, status, priority, due date, client name, assigned user.

6. **Preserve filters when sorting.** If the user has an active search or filter, clicking a sort header should keep that filter. Pass the current filter values alongside the sort parameters:

   ```html
   <a href="{{ url_for('tasks.task_list',
       sort='title',
       dir=next_dir,
       search=request.args.get('search', ''),
       status=request.args.get('status', ''),
       priority=request.args.get('priority', '')
   ) }}">
   ```

   > **Why is this necessary?** Without it, clicking "Sort by Title" would navigate to `/tasks?sort=title&dir=asc` — losing the user's search text and filter selections. By including the current filter values in the link, the full URL becomes `/tasks?sort=title&dir=asc&search=quarterly&status=open`, preserving everything.

**Common mistakes:**
- Putting `sort_column` directly into SQL without validation — this is a SQL injection vulnerability. Always validate against an allowlist
- Using `?` parameterised queries for column names — `cursor.execute("SELECT * FROM tasks ORDER BY ?", (sort_column,))` doesn't work in SQLite. The `?` placeholder is for values, not column names. Use f-string formatting **only after allowlist validation**
- Forgetting `| safe` on the arrow HTML entities — Jinja2 will escape them and you'll see `&#9650;` as text instead of as an arrow
- Not preserving filter values when generating sort links — the user loses their search when they sort
- Sorting by a column that doesn't exist in the query result — make sure your `SORTABLE_COLUMNS` allowlist matches the actual column names returned by your SQL query (including aliases like `assigned_name`)

**How to test it:**
1. Log in as `admin` / `admin123`. Navigate to Tasks. Click the "Title" column header — tasks should sort A to Z and an up-arrow should appear next to "Title".
2. Click "Title" again — tasks should reverse to Z to A and the arrow should change to a down-arrow.
3. Click "Status" — tasks should sort by status, the arrow should move to the Status column, and the Title column should have no arrow.
4. Type something in the search box and apply the filter. Then click a column header to sort — the search filter should still be active (filtered AND sorted).
5. Check the URL in the browser address bar — it should show the sort parameters: `?sort=title&dir=asc`. This means the sorted view is bookmarkable.

**You're done when:**
- [ ] Clicking a column header sorts the table by that column
- [ ] Clicking the same header again toggles between ascending and descending
- [ ] An arrow indicator shows on the currently sorted column only
- [ ] The sorted URL is bookmarkable (sort state is in the query string)
- [ ] Sorting works correctly alongside the existing search and filter controls
- [ ] Sort column names are validated against an allowlist (no SQL injection)

---

## Challenge 3: Audit Logging

**What you're building:** An `audit_log` table that records every create, update, and delete action across the system, plus a read-only log viewer page for admins.

> **What you'll learn:**
> - How to extend a database schema by adding a new table with a **foreign key** relationship
> - How to write a reusable **helper function** that gets called from multiple places (a "cross-cutting concern")
> - How to capture "before and after" values during an update to create meaningful change descriptions
> - How to create a new Blueprint, register it, and build a Jinja2 template from scratch

**Why it matters:** The reflective report identifies this as FR-AUDIT-01. In a real business, knowing *who changed what and when* is essential for accountability and debugging data issues. If a manager asks "who deleted that task last Tuesday?", the audit log answers it instantly. This is the first challenge where you're touching both backend and frontend, plus modifying existing code — which is closer to how real development works.

**Study these files first:**
- `database.py` — look at the `init_db()` function to see how existing tables are created. You'll add your new table here
- `routes/tasks.py` — look at how the POST handlers for create, edit, and delete work. You'll add one line to each one after the database operation
- `routes/clients.py` — same CRUD pattern, same approach. You'll add audit calls here too
- `templates/dashboard.html` — this is the simplest template in the project (stat cards and charts, no modals or forms). Use its structure as a starting point for your audit viewer

**Steps:**

1. **New table in `database.py`:** Add this `CREATE TABLE` statement inside the `init_db()` function, alongside the existing ones:

   ```sql
   CREATE TABLE IF NOT EXISTS audit_log (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER NOT NULL,
       action TEXT NOT NULL,
       entity_type TEXT NOT NULL,
       entity_id INTEGER NOT NULL,
       detail TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES users(id)
   )
   ```

   > **What's a foreign key?** The line `FOREIGN KEY (user_id) REFERENCES users(id)` tells the database "the `user_id` column must contain a value that exists in the `users` table's `id` column". It's a safety net — you can't accidentally log an action for a user that doesn't exist. Look at the existing `tasks` table definition — it uses the same pattern for `assigned_to` and `client_id`.

   The columns:
   - `action` — one of: `create`, `update`, `delete`
   - `entity_type` — one of: `task`, `client`, `attachment`
   - `entity_id` — the ID of the thing that was changed
   - `detail` — a human-readable summary like `"Changed status from 'open' to 'in_progress'"`. This is the most valuable column — a generic "updated task 7" tells you nothing useful

   > **Important:** After adding the new table, you must delete your database file and re-seed: `rm mj_limited.db && python seed_data.py`. The existing database file doesn't have the `audit_log` table, and SQLite won't add it automatically. This is a common gotcha — if your INSERT queries fail with "no such table: audit_log", this is why.

2. **Helper function:** Write a function that inserts an audit record. Put it in `database.py` (since it needs `get_db()`) or a new `utils.py` file — either works. The function signature:

   ```python
   def log_action(user_id, action, entity_type, entity_id, detail=None):
       conn = get_db()
       conn.execute(
           """INSERT INTO audit_log (user_id, action, entity_type, entity_id, detail)
              VALUES (?, ?, ?, ?, ?)""",
           (user_id, action, entity_type, entity_id, detail)
       )
       conn.commit()
       conn.close()
   ```

   This is intentionally simple — one INSERT query, nothing clever. The power comes from calling it consistently everywhere.

3. **Add calls in existing routes:** In each POST handler for create, edit, and delete across `tasks.py`, `clients.py`, and `attachments.py`, add one line **after the successful database operation and commit**:

   ```python
   log_action(session["user_id"], "create", "task", new_id, f"Created task: {title}")
   ```

   > **Why after the commit, not before?** If the database operation fails (e.g., validation error, constraint violation), the `commit()` won't happen and the route returns an error via `flash()`. If you logged the action before that, you'd have a log entry for something that never actually happened. Always log after confirming success.

   For deletes:
   ```python
   log_action(session["user_id"], "delete", "task", task_id, f"Deleted task: {task['title']}")
   ```

   Don't forget to import your helper function at the top of each file you use it in.

4. **Writing useful detail strings for updates.** This is the hardest part of the challenge. `"Updated task 7"` is useless to someone reading the log. `"Changed status from 'open' to 'completed', priority from 'medium' to 'high'"` tells you exactly what happened.

   The trick: read the **old values before running the UPDATE query**, then compare them with the new values:

   ```python
   # 1. Read the current row BEFORE updating
   old = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

   # 2. Run your UPDATE query as normal
   conn.execute("UPDATE tasks SET status = ?, ... WHERE id = ?", (new_status, ..., task_id))
   conn.commit()

   # 3. Build the detail string by comparing old and new
   changes = []
   if old["status"] != new_status:
       changes.append(f"status: '{old['status']}' -> '{new_status}'")
   if old["priority"] != new_priority:
       changes.append(f"priority: '{old['priority']}' -> '{new_priority}'")
   detail = "Changed " + ", ".join(changes) if changes else "No fields changed"

   # 4. Log it
   log_action(session["user_id"], "update", "task", task_id, detail)
   ```

   > **Why not just log all the new values?** Because "status: completed, priority: high" doesn't tell you what *changed*. Maybe the priority was already high and only the status changed. The "old -> new" format makes the log actually useful for debugging.

5. **New route and template:** Create `routes/audit.py` using the Blueprint starter template from the top of this document. One route: `GET /audit` — admin-only. Returns the most recent 100 log entries, newest first, with the user's name joined from the users table:

   ```python
   @audit_bp.route("/audit")
   @login_required
   @role_required("admin")
   def audit_log():
       conn = get_db()
       logs = conn.execute("""
           SELECT a.*, u.full_name
           FROM audit_log a
           JOIN users u ON a.user_id = u.id
           ORDER BY a.created_at DESC
           LIMIT 100
       """).fetchall()
       conn.close()
       return render_template("audit.html", logs=logs)
   ```

   > **Why `JOIN users`?** The audit table stores `user_id` (a number like `3`). That's meaningless on screen. The JOIN brings in the user's `full_name` so you can display "Jane Smith" instead of "3". This is the same pattern used in `routes/tasks.py` where it joins `users` to get the assigned user's name.

   Register the Blueprint in `app.py`.

6. **Template:** Create `templates/audit.html`. Extend `base.html` and display the log as a table with columns: Date, User, Action, Type, Detail. No edit or delete buttons — this is a read-only view:

   ```html
   {% extends "base.html" %}
   {% block content %}
   <h1>Audit Log</h1>
   <table>
       <thead>
           <tr>
               <th>Date</th>
               <th>User</th>
               <th>Action</th>
               <th>Type</th>
               <th>Detail</th>
           </tr>
       </thead>
       <tbody>
           {% for log in logs %}
           <tr>
               <td>{{ log.created_at }}</td>
               <td>{{ log.full_name }}</td>
               <td>{{ log.action }}</td>
               <td>{{ log.entity_type }}</td>
               <td>{{ log.detail }}</td>
           </tr>
           {% endfor %}
       </tbody>
   </table>
   {% endblock %}
   ```

7. **Navigation:** Add an "Audit Log" link in `templates/base.html`'s navigation, visible to admin only. Look at how other nav links are conditionally shown — add yours using the same `{% if %}` pattern:

   ```html
   {% if session.role == "admin" %}
       <a href="{{ url_for('audit.audit_log') }}">Audit Log</a>
   {% endif %}
   ```

**Common mistakes:**
- Forgetting to register the new Blueprint in `app.py` — every request to `/audit` returns 404 and you'll spend ages trying to debug the route when the problem is in `app.py`
- Calling `log_action()` before `conn.commit()` — you log an action that might never succeed
- Forgetting to delete your database file and re-seed after adding the new table — the existing `mj_limited.db` doesn't have the `audit_log` table. Run `rm mj_limited.db && python seed_data.py`
- Joining the wrong column — you need `JOIN users u ON a.user_id = u.id`, not `ON a.id = u.id`
- Forgetting to import `log_action` in each route file where you use it — you'll get a `NameError` at runtime on the first create/update/delete

**How to test it:**
1. Delete your database and re-seed: `rm mj_limited.db && python seed_data.py`. Start the server.
2. Log in as `admin` / `admin123`. Create a new task. Navigate to the Audit Log page. You should see one entry: "Created task: [your title]".
3. Edit that task's status. The log should show a second entry with the old and new status values.
4. Delete the task. The log should show a third entry.
5. Log out. Log in as `j.smith` / `staff123`. Try navigating to `/audit` — you should be redirected away. This proves the decorator protection works.
6. While logged in as `j.smith`, update one of your assigned task's status. Log back in as admin and check the audit log — the staff user's action should appear with their name.

**You're done when:**
- [ ] Creating, editing, or deleting any task/client/attachment produces a log entry
- [ ] Admin can view the log page with a table of recent actions
- [ ] Each entry shows who, what, when, and a useful description of the change
- [ ] Update entries show the old and new values, not just "updated"
- [ ] Non-admin users cannot access the audit page (redirected away)
- [ ] Deleting the database and re-seeding creates a clean empty audit log

---

## Challenge 4: User Management

**What you're building:** A full CRUD interface for admin users to create, edit, and delete user accounts — including setting roles, departments, and passwords.

> **What you'll learn:**
> - How to build a complete Create/Read/Update/Delete feature by replicating an existing pattern in the codebase
> - How **password hashing** works and why you never store passwords in plain text
> - How to handle **referential integrity** — what happens when you try to delete a user who has tasks assigned to them?
> - How to add safety checks that prevent an admin from accidentally locking themselves out

**Why it matters:** The system currently has 8 users hardcoded in `seed_data.py`. In a real deployment, the admin needs to add new starters, change roles when people get promoted, and remove leavers. Without this, every user change requires a developer to edit code and re-run the seed script. This is the most complex challenge — it combines everything from the previous three into one feature.

**Study these files first:**
- `seed_data.py` — shows how users are created with `generate_password_hash()`. This is the function you'll use in your create route
- `routes/clients.py` — **this is your primary template**. It has the full CRUD pattern (create, read, update, delete with validation) that you'll replicate for users. Read through it carefully — your `routes/users.py` will follow the same structure
- `templates/clients.html` — the template pattern you'll replicate. It has a table, create/edit dialog modals, and delete confirmation. Your `users.html` will be a modified copy

**Steps:**

1. **New Blueprint: `routes/users.py`**

   Create a new file using the Blueprint starter template from the top of this document. Four routes, all admin-only:

   | Method | Path | Purpose |
   |---|---|---|
   | GET | `/users` | List all users |
   | POST | `/users/create` | Create a new user |
   | POST | `/users/<id>/edit` | Update an existing user |
   | POST | `/users/<id>/delete` | Delete a user |

   Register it in `app.py`: `app.register_blueprint(users_bp)`

   You'll need this import at the top of your new file:
   ```python
   from werkzeug.security import generate_password_hash
   ```

   > **What does `generate_password_hash()` do?** It takes a plain text password like `"admin123"` and turns it into a long scrambled string like `"scrypt:32768:8:1$..."`. This is called "hashing". The crucial property: you can check whether a password matches a hash (using `check_password_hash()`), but you can't reverse a hash back into the original password. So even if someone steals the database, they don't get anyone's actual password. Look at `routes/auth.py` to see `check_password_hash()` in action.

2. **POST `/users/create` — Create:**

   Required fields: `username`, `password`, `full_name`, `email`, `role`, `department`

   Validation rules (check all of them before returning — same pattern as task/client creation):
   - All fields are required — collect all errors into a list, then flash them all at once
   - `username` must be unique — query the database with `SELECT id FROM users WHERE username = ?` before inserting
   - `role` must be one of `admin`, `manager`, `staff` — validate in Python for a clear error message (the database CHECK constraint would also reject bad values, but its error message is cryptic)
   - Hash the password before storing: `generate_password_hash(password)`
   - Never store the plain text password anywhere — not in the database, not in a log, not in a flash message

3. **POST `/users/<id>/edit` — Update:**

   Allow changing: `full_name`, `email`, `role`, `department`

   Two important decisions:

   - **Password changes** — handle separately. If a `password` field is included in the form **and is not empty**, hash and update it. If it's empty, leave the existing password unchanged. This way, an admin can edit a user's name without accidentally resetting their password.

     ```python
     password = request.form.get("password", "").strip()
     if password:
         hashed = generate_password_hash(password)
         # include password_hash in your UPDATE query
     else:
         # don't include password_hash in the UPDATE — leave it unchanged
     ```

   - **Self-protection** — an admin should not be able to change their own role away from admin. If they did, they'd lock themselves out of the admin panel with no way back (unless they edit the database directly). Check for this:

     ```python
     if user_id == session["user_id"] and new_role != "admin":
         flash("You cannot remove your own admin role", "error")
         return redirect(url_for("users.user_list"))
     ```

     > **Why is this necessary?** It seems obvious, but without this check, an admin could set their role to "staff" by accident. Once they reload the page, the Users link disappears and they can't undo it. This kind of "foot-gun prevention" is exactly what the examiner looks for under edge case handling.

4. **POST `/users/<id>/delete` — Delete:**

   Two safety checks before deleting:

   - **Self-deletion:** An admin cannot delete their own account. `if user_id == session["user_id"]` -> flash error and redirect.

   - **Referential integrity:** The user might have tasks assigned to them or attachments they uploaded. If you delete the user, those foreign keys would point to a user that no longer exists. You have three options:

     | Option | Approach | Difficulty |
     |--------|----------|------------|
     | **(a) Reject** | Refuse to delete if they have linked records. Flash a message explaining why. | Simplest |
     | **(b) Reassign** | Move their tasks to another user before deleting | Medium |
     | **(c) Nullify** | Set `assigned_to = NULL` on their tasks before deleting | Medium |

     Option (a) is recommended — it's the safest and simplest. The admin can manually reassign tasks first, then delete. This is the same pattern used by `delete_client()` in `routes/clients.py`.

     ```python
     task_count = conn.execute(
         "SELECT COUNT(*) FROM tasks WHERE assigned_to = ?", (user_id,)
     ).fetchone()[0]

     attachment_count = conn.execute(
         "SELECT COUNT(*) FROM attachments WHERE uploaded_by = ?", (user_id,)
     ).fetchone()[0]

     if task_count > 0 or attachment_count > 0:
         flash(f"Cannot delete: user has {task_count} task(s) and {attachment_count} attachment(s). Reassign them first.", "error")
         return redirect(url_for("users.user_list"))
     ```

5. **Template: `templates/users.html`**

   Copy `templates/clients.html` as your starting point and modify it. Here's what to change:

   **Page structure:**
   - Change the page title and heading from "Clients" to "Users"
   - Change the "Add Client" button to "Add User"

   **The form dialog:**
   - Replace the client form fields (company name, phone, industry, notes) with user fields: username, password, full name, email, role, department
   - Make the role field a `<select>` dropdown with three options: admin, manager, staff — not a free-text input
   - For the edit dialog: leave the password field blank by default. An empty password means "don't change the password"

   **The table:**
   - Change columns to Username, Full Name, Email, Role, Department, Actions
   - **Never display `password_hash`** — not even hidden. It shouldn't appear anywhere in the template

   > **Why copy `clients.html` instead of writing from scratch?** Because clients and users have the same pattern: a table of records with create, edit, and delete. Starting from a working example and modifying it is faster and produces more consistent code than starting from a blank file. This is how professional developers work — they find an existing pattern in the codebase and replicate it.

6. **Navigation:** Add a "Users" link in `templates/base.html`'s navigation, visible to admin only. Look at how other nav links are conditionally shown — yours follows the same pattern but checks for `session.role == "admin"` only (not manager).

**Common mistakes:**
- Forgetting to import `generate_password_hash` — you get a `NameError` at runtime when creating the first user
- Including `password_hash` in the template — always query with explicit column names: `SELECT id, username, full_name, email, role, department FROM users` (never `SELECT *`). If the hash appears in the page source, an examiner would flag it as a security issue
- Hashing an empty string when the admin doesn't change the password — `generate_password_hash("")` creates a valid hash for an empty password, meaning the user can't log in anymore. Always check `if password:` before hashing
- Forgetting to register the Blueprint in `app.py` — the route won't be found
- Forgetting `{% extends "base.html" %}` at the top of your template — the page will have no navigation bar or styling

**How to test it:**
1. Log in as `admin` / `admin123`. Navigate to the Users page.
2. **Create:** Click "Add User". Fill in: username `t.test`, password `test123`, full name `Test User`, email `test@mjlimited.co.uk`, role `staff`, department `IT`. Save. The new user should appear in the table.
3. **Verify login:** Log out. Log in as `t.test` / `test123`. You should see the staff view (only your own tasks). This confirms the password was hashed correctly.
4. **Edit:** Log back in as admin. Edit `t.test` — change role to `manager`. Save. Log out, log in as `t.test` again — you should now see the manager view with department tasks.
5. **Password reset:** Log in as admin. Edit `t.test` — leave all fields as they are but set password to `newpass`. Save. Log out, log in as `t.test` / `newpass` — should work. Try `test123` — should fail.
6. **Edit without password change:** Log in as admin. Edit `t.test` — change department but leave password blank. Save. Log in as `t.test` / `newpass` — should still work (password wasn't accidentally reset to empty).
7. **Self-protection:** While logged in as admin, try to change your own role to `staff`. You should get a flash error message.
8. **Delete blocked:** Try to delete a seeded user who has tasks (e.g., `j.smith`). You should get a flash error explaining they have linked tasks and attachments.
9. **Delete success:** Delete `t.test` (who has no tasks). Should succeed. The user should disappear from the table.
10. **Access control:** Log in as `m.jones` / `manager123`. Try navigating to `/users` — you should be redirected away.

**You're done when:**
- [ ] Admin can create a new user with a username, password, name, email, role, and department
- [ ] The new user can log in immediately with the credentials set by the admin
- [ ] Admin can edit any user's details (including resetting their password)
- [ ] Editing without typing a new password does not reset the password
- [ ] Admin can delete a user who has no linked tasks or attachments
- [ ] Deleting a user with linked tasks returns a clear flash error explaining why
- [ ] Admin cannot delete their own account or change their own role
- [ ] Non-admin users cannot see the Users page or access any user management route
- [ ] User-provided text is auto-escaped by Jinja2 (no manual escaping needed)
- [ ] Password hashes are never visible in page source or templates

---

## What the examiner is looking for

Each challenge demonstrates specific skills that map to the DPDD assessment criteria (see [EXAM-DECODER.md](EXAM-DECODER.md) for the full marking breakdown). Here's what the examiner would note when reviewing your extension work:

**Challenge 1 — CSV Export:**
- Uses `@role_required` to restrict access (Technical Audit 20%: access control)
- Sets correct HTTP headers for file downloads (Development 40%: HTTP semantics)
- Conditionally renders UI elements based on role using `{% if %}` (Development 40%: role-aware templates)
- Reuses an existing SQL query for a new purpose (Design 20%: code reuse)

**Challenge 2 — Server-Side Sortable Table:**
- Uses SQL `ORDER BY` for efficient database-level sorting (Development 40%: database proficiency)
- Validates column names against an allowlist to prevent SQL injection (Development 40%: security awareness)
- Uses query parameters to make sorted views bookmarkable (Development 40%: HTTP semantics)
- Generates dynamic links with Jinja2 `{% set %}` and `url_for()` (Development 40%: template logic)
- Integrates with existing filter controls without breaking them (Design 20%: feature integration)

**Challenge 3 — Audit Logging:**
- Extends the database schema with a new table and foreign key (Design 20%: database design)
- Captures old values before updates to generate meaningful change descriptions (Development 40%: data comparison logic)
- Writes a reusable helper function called from multiple route files (Development 40%: code reuse and DRY principle)
- Creates a new Blueprint with proper route registration (Development 40%: modular architecture)
- Restricts the audit viewer to admin only with `@role_required` (Technical Audit 20%: access control)

**Challenge 4 — User Management:**
- Hashes passwords before storage using Werkzeug (Technical Audit 20%: password security)
- Validates all inputs server-side, collecting all errors before responding with flash messages (Development 40%: input validation pattern)
- Prevents self-deletion and self-demotion with explicit safety checks (Development 40%: edge case handling)
- Checks referential integrity before deletion (Development 40%: data integrity)
- Excludes sensitive fields (`password_hash`) from templates (Technical Audit 20%: data exposure prevention)
- Replicates an existing CRUD pattern for a new entity, demonstrating understanding of the codebase's architecture (Design 20%: consistent design)
