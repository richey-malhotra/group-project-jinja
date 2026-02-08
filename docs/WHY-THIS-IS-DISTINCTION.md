# Why This Model Answer Scores Distinction

## What This Document Is

You've read the model answer. You've walked through the commit history. You might be thinking: "It looks good, but *why* is it good? What specifically makes it Distinction-level instead of Merit or Pass?"

This document answers that question. It walks through each of the four assessment areas, shows you exactly where the Distinction-level evidence lives in this project, and — most importantly — explains **what pattern you should copy in your own work**.

> **This is not about copying content.** It's about understanding the *shape* of quality work so you can produce your own.

---

## The Four Assessment Areas

| Area | Weight | What It Rewards |
|------|--------|-----------------|
| Technical Audit & Analysis | 20% | Understanding the employer's problem and planning a solution |
| Design | 20% | Designing the system before building it |
| Development | 40% | Building a working, secure, well-structured application |
| Evaluation | 20% | Testing, documenting, and reflecting on your work |

Development is worth **double** the other areas. That's where most of your evidence needs to be.

---

## The One Thing That Separates Distinction from Everything Else

Before looking at each area individually, understand the single pattern that runs through the entire project: **traceability**.

Traceability means an examiner can pick *any* feature and follow it through every deliverable:

```
Fact file -> stakeholder need -> user story -> requirement ID -> design artefact -> code -> test case
```

Here's a concrete example. Pick the RBAC restriction "staff can only update the status of their own tasks":

| Deliverable | Where to find it | What it says |
|---|---|---|
| Fact file | `docs/DPDD Fact File.docx` | "Some staff will need to enter or update information" |
| Stakeholder need | `docs/model-answer/task-0-briefing/` | Identified as a role-based access requirement |
| Requirement | `docs/model-answer/task-2-requirements/` | FR-TASK-04 — "Staff users shall only update the status field" |
| Pseudocode | `docs/model-answer/task-3-design/` | Algorithm showing separate route for staff status updates |
| Code | `routes/tasks.py` — POST status route | Staff-only route that accepts only the status field |
| Test case | `docs/model-answer/task-5-testing/` | TC-RBAC-09 — "Staff navigates to task edit route and is redirected" |

**That chain is unbroken.** Every link references the one before it. This is not decoration — it's the evidence that proves you worked systematically.

Most student projects break this chain somewhere. The most common break is between design and code: they write requirements, then skip to building something slightly different. If the examiner can't trace a feature from requirement to test case, marks are lost — even if the feature works perfectly.

> **For your project:** Before you submit, pick three features and try to trace each one from fact file to test case. If you can't, you have a gap to fill.

---

## Technical Audit & Analysis (20%)

### What this area rewards

Understanding the employer's problem deeply enough to plan a solution — not just listing what they want, but explaining *why* they need it and *how* you'll deliver it.

### What the model answer does

| Evidence | Where to find it | Why it scores Distinction |
|---|---|---|
| Problem analysis | `task-0-briefing/` | Every problem is connected to a **business impact**, not just listed. "Staff use shared spreadsheets" -> "this causes version conflicts and data loss" |
| Stakeholder identification | `task-0-briefing/` | **Five** stakeholder groups, including indirect users (clients). Each has specific needs, not generic ones |
| Project plan | `task-1-planning/` | 105-hour schedule matching the brief's phase allocation. Gantt chart. Risk register with 8 specific risks |
| MoSCoW prioritisation | `task-1-planning/` | Explicitly says what's **out of scope** (CSV export, audit trail) with justification for why — shows you've *chosen* what to build, not just built everything you could think of |
| Technology choices | `task-1-planning/` | Every choice has a reason connected to a project constraint: "Flask over Django because the project is small and we need readable code, not a large framework" |
| Requirements specification | `task-2-requirements/` | 25+ functional requirements with **traceable IDs** (FR-AUTH-01, FR-TASK-01, etc.). Each links to a user story and a business need from the fact file |
| Non-functional requirements | `task-2-requirements/` | 12 NFRs covering security, performance, accessibility, and maintainability — shows breadth of thinking |

### What most students do instead (and why it scores lower)

- **List problems without connecting them to business impacts.** "They use spreadsheets" is an observation. "They use spreadsheets, which causes version conflicts when two staff edit the same data" is analysis.
- **Write requirements without traceable IDs.** If your requirements are a bullet list with no IDs, you can't reference them in your design, your code comments, or your test cases. The traceability chain breaks at step one.
- **State technology choices without justification.** "I used Flask" is a fact. "I chose Flask over Django because the project scope is small and Flask's explicit routing makes the code easier to understand for a small team" is a justified decision.
- **Skip the risk register.** A project plan without risks says "nothing will go wrong" — which tells the examiner you haven't thought about it.

---

## Design (20%)

### What this area rewards

Proving you designed the system *before* you built it — and that your design connects to your requirements and translates into your code.

### What the model answer does

This project includes **nine** distinct design artefacts. Most students produce three or four.

| # | Artefact | Where to find it | Why it matters |
|---|---|---|---|
| 1 | System architecture | `task-3-design/` | Shows three-layer architecture (routes, database, templates) and how components interact — not just what exists, but how data flows between them |
| 2 | Functional decomposition | `task-3-design/` | Breaks the system into modules. Every leaf node has a **FR-ID reference** — traceability from design back to requirements |
| 3 | Data flow diagrams | `task-3-design/` | Level 0 context diagram AND Level 1 process breakdown. Shows how data moves through the system |
| 4 | ERD + data dictionary | `task-3-design/` | Entity-relationship diagram with all 4 tables, relationships, and cardinality. **Plus** a data dictionary showing every column's type, constraints, and purpose. The ERD directly matches `database.py` — you can verify this yourself |
| 5 | Wireframes + screen flow | `task-3-design/` | Wireframes show **role variants** — the same page looks different for admin, manager, and staff. Screen flow diagram shows navigation between pages |
| 6 | Sequence diagrams | `task-3-design/` | Shows runtime behaviour including the Post-Redirect-GET pattern and RBAC rejection flows — not just what happens when things work, but what happens when access is denied |
| 7 | Pseudocode | `task-3-design/` | Algorithms with plain-English explanations. Includes the `@login_required` decorator, the `@role_required` decorator, and the staff status-update restriction. These translate almost line-for-line into the Python code |
| 8 | Route design | `task-3-design/` | Summary table of every URL pattern, plus detailed specs for the most complex routes (auth + tasks). Includes RBAC rules, form fields, redirect targets, and flash messages |
| 9 | Design justifications | `task-3-design/` | "I chose X over Y because Z" format — acknowledges trade-offs, connects choices to project constraints |

### The key thing most students miss

**Your design should match your code.** If your ERD shows four tables but your database has five, or your wireframe shows a button that doesn't exist, the examiner notices. It tells them you designed after building (or didn't update your design).

In this model answer:
- The ERD has 4 tables -> `database.py` creates exactly 4 tables with the same columns
- The pseudocode for the staff status restriction -> `routes/tasks.py` implements it with a separate POST route for staff
- The wireframes show staff seeing a status dropdown instead of a full edit form -> `templates/tasks.html` renders exactly that with `{% if %}` conditionals

> **For your project:** After you've built everything, go back to your design documents and check they still match your code. Update them if they don't.

---

## Development (40%)

This is worth double the other areas. This is where the project is strongest.

### What this area rewards

Building a working, secure, well-structured application using two programming languages — with clean code, proper error handling, and evidence of a development process.

### Two languages, both doing real work

The specification requires two programming languages. The key word is *both doing real work*:

| Language | What it does in this project | Not just... |
|---|---|---|
| **Python** (Flask) | 5 route modules with business logic, authentication, RBAC enforcement, database access, input validation, template rendering, file security, error handling | ...a "Hello World" route |
| **Jinja2 / HTML** | Template inheritance (`{% extends %}`), conditional rendering (`{% if session.role == "admin" %}`), iteration (`{% for task in tasks %}`), expression evaluation (`{{ task.title }}`), role-based UI, flash message display | ...static HTML with no logic |

Additionally, **JavaScript** is used for Chart.js rendering on the dashboard — a third language providing data visualisation.

If one of your languages only does trivial work, the examiner will notice. Both need to demonstrate genuine programming — conditional logic, data processing, error handling, and user interaction.

### Two lines of defence — the technical centrepiece

The access control system is the single feature that most clearly demonstrates Distinction-level thinking, because it works at two independent layers:

| Layer | What it does | Where to find it | What happens if you skip it |
|---|---|---|---|
| **1. Backend decorators** | `@role_required('admin', 'manager')` blocks unauthorised requests and redirects users away | `routes/auth.py` | Anyone can submit a form directly to your route URL and bypass your template restrictions |
| **2. Database queries** | SQL WHERE clauses filter data by role — staff only see their own tasks | `routes/tasks.py`, `routes/dashboard.py` | A staff user navigating to the tasks page would see everyone's data |

In this server-rendered architecture, the Jinja2 template conditionals (`{% if session.role == "admin" %}`) are part of the server-side rendering — they run on the server, not in the browser. This means they're as trustworthy as the Python decorators themselves, unlike JavaScript UI hiding which can be bypassed via DevTools.

**Layer 1 is the one most students miss.** It's easy to wrap content in `{% if %}` blocks, but if you don't also block the POST route with a decorator, the "restriction" is incomplete — someone could craft a direct POST request (e.g., using `curl`) and bypass the template entirely. This project blocks at the server first and filters data second.

The staff field-restriction is handled differently from the API version: instead of checking which fields a staff user is trying to change, there's a **separate route** for staff status updates. Staff can only access the status-update route, not the full edit route. This is a simpler, more robust approach — there's no way to accidentally expose fields because the full edit route is a completely different function with its own decorator.

### Security beyond the minimum

| Security measure | Where to find it | Why it matters |
|---|---|---|
| Password hashing (scrypt) | `seed_data.py`, `routes/auth.py` | Passwords are never stored as plain text |
| Username enumeration prevention | `routes/auth.py` login route | Same error message for "user not found" and "wrong password" — attackers can't discover valid usernames |
| HttpOnly session cookies | `app.py` | JavaScript can't read the session cookie — prevents cookie theft via XSS |
| Parameterised SQL queries | Every route file | Prevents SQL injection — no string concatenation in queries |
| Jinja2 auto-escaping | All templates | Prevents cross-site scripting (XSS) automatically — no manual `escapeHtml()` function needed |
| UUID file renaming | `routes/attachments.py` | Uploaded files get random names — prevents path traversal attacks |
| File extension allowlist | `routes/attachments.py` | Only specific file types (pdf, docx, etc.) are accepted |
| Upload directory outside `static/` | `uploads/` folder | Uploaded files aren't served statically — they go through a controlled download endpoint |
| Post-Redirect-GET pattern | Every POST route | Prevents duplicate form submissions on browser refresh |

You don't need to implement every one of these, but you need more than just password hashing. Parameterised queries and server-side validation are essential — the examiner *will* check.

### Code quality — comments that explain *why*

Good code has comments. Distinction-level code has comments that explain *why*, not just *what*:

```python
# Bad (what):
# Check if user is admin
if session['role'] == 'admin':

# Good (why):
# Only admin can delete users — managers can edit but not remove,
# preventing accidental loss of staff accounts and their linked tasks
if session['role'] == 'admin':
```

Throughout this project, comments explain the reasoning behind decisions. This tells the examiner you understood what you were building, not just that you made it work.

### Commit history — proving your process

The 24 development commits follow a deliberate order:

| Phase | Commits | What they show |
|---|---|---|
| Setup | 1 | Professional project foundation before any content |
| Analysis & planning | 2-4 | Understanding the problem, planning the solution, specifying requirements |
| Design | 5-13 | Designing **nine** artefacts before writing code |
| Development | 14-21 | Building one feature at a time, each commit adding a working piece |
| Testing & evaluation | 22-24 | Testing against requirements, writing documentation, reflecting |

**Thirteen commits happen before any code is written.** That's more than half the development process dedicated to understanding, planning, and designing.

If your commit history shows two planning commits followed by twenty coding commits, that tells the examiner your process was unbalanced — even if your final code is good.

> **For your project:** Plan your commits before you start. Write a list of what each commit will contain, in what order. Make it tell a story of systematic development.

---

## Evaluation (20%)

### What this area rewards

Evidence that you tested your system properly, documented it for both users and developers, and reflected honestly on the process.

### Test cases that prove restrictions work

This project has **47 test cases**, but the ones that score highest are the **25 RBAC boundary tests**. These don't test "does the feature work?" — they test "does the *restriction* work?":

| Test ID | What it tests | Why it matters |
|---|---|---|
| TC-RBAC-04 | Staff submits a direct POST request to the task creation route | Proves server-side enforcement, not just template hiding |
| TC-RBAC-09 | Staff navigates to the task edit route and is redirected | Proves route-level access control via separate routes |
| TC-RBAC-15 | Staff navigates to `/clients` and is redirected to tasks | Proves page-level access control |

Most students only test "happy paths" — what happens when things go right. Distinction-level testing also covers what happens when things go wrong, or when users try to do something they shouldn't.

Every test case has a **TC-ID that maps to a FR-ID** from the requirements. This closes the traceability chain: the requirement said the system should do X, and the test case proves it does.

> **For your project:** For every permission rule in your system, write a test case for someone *without* that permission trying to use it. If you have three roles, that's a lot of boundary tests — and that's exactly what scores well.

### Documentation for two audiences

| Document | Audience | What it covers |
|---|---|---|
| User guide | End users (MJ Limited staff) | Step-by-step instructions for every feature, in non-technical language. Includes a permissions table showing what each role can do |
| Technical documentation | Developers | Installation, configuration, architecture, route reference, security measures, known limitations |

Writing for two different audiences demonstrates communication skill. The user guide should never mention "route handlers" or "SQL queries". The technical documentation should never say "click the blue button".

### A reflective report that's specific, not generic

Compare these two reflective statements:

> "I learned a lot about web development during this project."

> "I discovered during testing (BUG-006) that submitting a form and then refreshing the page caused a duplicate task to be created. The browser was re-sending the POST request. I fixed this by implementing the Post-Redirect-GET pattern — after processing the form, the server redirects the browser to a GET request, so refreshing the page only reloads the list."

The second version names a specific bug, explains what went wrong, describes the fix, and shows what was learned. That's Distinction-level reflection.

---

## A Self-Check Checklist

Before you submit your own project, check these against your work:

### Traceability
- [ ] Every functional requirement has a unique ID (e.g., FR-AUTH-01)
- [ ] Every design artefact references requirement IDs
- [ ] Code comments reference the requirements they implement
- [ ] Every test case maps to a requirement ID
- [ ] You can trace any feature from fact file -> requirement -> design -> code -> test

### Technical Audit & Analysis
- [ ] Problems are connected to business impacts, not just listed
- [ ] At least three stakeholder groups identified with specific needs
- [ ] Technology choices are justified with reasons, not just stated
- [ ] Project plan includes a risk register with specific risks
- [ ] MoSCoW prioritisation explains what's out of scope and why

### Design
- [ ] ERD matches your actual database schema
- [ ] Wireframes show how different roles see different things
- [ ] Pseudocode translates recognisably into your actual code
- [ ] Route design lists every URL with methods, roles, and redirect behaviour
- [ ] You have at least one "chose X over Y because Z" justification

### Development
- [ ] Both languages do substantial work (not just static HTML with no logic)
- [ ] Passwords are hashed, not stored in plain text
- [ ] SQL queries use parameterised values, not string concatenation
- [ ] User input is validated on the server, not just assumed correct
- [ ] Access control is enforced with decorators, not just template conditionals
- [ ] Templates extend a base template for consistent layout
- [ ] Commit messages describe what changed and why
- [ ] Commits follow a logical order (plan -> design -> build -> test)

### Evaluation
- [ ] Test cases include what should *fail*, not just what should work
- [ ] Test case IDs map to requirement IDs
- [ ] User guide is written for non-technical users
- [ ] Technical documentation is written for developers
- [ ] Reflective report names specific problems and specific solutions

---

## "But Can I Actually Build This?"

You've just read through everything this model answer does. It's natural to look at nine design artefacts, five route modules, two lines of defence, 47 test cases, and think: *there's no way I can do all of that in 30 development hours.*

Here's the honest answer: **you can, because every individual piece is straightforward.** The complexity comes from the *combination*, not from any single part.

### Every technology was chosen to be beginner-friendly

| Technology | Why it's simpler than it looks |
|---|---|
| **Flask** | A route is a function with a decorator. If you can write a Python function, you can write a Flask route. No "magic" — every line of configuration is explicit. |
| **Jinja2** | If you can write `{% if %}` and `{% for %}`, you can build templates. It's just HTML with Python-like logic inserted. No build step, no compilation, no JavaScript toolchain. |
| **SQLite** | No database server to install. No connection strings. No Docker. It's a file. Python includes it out of the box. |
| **Chart.js** | Give it an array of labels and an array of numbers. It draws a chart. That's genuinely it. |

### The pattern repeats — learn it once, use it everywhere

Once you've built one CRUD module (say, tasks), the others follow the same structure:

```
1. Create a Blueprint          ->  tasks_bp = Blueprint('tasks', __name__)
2. Write a GET route (list)    ->  SELECT * FROM tasks WHERE ...
3. Write a GET route (detail)  ->  SELECT * FROM tasks WHERE id = ?
4. Write a POST route (create) ->  INSERT INTO tasks (...) VALUES (...)
5. Write a POST route (edit)   ->  UPDATE tasks SET ... WHERE id = ?
6. Write a POST route (delete) ->  DELETE FROM tasks WHERE id = ?
7. Add @role_required decorator ->  Copy from auth.py, change the role list
8. Create a Jinja2 template    ->  {% extends "base.html" %}, table, form
```

Clients, dashboard, and attachments all follow this same skeleton. You're not learning five different patterns — you're learning *one pattern* and applying it five times.

### The 30-hour budget is tight but realistic

Here's roughly how the hours break down for the development phase:

| Activity | Hours | Cumulative | Difficulty |
|---|---|---|---|
| Project setup (folders, app factory, base template) | 2 | 2 | Easy |
| Database schema + seed script | 3 | 5 | Easy |
| Login/logout + session handling | 4 | 9 | Moderate |
| Task CRUD (the biggest feature) | 6 | 15 | Moderate |
| Client CRUD (same pattern as tasks) | 4 | 19 | Easy — it's a repeat |
| Dashboard + charts | 3 | 22 | Moderate |
| File attachments | 3 | 25 | Moderate |
| RBAC enforcement + role-adaptive templates | 5 | 30 | Moderate-Hard |

The first 15 hours get you a working app with login and tasks. The second 15 hours add breadth and security. If you're running short on time, you still have a functional system at the halfway point.

### Where you can simplify without dropping below Merit

Not everything in this model answer is required for a strong grade. Here's what you could scale back:

| Model answer feature | Simpler alternative | Impact on grade |
|---|---|---|
| Two lines of RBAC defence | Backend decorators only (skip query-level filtering) | Still Merit+. The decorator is the critical line. |
| File attachments with UUID renaming | Drop file uploads entirely | Minor — it's a "nice to have" feature |
| Nine design artefacts | Five core ones: architecture, ERD, wireframes, pseudocode, route design | Still strong — quality over quantity |
| 47 test cases | 20 well-chosen test cases covering happy paths + key RBAC boundaries | Still strong — coverage matters more than count |
| Pico CSS + custom overrides | Pico alone with no custom CSS | Minimal impact — functionality matters more than visual polish |
| Post-Redirect-GET on every form | Render directly after POST (risk of duplicate submissions) | Minor mark loss — PRG is best practice but not required |
| Username enumeration prevention | Same error message for all login failures | Minor — this is a security refinement |

**The non-negotiables** — things you genuinely cannot skip and still score well:
- Two languages doing real work (Python backend + Jinja2 templates with logic)
- Some form of access control enforced on the server (not just template conditionals)
- Password hashing (never store plain text)
- Parameterised SQL (never concatenate user input into queries)
- Requirements with traceable IDs
- Test cases that reference those IDs
- A commit history that shows a logical process

### A team project means you share the load

This is a collaborative project. The model answer is written as if one person did everything, but in practice:
- One person builds authentication + RBAC
- One person builds task management
- One person builds client management + dashboard
- Everyone contributes to design and documentation

Flask Blueprints make this easy — each module is a separate file. You can work in parallel without merge conflicts as long as you agree on the database schema first.

### The bottom line

This model answer is at the top end of what's achievable. It's meant to be. But it's built entirely from simple, well-documented tools and repeating patterns. You don't need to match it feature-for-feature — you need to understand the *principles* it demonstrates (traceability, server-side security, both languages working hard, testing restrictions not just features) and apply them at whatever scale you can manage.

A smaller project that's well-connected and properly traced will outscore a larger project that's disorganised and untraceable. Every time.

---

## One Final Thought

This model answer isn't good because it's long. It's good because **every piece connects to every other piece**. The requirements trace to the design. The design traces to the code. The code traces to the test cases. The test cases trace back to the requirements.

That loop is what Distinction looks like. Not perfection — connection.

Your project doesn't need to be identical to this one. It needs to tell a connected story from problem to solution to proof. If you can do that, you're aiming at Distinction.
