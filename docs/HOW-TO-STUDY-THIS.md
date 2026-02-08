# How to Study This Model Answer

## What This Repo Is

This repository contains a **complete, finished** model answer for the T Level DPDD Occupational Specialism project. Every deliverable — from briefing notes to reflective report — is here, alongside a fully working web application.

But the finished product isn't the point. **The process is the point.**

Every commit in this repository represents a deliberate step in the development process. They are in the exact order a developer would work through the project. Your job is to follow this sequence for your own project — not to copy the content, but to understand **what to produce, in what order, and why**.

---

## Supporting Documents

You don't need these to follow the 24 steps below, but they're here when you need them:

- **[BEGINNERS-BRIDGE.md](BEGINNERS-BRIDGE.md)** — If the code looks unfamiliar even though you can write Python in class, start here. It maps classroom concepts (variables, functions, if-statements) to the patterns used in this codebase.
- **[WALKTHROUGH.md](WALKTHROUGH.md)** — Explains *why* each technical decision was made (Why Flask? Why Jinja2? Why not a JavaScript frontend?). Read this when you're wondering "but why not just...?"
- **[EXAM-DECODER.md](EXAM-DECODER.md)** — Maps the marking criteria to specific evidence in this project. Use it to check your own work before submission.
- **[EXTENSION-CHALLENGES.md](EXTENSION-CHALLENGES.md)** — Scaffolded exercises to try after you've studied the model answer. Builds confidence by letting you add features yourself.
- **[WHY-THIS-IS-DISTINCTION.md](WHY-THIS-IS-DISTINCTION.md)** — Walks through each assessment area and shows specifically *why* the model answer scores Distinction. Includes a self-check checklist you can use on your own project.

---

## How to Walk Through the History

This guide is built around **time-travel**. Each step includes a commit hash — a snapshot of the project at that exact moment. You check out each one in order and see the project grow, piece by piece.

#### Before you start

When you check out an earlier commit, your local files revert to that point in time — **none of the teaching documents or the full README will exist locally yet.** So before you begin, open these browser tabs on GitHub. They show the `main` branch and won't change when you check out different commits locally:

1. **[README.md](https://github.com/richey-malhotra/group-project-jinja/blob/main/README.md)** — project structure, login credentials, tech stack
2. **[HOW-TO-STUDY-THIS.md](https://github.com/richey-malhotra/group-project-jinja/blob/main/docs/HOW-TO-STUDY-THIS.md)** — this guide (the 24-step walkthrough you're following)
3. **[BEGINNERS-BRIDGE.md](https://github.com/richey-malhotra/group-project-jinja/blob/main/docs/BEGINNERS-BRIDGE.md)** — maps classroom Python to the patterns in the codebase
4. **[WALKTHROUGH.md](https://github.com/richey-malhotra/group-project-jinja/blob/main/docs/WALKTHROUGH.md)** — explains why each technical decision was made
5. **[EXAM-DECODER.md](https://github.com/richey-malhotra/group-project-jinja/blob/main/docs/EXAM-DECODER.md)** — maps marking criteria to specific evidence
6. **[EXTENSION-CHALLENGES.md](https://github.com/richey-malhotra/group-project-jinja/blob/main/docs/EXTENSION-CHALLENGES.md)** — scaffolded exercises to practise adding features
7. **[WHY-THIS-IS-DISTINCTION.md](https://github.com/richey-malhotra/group-project-jinja/blob/main/docs/WHY-THIS-IS-DISTINCTION.md)** — why the model answer scores Distinction, with a self-check checklist

Keep these tabs open throughout. They're your reference while your local folder shows the project at each stage of development.

#### The one command you need

```bash
git checkout <hash>
```

When you run this, Git will say "You are in 'detached HEAD' state." **This is normal and safe.** It just means you're looking at an older version of the project. Nothing is broken.

You go **straight from one hash to the next** — there's no need to return to `main` between steps. At step 1 you check out the first hash, at step 2 you check out the second hash, and so on. When you've finished all 24 steps, you run `git checkout main` once to return to the complete project.

#### The walkthrough

For each step below:
1. **Run** `git checkout <hash>` to jump to that point in the project's history
2. **Look at your local folder** — notice what files exist and what doesn't exist yet
3. **Read** the step guidance here (in your browser tab) to understand what was done and why
4. **Check out the next hash** when you're ready to move on

> **Tip:** At step 1, your folder has almost nothing — a README, a requirements file, and empty folders. By step 24, there's a complete working application. Watching it grow is the point.

---

### Setup

| Step | Commit | What was done |
|------|--------|---------------|
| 1 | `a0cd7a5` | **Project setup** — README, dependencies, folder structure |

**Checkout:** `git checkout a0cd7a5` — then look at the folder. This is the starting point: just a README, a requirements file, a `.gitignore`, and an empty folder structure. No code yet.

**For your own project:** Before writing anything, set up your repository. Create a README that explains what your project is. Set up your Python environment. Install Flask. Make your first commit. This shows the examiner you started with professional discipline, not by hacking code together.

---

### Task 0 — Employer Briefing (1 step)

| Step | Commit | What was done |
|------|--------|---------------|
| 2 | `e745fe6` | **Briefing notes** — Problems, stakeholders, proposed solution |

**Checkout:** `git checkout e745fe6` — the first document has appeared in `docs/model-answer/task-0-briefing/`. Still no code.

**For your own project:** Read the fact file carefully. Write up:
- What is MJ Limited's actual problem? (Not "they need a website" — what's going wrong day-to-day?)
- Who are the stakeholders and what does each group need?
- What solution are you proposing and why?
- What technology choices are you making, and what's the justification?

This is where you demonstrate you **understand the business problem before jumping to code**. The marking scheme rewards analysis, not just building.

---

### Task 1 — Planning (1 step)

| Step | Commit | What was done |
|------|--------|---------------|
| 3 | `abf9195` | **Project plan** — Waterfall schedule, risk register, MoSCoW priorities |

**Checkout:** `git checkout abf9195` — the planning folder now has content. Notice how the plan references the briefing notes from the previous step.

**For your own project:** Create a realistic plan that covers all 105 hours across the six phases. Include:
- A timeline showing what you'll do in each phase
- A risk register (what could go wrong, and what you'll do about it)
- MoSCoW prioritisation (what you MUST build vs what you'd LIKE to build)

Common mistake: students allocate all the time to coding. Look at the model answer — development is only 30 of the 105 hours. Planning, design, testing, and presentation take up the rest. Your plan should reflect this.

---

### Task 2 — Requirements (1 step)

| Step | Commit | What was done |
|------|--------|---------------|
| 4 | `ae88260` | **Requirements specification** — Functional requirements, user stories, traceability |

**Checkout:** `git checkout ae88260` — the requirements folder appears. Each requirement has a unique ID (like `FR-AUTH-01`) that will be referenced in every later document.

**For your own project:** This is where you turn the briefing notes into specific, testable requirements. Each requirement needs:
- A unique ID (like `FR-AUTH-01`) so you can reference it later in design, code, and test documents
- A clear statement of what the system SHALL do
- A link back to the user story or business need it addresses
- A priority (Must / Should / Could / Won't)

Notice how the model answer traces every requirement back to a quote from the fact file. The examiner wants to see that your requirements come from the brief, not from thin air.

---

### Task 3 — Design (9 steps)

This is the largest section. Nine separate design documents were created, each as its own commit. This is deliberate — it shows that design is not a single activity but a collection of specific artefacts, each serving a different purpose.

| Step | Commit | What was done |
|------|--------|---------------|
| 5 | `7532411` | **System architecture** — Three-layer design and technology choices |
| 6 | `af6f5de` | **Functional decomposition** — Breaking the system into modules |
| 7 | `95d97f6` | **Data flow diagrams** — Level 0 context and Level 1 processes |
| 8 | `dd03144` | **ERD and data dictionary** — Tables, relationships, field definitions |
| 9 | `f4b6b61` | **Wireframes and screen flow** — Page layouts for each user role |
| 10 | `1a494ac` | **Sequence diagrams** — How components interact for each feature |
| 11 | `0c9fcf4` | **Pseudocode** — Key algorithms in plain English |
| 12 | `e43e69a` | **Route design** — URL patterns, methods, and role permissions |
| 13 | `88e2dba` | **Design justifications** — Why each technology and pattern was chosen |

**Checkout each one in order** to watch the design grow:
- `git checkout 7532411` — Architecture appears. Just one design document.
- `git checkout af6f5de` — Decomposition added. The system is being broken into modules.
- `git checkout 95d97f6` — DFDs show how data moves through the system.
- `git checkout dd03144` — ERD and data dictionary define the database structure.
- `git checkout f4b6b61` — Wireframes show what each page looks like for each role.
- `git checkout 1a494ac` — Sequence diagrams show component interactions.
- `git checkout 0c9fcf4` — Pseudocode translates the design into plain-English algorithms.
- `git checkout e43e69a` — Route design maps every URL pattern, method, and permission.
- `git checkout 88e2dba` — Design justifications explain *why* each choice was made.

By step 13, the `docs/model-answer/task-3-design/` folder has nine documents — and still no application code. The entire system has been designed on paper first.

**For your own project:** You don't have to produce all nine documents. But the more design work you show, the stronger your evidence for the design marks. At minimum, most students should produce:

- **System architecture** — How does your system fit together? What talks to what?
- **ERD** — What tables does your database have? What are the relationships?
- **Wireframes** — What will each page look like? How does the layout change for different user roles?
- **Pseudocode** — How do your key algorithms work in plain English before you write code?

The model answer also includes design **justifications** (Step 13). This is where many students lose marks. It's not enough to say "I used Flask." You need to say "I chose Flask over Django because Flask is lightweight and has minimal boilerplate, which suits a small team building a prototype. Django's admin panel and ORM would add unnecessary complexity for our scale."

---

### Task 4 — Development (8 steps)

Notice the order: database first, then application factory with the base template, then authentication, then features one at a time. This is not random — each piece depends on the one before it.

| Step | Commit | What was done |
|------|--------|---------------|
| 14 | `ba945de` | **Database + seed data** — Tables and sample data |
| 15 | `c1a7f68` | **Application factory + base template** — Flask app structure, Jinja2 layout, CSS |
| 16 | `560aae6` | **Authentication** — Login system with role-based access control |
| 17 | `88b175b` | **Task management** — Create, read, update, delete with role checks |
| 18 | `c2f1d70` | **Client management** — CRUD operations with data integrity checks |
| 19 | `63ed8d0` | **Dashboard** — Charts showing role-appropriate statistics |
| 20 | `c00bbea` | **File attachments** — Upload and download with security validation |
| 21 | `e3a6b8c` | **Developer notes** — What was built, problems hit, and how they were solved |

**Checkout each one in order** to watch the application come to life:

| Step | Command | What you'll see |
|------|---------|-----------------|
| 14 | `git checkout ba945de` | `database.py` and `seed_data.py` appear — the database exists but there's no web application yet |
| 15 | `git checkout c1a7f68` | `app.py`, `templates/base.html`, `templates/login.html`, and `static/css/style.css` appear — the Flask server can start and the base layout is ready, but there's nothing beyond the login page |
| 16 | `git checkout 560aae6` | `routes/auth.py` appears — you can now log in and out, but there's nothing to do after login |
| 17 | `git checkout 88b175b` | `routes/tasks.py` + `templates/tasks.html` appear — the first real feature works end-to-end |
| 18 | `git checkout c2f1d70` | `routes/clients.py` + `templates/clients.html` appear — a second feature, following the same pattern |
| 19 | `git checkout 63ed8d0` | `routes/dashboard.py` + `templates/dashboard.html` + `static/js/charts.js` appear — data from tasks and clients is aggregated into charts |
| 20 | `git checkout c00bbea` | `routes/attachments.py` + `templates/task_detail.html` appear — file upload and download with security validation |
| 21 | `git checkout e3a6b8c` | Developer notes added — documenting what was built, problems hit, and how they were solved |

> **Try this:** At step 16, run `python app.py` and log in. You'll see there are no tasks, no clients, no dashboard — just authentication. Then checkout step 17 and run it again. Tasks appear. This is how professional developers build systems: one working feature at a time.

**For your own project:**

**Build in this order.** Database first — because every feature reads from or writes to it. Authentication second — because every feature needs to know who's logged in. Then individual features one at a time.

Notice the difference from a JavaScript SPA approach: there is no separate "frontend" step. In this server-rendered architecture, each feature includes both the route handler (Python) and the template (Jinja2) in the same commit. The template extends `base.html` and renders data passed from the route — there's no JavaScript `fetch()` cycle to wire up. Each feature is self-contained.

Each time you complete a feature, commit it. Your commit history is evidence of your development process. Examiners can see whether you built methodically or pasted everything in one go.

Step 21 is easy to overlook but important: write developer notes explaining what you built, what problems you hit, and how you solved them. The model answer's bug log (`docs/model-answer/task-4-development/developer-notes.md`) lists seven real bugs that were encountered and fixed. Examiners find this more credible than "everything worked perfectly."

---

### Task 5 — Testing and Documentation (2 steps)

| Step | Commit | What was done |
|------|--------|---------------|
| 22 | `51a130f` | **Test plan** — Test cases including access control boundary tests |
| 23 | `6758005` | **User guide + technical documentation** |

**Checkout:** `git checkout 51a130f` for the test plan, then `git checkout 6758005` for user guide and technical documentation. Notice how the test cases reference the requirement IDs from step 4 — that traceability chain runs from briefing to requirements to design to code to tests.

**What to look at:**
- `docs/model-answer/task-5-testing/test-plan-and-cases.md` — Full test plan
- `docs/model-answer/task-5-testing/user-guide.md` — How an end user operates the system
- `docs/model-answer/task-5-testing/technical-documentation.md` — How a developer sets up and maintains it

**For your own project:**

Your test plan should reference the requirement IDs from Task 2. Every FR-ID should have at least one test case verifying it works. The model answer traces each test case back to a specific requirement — that traceability is what earns higher marks.

Pay attention to **RBAC boundary testing**. The model answer has 25 test cases just for access control — testing that staff CANNOT do things they shouldn't, not just that admins CAN do things they should. Testing what should fail is as important as testing what should succeed.

In this server-rendered version, RBAC boundary tests work differently from an API version. Instead of testing with `fetch()` in the browser console, you test by navigating directly to restricted URLs or submitting POST requests (e.g., via `curl`). The test plan covers both approaches — direct URL access and form submission attempts.

Write the user guide for someone who has never seen the system. Write the technical documentation for a developer who needs to set it up from scratch. These are different audiences — the language and level of detail should be different.

---

### Task 6 — Presentation and Reflection (1 step)

| Step | Commit | What was done |
|------|--------|---------------|
| 24 | `0256a55` | **Presentation guide + reflective report** |

**Checkout:** `git checkout 0256a55` — the final deliverables. Run `git log --oneline --reverse` at this point and you'll see all 24 development steps laid out — that's your complete development narrative.

**What to look at:**
- `docs/model-answer/task-6-presentation/presentation-guide.md` — Structure, timing, demo script
- `docs/model-answer/task-6-presentation/reflective-report.md` — Individual reflection on the process

**For your own project:**

The presentation guide shows a 15-minute structure: 2 min introduction, 6 min live demo, 4 min technical highlights, 3 min reflection and questions. Practise your demo. Know exactly which features you'll show and in what order. Log in as each role to demonstrate access control differences.

The reflective report is personal — it's about YOUR experience, not a summary of the project. What skills did you develop? What would you do differently? What did you learn from problems you encountered? Be specific and honest.

---

## The Pattern You Should Notice

Now that you've walked through the history, look at the sequence again:

1. **Understand** the problem (Task 0)
2. **Plan** how to solve it (Task 1)
3. **Specify** what exactly to build (Task 2)
4. **Design** how it will work before writing code (Task 3)
5. **Build** it, one piece at a time (Task 4)
6. **Test** that it actually works as specified (Task 5)
7. **Present** and reflect on the process (Task 6)

Thirteen of the 24 commits happen **before any code is written**. That's more than half the process dedicated to understanding, planning, and designing. This is not an accident — it's how professional software development works. The code is the easy part. Knowing what to build, and why, is the hard part.

Your own project should follow this same shape. If your commit history shows 2 planning commits followed by 20 coding commits, that tells the examiner your process was unbalanced.

---

## Return to the Finished Version

Once you've walked through all 24 steps, run this one command to come back:

```bash
git checkout main
```

This restores the complete, finished project. From here you can run the application (`python app.py`), explore the full codebase, and try the extension challenges. You can close your GitHub browser tabs now — everything is back in your local folder.

---

## A Warning About Copying

**Don't copy.** Examiners compare submissions. The model answer uses MJ Limited's specific context — your version should use the same context but in your own words, reflecting your own understanding. Two submissions with identical phrasing will both be flagged.

To run the application and see it in action, follow the instructions in the [README](../README.md).

---

## What Next?

Once you've studied the model answer and understand the patterns:

1. Try the **[Extension Challenges](EXTENSION-CHALLENGES.md)** — scaffolded exercises where you add real features (CSV export, sortable tables, audit logging, user management) to a copy of this project. They're ordered from easiest to hardest, and each one maps to assessment criteria.

2. Read **[Why This Is Distinction](WHY-THIS-IS-DISTINCTION.md)** — it walks through each assessment area, explains what specifically makes the model answer Distinction-level, and includes a self-check checklist you can run against your own project before submission.
