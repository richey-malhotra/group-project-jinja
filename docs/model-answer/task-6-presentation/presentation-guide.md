# Task 6a: Presentation Guide

## Presenting the MJ Limited Business Task Manager

> **📋 Student Scope**
>
> **Core — what you need:** A clear structure (introduction → live demo → reflection), a live demo that shows the system RUNNING with at least two different roles, and confident answers to likely questions about your technology choices. Demo the restrictions, not just the features — showing a staff user being blocked is more impressive than showing an admin who can do everything.
>
> **Stretch — what makes it exceptional:** This document shows the full stretch version: a timed structure (Section 1), an introduction script (Section 2), a three-role demo sequence building from staff → manager → admin (Section 3), technical highlights including the RBAC proof (Section 4), and a reflection section with prepared answers to likely questions (Section 5). The RBAC proof — showing a staff user being blocked at both the template and route level — is the single most impressive thing you can do in a presentation.

---

### 1. Presentation Structure (15 minutes)

| Section | Time | Content |
|---|---|---|
| **Introduction** | 2 min | Problem statement, project scope, team roles |
| **Live Demo** | 6 min | Walk through the system as each role |
| **Technical Highlights** | 4 min | Architecture, RBAC, security decisions |
| **Reflection & Questions** | 3 min | What went well, what we'd improve, Q&A |

---

### 2. Introduction (2 minutes)

**Key points to cover:**
- MJ Limited is a business support services company with ~40 staff across 6 departments
- They currently manage tasks and client data using spreadsheets — error-prone, no access control, no overview
- Our system replaces this with a web application that provides task management, client tracking, and dashboards
- The system has **three user roles** (admin, manager, staff) with different levels of access — this is based on the fact file which describes different access needs for different staff types

**Opening line example:**
> "MJ Limited's staff were managing tasks and client information across disconnected spreadsheets. Our web application centralises this into one system with role-based access control, so each member of staff sees only what they need to see and can only do what they're authorised to do."

---

### 3. Live Demo (6 minutes)

#### Demo as Staff (2 min)
1. Log in as `j.smith` / `staff123`
2. **Show:** Page title says "My Tasks" — they see only their assigned tasks
3. **Show:** No "+ New Task" button — the button does not exist in the page source
4. **Show:** Navigation bar has only "Dashboard" and "Tasks" — no Clients link
5. **Demonstrate:** Change the status dropdown on a task → page reloads with flash "Task status updated"
6. **Explain:** "Staff can update the status of their own tasks — nothing else. The form only has a status dropdown because the route only accepts status changes."

#### Demo as Manager (2 min)
1. Log in as `m.jones` / `manager123`
2. **Show:** Dashboard with department-scoped statistics (Client Services department)
3. **Show:** 3 charts (no department chart — already filtered to their dept)
4. **Show:** Tasks page with "+ New Task" button and Edit/Delete controls
5. **Demonstrate:** Create a task, assign it to a staff member, see flash success message
6. **Show:** Clients page — can create and edit but NOT delete (no Delete button rendered)
7. **Explain:** "Managers oversee their department. They can manage tasks and clients, but only admins can delete client records."

#### Demo as Admin (2 min)
1. Log in as `admin` / `admin123`
2. **Show:** Dashboard with organisation-wide statistics + client count + staff count cards
3. **Show:** 4 charts including "Tasks by Department" (admin-only)
4. **Show:** All tasks visible, full CRUD access
5. **Demonstrate:** Try to delete a client with linked tasks → flash error with task count
6. **Explain:** "Admins have full system access. The system prevents accidental data loss — you can't delete a client that has linked tasks."

---

### 4. Technical Highlights (4 minutes)

#### RBAC Defence in Depth
> "Security is enforced across two lines of defence. The server-rendered templates control exactly what HTML each user receives — restricted buttons and forms are never sent to unauthorised users. But even if someone bypasses the template by submitting a POST request directly, the route decorator blocks it with 403 Forbidden. And as a safety net, database queries are filtered so a staff member's query only returns their own data."

**Live proof:** Right-click the page → "View Page Source" while logged in as staff:
- The "+ New Task" button does not appear in the HTML at all — the server never sent it
- The Edit and Delete buttons are absent from every table row
- The only form available is the status dropdown

**Alternative proof:** Use the terminal/curl to demonstrate:
```bash
curl -X POST http://localhost:5001/tasks/create -b "session=<staff-cookie>" -d "title=test"
```
→ Returns 403 Forbidden. The `@role_required("admin", "manager")` decorator blocks the request before any code runs.

#### Architecture
> "The system uses a server-rendered architecture. Flask generates complete HTML pages using Jinja2 templates — the browser receives finished pages, not JSON data. There's no separate JavaScript frontend to maintain, no async fetch calls to debug. The only JavaScript is Chart.js for dashboard charts."

#### Security
> "Every SQL query uses parameterised placeholders to prevent injection. Jinja2 auto-escapes all template variables to prevent XSS — we don't need a manual escaping function. Uploaded files are renamed with UUIDs to prevent path traversal. Passwords are hashed with scrypt — Werkzeug's memory-hard default with unique salts."

---

### 5. Reflection (3 minutes)

#### What went well
- RBAC was identified from the requirements stage (from the fact file's description of different access needs)
- Server-rendered architecture meant auto-escaping is built-in — XSS prevention is free
- Template inheritance (`base.html`) ensured consistent layout across all pages
- The PRG pattern prevented every double-submission bug before it could happen

#### What we'd improve
- **Database:** SQLite is fine for prototyping but would need PostgreSQL for production concurrent access
- **Testing:** Add automated tests (pytest) instead of only manual testing
- **Audit trail:** We identified FR-AUDIT-01 as a "Could Have" — with more time, we'd implement change logging
- **Real-time updates:** Currently users must refresh to see changes — WebSocket support would improve UX
- **Mobile support:** The server-rendered approach works well on mobile browsers, but a dedicated mobile app would need an API layer

#### Handling Questions

| Likely Question | Strong Answer |
|---|---|
| "Why not Django?" | "Flask gives us explicit control — we can see exactly how password hashing, SQL queries, and template rendering work. Django's ORM and auth system hide those details. For a learning project, understanding the mechanics matters more than convenience." |
| "Why not a React/SPA frontend?" | "Server-rendered is simpler — no async JavaScript, no state management, no build tools. Jinja2 auto-escapes XSS for free. The entire frontend is HTML templates and one small JS file for charts. For a team of DSD students, this reduces complexity without reducing functionality." |
| "Why SQLite?" | "Zero configuration, built into Python, perfect for prototyping. For production we'd migrate to PostgreSQL — only database.py would change." |
| "How does RBAC really work?" | "Two lines of defence: route decorators block the request, and database queries filter the data. Let me show you the page source — the restricted buttons don't even exist in the HTML." |
| "What if someone bypasses the frontend?" | "There's nothing to bypass — the server never sends restricted markup. But even if someone POSTs directly to a restricted route, the `@role_required` decorator blocks it before any code runs." |
| "How do you prevent SQL injection?" | "Every query uses parameterised placeholders — the ? symbol. The database driver treats user input as data, never as SQL code." |

---

> **📝 Examiner Note:** The presentation should demonstrate the RUNNING system, not just describe it. The role-based demo structure (staff → manager → admin) builds from least privilege to most, which tells a clear story. The "View Page Source" proof of RBAC is a powerful demonstration — it shows the examiner that restricted elements are never sent to the browser, not just hidden with CSS or JavaScript. The reflection section should be honest about limitations — examiners respect candidates who acknowledge what could be improved.
