# Task 5a: Test Plan & Test Cases

> **📋 Student Scope**
>
> **Core — what you need:** A test strategy (Section 1), 15–20 well-chosen test cases covering authentication, RBAC boundaries, and key functional features, plus a test summary table. Focus on tests that verify RESTRICTIONS — what users CANNOT do is as important as what they can. Each test case must trace to a requirement ID.
>
> **Stretch — what makes it exceptional:** This document shows the full stretch version: 47 test cases covering every permission boundary for all three roles (Sections 2–3), functional feature tests (Section 4), input validation and security tests including XSS and SQL injection (Section 5), a summary table (Section 6), and a bug log showing genuine bugs found during testing (Section 7). You don't need 47 tests — but 5 is too few. The sweet spot is enough to show you tested every role's boundaries, not just the happy path.

---

## 1. Test Strategy

### Approach
Testing follows a **black-box functional testing** approach — tests verify that the system behaves correctly from the user's perspective without examining internal code. Each test case traces to a specific functional requirement (FR-ID) from the requirements specification.

### Scope
| In Scope | Out of Scope |
|---|---|
| All FR and NFR requirements | Performance load testing |
| All three user roles (admin, manager, staff) | Automated CI/CD pipeline |
| RBAC permission boundaries | Cross-browser compatibility |
| Input validation | Penetration testing |
| Error handling | Accessibility audit |

### Test Data
The seed data provides:
- **Admin:** username `admin`, password `admin123`
- **Manager:** username `m.jones`, password `manager123`
- **Staff:** username `j.smith`, password `staff123`
- 5 clients, 10 tasks across departments, various statuses and priorities

---

## 2. Test Cases — Authentication

| TC-ID | Requirement | Test Description | Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-AUTH-01 | FR-AUTH-01 | Valid login with admin credentials | 1. Navigate to / 2. Enter `admin` / `admin123` 3. Click Sign In | Login succeeds, redirected to /dashboard, session cookie set | As expected | ✅ Pass |
| TC-AUTH-02 | FR-AUTH-01 | Valid login with manager credentials | 1. Enter `m.jones` / `manager123` 2. Click Sign In | Login succeeds, redirected to /dashboard | As expected | ✅ Pass |
| TC-AUTH-03 | FR-AUTH-01 | Valid login with staff credentials | 1. Enter `j.smith` / `staff123` 2. Click Sign In | Login succeeds, redirected to /dashboard | As expected | ✅ Pass |
| TC-AUTH-04 | FR-AUTH-01 | Login with wrong password | 1. Enter `admin` / `wrongpass` 2. Click Sign In | Flash error: "Invalid username or password" | As expected | ✅ Pass |
| TC-AUTH-05 | FR-AUTH-01 | Login with non-existent username | 1. Enter `nobody` / `pass123` 2. Click Sign In | Same flash error: "Invalid username or password" (prevents username enumeration) | As expected | ✅ Pass |
| TC-AUTH-06 | FR-AUTH-01 | Login with empty fields | 1. Leave both fields empty 2. Click Sign In | Flash error: "Username and password are required" | As expected | ✅ Pass |
| TC-AUTH-07 | FR-AUTH-04 | Access /tasks without login | 1. Clear cookies 2. Navigate to /tasks directly | Redirected to login page with flash: "Please log in to access this page" | As expected | ✅ Pass |
| TC-AUTH-08 | FR-AUTH-04 | Logout clears session | 1. Login as admin 2. Click Logout 3. Try to access /dashboard | Redirected to login page | As expected | ✅ Pass |

---

## 3. Test Cases — RBAC Permission Boundaries

These tests verify that role restrictions work correctly. They are the MOST IMPORTANT tests because RBAC failures are security vulnerabilities.

### 3.1 Task Permissions

| TC-ID | Requirement | Test Description | Role | Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|---|
| TC-RBAC-01 | FR-TASK-01 | Admin can create task | Admin | 1. Login as admin 2. Go to /tasks 3. Click "+ New Task" 4. Fill form 5. Submit | Task created, flash success, appears in list | As expected | ✅ Pass |
| TC-RBAC-02 | FR-TASK-01 | Manager can create task | Manager | 1. Login as m.jones 2. Go to /tasks 3. Click "+ New Task" 4. Fill form 5. Submit | Task created successfully | As expected | ✅ Pass |
| TC-RBAC-03 | FR-TASK-01 | **Staff CANNOT create task** | Staff | 1. Login as j.smith 2. Go to /tasks 3. Look for "+ New Task" button | Button does not exist in the page — template never renders it for staff | As expected — button absent | ✅ Pass |
| TC-RBAC-04 | FR-TASK-01, FR-AUTH-03 | **Staff CANNOT create task via direct POST** | Staff | 1. Login as j.smith 2. Submit `curl -X POST /tasks/create` with valid form data | 403 Forbidden — `@role_required("admin", "manager")` blocks the request | As expected — route blocks | ✅ Pass |
| TC-RBAC-05 | FR-TASK-02 | Staff sees ONLY own tasks | Staff | 1. Login as j.smith 2. Go to /tasks 3. Count visible rows | Only tasks assigned to j.smith are shown (not all 10 tasks) | As expected — 2 tasks visible | ✅ Pass |
| TC-RBAC-06 | FR-TASK-02 | Admin sees ALL tasks | Admin | 1. Login as admin 2. Go to /tasks | All 10 tasks visible | As expected | ✅ Pass |
| TC-RBAC-07 | FR-TASK-03 | Admin can update any task field | Admin | 1. Login as admin 2. Click Edit on a task 3. Change title, priority, assigned_to 4. Submit | All changes saved, flash success | As expected | ✅ Pass |
| TC-RBAC-08 | FR-TASK-04 | **Staff can update status of own task** | Staff | 1. Login as j.smith 2. Change status dropdown on own task | Status updated, flash success | As expected | ✅ Pass |
| TC-RBAC-09 | FR-TASK-04 | **Staff CANNOT access full edit route** | Staff | 1. Login as j.smith 2. POST to /tasks/1/edit with form data | 403 Forbidden — separate route restricted to admin/manager | As expected | ✅ Pass |
| TC-RBAC-10 | FR-TASK-04 | **Staff CANNOT update another user's task status** | Staff | 1. Login as j.smith (user_id=5) 2. POST to /tasks/<id>/status for task assigned to user_id=6 | Flash error: "You can only update tasks assigned to you" | As expected | ✅ Pass |
| TC-RBAC-11 | FR-TASK-05 | Admin can delete task | Admin | 1. Login as admin 2. Click Delete on a task 3. Confirm | Task deleted, flash success | As expected | ✅ Pass |
| TC-RBAC-12 | FR-TASK-05 | Manager can delete task | Manager | 1. Login as m.jones 2. Click Delete on a task 3. Confirm | Task deleted | As expected | ✅ Pass |
| TC-RBAC-13 | FR-TASK-05 | **Staff CANNOT delete task** | Staff | 1. Login as j.smith 2. Look for Delete button | Delete button not rendered. POST to /tasks/<id>/delete returns 403. | As expected | ✅ Pass |

### 3.2 Client Permissions

| TC-ID | Requirement | Test Description | Role | Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|---|
| TC-RBAC-14 | FR-CLIENT-01 | Admin can create client | Admin | 1. Login as admin 2. Go to /clients 3. Add client | Client created, flash success | As expected | ✅ Pass |
| TC-RBAC-15 | FR-CLIENT-01 | Manager can create client | Manager | 1. Login as m.jones 2. Go to /clients 3. Add client | Client created | As expected | ✅ Pass |
| TC-RBAC-16 | FR-CLIENT-05 | **Staff CANNOT access clients page** | Staff | 1. Login as j.smith 2. Navigate to /clients directly | 403 Forbidden. "Clients" link not in nav bar. | As expected | ✅ Pass |
| TC-RBAC-17 | FR-CLIENT-05 | **Staff CANNOT access clients via direct POST** | Staff | 1. Login as j.smith 2. POST to /clients/create with form data | 403 Forbidden — `@role_required` blocks | As expected | ✅ Pass |
| TC-RBAC-18 | FR-CLIENT-03 | Admin can delete client (no linked tasks) | Admin | 1. Login as admin 2. Create a new client 3. Delete it | Client deleted, flash success | As expected | ✅ Pass |
| TC-RBAC-19 | FR-CLIENT-03 | **Manager CANNOT delete client** | Manager | 1. Login as m.jones 2. Look for Delete button on clients | Delete button not rendered. POST returns 403. | As expected | ✅ Pass |
| TC-RBAC-20 | FR-CLIENT-04 | Admin cannot delete client with linked tasks | Admin | 1. Login as admin 2. Try to delete a client with tasks | Flash error: "Cannot delete client with X linked task(s)" | As expected | ✅ Pass |

### 3.3 Dashboard Permissions

| TC-ID | Requirement | Test Description | Role | Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|---|
| TC-RBAC-21 | FR-DASH-01 | Admin sees org-wide stats | Admin | 1. Login as admin 2. Go to /dashboard | Shows total across ALL departments + client count + staff count | As expected | ✅ Pass |
| TC-RBAC-22 | FR-DASH-01 | Manager sees dept-scoped stats | Manager | 1. Login as m.jones (Client Services dept) 2. Go to /dashboard | Shows totals for Client Services department ONLY | As expected | ✅ Pass |
| TC-RBAC-23 | FR-DASH-02 | Admin sees 4 charts | Admin | 1. Login as admin 2. Count charts on dashboard | 4 charts: by status, priority, department, workload | As expected | ✅ Pass |
| TC-RBAC-24 | FR-DASH-02 | Manager sees 3 charts | Manager | 1. Login as m.jones 2. Count charts | 3 charts: by status, priority, workload (no department chart) | As expected | ✅ Pass |
| TC-RBAC-25 | FR-DASH-02 | Staff sees 2 charts | Staff | 1. Login as j.smith 2. Count charts on dashboard | 2 charts: by status, by priority only (no department, no workload) | As expected | ✅ Pass |

---

## 4. Test Cases — Functional Features

| TC-ID | Requirement | Test Description | Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-FUNC-01 | FR-TASK-06 | Search tasks by title | 1. Login as admin 2. Type "update" in search box 3. Click Filter | Only tasks with "update" in title/description shown | As expected | ✅ Pass |
| TC-FUNC-02 | FR-TASK-07 | Filter tasks by status | 1. Login as admin 2. Select "In Progress" from status filter 3. Click Filter | Only in-progress tasks shown | As expected | ✅ Pass |
| TC-FUNC-03 | FR-TASK-07 | Filter tasks by priority | 1. Login as admin 2. Select "High" from priority filter | Only "High" priority tasks shown | As expected | ✅ Pass |
| TC-FUNC-04 | FR-TASK-07 | Filter tasks by department | 1. Login as admin 2. Select "Finance" from department filter | Only Finance department tasks shown | As expected | ✅ Pass |
| TC-FUNC-05 | FR-TASK-06+07 | Combined search and filter | 1. Search "report" + filter status "Open" 2. Click Filter | Only matching tasks shown | As expected | ✅ Pass |
| TC-FUNC-06 | FR-ATT-01 | Upload valid file | 1. Open a task detail 2. Upload a .pdf file (< 5MB) | File uploaded, flash success, appears in attachments list | As expected | ✅ Pass |
| TC-FUNC-07 | FR-ATT-02 | Upload invalid file type | 1. Try to upload a .exe file | Flash error: "File type not allowed" | As expected | ✅ Pass |
| TC-FUNC-08 | FR-ATT-02 | Upload file exceeding 5MB | 1. Try to upload a 10MB file | Error: request too large (413) | As expected | ✅ Pass |
| TC-FUNC-09 | FR-ATT-03 | Download attachment | 1. Click Download on an attachment | File downloads with original filename | As expected | ✅ Pass |

---

## 5. Test Cases — Input Validation

| TC-ID | Requirement | Test Description | Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-VAL-01 | NFR-USAB-01 | Create task with empty title | 1. Login as admin 2. Open create form 3. Leave title empty 4. Submit | Flash error: "Title is required" | As expected | ✅ Pass |
| TC-VAL-02 | NFR-USAB-01 | Create client with empty company name | 1. Open create client form 2. Leave company_name empty 3. Submit | Flash error: "Company name is required" | As expected | ✅ Pass |
| TC-VAL-03 | NFR-USAB-01 | Multiple validation errors at once | 1. Submit task with empty title + empty department | Both errors flashed: "Title is required", "Department is required" | As expected | ✅ Pass |
| TC-VAL-04 | NFR-SEC-03 | XSS in task title | 1. Create task with title `<script>alert('xss')</script>` | Script tags rendered as text, not executed — Jinja2 auto-escapes | As expected — escaped | ✅ Pass |
| TC-VAL-05 | NFR-SEC-02 | SQL injection in search | 1. Search for `'; DROP TABLE tasks; --` | Search treats input as literal text, no SQL execution | As expected — parameterised | ✅ Pass |

---

## 6. Test Summary

| Category | Total Tests | Pass | Fail | Pass Rate |
|---|---|---|---|---|
| Authentication | 8 | 8 | 0 | 100% |
| RBAC Boundaries | 25 | 25 | 0 | 100% |
| Functional Features | 9 | 9 | 0 | 100% |
| Input Validation | 5 | 5 | 0 | 100% |
| **Total** | **47** | **47** | **0** | **100%** |

---

## 7. Bug Log

| Bug # | Found In | Description | Severity | Root Cause | Fix | Status |
|---|---|---|---|---|---|---|
| BUG-001 | TC-AUTH-07 | Accessing /tasks without login showed an error page instead of redirecting | Medium | `login_required` used `abort(401)` instead of `redirect()` | Changed to `redirect(url_for("auth.login"))` with flash message | Fixed |
| BUG-002 | TC-RBAC-04 | Staff could create tasks via direct POST to /tasks/create | Critical | Route had `@login_required` but no `@role_required` decorator | Added `@role_required("admin", "manager")` to create route | Fixed |
| BUG-003 | TC-RBAC-05 | Staff could see all tasks, not just own | High | GET /tasks query had no role-based WHERE clause | Added `WHERE assigned_to = ?` filter for staff role | Fixed |
| BUG-004 | TC-RBAC-10 | Staff could update status on any task | Critical | Status update route didn't verify task ownership | Added ownership check: `task["assigned_to"] == session["user_id"]` | Fixed |
| BUG-005 | TC-RBAC-19 | Manager could delete clients | Medium | Delete route used `@role_required("admin", "manager")` | Changed to `@role_required("admin")` — admin only | Fixed |
| BUG-006 | TC-FUNC-01 | Refreshing page after creating a task duplicated the task | High | Create route returned `render_template()` instead of `redirect()` | Applied PRG pattern: `return redirect(url_for("tasks.task_list"))` | Fixed |
| BUG-007 | TC-AUTH-04 | Flash messages not visible after login failure | Medium | `base.html` was missing `get_flashed_messages()` call | Added flash rendering block to base template | Fixed |

---

> **📝 Examiner Note:** The test plan demonstrates systematic testing with traceability back to requirements. The RBAC boundary tests (Section 3) are the strongest evidence of thorough testing — they verify not just "does the feature work?" but "does the RESTRICTION work?" Testing what users CAN'T do is as important as testing what they can. The bug log shows genuine development iteration — bugs were found, analysed, and fixed. Students should note that BUG-002 through BUG-005 were all RBAC failures, reinforcing why two lines of defence are necessary: decorator-level blocking AND query-level filtering.
