# Design Artefact 9 — Design Justifications

## Overview

This document explains WHY each major design decision was made. Every decision is framed as: **"We chose X over Y because Z."** This format demonstrates analytical thinking — the examiner sees that the developer considered alternatives, not just picked the first option.

> **📋 Student Scope**
>
> **Core — what you need:** Four to five key decisions where you genuinely weighed alternatives, written as comparison tables. At minimum: your language/framework choice, your database choice, and your rendering approach. These prove analytical thinking.
>
> **Stretch — what makes it exceptional:** Covering all your major decisions across every layer — this document shows the full stretch version: architecture (Section 1), data (Section 2), presentation (Section 3), security (Section 4), development process (Section 5), and a trade-offs summary table (Section 6). It covers 12 decisions — you don't need that many. But the format is simple: for each choice, ask yourself "What else could I have used, and why didn't I?" If you picked your tech stack, you already have the raw material.

---

## 1. Architecture Decisions

### 1.1 Server-Rendered over Client–Server SPA

| Aspect | Chosen: Server-Rendered (Flask + Jinja2) | Alternative: Client–Server (REST + SPA) |
|---|---|---|
| **Simplicity** | One language (Python) handles logic and rendering | Requires Python backend + JavaScript frontend — two codebases |
| **Build tools** | None — Jinja2 templates are plain HTML | SPA typically needs build tools (webpack, vite) |
| **Security model** | Server controls exactly what HTML is sent — restricted markup never reaches the browser | Frontend can be bypassed — defence-in-depth requires extra UI-hiding layer |
| **Debugging** | View source shows the final rendered HTML | DevTools needed to trace fetch() → JSON → DOM rendering |
| **Trade-off** | No API reusability — HTML responses only useful for browsers | Same API could serve mobile apps or third-party integrations |

**Decision:** Server-rendered. For a team of DSD students building a business task manager, the simplicity of one language and one rendering pipeline significantly reduces complexity. The system does not need a reusable API — it serves one web interface. Flask + Jinja2 achieves the same security guarantees with less code.

### 1.2 Flask over Django

| Aspect | Chosen: Flask | Alternative: Django |
|---|---|---|
| **Complexity** | Micro-framework — only includes what you need | Full framework with ORM, admin panel, auth built in |
| **Transparency** | Every route, query, and template call is visible in the code | Significant abstraction; "magic" hides implementation details |
| **Blueprint system** | Clean modular routing — each feature is a separate file | App-based modularity — heavier structure |
| **Database** | Direct SQL with parameterised queries — security is visible | Django ORM abstracts SQL — security is automatic but hidden |
| **Trade-off** | No built-in admin panel, user model, or ORM | Faster to prototype with batteries included |

**Decision:** Flask. The explicit nature of Flask — where every SQL query, route, and security check is visible in the code — means the team can understand, debug, and explain every part of the system. With Django, password hashing, SQL injection prevention, and session management are handled automatically behind abstractions — convenient, but harder to demonstrate understanding of in a design portfolio.

---

## 2. Data Decisions

### 2.1 SQLite over PostgreSQL/MySQL

| Aspect | Chosen: SQLite | Alternative: PostgreSQL |
|---|---|---|
| **Setup** | Zero configuration — single file, built into Python | Requires server installation and configuration |
| **Deployment** | Zero configuration — single file, runs anywhere Python runs | Requires managed database service (cost, complexity) |
| **Scalability** | Single-writer, file locking — not suitable for high traffic | Concurrent writers, connection pooling — production-grade |
| **Inspectability** | Same SQL syntax, single .db file that can be opened and examined directly | Same SQL but requires a running server to inspect |
| **Trade-off** | Not suitable for concurrent multi-user production use | Overkill for a prototype with 8 seed users |

**Decision:** SQLite. For a prototype system with ~40 staff (fact file), SQLite is more than adequate. The development and deployment simplicity lets the team focus on application logic rather than database administration.

### 2.2 Direct SQL over an ORM

| Aspect | Chosen: Parameterised SQL | Alternative: SQLAlchemy ORM |
|---|---|---|
| **Visibility** | Every query is visible — easy to audit for SQL injection | ORM generates SQL behind the scenes |
| **Auditability** | `?` placeholders are explicit in the code — a reviewer can verify every query is safe | ORM prevents injection automatically but the mechanism is hidden |
| **Complexity** | Simple — no model classes, migrations, or session management | Additional layer of abstraction and configuration |
| **Trade-off** | Schema changes require manual SQL updates | ORM handles migrations automatically |

**Decision:** Direct parameterised SQL. Seeing `cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))` makes the security mechanism explicit — every query can be audited for injection vulnerabilities by reading the code. An ORM provides the same protection but hides it, making it harder to demonstrate in a design portfolio or explain during review.

### 2.3 Password Hashing: Werkzeug scrypt

| Aspect | Detail |
|---|---|
| **Algorithm** | scrypt with parameters 32768:8:1 (Werkzeug 3.x default) |
| **Salt** | Unique per-user, generated automatically by Werkzeug |
| **Why not bcrypt?** | Werkzeug is already a Flask dependency — no extra install. scrypt is memory-hard and resistant to GPU/ASIC attacks. |
| **Why not plain text?** | Catastrophic security failure. If the database is compromised, all passwords would be exposed. |
| **Why not SHA-256 alone?** | Vulnerable to rainbow table attacks. Salting + key stretching (iterations) makes brute force impractical. |

---

## 3. Presentation Decisions

### 3.1 Jinja2 Templates over Vanilla JavaScript DOM Manipulation

| Aspect | Chosen: Jinja2 Templates | Alternative: Vanilla JS + fetch() |
|---|---|---|
| **Rendering** | Server generates complete HTML — browser displays it immediately | Browser fetches JSON, then JavaScript builds the DOM element by element |
| **Security** | Auto-escaping enabled by default — XSS protection is automatic | Developer must manually call `escapeHtml()` on every dynamic value |
| **Complexity** | Template syntax is HTML with `{{ variables }}` — familiar to anyone who knows HTML | Requires understanding of async/await, DOM APIs, event delegation |
| **State management** | No client-side state — every page load is a fresh render from the database | JavaScript must track local state and keep it in sync with the server |
| **Trade-off** | Full page reloads on every navigation — no partial updates | Smoother UX with partial DOM updates |

**Decision:** Jinja2 templates. The auto-escaping alone justifies this choice — XSS is the most common web vulnerability, and Jinja2 prevents it by default rather than relying on developers to remember `escapeHtml()` on every output. The full-page-reload trade-off is negligible for a 4-page application.

### 3.2 Pico CSS over Bootstrap/Tailwind

| Aspect | Chosen: Pico CSS | Alternative: Bootstrap |
|---|---|---|
| **Classes** | Classless — styles semantic HTML automatically | Class-heavy — `<button class="btn btn-primary btn-lg">` |
| **HTML quality** | Forces clean, semantic HTML | Allows (encourages) non-semantic markup |
| **Accessibility** | Semantic elements are inherently accessible | Requires ARIA attributes to compensate for non-semantic markup |
| **File size** | ~10 KB | ~200 KB (CSS + JS) |
| **Trade-off** | Less customisation without overrides | Extensive component library and utility classes |

**Decision:** Pico CSS. The classless approach enforces clean semantic HTML (`<nav>`, `<article>`, `<table>`) and provides professional styling automatically. HTML describes content structure, not visual presentation — which improves accessibility and maintainability.

### 3.3 Chart.js for Dashboard Visualisation

| Aspect | Chosen: Chart.js | Alternative: D3.js |
|---|---|---|
| **API** | Declarative — pass data and options, get a chart | Imperative — manually bind data to SVG elements |
| **Learning curve** | Minutes to create basic charts | Hours/days for basic charts |
| **Responsiveness** | Built-in responsive behaviour | Manual responsive handling |
| **Trade-off** | Limited to standard chart types | Unlimited custom visualisations |

**Decision:** Chart.js. The dashboard needs standard chart types (doughnut, bar). Chart.js is the ONLY JavaScript in the project — the rest of the rendering is handled by Jinja2 templates. D3's power is unnecessary and would consume development time better spent on RBAC and business logic.

### 3.4 Template Inheritance for DRY Layout

| Aspect | Detail |
|---|---|
| **Pattern** | `base.html` defines the shared layout (nav, flash messages, footer, scripts). Each page template uses `{% extends "base.html" %}` and fills `{% block content %}`. |
| **Benefit** | Navigation bar, flash message rendering, and CSS/JS includes are defined ONCE. Changes to the nav update all pages automatically. |
| **Benefit** | Role-conditional UI (e.g., hiding the "Clients" nav link for staff) is defined in one place — `base.html` — not duplicated across pages. |
| **Industry parallel** | Template inheritance is the standard DRY pattern in Django, Rails (layouts), and Laravel (Blade). |

---

## 4. Security Decisions

### 4.1 Two Lines of Defence (Defence in Depth)

| Line of Defence | Purpose | What If It's Missing? |
|---|---|---|
| **Route decorators** | Security — rejects unauthorised requests at the server | Without it: anyone can POST to a create/delete route directly |
| **Query-level filtering** | Safety net — ensures data leaks can't happen even if decorators fail | Without it: a missing decorator means full data exposure |

**Why not three lines (with frontend UI hiding)?** In a server-rendered architecture, the template conditionally renders UI elements using `{% if role == 'admin' %}`. But this is a **design property**, not a defence line — the restricted HTML is never sent to the browser in the first place. In an SPA, the frontend hides elements that are already in the DOM — that's a defence line because it can be bypassed with DevTools. Here, there is nothing to bypass.

**Decision:** Two lines of defence. Each line catches a different class of failure:
- Decorators catch direct URL access (someone bookmarking or crafting a POST)
- Query filters catch logic errors (a forgotten decorator on a secondary route)

### 4.2 Jinja2 Auto-Escaping over Manual Escaping

| Aspect | Chosen: Jinja2 Auto-Escaping | Alternative: Manual escapeHtml() |
|---|---|---|
| **Default behaviour** | All `{{ variables }}` are escaped automatically | Developer must remember to escape EVERY dynamic value |
| **Error mode** | Fails safe — forgetting to escape still renders safely | Fails open — forgetting to escape creates an XSS vulnerability |
| **Opt-out** | Must explicitly use `{{ value\|safe }}` to render raw HTML | Must explicitly call `escapeHtml()` to render safely |
| **Coverage** | 100% of template variables are protected by default | Coverage depends on developer discipline |

**Decision:** Auto-escaping. This is a "secure by default" approach — the developer must actively opt OUT of security (using the `|safe` filter) rather than remembering to opt IN for every output. In a team setting, this eliminates an entire class of security bugs.

### 4.3 Post-Redirect-Get (PRG) Pattern

| Aspect | Detail |
|---|---|
| **Problem** | If a POST handler renders a page directly, refreshing the browser resubmits the form — creating duplicate records |
| **Solution** | Every POST handler ends with `redirect()`, never `render_template()`. The browser follows the redirect (GET), and refreshing reloads the GET — no resubmission. |
| **Benefit** | Prevents duplicate task creation, double file uploads, and accidental deletions |
| **Industry parallel** | PRG is the standard pattern in every server-rendered framework (Django, Rails, Laravel, ASP.NET) |

### 4.4 Session Cookies over JWT Tokens

| Aspect | Chosen: Session Cookies | Alternative: JWT |
|---|---|---|
| **Storage** | Server-side session store | Client-side token |
| **Revocation** | Instant — clear session on server | Difficult — token valid until expiry |
| **Complexity** | Flask built-in session handling | Requires token generation, validation, refresh logic |
| **Security** | HttpOnly flag prevents JavaScript access to the session cookie (XSS protection) | Token stored in localStorage is vulnerable to XSS |
| **Trade-off** | Server must store session state | Stateless — better for microservices |

**Decision:** Session cookies. Flask's built-in session support is simpler, more secure by default (HttpOnly prevents JavaScript access), and sufficient for a server-rendered application.

### 4.5 UUID File Renaming

| Aspect | Detail |
|---|---|
| **Problem** | User-provided filenames could contain path traversal (`../../`), special characters, or collisions |
| **Solution** | Rename every uploaded file to a UUID (`a1b2c3d4e5f6...pdf`), store original name separately |
| **Benefit 1** | Path traversal is impossible — UUID contains only hex digits and dashes |
| **Benefit 2** | Two users uploading `report.pdf` get different UUIDs — no collision |
| **Benefit 3** | Original name preserved in database — displayed to user for download |

---

## 5. Development Process Decisions

### 5.1 Blueprint-Based Modularity

| Aspect | Detail |
|---|---|
| **Pattern** | Each functional area (auth, tasks, clients, dashboard, attachments) is a Flask Blueprint in its own file |
| **Benefit** | Team members can work on different Blueprints simultaneously without merge conflicts |
| **Benefit** | Each file is focused — auth.py handles authentication, nothing else |
| **Benefit** | New features can be added as new Blueprints without modifying existing code |
| **Traceable** | Each Blueprint maps to a subsystem in the decomposition diagram |

### 5.2 Application Factory Pattern

| Aspect | Detail |
|---|---|
| **Pattern** | `create_app()` function in app.py builds and configures the Flask app |
| **Benefit** | Multiple app instances can be created for testing with different configs |
| **Benefit** | Circular import issues are avoided — Blueprints import from `database.py`, not from `app.py` |

### 5.3 Flash Messages for User Feedback

| Aspect | Detail |
|---|---|
| **Pattern** | All user-facing feedback uses Flask's `flash()` mechanism with categories ("success", "error") |
| **Benefit** | One rendering point in `base.html` — every page displays flash messages the same way |
| **Benefit** | Messages survive the redirect (PRG pattern) — flash stores in session, consumed on next render |
| **Industry parallel** | Flash messages are the standard feedback pattern in Django, Rails, and Laravel |

---

## 6. Trade-offs Acknowledged

| Decision | What We Gained | What We Gave Up |
|---|---|---|
| Server-rendered over SPA | Simplicity, one language, auto-escaping | API reusability, partial page updates |
| Jinja2 over vanilla JS | Auto-escaping, no build tools, template inheritance | Client-side interactivity, smoother UX |
| SQLite over PostgreSQL | Zero-config setup, file portability | Concurrent write support, production scalability |
| Session cookies over JWT | Simplicity, instant revocation | Stateless architecture, cross-domain auth |
| Direct SQL over ORM | Visible, auditable security | Auto-migrations, model validation |
| Pico CSS over Bootstrap | Clean HTML, small size | Component library, utility classes |
| PRG pattern over direct render | No double-submission | Extra redirect on every form submission |

---

> **📝 Examiner Note:** Design justifications demonstrate the highest-order thinking the OS exam assesses: the ability to evaluate options and make reasoned decisions. The "We chose X over Y because Z" format shows analytical skills. Students who simply STATE their technology choices without explaining WHY lose significant marks in the Design assessment area (worth 20% of the total). Every justification should connect back to a project constraint — educational context, team size, deployment target, or security requirement. Acknowledging trade-offs explicitly ("We gave up X to gain Y") shows mature engineering judgement.
