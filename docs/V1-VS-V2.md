# V1 vs V2 — Which Model Answer Should I Study?

Both model answers solve the same DPDD project brief and both score Distinction. The difference is **how** they build the web application — and that choice does not affect your marks.

This document explains the difference, helps you choose, and reassures you that neither choice is "easier" or "weaker."

---

## The Short Answer

| | V1 — [`group-project`](https://github.com/richey-malhotra/group-project) | V2 — [`group-project-jinja`](https://github.com/richey-malhotra/group-project-jinja) |
|---|---|---|
| **Architecture** | REST API + vanilla JavaScript SPA | Flask + Jinja2 server-rendered pages |
| **Languages you'll write** | Python (backend) AND JavaScript (frontend) | Python + Jinja2 templates |
| **How pages appear** | JavaScript fetches JSON from the API and builds the HTML in the browser | Flask builds the complete HTML on the server and sends it to the browser |
| **RBAC defence lines** | 3 — frontend hiding + route decorators + query filters | 2 — route decorators + query filters |
| **Number of commits** | 28 | 27 |
| **Difficulty** | More moving parts — two languages, `fetch()` calls, CORS-style thinking | Fewer moving parts — one language, one request–response cycle |
| **Marks** | Distinction ✅ | Distinction ✅ |

---

## What's the Same?

Almost everything that matters for the exam is identical:

- **Same database** — SQLite with the same four tables (`users`, `clients`, `tasks`, `attachments`), same schema, same seed data.
- **Same features** — Login, dashboard with charts, task CRUD, client CRUD, file upload/download, role-based access control.
- **Same roles** — Admin, Manager, Staff — with the same permissions in both versions.
- **Same documentation portfolio** — The same 18 model-answer documents, structured identically across tasks 0–6.
- **Same supporting guides** — HOW-TO-STUDY-THIS, WALKTHROUGH, BEGINNERS-BRIDGE, EXAM-DECODER, WHY-THIS-IS-DISTINCTION, EXTENSION-CHALLENGES.
- **Same security patterns** — Password hashing (Werkzeug), session-based auth, parameterised SQL, input validation, UUID file renaming.
- **Same marking criteria** — Both hit every Distinction-level criterion in the DPDD specification.

---

## What's Different?

### 1. How Pages Get to the Browser

**V1 (API + SPA):**
```
Browser loads static HTML  →  JavaScript runs  →  fetch("/api/tasks")  →  Server returns JSON  →  JavaScript builds the HTML
```

**V2 (Jinja2):**
```
Browser requests /tasks  →  Flask queries the database  →  Jinja2 builds the HTML  →  Server sends complete page
```

In V1, the server only sends raw data (JSON). The browser's JavaScript is responsible for turning that data into something visible. In V2, the server does everything — the browser just displays the finished page.

### 2. Number of Languages

| | V1 | V2 |
|---|---|---|
| Backend | Python (Flask) | Python (Flask) |
| Frontend | JavaScript (`app.js` — ~400 lines) | Jinja2 templates (HTML with `{{ }}` tags) |
| Total files to understand | ~12 Python + ~5 HTML + 1 JS | ~8 Python + ~6 HTML |

V2 has no standalone JavaScript application. The only JavaScript is `charts.js` — a small file that feeds data into Chart.js for the dashboard graphs.

### 3. RBAC Defence Lines

**V1 has three lines of defence:**
1. Frontend hides buttons/links the user shouldn't see
2. Route decorators (`@role_required`) block unauthorised API calls
3. SQL `WHERE` clauses filter data by user/department

**V2 has two lines of defence:**
1. Route decorators (`@role_required`) block unauthorised requests
2. SQL `WHERE` clauses filter data by user/department

Why does V2 have fewer? Because there is no separate frontend to "hide" things. The Jinja2 template simply never renders the restricted HTML in the first place — `{% if role == 'admin' %}` is evaluated on the server, so the restricted markup never reaches the browser. This is a property of the architecture, not a missing security feature.

Both approaches are equally secure. The examiner will recognise this.

### 4. Form Handling

**V1:** JavaScript intercepts the form, calls `fetch()` with JSON, receives a JSON response, and updates the page without a full reload.

**V2:** The HTML form submits directly via POST. Flask processes the data, saves to the database, and redirects the user back to the page (the Post-Redirect-Get pattern). The whole page reloads.

V2's approach is simpler. V1's approach gives a smoother user experience (no full page reload). For this project's requirements, both are perfectly fine.

---

## Why Does V2 Still Get Distinction?

The marking criteria reward **understanding**, not complexity. Here's what the examiner is looking for, and how V2 delivers:

| Criterion | How V2 Demonstrates It |
|---|---|
| System architecture with clear justification | Server-rendered monolith with layered architecture diagram. Justified in design docs. |
| RBAC with defence in depth | Two lines: decorators + query filters. Explained why a third line isn't needed. |
| CRUD with validation | All four operations on tasks and clients with server-side validation. |
| Security best practices | Password hashing, parameterised SQL, session cookies, UUID file renaming, auto-escaping. |
| Testing with boundary cases | Test plan includes RBAC boundary tests (what staff CANNOT do). |
| Developer reflection | Developer notes explain what was built, problems encountered, and how they were solved. |

The design documents explicitly justify the simpler architecture — for example, the design justifications doc explains why server-rendered was chosen over SPA and discusses the trade-offs honestly. This kind of reasoned decision-making is exactly what examiners want to see.

---

## Which Should I Study?

**Choose V2 if:**
- You're more comfortable with Python than JavaScript
- You want fewer files to read and understand
- You prefer a straightforward request → response → page pattern
- You want to focus on the documentation and design thinking rather than frontend wiring

**Choose V1 if:**
- You already know some JavaScript and want to deepen that skill
- You're interested in how APIs work (useful for future projects and jobs)
- You want to demonstrate the widest possible technical range
- You enjoy understanding how the frontend and backend communicate

**Either way:**
- Both repositories have the same study guides, the same walkthrough, the same exam preparation materials.
- Your documentation portfolio will be equally strong with either version.
- The examiner does not prefer one architecture over the other.

---

## Can I Mix and Match?

Yes. The documentation and study guides are written for each version specifically, so you should study one version's code and docs together rather than mixing code from V1 with docs from V2. But you can absolutely:

- Read both sets of design documents to see how the same system can be designed two ways.
- Use V2 as your main study version and skim V1's JavaScript to understand APIs.
- Start with V2 (simpler) and progress to V1 later if you want a challenge.

---

## One More Thing

Neither version is a shortcut. Both require you to understand what the code does, why it was designed that way, and how to explain it in your documentation. The Distinction comes from that understanding — not from how many languages the project uses.

Pick the version that makes the most sense to you, study it thoroughly, and write your documentation with confidence.
