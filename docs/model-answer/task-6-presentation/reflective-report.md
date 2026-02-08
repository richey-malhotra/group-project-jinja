# Task 6b: Reflective Report

## Individual Reflective Report

> **📋 Student Scope**
>
> **Core — what you need:** A project overview, specific skills demonstrated (with examples from YOUR code, not generic statements), 2–3 real challenges you faced and how you solved them, and an honest evaluation of strengths and weaknesses. Every claim must be backed by a concrete example — "I implemented RBAC" is weak; "I designed two lines of defence because template hiding alone doesn't prevent direct POST requests to restricted routes" is strong.
>
> **Stretch — what makes it exceptional:** This document shows the full stretch version: a project overview (Section 1), detailed skills demonstrated with code examples (Section 2), three genuine challenges with problem → solution → lesson structure (Section 3), an honest evaluation with strengths, weaknesses, and "if I had more time" specifics (Section 4), and a professional development table linking skills to industry relevance (Section 5). Your report can be shorter, but it must be PERSONAL and SPECIFIC — every claim backed by a concrete example from YOUR project, not generic statements.

---

### 1. Project Overview

This project involved designing and developing a web-based Business Task Manager for MJ Limited, a business support services company with approximately 40 staff across six departments. The system replaces spreadsheet-based workflows with a centralised application that provides task management, client tracking, dashboards, and role-based access control.

The project was completed as part of a small development team following a waterfall development methodology, with formal submission gates for planning, design, development, testing, and presentation.

---

### 2. Skills Demonstrated

#### 2.1 Requirements Analysis
I analysed the MJ Limited fact file to identify that the system needed **three distinct access levels** — not all users should see the same data or have the same capabilities. The fact file describes administrative staff, managers who "rely on information from all departments", and regular staff who need to "enter or update information". This directly informed our three-tier RBAC model (admin, manager, staff) which became one of the most technically significant features of the system.

I documented 25 functional requirements with traceable identifiers (FR-AUTH-01, FR-TASK-01, etc.) and 12 non-functional requirements. These IDs were referenced throughout design, code, and test documents to maintain traceability — a practice I adopted from industry standards.

#### 2.2 Design
I created multiple design artefacts including:
- **System architecture diagram** showing the three-layer structure and server-rendered approach
- **Decomposition diagram** breaking the system into functional subsystems
- **Data flow diagrams** (Level 0 and Level 1) showing how data moves through the system
- **Entity-Relationship Diagram** with a full data dictionary
- **Wireframes** showing how the same pages appear differently for different roles
- **Sequence diagrams** showing runtime interactions, particularly RBAC enforcement and the PRG pattern
- **Pseudocode** for key algorithms (login, role checking, data filtering)
- **Route design** specifying every route's roles, inputs, and returns

Each artefact was created before the corresponding code was written. The ERD directly translated to SQL CREATE TABLE statements. The pseudocode was refined into Python. The route design was used as a contract within the team.

#### 2.3 Development
I used Python (Flask) with Jinja2 templates for a server-rendered architecture. Key technical skills demonstrated:

- **Modular architecture:** Five Flask Blueprints, each handling a distinct feature area. This allowed parallel development and clean separation of concerns.
- **Template inheritance:** All pages extend `base.html`, which provides consistent navigation, flash message rendering, and layout. Changing the nav bar in one place updates every page.
- **Security implementation:** Parameterised SQL queries (preventing injection), Jinja2 auto-escaping (preventing XSS without manual effort), password hashing with scrypt (preventing credential exposure), UUID file renaming (preventing path traversal), and two lines of RBAC defence (preventing unauthorised access).
- **PRG pattern:** Every POST route redirects on success, preventing double form submission when users refresh the page.
- **Chart.js integration:** Dashboard charts receive data via `{{ charts | tojson }}` — the standard Flask pattern for passing Python data to JavaScript, satisfying the two-language requirement.

#### 2.4 Testing
I wrote 47 test cases organised by category: authentication, RBAC permission boundaries, functional features, and input validation. The RBAC boundary tests were the most important — they verified not just "does the feature work?" but "does the RESTRICTION work?"

For example, TC-RBAC-04 verifies that a staff user cannot create a task by posting directly to `/tasks/create` (bypassing the hidden button). This test caught BUG-002, where the route had `@login_required` but no `@role_required` decorator — a critical security flaw that would have allowed any logged-in user to create tasks.

#### 2.5 Team Collaboration
Working as part of a team required:
- **Communication:** Regular check-ins to ensure everyone understood the RBAC rules (which are applied across every feature)
- **Version control:** Git commits with descriptive messages, enabling team members to understand each change
- **Modular code:** The Blueprint pattern meant team members could work on different modules (auth, tasks, clients, dashboard) simultaneously with minimal merge conflicts
- **Shared documentation:** The route design document served as a contract — each developer knew which routes returned which templates

---

### 3. Challenges and How I Addressed Them

#### Challenge 1: RBAC Complexity
**Problem:** Implementing three-tier access control across every feature was more complex than anticipated. It was not just about blocking pages — it required field-level restrictions (staff can only change status), data-level filtering (staff only see own tasks), and UI adaptation (hiding buttons, changing headings).

**Solution:** I designed the RBAC system with two lines of defence — route decorators and query-level filtering. For the field restriction, I used separate routes instead of field whitelisting: staff use `POST /tasks/<id>/status` (which only accepts a status value), while admins/managers use `POST /tasks/<id>/edit` (which accepts all fields). This is simpler and more secure than checking which fields were submitted in a single endpoint. The `_role_filter()` helper in the dashboard module centralised the query-scoping logic.

**Lesson:** Security features should be designed architecturally, not bolted on. Separate routes for different permission levels make the code clearer than conditional logic within a single route.

#### Challenge 2: Post-Redirect-Get Pattern
**Problem:** After implementing task creation, refreshing the page after creating a task caused the browser to re-submit the POST request, creating a duplicate task. This is a well-known problem with server-rendered forms — the browser remembers the POST data and re-sends it.

**Solution:** I applied the Post-Redirect-Get (PRG) pattern to every POST route. Instead of rendering a template directly after processing, each POST handler calls `redirect(url_for(...))`. The browser follows the redirect with a GET request, so refreshing the page only re-sends the GET — no duplicate data.

**Lesson:** PRG is not optional in server-rendered applications — it's a fundamental pattern. Every POST handler in the codebase follows the same structure: validate → process → flash → redirect.

#### Challenge 3: Balancing Security and Usability
**Problem:** The strictest security approach would be to give no feedback when users are restricted. But this creates a poor user experience — users don't know why they can't see certain features.

**Solution:** I implemented role-specific template rendering rather than generic blocking. Staff see "My Tasks" (not "Task Management"), their navigation only shows relevant links, and flash messages explain what happened after every action. The Jinja2 `{% if role in ("admin", "manager") %}` conditionals control exactly what markup each user receives — restricted elements are never sent, not just hidden with CSS.

**Lesson:** Security and usability are not opposites. Server-rendered templates make this easier than SPA architectures — the server decides what to send, so there's no client-side code to bypass.

---

### 4. Evaluation of the Final Product

#### Strengths
- **Complete RBAC implementation** with two lines of defence — matches the brief's requirement for different access levels
- **Auto-escaping XSS prevention** — Jinja2 handles this by default, eliminating an entire class of vulnerabilities
- **Clean, modular codebase** that is easy to extend with new features
- **Consistent patterns** — every POST route follows PRG, every template extends base.html, every query uses parameterised placeholders

#### Weaknesses
- **SQLite** limits concurrent access — would need PostgreSQL for production
- **No automated testing** — all 47 test cases were manual. pytest would catch regressions automatically
- **No audit trail** — the system does not log who changed what, which is important for a business application

#### If I Had More Time
1. **Automated tests** with pytest — running all 47 test cases manually is time-consuming
2. **Audit logging** (FR-AUDIT-01) — INSERT a record into an audit table on every create/update/delete
3. **Data export** (FR-EXPORT-01) — CSV export for managers to share reports externally
4. **Email notifications** — alert staff when they are assigned a new task
5. **API layer** — add a REST API alongside the templates for potential mobile app integration

---

### 5. Professional Development

This project developed several skills that align with the Digital Product Development specialism:

| Skill | How Demonstrated | Industry Relevance |
|---|---|---|
| Requirements analysis | Identified RBAC need from the brief before coding | Business analysts must extract technical requirements from non-technical descriptions |
| Database design | ERD, data dictionary, referential integrity | All database-backed applications require structured data design |
| Server-rendered web development | Flask + Jinja2 templates with PRG pattern | Many enterprise applications use server-rendered frameworks (Django, Rails, Laravel) |
| Security engineering | Defence-in-depth, password hashing, auto-escaping | Security is a non-negotiable requirement in every organisation |
| Version control | Git workflow with descriptive commits | Every development team uses version control |
| Technical writing | User guide, technical docs, developer notes | Communication is as important as coding in professional environments |

---

> **📝 Examiner Note:** A strong reflective report is PERSONAL and SPECIFIC. Generic statements like "I learned a lot about Python" score poorly. Specific statements like "I used separate routes for different permission levels because checking field whitelists in a single endpoint is error-prone and harder to audit" demonstrate genuine understanding. The challenges section should describe REAL problems encountered — not invented difficulties. The self-evaluation should be honest — acknowledging weaknesses (like no automated testing) shows maturity and is always rewarded over claiming perfection.
