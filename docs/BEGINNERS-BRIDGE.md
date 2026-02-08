# Beginner's Bridge

## From Classroom Python to This Codebase

If you've learned Python basics in class — variables, loops, functions, lists — but this project looks like a different language, that's normal. This document bridges what you already know to what you'll see in this codebase.

---

## How to Read a Route File

Every route file in this project follows the same pattern. Once you can read one, you can read them all. Here's the template:

```python
# 1. Imports
from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from database import get_db
from routes.auth import login_required, role_required

# 2. Create the Blueprint
example_bp = Blueprint("example", __name__)

# 3. GET route — display a page with data
@example_bp.route("/example")
@login_required
def example_list():
    conn = get_db()                          # Connect to database
    cursor = conn.cursor()
    rows = cursor.fetchall()                 # Get the data
    conn.close()
    return render_template("example.html",   # Render the template
                           items=rows)       # Pass data to the template

# 4. POST route — process a form submission
@example_bp.route("/example/create", methods=["POST"])
@login_required
@role_required("admin", "manager")           # Only these roles can create
def create_example():
    title = request.form.get("title", "").strip()  # Get what the form sent
    errors = []                                     # Collect validation errors
    if not title:
        errors.append("Title is required")
    if errors:
        for e in errors:
            flash(e, "error")                       # Show errors on the page
        return redirect(url_for("example.example_list"))
    # ... insert into database ...
    flash("Created successfully", "success")
    return redirect(url_for("example.example_list"))  # Redirect back to the list
```

Every file follows this order: imports, blueprint, GET routes, POST routes. The decorators (`@login_required`, `@role_required`) appear between the route decorator and the function definition.

If something in the code doesn't make sense, look for the comment directly above or beside it. Every non-obvious line in this project has a comment explaining what it does and why.

---

## Things You Already Know (Even If They Look Different)

This codebase looks more complex than classroom Python, but most of it uses the same building blocks. Two examples:

#### Variables

**What you learned:**
```python
name = "Alice"
age = 17
```

**Where it appears in this project:**
```python
# routes/auth.py
username = request.form.get("username")
password = request.form.get("password")
```

It's the same thing. `request.form.get("username")` just means "get the value called 'username' from the form the browser sent." The variable assignment works exactly like classroom Python.

---

#### Functions

**What you learned:**
```python
def greet(name):
    return f"Hello, {name}"
```

**Where it appears in this project:**
```python
# routes/dashboard.py
def _role_filter():
    role = session.get("role")
    user_id = session.get("user_id")
    department = session.get("department")

    if role == "staff":
        return " AND t.assigned_to = ?", [user_id]
    elif role == "manager":
        return " AND t.department = ?", [department]
    else:
        return "", []
```

A function that takes no parameters — it reads what it needs from `session` (the logged-in user's data). It returns **two things** (a string and a list) — Python lets you do that with a comma.

Everything else — `if`/`else`, `for` loops, lists, dictionaries — works identically to what you've used in class. When you see `errors = []` followed by `errors.append("Title is required")`, that's a list being built, same as always.

---

## New Concepts You'll Encounter

These aren't in the GCSE/classroom syllabus but they appear throughout this project. Each one is explained briefly — just enough to read the code.

---

#### Decorators (`@something` above a function)

```python
@app.route("/dashboard")
@login_required
@role_required("admin", "manager")
def dashboard():
    ...
```

A **decorator** is a function that wraps another function. Think of it as: "before running `dashboard()`, run these checks first — and only continue if they pass."

`@app.route("/dashboard")` means "when someone visits `/dashboard`, run this function."
`@login_required` means "but only if they're logged in."
`@role_required("admin", "manager")` means "and only if their role is admin or manager."

The arguments to `@role_required` are the roles that **are allowed**. Anyone else gets redirected away. You'll use this pattern in your own route files — put the decorator above any function, and list the roles that should have access.

---

#### `request.form`, `redirect`, and `flash`

```python
from flask import request, redirect, url_for, flash

# Getting form data (what the user typed)
title = request.form.get("title")

# Showing a message on the next page
flash("Task created successfully", "success")

# Sending the user to a different page
return redirect(url_for("tasks.task_list"))
```

`request.form` is the data from an HTML form submission (what the user typed into the fields).
`flash()` stores a one-time message that appears on the next page the user sees.
`redirect()` sends the browser to a different URL instead of rendering a page.
`url_for()` builds the URL from a function name so you don't have to hardcode paths.

This is the **Post-Redirect-GET pattern**: the user submits a form (POST), the server processes it and redirects (GET), and the new page shows a flash message confirming what happened. This prevents duplicate submissions if the user refreshes the page.

---

#### `render_template` and Jinja2

```python
from flask import render_template

@tasks_bp.route("/tasks")
def task_list():
    tasks = get_tasks_from_database()
    return render_template("tasks.html", tasks=tasks, user=session)
```

`render_template()` takes an HTML template file and fills in the blanks with data. The template uses Jinja2 syntax — special tags that Python processes before sending the HTML to the browser:

```html
<!-- Display a variable -->
<h1>Welcome, {{ user.full_name }}</h1>

<!-- Loop through a list -->
{% for task in tasks %}
    <tr><td>{{ task.title }}</td></tr>
{% endfor %}

<!-- Conditional display -->
{% if user.role == "admin" %}
    <button>Delete</button>
{% endif %}
```

The `{{ }}` tags output a value. The `{% %}` tags contain logic (if/for/extends). Everything between `{% for %}` and `{% endfor %}` repeats once for each item in the list — just like a Python `for` loop.

**Key safety feature:** Jinja2 automatically escapes special characters. If someone types `<script>alert('hacked')</script>` into a task title, Jinja2 renders it as harmless text, not as executable code. This prevents cross-site scripting (XSS) attacks without you having to do anything extra.

---

#### Template Inheritance (`{% extends %}`)

```html
<!-- templates/base.html — the shared layout -->
<html>
<body>
    <nav>...</nav>
    {% block content %}{% endblock %}
</body>
</html>

<!-- templates/tasks.html — a specific page -->
{% extends "base.html" %}
{% block content %}
    <h1>Tasks</h1>
    <table>...</table>
{% endblock %}
```

`{% extends "base.html" %}` means "use the base template as the outer wrapper." The `{% block content %}` tag defines a placeholder that each page fills with its own content. This way, the navigation bar, CSS links, and page structure are written once in `base.html` and shared by every page.

This is the same idea as functions in Python — write it once, use it everywhere. Without template inheritance, every page would repeat the full HTML structure, and changing the nav would mean editing every single file.

---

#### SQL (Database Queries)

```python
cursor.execute("SELECT * FROM tasks WHERE assigned_to = ?", (username,))
rows = cursor.fetchall()
```

SQL is how you talk to the database. The basic patterns:

| Operation | SQL | Python |
|-----------|-----|--------|
| Get all | `SELECT * FROM tasks` | `cursor.execute("SELECT * FROM tasks")` |
| Get one | `SELECT * FROM tasks WHERE id = ?` | `cursor.execute("...", (task_id,))` |
| Create | `INSERT INTO tasks (...) VALUES (?, ?)` | `cursor.execute("...", (title, status))` |
| Update | `UPDATE tasks SET status = ? WHERE id = ?` | `cursor.execute("...", (status, id))` |
| Delete | `DELETE FROM tasks WHERE id = ?` | `cursor.execute("...", (task_id,))` |

The `?` is a placeholder. The actual values go in a tuple after the query. **Never** put the values directly in the string — that's a security vulnerability called SQL injection. This:

```python
cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))  # SAFE
```

Not this:

```python
cursor.execute(f"SELECT * FROM tasks WHERE id = {task_id}")  # VULNERABLE
```

If `task_id` contains `1 OR 1=1`, the second version returns every row in the table. The parameterised version treats the entire input as a literal value — it can never be interpreted as SQL syntax. Every query in this project uses `?` placeholders for this reason.

---

#### HTML Forms

```html
<form method="POST" action="{{ url_for('tasks.create_task') }}">
    <label for="title">Title</label>
    <input type="text" name="title" id="title" required>

    <label for="status">Status</label>
    <select name="status" id="status">
        <option value="open">Open</option>
        <option value="in_progress">In Progress</option>
    </select>

    <button type="submit">Create Task</button>
</form>
```

Forms are how users send data to the server without JavaScript. The `method="POST"` means the form data is sent in the request body (not visible in the URL). The `name` attribute on each input matches the key you read in Python with `request.form.get("title")`.

The `action` attribute uses `url_for()` inside a Jinja2 tag — this generates the correct URL automatically, so you don't have to hardcode paths that might change.

---

#### Blueprints

```python
# routes/tasks.py
from flask import Blueprint
tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
def task_list():
    ...
```

A Blueprint is just a way to put routes in a separate file. Instead of `@app.route(...)` in `app.py`, you write `@tasks_bp.route(...)` in `routes/tasks.py`. Then in `app.py`:

```python
from routes.tasks import tasks_bp
app.register_blueprint(tasks_bp)
```

This keeps each feature in its own file. Without Blueprints, every route would be in `app.py` — hundreds of lines in one file.
