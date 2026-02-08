# MJ Limited Staff Portal

## Model Answer — T Level DPDD Industry Project (Server-Rendered)

A fully working digital solution for MJ Limited, demonstrating how to complete the Occupational Specialism project to **Distinction** standard. This version uses **Flask + Jinja2 templates** — a server-rendered architecture with no JavaScript SPA.

> **Looking for the API version?** A REST API + vanilla JavaScript SPA version of this model answer is available at [group-project](https://github.com/richey-malhotra/group-project). It demonstrates additional technical breadth (client-server separation, async JavaScript, three lines of RBAC defence) for students who want to explore a more advanced architecture. See [V1-VS-V2.md](docs/V1-VS-V2.md) for a full comparison.

---

### What This Is

This repository contains a **complete model answer** for the T Level Digital Production, Design and Development industry project. It includes:

- ✅ A **working web application** (Python Flask + Jinja2 templates)
- ✅ **Full documentation** matching every deliverable in Tasks 0–6
- ✅ **Deliberate commit history** showing how a developer builds a system step by step

---

### Quick Start

#### Prerequisites
- Python 3.10 or higher *(not sure? Open a terminal and type `python --version` — if you get an error, download Python from [python.org](https://www.python.org/downloads/))*
- A web browser (Chrome, Firefox, Edge, Safari)

#### Setup
```bash
# 1. Create a virtual environment (a private copy of Python for this project)
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Seed the database with sample data
python seed_data.py

# 5. Start the application
python app.py
```

#### Login Credentials

All 8 seeded users are listed below. Users sharing a role share the same password.

| Role    | Username    | Password     | Name             | Department            |
|---------|-------------|-------------|------------------|----------------------|
| Admin   | admin       | admin123    | Sarah Mitchell   | Management & Strategy |
| Manager | m.jones     | manager123  | Michael Jones    | Client Services       |
| Manager | l.chen      | manager123  | Lisa Chen        | Finance               |
| Manager | r.patel     | manager123  | Raj Patel        | Administration        |
| Staff   | j.smith     | staff123    | James Smith      | Client Services       |
| Staff   | e.williams  | staff123    | Emma Williams    | Finance               |
| Staff   | d.brown     | staff123    | David Brown      | Administration        |
| Staff   | a.taylor    | staff123    | Amy Taylor        | HR                   |

Open your browser to **http://127.0.0.1:5001** and sign in.

---

### Tech Stack

| Layer      | Technology        | Why                                             |
|------------|-------------------|-------------------------------------------------|
| Backend    | Python Flask      | Lightweight, readable, minimal boilerplate      |
| Templates  | Jinja2            | Server-rendered HTML, auto-escapes XSS          |
| Styling    | Pico CSS + custom overrides        | Classless framework with project-specific overrides                 |
| Database   | SQLite            | Zero setup, ships with Python                   |
| Charts     | Chart.js          | Simple, well-documented data visualisation      |

---

### Project Structure

```
group-project-jinja/
├── app.py                    # Flask application entry point
├── database.py               # SQLite connection and schema
├── seed_data.py              # Sample data generator
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
├── .env.example              # Template for .env
│
├── routes/                   # Backend route handlers (Python)
│   ├── auth.py               # Login, logout, session management
│   ├── tasks.py              # Task CRUD operations
│   ├── clients.py            # Client CRUD operations
│   ├── dashboard.py          # Aggregated statistics and chart data
│   └── attachments.py        # File upload/download
│
├── templates/                # Jinja2 templates (rendered server-side)
│   ├── base.html             # Base template (nav, flash messages, layout)
│   ├── login.html            # Login page
│   ├── tasks.html            # Task list with filters and modals
│   ├── task_detail.html      # Single task with attachments
│   ├── clients.html          # Client list with filters and modals
│   └── dashboard.html        # Dashboard with stat cards and charts
│
├── static/                   # Static files (served to the browser)
│   ├── css/
│   │   └── style.css         # Custom styles
│   └── js/
│       └── charts.js         # Chart.js rendering (dashboard only)
│
├── uploads/                  # File attachment storage
│
└── docs/                     # Project documentation
    ├── DPDD Fact File.docx
    ├── DPDD Project Brief.docx
    ├── DPDD Task List.docx
    ├── HOW-TO-STUDY-THIS.md  # ← Start here: 24-step learning trajectory
    ├── BEGINNERS-BRIDGE.md   # Maps basic concepts to this codebase
    ├── WALKTHROUGH.md        # Explains every technical decision
    ├── EXAM-DECODER.md       # Maps marking criteria → evidence
    ├── EXTENSION-CHALLENGES.md # Scaffolded exercises to practise adding features
    ├── WHY-THIS-IS-DISTINCTION.md # Why the model answer scores Distinction
    │
    └── model-answer/         # ← Completed deliverables for all tasks
        ├── task-0-briefing/
        ├── task-1-planning/
        ├── task-2-requirements/
        ├── task-3-design/
        ├── task-4-development/
        ├── task-5-testing/
        └── task-6-presentation/
```

---

### Features Implemented (Must Have — MoSCoW)

| Feature                        | Backend (Python)       | Frontend (Jinja2 Templates)       |
|-------------------------------|------------------------|----------------------------------|
| User authentication + roles   | Session management     | Login form, conditional nav       |
| Task management (CRUD)        | Form processing        | Server-rendered table, modals     |
| Client management (CRUD)      | Form processing        | Server-rendered table, modals     |
| Dashboard with charts         | Aggregation queries    | Chart.js via tojson filter        |
| File attachments              | Multipart upload       | Upload form, download links       |
| Search & filtering            | SQL WHERE clauses      | GET form with query parameters    |
| Responsive layout             | N/A                    | CSS media queries                 |
| Data validation               | Server-side checks     | Flash messages for errors         |

---

### How to Study This Project

> **Start here → [How to Study This Model Answer](docs/HOW-TO-STUDY-THIS.md)**
> It maps every commit in this repo to the exact task, process, and deliverable — so you know the order to follow for your own submission.

1. **Read the Study Guide first** — it shows the 24-step development trajectory and what each step produces
2. **Run the application** — click through every feature as each user role to understand what it does
3. **Read the documentation in order** — Task 0 → Task 6, see how each builds on the last
4. **Walk through the commit history** — the Study Guide teaches you how to use `git checkout` to step through each stage of development, watching the project grow from an empty folder to a finished application. Open this README and all the teaching documents on GitHub in browser tabs first — your local copies revert during checkouts *(you must clone the repo with `git clone`, not download the ZIP — the ZIP doesn’t include commit history)*
5. **Read the code** — every file has detailed comments explaining what and why
6. **Try the extension challenges** — [EXTENSION-CHALLENGES.md](docs/EXTENSION-CHALLENGES.md) has scaffolded exercises to test your understanding
7. **Check your work against the criteria** — [WHY-THIS-IS-DISTINCTION.md](docs/WHY-THIS-IS-DISTINCTION.md) explains what makes each area Distinction-level and includes a self-check checklist
8. **Write your own** — close this project, open a new folder, and build yours

#### Supporting Documents

| Document | When to use it |
|----------|----------------|
| [HOW-TO-STUDY-THIS.md](docs/HOW-TO-STUDY-THIS.md) | **Start here.** The main 24-step learning trajectory — follow this from beginning to end |
| [BEGINNERS-BRIDGE.md](docs/BEGINNERS-BRIDGE.md) | If you can write Python in class but the codebase looks unfamiliar — this maps what you already know to the patterns used here |
| [WALKTHROUGH.md](docs/WALKTHROUGH.md) | If you’re wondering *why* a technical decision was made ("Why Flask? Why Jinja2? Why not a JavaScript frontend?") |
| [EXAM-DECODER.md](docs/EXAM-DECODER.md) | When you’re ready to check your own work against the marking criteria — shows exactly what earns Distinction marks |
| [EXTENSION-CHALLENGES.md](docs/EXTENSION-CHALLENGES.md) | After you’ve studied the model answer — scaffolded exercises to practise adding features yourself |
| [WHY-THIS-IS-DISTINCTION.md](docs/WHY-THIS-IS-DISTINCTION.md) | When you want to understand *why* the model answer scores Distinction — walks through each assessment area with a self-check checklist for your own work |
