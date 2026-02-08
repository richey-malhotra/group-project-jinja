# Walkthrough

## Why Every Technical Decision Was Made

This document explains the reasoning behind the major technical decisions in the MJ Limited Staff Portal. It's not a description of what the code does — the code comments handle that. This is the **"why"** layer: why this architecture, why this pattern, why this trade-off.

**Jump to the question you have:**

- [Why Jinja2 templates instead of a JavaScript frontend?](#1-why-jinja2-templates-instead-of-a-javascript-frontend)
- [Why Flask and not Django?](#2-why-flask-and-not-django)
- [Why SQLite and not a "real" database?](#3-why-sqlite-and-not-a-real-database)
- [Why is access control enforced in two different places?](#4-why-is-access-control-enforced-in-two-different-places)
- [Why `create_app()` instead of just `app = Flask(__name__)`?](#5-why-create_app-instead-of-just-app--flaskname)
- [Why a separate file for every feature?](#6-why-a-separate-file-for-every-feature)
- [Why are uploaded files renamed to random strings?](#7-why-are-uploaded-files-renamed-to-random-strings)
- [Why session cookies instead of JWTs?](#8-why-session-cookies-instead-of-jwts)
- [Why POST-Redirect-GET instead of just rendering after POST?](#9-why-post-redirect-get-instead-of-just-rendering-after-post)

---

### 1. Why Jinja2 templates instead of a JavaScript frontend?

The system renders HTML on the server using Jinja2 templates. There is no JavaScript SPA, no `fetch()` cycle, no client-side DOM manipulation (except for Chart.js on the dashboard).

**Why not a JavaScript SPA (React, Vue, or vanilla JS)?** A separate JavaScript frontend adds significant complexity: a `fetch()` call for every data operation, `credentials: "include"` on every request, manual DOM construction with `document.createElement()`, manual XSS escaping with `escapeHtml()`, and a third line of RBAC defence (UI hiding) that must stay in sync with the server. For a T Level project, that's a lot of moving parts that can go wrong independently. With server-rendered templates, the page arrives fully formed — no JavaScript glue needed.

**But what about the two-language requirement?** The brief says students should use two programming languages. In this version, Python is the primary language doing the heavy lifting (routing, business logic, data access, authentication, template rendering). HTML with Jinja2 template syntax is the second language — it includes conditional logic (`{% if %}`, `{% for %}`), inheritance (`{% extends %}`), and expression evaluation (`{{ }}`). Jinja2 templates are not passive markup — they contain real programming logic that controls what the user sees based on their role. Additionally, JavaScript is used for Chart.js on the dashboard, providing a third language.

**The trade-off:** This architecture produces a simpler, more robust application — but it has less technical breadth than an API + SPA version. There is no client-server separation, no async JavaScript, and the RBAC system has two lines of defence instead of three. For students who want to demonstrate those additional skills, the [API version](https://github.com/richey-malhotra/group-project) of this model answer is available.

**Why this trade-off is worth it for most students:** The server-rendered approach eliminates entire categories of bugs. There's no CORS configuration, no cookie/session mismatch between frontend and backend, no "Failed to fetch" errors, no manual HTML escaping. Every page renders with the correct data and permissions because the server controls the output. This lets students focus on the business logic and the assessment criteria, not on debugging JavaScript async issues.

---

### 2. Why Flask and not Django?

| Factor | Flask | Django |
|--------|-------|--------|
| Learning curve | Minimal — a "hello world" is 5 lines | Steeper — project scaffolding, settings, apps, migrations |
| Boilerplate | Almost none — you add what you need | Substantial — admin panel, ORM, forms, middleware by default |
| Visibility | Every route, config, and middleware choice is explicit | Convention-over-configuration hides decisions |
| Database | Manual SQL (educational) | ORM abstracts SQL away (convenient but hides the learning) |
| Templates | Jinja2 built in — same syntax, same engine | Django templates — similar but slightly different syntax |

For this project, Flask's explicitness is the point. When a student writes `cursor.execute("SELECT * FROM tasks WHERE assigned_to = ?", (user_id,))`, they're learning SQL. Django's `Task.objects.filter(assigned_to=user_id)` is easier but teaches an ORM, not a database.

Flask also forces architectural decisions to be visible. The Blueprint registration in `app.py`, the decorator stack order in route files, the manual session management — these are all things Django handles automatically, which means Django projects don't demonstrate the student's understanding of those concepts.

---

### 3. Why SQLite and not a "real" database?

SQLite is a file-based database that ships with Python. No server to install, no credentials to configure, no connection strings to manage.

**For a prototype**, this is ideal. Running `python seed_data.py` creates a working database instantly. A student can delete `mj_limited.db` and re-seed from scratch in seconds. There's no setup barrier.

**The limitation** is concurrency. SQLite locks the entire database file on write. In production with multiple simultaneous users, this causes timeouts. PostgreSQL handles concurrent writes properly. But this project is a prototype — typically one user at a time during development and testing.

**Why raw SQL instead of an ORM?** Same reasoning as Flask over Django: educational visibility. Writing `CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, ...)` teaches database design. An ORM migration file does the same thing but obscures the SQL. For the assessment, the examiner wants to see that the student understands relational schema design, constraints, and queries — not that they can use a tool that generates SQL for them.

---

### 4. Why is access control enforced in two different places?

The role-based access control system enforces permissions at two separate layers:

1. **Backend decorators** (`@role_required("admin", "manager")`) — block the request before handler code runs
2. **Database query filters** (`WHERE assigned_to = ?` for staff) — ensure queries only return permitted data

In a JavaScript SPA version, there would be a third layer: frontend UI hiding (staff don't see the "Add Task" button). In this server-rendered version, the template itself handles UI hiding — but that's not a separate security layer, it's part of the server-side rendering. The `{% if %}` blocks in Jinja2 templates run on the server, so they're as trustworthy as the Python decorators.

**Why not just the backend decorator?** Because of data leakage. The decorator on `GET /tasks` confirms the user is authenticated and has the right role, but without a query filter, it returns ALL tasks — including ones assigned to other staff members. The user doesn't have a button to edit them, but they can see the data. For sensitive information (client details, task descriptions), that's a security failure.

**Why two layers instead of three?** In a JavaScript SPA, the frontend runs in the browser — the user controls it. Hiding a button with JavaScript is convenience, not security: the user can open DevTools and call the API directly. That's why an SPA needs server-side enforcement as a separate security layer.

In a Jinja2 application, the template runs on the server. The user never sees the raw template — they only see the rendered HTML output. An `{% if session.role == "admin" %}` block is enforced by the server before the page reaches the browser. You can't "bypass" it from DevTools because it never existed in the HTML. This means the template conditional and the decorator are both server-side — two lines of defence, both trustworthy.

This defence-in-depth approach is an industry pattern. Each layer compensates for failures in the other.

---

### 5. Why `create_app()` instead of just `app = Flask(__name__)`?

`app.py` uses `create_app()` rather than creating the Flask app at module level.

```python
# This project uses a factory
def create_app():
    app = Flask(__name__)
    # configure, register blueprints
    return app

# NOT this (common in tutorials)
app = Flask(__name__)
```

**Why it matters:**
- **Testability** — you can call `create_app()` with different configurations for testing vs production
- **Circular imports** — Blueprints import from `database.py`, not from `app.py`. If the app were a module-level global, Blueprints would need to import from `app.py`, and `app.py` imports Blueprints — circular dependency
- **Professional practice** — most production Flask applications use factories. The tutorial pattern (`app = Flask(__name__)` at module level) works for small scripts but breaks down as the application grows

---

### 6. Why a separate file for every feature?

Each feature has its own file in `routes/` and a corresponding template in `templates/`:

```
routes/auth.py       → login/logout
routes/tasks.py      → /tasks, /tasks/<id>
routes/clients.py    → /clients
routes/dashboard.py  → /dashboard
routes/attachments.py → file upload/download

templates/login.html
templates/tasks.html
templates/task_detail.html
templates/clients.html
templates/dashboard.html
```

**Why not put all routes in one file?** Because `app.py` would be 800+ lines long. That's unmaintainable — finding the bug in the client deletion handler means scrolling through authentication code, task code, dashboard code, and attachment code to find it.

Blueprints also enforce module boundaries. The authentication decorators (`login_required`, `role_required`) are defined in `auth.py` and imported by other modules. If you need to change how authentication works, you change one file.

**Each Blueprint is independently testable.** You can verify that `clients.py` correctly blocks staff access without loading the tasks or dashboard code.

---

### 7. Why are uploaded files renamed to random strings?

When a user uploads `quarterly-report.pdf`, the file is saved as `a3f7c8e21b4d4f6a9e3c5d8f2b7a1c4e.pdf` on the server. The original filename is stored in the database.

**Three security problems this solves:**

1. **Path traversal** — A malicious filename like `../../etc/passwd` could write outside the uploads folder. A UUID cannot contain `/` or `..`
2. **Filename collisions** — Two users uploading `report.pdf` would overwrite each other's files. UUIDs are unique
3. **Information leakage** — Filenames on the server file system could reveal business information to anyone with server access. UUIDs reveal nothing

**The trade-off:** The download endpoint must look up the original filename in the database to set the `Content-Disposition` header — so the user sees `quarterly-report.pdf` in their download dialog, not the UUID. This is a small complexity cost for a significant security benefit.

---

### 8. Why session cookies instead of JWTs?

The authentication system uses Flask's built-in session (a signed cookie) rather than JSON Web Tokens.

**Sessions:** Server generates a signed cookie containing the user ID and role. The browser sends it automatically with every request. The server validates the signature and reads the data.

**JWTs:** The server generates a token containing user data, signed with a secret key. The frontend stores it (usually in localStorage) and manually attaches it to every request via an `Authorization` header.

**Why sessions?**
- Flask has built-in session support — zero additional dependencies
- Cookies are sent automatically by the browser — no JavaScript needed to attach them
- `httponly` cookies cannot be accessed by JavaScript, reducing XSS impact
- Session invalidation is straightforward (clear the cookie)
- In a server-rendered application, cookies are the natural authentication mechanism — the browser sends them with every page request automatically

**Why not JWTs?**
- JWTs require manual token management in the frontend (store, attach, refresh)
- localStorage is accessible to any JavaScript on the page (XSS vulnerability)
- Token revocation is complex (JWTs are valid until they expire — you can't invalidate them server-side without maintaining a blacklist, which defeats the purpose of stateless tokens)
- For a single-server prototype with server-rendered pages, the "stateless" benefit of JWTs has no value
- JWTs are designed for API-to-API authentication, not browser-to-server page requests

---

### 9. Why POST-Redirect-GET instead of just rendering after POST?

When a user submits a form (e.g., creates a task), the server processes the form, then **redirects** the browser to a GET page instead of rendering a template directly. This is called the **Post-Redirect-GET (PRG) pattern**.

```python
# The pattern used in this project:
@tasks_bp.route("/tasks/create", methods=["POST"])
def create_task():
    # ... process form data ...
    flash("Task created successfully", "success")
    return redirect(url_for("tasks.task_list"))   # ← redirect, not render

# NOT this:
@tasks_bp.route("/tasks/create", methods=["POST"])
def create_task():
    # ... process form data ...
    return render_template("tasks.html", ...)      # ← dangerous
```

**Why redirect instead of render?**

Without the redirect, the browser's last request was a POST. If the user refreshes the page (F5 or Ctrl+R), the browser re-sends the POST — creating a duplicate task, client, or attachment. Worse, the browser shows a confusing "Confirm Form Resubmission" dialog.

With the redirect, the browser's last request is a GET. Refreshing the page just reloads the list — no duplicate data, no confusing dialogs.

**Why `flash()` instead of passing a success message to the template?** Because the redirect creates a new request — any variables you set during the POST handler are gone. Flask's `flash()` function stores a message in the session cookie, which survives the redirect and is displayed once on the next page load. It's designed specifically for this pattern.

This is an industry-standard pattern. Django, Rails, and every other server-rendered framework uses it for the same reason.


---

## Further Reading

These are the official documentation pages and tutorials for the technologies used in this project. Bookmark them — they are the same resources a professional developer would use day-to-day.

### Flask (Python Web Framework)
- [Flask Documentation](https://flask.palletsprojects.com/) — official docs covering routing, templates, sessions, and configuration
- [Flask Quickstart](https://flask.palletsprojects.com/quickstart/) — a short tutorial that builds a minimal Flask app from scratch
- [Flask Tutorial](https://flask.palletsprojects.com/tutorial/) — the official step-by-step tutorial that builds a blog application

### Jinja2 (Template Engine)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/) — the official reference for template syntax, filters, template inheritance, and macros
- [Jinja2 Template Designer](https://jinja.palletsprojects.com/templates/) — how to write templates using `{% block %}`, `{% extends %}`, `{{ variable }}`, and `{% for %}`
- [Flask: Templates](https://flask.palletsprojects.com/patterns/templateinheritance/) — how Flask uses Jinja2, including template inheritance and the `render_template()` function

### HTML Forms and HTTP
- [MDN: HTML Forms](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms) — how forms work, including GET vs POST, input types, and validation
- [MDN: HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods) — what GET and POST actually mean and when to use each one
- [MDN: HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — what 200, 302, 400, 401, 403, 404, 500 mean and when to return each one

### SQLite (Database)
- [SQLite Documentation](https://www.sqlite.org/docs.html) — official reference for SQL syntax, data types, and built-in functions
- [Python `sqlite3` Module](https://docs.python.org/3/library/sqlite3.html) — how Python connects to SQLite, including parameterised queries and cursor operations
- [SQLite Tutorial](https://www.sqlitetutorial.net/) — beginner-friendly guide covering SELECT, INSERT, UPDATE, DELETE, JOINs, and more

### Pico CSS (Stylesheet)
- [Pico CSS Documentation](https://picocss.com/docs) — the classless CSS framework used for styling, with examples of every component
- [Pico CSS GitHub](https://github.com/picocss/pico) — source code and release notes

### Chart.js (Data Visualisation)
- [Chart.js Documentation](https://www.chartjs.org/docs/) — how to create bar charts, pie charts, and other visualisations used on the dashboard
- [Chart.js Getting Started](https://www.chartjs.org/docs/latest/getting-started/) — a quick tutorial for your first chart

### Python
- [Python Documentation](https://docs.python.org/3/) — the official language reference
- [Python Tutorial](https://docs.python.org/3/tutorial/) — the official beginner's tutorial covering data structures, control flow, functions, and modules
- [Real Python](https://realpython.com/) — practical tutorials with clear explanations, covering Flask, SQLite, testing, and more

### Git
- [Git Documentation](https://git-scm.com/doc) — the official reference manual
- [GitHub: Git Handbook](https://docs.github.com/en/get-started/using-git/about-git) — a short introduction to version control concepts
- [Oh My Git!](https://ohmygit.org/) — an interactive game that teaches Git concepts visually
