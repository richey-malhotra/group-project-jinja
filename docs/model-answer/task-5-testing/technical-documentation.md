# Task 5c: Technical Documentation

## System Technical Documentation

> **📋 Student Scope**
>
> **Core — what you need:** System requirements, an installation guide (how to clone, install, and run), the file/folder structure, and a security overview explaining how you protect against key threats (SQL injection, XSS, unauthorised access). This proves another developer could set up and understand your system.
>
> **Stretch — what makes it exceptional:** This document shows the full stretch version: system requirements (Section 1), installation guide (Section 2), architecture overview with file tree (Section 3), database schema summary (Section 4), security architecture covering authentication, RBAC, and input threats (Section 5), route reference table (Section 6), deployment notes (Section 7), backup/recovery (Section 8), and known limitations (Section 9). The known limitations section is particularly valued — it shows honest, mature engineering judgement. You don't need all 9 sections, but you DO need enough for someone unfamiliar with your code to install, run, and understand the security model.

---

### 1. System Requirements

#### Server Requirements
| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.10+ | 3.12+ |
| Disk Space | 50 MB (app + database) | 500 MB (including uploads) |
| RAM | 256 MB | 512 MB |
| Operating System | Any (Linux, macOS, Windows) | Linux (for production) |

#### Client Requirements
| Requirement | Minimum |
|---|---|
| Browser | Chrome 90+, Firefox 88+, Edge 90+, Safari 14+ |
| JavaScript | Enabled (for Chart.js on dashboard only) |
| Screen Resolution | 320px width (responsive) |

---

### 2. Installation Guide

#### Step 1: Clone Repository
```bash
git clone <repository-url>
cd group-project-jinja
```

#### Step 2: Create Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
| Package | Version | Purpose |
|---|---|---|
| Flask | 3.1.0 | Web framework |
| Jinja2 | 3.1.x | Template engine (bundled with Flask) |
| Werkzeug | 3.1.3 | Password hashing, HTTP utilities |
| python-dotenv | 1.1.0 | Load environment variables from .env |

#### Step 4: Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```

The `.env.example` file contains sensible defaults. The `SECRET_KEY` is used to sign session cookies — in production, replace it with a long random string.

#### Step 5: Initialise Database
```bash
python seed_data.py
```

This creates `mj_limited.db` with the schema and sample data:
- 8 users (1 admin, 3 managers, 4 staff)
- 5 clients
- 10 tasks

#### Step 6: Start the Server
```bash
python app.py
```

The server starts on `http://localhost:5001`. Open this URL in a browser to access the application.

---

### 3. Architecture Overview

```
group-project-jinja/
├── app.py                   # Application factory + entry point
├── database.py              # Database connection management
├── seed_data.py             # Database initialisation + sample data
├── .env                     # Environment variables (SECRET_KEY)
├── requirements.txt         # Python dependencies
├── routes/
│   ├── auth.py              # Authentication + RBAC decorators
│   ├── tasks.py             # Task CRUD routes
│   ├── clients.py           # Client CRUD routes
│   ├── dashboard.py         # Dashboard statistics + chart data
│   └── attachments.py       # File upload/download routes
├── templates/
│   ├── base.html            # Base template (nav, flash messages, layout)
│   ├── login.html           # Login page
│   ├── tasks.html           # Task list with filters and modals
│   ├── task_detail.html     # Single task with attachments
│   ├── clients.html         # Client list with filters and modals
│   └── dashboard.html       # Dashboard with stat cards and charts
├── static/
│   ├── js/
│   │   └── charts.js        # Chart.js rendering (dashboard only)
│   └── css/
│       └── style.css        # Custom styles
├── uploads/                 # File attachment storage
└── docs/                    # Project documentation
```

The system uses a **three-layer architecture**:
1. **Template Layer:** Jinja2 templates rendered server-side (HTML sent to browser)
2. **Route Layer:** Flask Blueprints handling requests, validation, and database calls
3. **Data Access Layer:** database.py with parameterised SQL + SQLite file storage

Unlike a traditional SPA (Single Page Application), there is no separate API layer — routes render templates directly. The browser receives complete HTML pages, not JSON data.

---

### 4. Database Schema

Four tables with foreign key relationships:

```sql
users       →  tasks       (assigned_to references users.id)
clients     →  tasks       (client_id references clients.id)
tasks       →  attachments (task_id references tasks.id)
users       →  attachments (uploaded_by references users.id)
```

Foreign keys are enforced via `PRAGMA foreign_keys = ON` executed on every database connection.

See Design Artefact 4 (ERD + Data Dictionary) for full schema details.

---

### 5. Security Architecture

#### 5.1 Authentication
- Passwords hashed with scrypt (Werkzeug 3.x default), unique salt per user
- Sessions managed via signed cookies (Flask session)
- Cookie flags: `HttpOnly=True` (no JavaScript access)

#### 5.2 Role-Based Access Control (RBAC)

Two lines of defence (defence-in-depth):

| Layer | Implementation | Purpose |
|---|---|---|
| Route Decorators | `@role_required()` checks session role before handler runs | Primary security — blocks unauthorised requests |
| Query Filters | SQL WHERE clauses filter data by user/department/role | Safety net — limits data exposure even if decorator is missing |

Because templates are rendered server-side, the server controls exactly what HTML the user receives. There is no client-side rendering to bypass — restricted buttons, forms, and data are never sent to unauthorised users. This eliminates an entire attack surface compared to SPA architectures where the frontend code runs on the user's machine.

#### 5.3 Input Security
| Threat | Countermeasure |
|---|---|
| SQL Injection | Parameterised queries (`?` placeholders) — no string concatenation |
| Cross-Site Scripting (XSS) | Jinja2 auto-escapes all template variables by default |
| Path Traversal | File uploads renamed with UUID; original names stored separately |
| File-Based Attacks | Extension allowlist + 5MB size limit |
| Session Hijacking | HttpOnly cookie flag |
| Double Form Submission | POST-Redirect-Get (PRG) pattern on all POST routes |

---

### 6. Route Reference

All routes are served by Flask Blueprints. POST routes redirect after processing (PRG pattern).

| Route | Method | Auth | Roles | Returns |
|---|---|---|---|---|
| `/login` | GET | No | Public | Login page |
| `/login` | POST | No | Public | Redirect to /dashboard |
| `/logout` | GET | Yes | All | Redirect to /login |
| `/tasks` | GET | Yes | All (filtered) | Task list page |
| `/tasks/<id>` | GET | Yes | All (filtered) | Task detail page |
| `/tasks/create` | POST | Yes | Admin, Manager | Redirect to /tasks |
| `/tasks/<id>/edit` | POST | Yes | Admin, Manager | Redirect to /tasks |
| `/tasks/<id>/status` | POST | Yes | All (own tasks) | Redirect to /tasks |
| `/tasks/<id>/delete` | POST | Yes | Admin, Manager | Redirect to /tasks |
| `/clients` | GET | Yes | Admin, Manager | Client list page |
| `/clients/create` | POST | Yes | Admin, Manager | Redirect to /clients |
| `/clients/<id>/edit` | POST | Yes | Admin, Manager | Redirect to /clients |
| `/clients/<id>/delete` | POST | Yes | Admin | Redirect to /clients |
| `/dashboard` | GET | Yes | All (filtered) | Dashboard page |
| `/attachments/upload/<task_id>` | POST | Yes | All | Redirect to /tasks/<task_id> |
| `/attachments/<id>/delete` | POST | Yes | Uploader/Admin/Mgr | Redirect to /tasks/<task_id> |
| `/attachments/download/<filename>` | GET | Yes | All | File download |

---

### 7. Deployment

#### Local Development
```bash
python app.py
# Server runs at http://localhost:5001
```

The application runs as a standalone Flask development server. SQLite provides zero-configuration data storage as a single file (`mj_limited.db`). File uploads are stored in the `uploads/` directory.

**For production deployment**, the application would need:
- A production WSGI server (e.g., Gunicorn)
- A production database (e.g., PostgreSQL)
- Cloud storage for file uploads (e.g., AWS S3)
- HTTPS via a reverse proxy (e.g., Nginx)

---

### 8. Backup & Recovery

#### Database Backup
```bash
# Copy the database file
cp mj_limited.db mj_limited.db.backup

# Restore from backup
cp mj_limited.db.backup mj_limited.db
```

#### Full Reset
```bash
# Delete database and recreate with seed data
rm mj_limited.db
python seed_data.py
```

---

### 9. Known Limitations

| Limitation | Impact | Mitigation Path |
|---|---|---|
| SQLite single-writer | Cannot handle concurrent writes from multiple users | Migrate to PostgreSQL for production |
| No real-time updates | Users must refresh to see changes made by others | Add WebSocket support or polling |
| Session-based auth | Does not support API access from mobile apps | Add JWT option for API consumers |
| No audit trail | Cannot track who changed what and when | Add audit log table (FR-AUDIT-01 — Could Have) |

---

> **📝 Examiner Note:** Technical documentation is written for DEVELOPERS and system administrators — not end users. It covers installation, configuration, architecture, security, and deployment. The security section is particularly important — it shows the examiner that the developer understands the threats and has implemented countermeasures. The known limitations section shows honest, mature assessment of the system's boundaries.
