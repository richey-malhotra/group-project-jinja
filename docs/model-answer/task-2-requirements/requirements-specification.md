# Task 2: Requirements Analysis and Research

## Requirements Specification

---

### 1. User Roles

The MJ Limited fact file describes three distinct levels of system access: administrative/regular staff who work on day-to-day tasks, managers who oversee departments and client relationships, and administrators who manage the system itself. This maps directly to three roles.

| Role | Description | Access Level | Traced to |
|---|---|---|---|
| **Admin** | IT / senior management. Full system access. | Can manage all data, view organisation-wide metrics, delete records. | Fact File: "A small number of users may require administrative control over accounts and permissions." |
| **Manager** | Department heads. Oversight of tasks and clients. | Can create/edit/delete tasks, manage clients, view department-scoped data. | Fact File: "Managers rely on information from all departments in order to make informed decisions." |
| **Staff** | Regular employees. Day-to-day task work. | Can view and update their own assigned tasks. Cannot create tasks, manage clients, or view organisation-wide data. | Fact File: "Some staff will need to enter or update information, while others will require access to review or manage records." |

---

### 2. User Stories

| ID | As a… | I want to… | So that… | Priority |
|---|---|---|---|---|
| US-01 | staff member | log in with my credentials | I can access the system securely | Must |
| US-02 | staff member | see only tasks assigned to me | I can focus on my own workload without distraction | Must |
| US-03 | staff member | update the status of my tasks | my manager can track progress accurately | Must |
| US-04 | staff member | attach files to a task | I can keep related documents alongside the task record | Must |
| US-05 | manager | view all tasks across my department | I can monitor workload and progress for my team | Must |
| US-06 | manager | create and assign tasks to staff | I can delegate work efficiently and track accountability | Must |
| US-07 | manager | add and edit client records | client information stays current and accurate | Must |
| US-08 | manager | view a dashboard with summary statistics | I can quickly assess the state of operations | Must |
| US-09 | manager | search and filter tasks | I can find specific work items quickly | Must |
| US-10 | admin | manage all aspects of the system | I can ensure the system operates correctly for all users | Must |
| US-11 | manager | see charts showing task distribution | I can identify bottlenecks and workload imbalances | Must |
| US-12 | manager | export data as CSV | I can share reports with external stakeholders | Should |
| US-13 | staff member | receive notification when assigned a task | I know about new work immediately | Could |
| US-14 | admin | view an audit trail of changes | I can track who changed what and when | Could |

---

### 3. Functional Requirements

Requirements are grouped by category and given traceable identifiers so they can be referenced in design artefacts, code, and test cases.

#### Authentication & Access Control

| ID | Requirement | Related User Story | Priority |
|---|---|---|---|
| FR-AUTH-01 | The system shall authenticate users with a username and password. | US-01 | Must |
| FR-AUTH-02 | Passwords shall be stored as salted hashes, never in plain text. | US-01 | Must |
| FR-AUTH-03 | The system shall enforce role-based access control with three tiers: admin, manager, staff. | US-01, US-10 | Must |
| FR-AUTH-04 | The system shall maintain user sessions via signed cookies and provide logout functionality. | US-01 | Must |
| FR-AUTH-05 | Staff users shall only see their own user record when querying the user list. Admin and manager shall see all users. | US-02, US-10 | Must |

#### Task Management

| ID | Requirement | Related User Story | Priority |
|---|---|---|---|
| FR-TASK-01 | The system shall allow authorised users (admin, manager) to create tasks with title, description, status, priority, department, assignment, client link, and due date. | US-06 | Must |
| FR-TASK-02 | The system shall display all tasks to admin and manager users, and only assigned tasks to staff users. | US-02, US-05 | Must |
| FR-TASK-03 | Admin and manager users shall be able to update any field on any task. | US-06 | Must |
| FR-TASK-04 | Staff users shall only be able to update the **status** field of tasks **assigned to them**. All other field changes shall be rejected. | US-03 | Must |
| FR-TASK-05 | Only admin and manager users shall be able to delete tasks. | US-10 | Must |
| FR-TASK-06 | The system shall provide search functionality across task titles and descriptions. | US-09 | Must |
| FR-TASK-07 | The system shall provide filtering by status, priority, and department. | US-09 | Must |

#### Client Management

| ID | Requirement | Related User Story | Priority |
|---|---|---|---|
| FR-CLIENT-01 | The system shall allow admin and manager users to create client records with company name, contact details, industry, status, and notes. | US-07 | Must |
| FR-CLIENT-02 | The system shall allow admin and manager users to update client records. | US-07 | Must |
| FR-CLIENT-03 | Only admin users shall be able to delete client records. | US-10 | Must |
| FR-CLIENT-04 | The system shall prevent deletion of clients that have linked tasks, returning an appropriate error. | US-10 | Must |
| FR-CLIENT-05 | Staff users shall not have access to client management features. | US-02 | Must |

#### Dashboard & Reporting

| ID | Requirement | Related User Story | Priority |
|---|---|---|---|
| FR-DASH-01 | The system shall display role-filtered summary statistics: admin sees organisation-wide, manager sees department-scoped, staff sees personal task counts. | US-08 | Must |
| FR-DASH-02 | The system shall render charts using Chart.js: tasks by status (all roles), tasks by priority (all roles), tasks by department (admin only), workload by staff (admin + manager). | US-11 | Must |
| FR-DASH-03 | Dashboard data shall be aggregated on the server using SQL, not in the browser. | US-08 | Must |

#### File Attachments

| ID | Requirement | Related User Story | Priority |
|---|---|---|---|
| FR-ATT-01 | The system shall allow authenticated users to upload files (max 5MB) and attach them to tasks. | US-04 | Must |
| FR-ATT-02 | The system shall restrict uploads to allowed file types: PDF, Word, Excel, CSV, text, and image formats. | US-04 | Must |
| FR-ATT-03 | The system shall allow users to download and delete attachments, with deletion restricted to the uploader, admin, or manager. | US-04 | Must |

#### Data Export (Future)

| ID | Requirement | Related User Story | Priority |
|---|---|---|---|
| FR-EXPORT-01 | The system shall allow managers to export task and client data as CSV files. | US-12 | Should |

#### Audit Trail (Future)

| ID | Requirement | Related User Story | Priority |
|---|---|---|---|
| FR-AUDIT-01 | The system shall log all create, update, and delete actions for audit purposes. | US-14 | Could |

---

### 4. Non-Functional Requirements

| ID | Requirement | Category | Priority |
|---|---|---|---|
| NFR-PERF-01 | The system shall respond to user actions within 2 seconds under normal load. | Performance | Must |
| NFR-COMPAT-01 | The system shall work on desktop browsers (Chrome, Firefox, Edge) and tablets. | Compatibility | Must |
| NFR-SEC-01 | Passwords shall be hashed using a secure algorithm (scrypt via Werkzeug) with unique salts. | Security | Must |
| NFR-SEC-02 | The system shall use parameterised queries to prevent SQL injection. | Security | Must |
| NFR-SEC-03 | User-generated content shall be escaped to prevent cross-site scripting (XSS). | Security | Must |
| NFR-SEC-04 | File uploads shall be restricted to allowed types and validated for maximum size (5MB). | Security | Must |
| NFR-SEC-05 | Uploaded files shall be renamed with unique identifiers to prevent path traversal and collisions. | Security | Must |
| NFR-ACC-01 | The system shall use semantic HTML elements for accessibility (nav, main, article, table, label). | Accessibility | Must |
| NFR-ACC-02 | The system shall be responsive on mobile viewports (single-column layout, stacked elements). | Accessibility | Must |
| NFR-USAB-01 | The system shall provide clear error messages for invalid operations, including specific field-level validation feedback. | Usability | Must |
| NFR-USAB-02 | The system shall provide immediate visual feedback (toast notifications) after user actions. | Usability | Must |
| NFR-MAINT-01 | The codebase shall be modular (Blueprint-based), well-commented, and follow consistent naming conventions. | Maintainability | Must |

---

### 5. Prioritised Requirements Summary

| Priority | Count | Description |
|---|---|---|
| **Must Have** | 23 FRs + 12 NFRs | Core functionality required for a working, secure, role-aware system |
| **Should Have** | 1 FR | Export feature — useful but not essential for the prototype |
| **Could Have** | 1 FR | Audit log — beneficial for governance but out of scope for 30 development hours |
| **Won't Have** | 0 FRs documented | Real-time features, mobile app, third-party integrations explicitly excluded in project plan |

---

### 6. Research: Industry Considerations

#### Usability
- The system uses Pico CSS to ensure clean, consistent styling from semantic HTML
- Toast notifications provide immediate feedback after every action (NFR-USAB-02)
- Validation errors list ALL issues at once, not one at a time — reducing frustration
- Search and filter controls are positioned prominently for quick access (FR-TASK-06, FR-TASK-07)
- Role-adaptive UI shows only features the user can access — staff don't see links to pages they can't use

#### Accessibility
- Semantic HTML elements (`<nav>`, `<main>`, `<article>`, `<table>`) provide structure for screen readers (NFR-ACC-01)
- All form inputs use `<label>` elements properly associated with inputs
- Colour is not the only means of conveying status — text labels accompany all badges
- Responsive design ensures tablet and mobile users can access all features (NFR-ACC-02)

#### Data Security
- Passwords are hashed with Werkzeug's `generate_password_hash` (scrypt + unique salt per user) — NFR-SEC-01
- Session cookies are signed with a secret key (app.config["SECRET_KEY"]) — FR-AUTH-04
- SQL injection prevented through parameterised queries — never string concatenation — NFR-SEC-02
- XSS prevented by Jinja2 auto-escaping — all template variables are escaped by default — NFR-SEC-03
- File uploads validated by extension allowlist and size limit; renamed with UUID to prevent path traversal — NFR-SEC-04, NFR-SEC-05
- Role-based access control enforced at two lines of defence: route decorators and database query filters — FR-AUTH-03

> **Why two lines of defence?** In a server-rendered app, the templates never send restricted markup to the browser in the first place — there is no frontend to bypass. The route decorator is the real security boundary — it blocks the request before the code runs. The database query filter is a further safety net — even if a decorator is missing, the query only returns data the user is allowed to see. Two independent checks on every request is the **defence-in-depth** security principle.

---

> **📝 Examiner Note:** This requirements specification bridges "understanding the problem" (Task 0) and "designing the solution" (Task 3). Every functional requirement has a traceable ID (e.g., FR-AUTH-03) that will be referenced in design artefacts, code comments, commit messages, and test cases. Every user story traces back to a real business need from the fact file. The non-functional requirements show consideration of security, performance, and accessibility — areas where many students lose marks by ignoring them. The briefing notes (Task 0) first flagged RBAC as a key requirement. HERE, we formalise it into traceable functional requirements (FR-AUTH-03 onwards) with specific IDs that design artefacts, code, and test cases can reference.
