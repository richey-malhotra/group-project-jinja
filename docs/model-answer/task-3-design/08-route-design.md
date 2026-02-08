# Design Artefact 8 — Route Design

## Overview

This document specifies every route in the application: the HTTP method, URL, required roles, form inputs, template rendered, and redirect target. It serves as the contract between the route handlers and the Jinja2 templates — a developer can build any page using ONLY this document, without reading the Python code.

> **📋 Student Scope**
>
> **Core — what you need:** The summary table (Section 1) listing every route with its method, URL, required role, and purpose. Plus error handling conventions (Section 3). This proves you planned the route structure before coding.
>
> **Stretch — what makes it exceptional:** This document shows two levels of detail on purpose. The summary table (Section 1) catalogues every route — that is the minimum for Distinction. The detailed specifications (Section 2) then zoom into the two most complex groups: authentication (session handling, password hashing) and tasks (RBAC-filtered queries, field-level restrictions). You do NOT need detailed specs for every route — pick the 2–3 that demonstrate the most interesting design decisions and let the summary table cover the rest.

---

## 1. Route Summary Table

| Method | URL | Roles Allowed | Returns | Purpose | Req ID |
|---|---|---|---|---|---|
| GET | `/login` | Public | HTML page | Show login form | FR-AUTH-01 |
| POST | `/login` | Public | Redirect | Authenticate user | FR-AUTH-01 |
| GET | `/logout` | All authenticated | Redirect | End session | FR-AUTH-04 |
| GET | `/dashboard` | All (filtered) | HTML page | Dashboard with stats + charts | FR-DASH-01 |
| GET | `/tasks` | All (filtered) | HTML page | List tasks | FR-TASK-02 |
| GET | `/tasks/<id>` | All (staff: own only) | HTML page | Task detail + attachments | FR-TASK-02 |
| POST | `/tasks/create` | Admin, Manager | Redirect | Create task | FR-TASK-01 |
| POST | `/tasks/<id>/edit` | Admin, Manager | Redirect | Update task (full) | FR-TASK-03 |
| POST | `/tasks/<id>/status` | All authenticated (staff: own only) | Redirect | Update status only | FR-TASK-04 |
| POST | `/tasks/<id>/delete` | Admin, Manager | Redirect | Delete task | FR-TASK-05 |
| GET | `/clients` | Admin, Manager | HTML page | List clients | FR-CLIENT-01 |
| POST | `/clients/create` | Admin, Manager | Redirect | Create client | FR-CLIENT-01 |
| POST | `/clients/<id>/edit` | Admin, Manager | Redirect | Update client | FR-CLIENT-02 |
| POST | `/clients/<id>/delete` | Admin only | Redirect | Delete client | FR-CLIENT-03 |
| POST | `/attachments/upload/<task_id>` | All authenticated | Redirect | Upload file | FR-ATT-01 |
| GET | `/attachments/download/<filename>` | All authenticated | File | Download file | FR-ATT-03 |
| POST | `/attachments/<id>/delete` | Uploader/Admin/Mgr | Redirect | Delete attachment | FR-ATT-03 |

### Why POST Instead of PUT/DELETE?

HTML forms only support `GET` and `POST` methods. Since this is a server-rendered application (no JavaScript-driven `fetch()` calls), all mutating operations use `POST` with descriptive URLs:

- **Create:** `POST /tasks/create`
- **Update:** `POST /tasks/5/edit`
- **Delete:** `POST /tasks/5/delete`

The URL makes the intent clear. This is the standard approach in Django, Rails, and Flask.

---

## 2. Detailed Route Specifications

### 2.1 Authentication

#### GET /login

Display the login form.

| Property | Value |
|---|---|
| **Auth Required** | No |
| **Template** | `login.html` |

If the user is already logged in (session exists), redirects to `/dashboard`.

---

#### POST /login

Process the login form submission.

| Property | Value |
|---|---|
| **Auth Required** | No |

**Form Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `username` | text | Yes | Username |
| `password` | password | Yes | Password |

**Success:** Set session → `302 Redirect → /dashboard`

**Error Handling:**

| Condition | Action |
|---|---|
| Missing fields | `flash("Username and password are required")` → redirect `/login` |
| Invalid credentials | `flash("Invalid username or password")` → redirect `/login` |

---

#### GET /logout

End the current session.

| Property | Value |
|---|---|
| **Auth Required** | Yes |

**Action:** Clear session → `302 Redirect → /login`

---

### 2.2 Tasks

#### GET /tasks

List tasks. **Filtered by role** — staff only see assigned tasks.

| Property | Value |
|---|---|
| **Auth Required** | Yes |
| **Roles** | All (data filtered) |
| **Template** | `tasks.html` |

**Query Parameters (via GET form):**

| Parameter | Type | Description |
|---|---|---|
| `search` | string | Search in title and description (LIKE %term%) |
| `status` | string | Filter by status value |
| `priority` | string | Filter by priority value |
| `department` | string | Filter by department |

**Template Context:**

| Variable | Type | Description |
|---|---|---|
| `tasks` | list | Filtered task records (with assigned_name and client_name joined) |
| `users` | list | All users (for assignment dropdown, admin/manager only) |
| `clients` | list | All clients (for linking dropdown, admin/manager only) |
| `role` | string | Current user's role (controls which UI elements render) |
| `filters` | dict | Current filter values (to preserve form state) |

**RBAC filtering behaviour:**

| Role | SQL WHERE clause | Template rendering |
|---|---|---|
| Admin | (none) | Create form + edit/delete buttons + all tasks |
| Manager | (none) | Create form + edit/delete buttons + all tasks |
| Staff | `WHERE assigned_to = ?` | Status dropdown only + own tasks |

---

#### POST /tasks/create

Create a new task.

| Property | Value |
|---|---|
| **Auth Required** | Yes |
| **Roles** | Admin, Manager only |

**Form Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | text | Yes | Task title |
| `description` | textarea | No | Detailed description |
| `status` | select | No | Default: "open" |
| `priority` | select | No | Default: "medium" |
| `department` | select | Yes | Department name |
| `assigned_to` | select | No | User ID |
| `client_id` | select | No | Client ID |
| `due_date` | date | No | Due date |

**Success:** Insert task → `flash("Task created successfully")` → `302 Redirect → /tasks`

**Error Handling:**

| Condition | Action |
|---|---|
| Missing title | `flash("Title is required")` → redirect `/tasks` |
| Invalid foreign key | `flash("Selected user not found")` → redirect `/tasks` |
| Staff user | `403 Forbidden` (decorator blocks before route runs) |

---

#### POST /tasks/\<id\>/status

Update task status — **staff only, own tasks only.**

| Property | Value |
|---|---|
| **Auth Required** | Yes |
| **Roles** | All authenticated |

**Form Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `status` | select | Yes | New status value |

**RBAC enforcement:**

| Check | Action |
|---|---|
| Staff + not own task? | `flash("You can only update tasks assigned to you")` → redirect |
| Valid status value? | If not, `flash("Invalid status")` → redirect |

**Success:** Update status → `flash("Task status updated")` → `302 Redirect → /tasks`

---

#### POST /tasks/\<id\>/edit

Update all task fields — **admin and manager only.**

| Property | Value |
|---|---|
| **Auth Required** | Yes |
| **Roles** | Admin, Manager only |

Same form fields as POST /tasks/create. Same validation. On success: `302 Redirect → /tasks`

---

#### POST /tasks/\<id\>/delete

Delete a task and its attachments.

| Property | Value |
|---|---|
| **Auth Required** | Yes |
| **Roles** | Admin, Manager only |

**Success:** Delete task + cascade attachments → `flash("Task deleted")` → `302 Redirect → /tasks`

---

### 2.3 Clients, Dashboard, and Attachments

The remaining routes follow the same patterns shown above. Key details:

| Route Group | Key RBAC Rule | Notable Behaviour |
|---|---|---|
| **Clients** (GET, POST create, POST edit, POST delete) | Admin and Manager can view/create/edit. DELETE is Admin-only. Staff get 403 Forbidden. | Cannot delete a client if tasks are linked — `flash("Cannot delete: X tasks linked")` → redirect |
| **Dashboard** (GET /dashboard) | All roles — but data is scoped by role | Admin: org-wide stats + 4 charts. Manager: dept-scoped stats + 3 charts. Staff: personal stats + 2 charts. Chart data is embedded in the template as JSON for Chart.js. |
| **Attachments** (POST upload, GET download, POST delete) | All authenticated can upload. Only the uploader, admin, or manager can delete. | Files renamed to UUID on upload. Max 5 MB enforced by `MAX_CONTENT_LENGTH`. Upload and delete redirect to task detail page (`/tasks/<id>`). Allowed extensions: pdf, doc, docx, xls, xlsx, csv, txt, png, jpg, jpeg, gif |

---

## 3. Error Handling Conventions

### Flash Messages

All user-facing errors use Flask's `flash()` mechanism:

```python
flash("Title is required", "error")      # Validation error
flash("Task created successfully", "success")  # Success confirmation
abort(403)                                 # RBAC rejection (role_required decorator)
```

The `base.html` template renders all flashed messages automatically:

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
    <article class="flash-{{ category }}">{{ message }}</article>
    {% endfor %}
{% endwith %}
```

### HTTP Status Codes

| Code | Meaning | Used When |
|---|---|---|
| 200 | OK | Successful GET (page rendered) |
| 302 | Found (Redirect) | After successful POST (PRG pattern) |
| 403 | Forbidden | Logged in but wrong role |
| 404 | Not Found | Resource doesn't exist |

### The PRG Pattern

Every successful POST follows **Post-Redirect-Get**:

1. Browser submits form (POST)
2. Server processes the request
3. Server responds with `302 Redirect → /target-page`
4. Browser follows redirect (GET)
5. Server renders the page with any flash messages

This prevents the "resubmit form?" warning when users refresh the page.

---

> **📝 Examiner Note:** This route design document demonstrates that the URL structure and access control were planned systematically — not invented during coding. Notice the POST-only approach for mutations (create, edit, delete) — this is because HTML forms only support GET and POST, so we use descriptive URL patterns instead of HTTP method semantics. The RBAC columns show that every route was considered through the lens of "who can access this?" The flash message conventions show consistency across the application. For the exam, this document is the bridge between design (Task 3) and implementation (Task 4) — it is the specification the developer codes against, and the specification the tester tests against.
