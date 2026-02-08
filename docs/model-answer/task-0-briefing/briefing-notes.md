# Task 0: Employer Briefing Notes

## Understanding the Problem

---

### 1. Client Background

**MJ Limited** is a business support services company based in the West Midlands. The company employs approximately 40 staff across six departments:

| Department | Function |
|---|---|
| Administration | Office management, reception, general operations |
| Finance | Invoicing, payroll, financial reporting |
| Human Resources | Staff management, recruitment, training |
| IT | Infrastructure, software, technical support |
| Marketing | Client outreach, campaigns, brand management |
| Operations | Service delivery, logistics, resource allocation |

The company provides support services to external business clients. Managers oversee departmental teams and report to senior leadership.

---

### 2. Current Problems

MJ Limited currently manages tasks and client information using **spreadsheets**. The fact file identifies several problems with this approach:

| Problem | Impact | Our Solution |
|---|---|---|
| Data is scattered across multiple spreadsheets | Staff waste time searching for information; risk of outdated data | Centralised database accessible via web browser |
| No access control | Any staff member can view or edit any data, including sensitive client information | Three-tier RBAC: admin, manager, staff with different permissions |
| No overview of workload | Managers cannot see task distribution or identify bottlenecks | Dashboard with role-filtered statistics and charts |
| Manual reporting | Generating summaries requires manually counting and calculating from spreadsheets | Automated aggregation via SQL queries displayed on dashboard |
| Risk of data loss | Spreadsheets are not backed up systematically; version conflicts when multiple people edit | Database provides single source of truth; seed data enables recovery |
| No audit of who changed what | Changes to spreadsheets are not tracked | (Identified as future enhancement — FR-AUDIT-01) |

---

### 3. Stakeholder Analysis

| Stakeholder | Needs | Concerns |
|---|---|---|
| **Senior Management / Admin** | Full visibility of all operations; ability to manage users and data | Data integrity, security, system reliability |
| **Department Managers** | View of their department's tasks and workload; ability to assign and track work | Ease of use, accurate reporting, client management |
| **Staff Members** | Clear view of their own tasks; simple way to update progress | Privacy (not seeing others' work), simplicity, mobile access |
| **IT Department** | Maintainable system; clear documentation; secure deployment | Code quality, security vulnerabilities, deployment complexity |
| **Clients (indirect)** | Their data handled securely and accurately | Data protection, professional service delivery |

---

### 4. Proposed Solution

A **web-based Business Task Manager** with:

1. **Task Management** — Create, assign, track, and complete tasks across departments
2. **Client Management** — Maintain a central record of business clients with contact details
3. **Dashboard** — Visual overview with statistics and charts, filtered by the user's role
4. **File Attachments** — Upload documents against tasks for reference
5. **Role-Based Access Control** — Three tiers of access matching the organisational hierarchy:
   - **Admin:** Full system access, organisation-wide visibility
   - **Manager:** Department oversight, task and client management
   - **Staff:** View and update their own assigned tasks only

---

### 5. Key Requirement: Access Control

The fact file states:
> *"Some staff will need to enter or update information, while others will require access to review or manage records."*

And:
> *"Students should consider how access levels are managed."*

This directly implies that the system must implement **differentiated access** — not all users should see the same data or have the same capabilities. We identified three access tiers from the organisational structure described in the brief:

| Tier | Who | Access Level | Justification from Brief |
|---|---|---|---|
| Admin | IT / senior management | Full CRUD on all data, organisation-wide views | System needs an owner with unrestricted access |
| Manager | Department heads | Create/edit tasks and clients, department-scoped dashboard | "Managers rely on information from all departments" |
| Staff | Regular employees | View own tasks, update status only | "Some staff will need to enter or update information" |

This access control requirement is a MUST-HAVE because without it, any staff member could view sensitive client data, delete records, or modify other people's tasks — exactly the problems MJ Limited already has with spreadsheets.

---

### 6. Technology Decisions (Initial)

| Decision | Choice | Reason |
|---|---|---|
| Architecture | Server-rendered (Flask + Jinja2 templates) | Single codebase serves routes and HTML; simpler than a separate frontend |
| Backend | Python / Flask | Lightweight, educational, team familiarity |
| Frontend | Jinja2 templates, Pico CSS, Chart.js | Server-rendered HTML; no build tools; Chart.js for dashboard charts |
| Database | SQLite | Zero configuration; suitable for prototype |
| Deployment | Local (Flask dev server) | Zero configuration; runs on any machine with Python |

These choices balance development speed (prototype in 30 hours) and educational clarity (visible code without framework abstractions).

---

### 7. Success Criteria

The system will be considered successful if:

1. ✅ Users can log in with their credentials and are directed to role-appropriate pages
2. ✅ Admin and manager users can create, edit, and delete tasks
3. ✅ Staff users can view and update the status of their own assigned tasks only
4. ✅ Client records can be managed by admin and manager users
5. ✅ The dashboard displays role-filtered statistics and charts
6. ✅ Files can be uploaded, downloaded, and managed with appropriate permissions
7. ✅ All access is controlled by role — no user can access data or actions beyond their authorisation level

---

> **📝 Examiner Note:** Task 0 demonstrates understanding of the employer's problem BEFORE proposing a solution. Notice how Section 5 connects the fact file's sentence about "access levels" to a concrete RBAC requirement — strong candidates identify this here at the briefing stage, not later during coding. The stakeholder analysis shows understanding of who will use the system and what they need. The success criteria establish measurable goals that the test plan (Task 5) will verify.
