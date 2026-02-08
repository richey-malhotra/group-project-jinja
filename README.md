# MJ Limited Staff Portal

## Model Answer — T Level DSD Industry Project (Server-Rendered)

A fully working digital solution for MJ Limited, demonstrating how to complete the Occupational Specialism project to **Distinction** standard. This version uses **Flask + Jinja2 templates** — a server-rendered architecture with no JavaScript SPA.

> **Looking for the API version?** A REST API + vanilla JavaScript SPA version of this model answer is available at [group-project](https://github.com/richey-malhotra/group-project). It demonstrates additional technical breadth (client-server separation, async JavaScript, three lines of RBAC defence) for students who want to explore a more advanced architecture.

---

### Quick Start

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
python seed_data.py
python app.py
```

Open **http://127.0.0.1:5001** in your browser.

---

### Login Credentials

| Role    | Username    | Password     |
|---------|-------------|-------------|
| Admin   | admin       | admin123    |
| Manager | m.jones     | manager123  |
| Staff   | j.smith     | staff123    |
