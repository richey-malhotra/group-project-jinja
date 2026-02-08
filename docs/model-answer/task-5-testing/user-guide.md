# Task 5b: User Guide

## MJ Limited Business Task Manager — User Guide

> **📋 Student Scope**
>
> **Core — what you need:** A getting started section (login/logout), a permissions summary table showing what each role can do, and step-by-step instructions for the main tasks (viewing, creating, editing, deleting). The permissions table is critical — it MUST match your actual implementation. Write for end users, not developers.
>
> **Stretch — what makes it exceptional:** This document shows the full stretch version: getting started (Section 1), role permissions (Section 2), navigation (Section 3), dashboard (Section 4), task management with role-specific instructions (Section 5), client management (Section 6), file attachments (Section 7), and a troubleshooting table (Section 8). Screenshots should be added for final submission. A shorter version covering login + tasks + permissions is perfectly acceptable — but the permissions table must match your actual implementation.

---

### 1. Getting Started

#### Accessing the System
Open a web browser and navigate to the application URL. You will see the login page.

#### Logging In
1. Enter your **username** in the first field
2. Enter your **password** in the second field
3. Click **Sign In**

If your credentials are correct, you will be redirected to your default page:
- **Admin / Manager:** Dashboard
- **Staff:** Dashboard

If you see "Invalid username or password", check your credentials and try again. Contact your IT administrator if the problem persists.

#### Logging Out
Click **Logout** in the top-right corner of any page. You will be returned to the login page.

---

### 2. Understanding Your Role

The system has three user roles. Your role determines what you can see and do.

#### Permissions Summary

| Feature | Admin | Manager | Staff |
|---|---|---|---|
| **View dashboard** | ✅ Organisation-wide | ✅ Department only | ✅ Personal tasks only |
| **View tasks** | ✅ All tasks | ✅ All tasks | ✅ Own tasks only |
| **Create tasks** | ✅ | ✅ | ❌ |
| **Edit tasks (all fields)** | ✅ Any task | ✅ Any task | ❌ |
| **Update task status** | ✅ Any task | ✅ Any task | ✅ Own tasks only |
| **Delete tasks** | ✅ | ✅ | ❌ |
| **View clients** | ✅ | ✅ | ❌ |
| **Create/edit clients** | ✅ | ✅ | ❌ |
| **Delete clients** | ✅ | ❌ | ❌ |
| **Upload attachments** | ✅ | ✅ | ✅ |
| **Delete attachments** | ✅ Any | ✅ Any | ✅ Own uploads only |

> **Important:** Staff members can ONLY update the **status** of tasks **assigned to them**. They cannot change the title, priority, description, assignment, or any other field. They cannot create new tasks or delete tasks.

---

### 3. Navigation

The navigation bar appears at the top of every page. The links you see depend on your role:

| Link | Visible To | Where It Goes |
|---|---|---|
| Dashboard | Everyone | Summary statistics and charts (scoped to role) |
| Tasks | Everyone | Task list and management |
| Clients | Admin, Manager only | Client records |

Your **role badge** is displayed next to your name in the navigation bar:
- 🔴 **Admin** — red badge
- 🟡 **Manager** — amber badge
- 🟢 **Staff** — green badge

---

### 4. Dashboard

The dashboard provides a visual overview of work across the organisation (admin), your department (manager), or your personal tasks (staff).

#### Stat Cards
- **Total Tasks** — Count of all tasks in your scope
- **Open Tasks** — Tasks with status "open"
- **In Progress Tasks** — Tasks with status "in_progress"
- **Completed Tasks** — Tasks with status "completed"
- **Overdue Tasks** — Tasks past their due date that are not completed
- **Urgent Tasks** — Tasks with "urgent" priority that are not completed
- **Active Clients** — Active client count (admin and manager only)
- **Total Staff** — Total user count across the organisation (admin only)

#### Charts
| Chart | Shows | Visible To |
|---|---|---|
| Tasks by Status | Doughnut chart of status distribution | All roles |
| Tasks by Priority | Doughnut chart of priority distribution | All roles |
| Tasks by Department | Bar chart of tasks per department | Admin only |
| Workload by Staff | Bar chart of tasks per team member | Admin, Manager |

---

### 5. Task Management

#### Viewing Tasks

**Admin/Manager:** You see all tasks in the system. Use the filters at the top to narrow the list:
- **Search** — type keywords to find tasks by title or description
- **Status filter** — show only tasks with a specific status
- **Priority filter** — show only tasks with a specific priority
- **Department filter** — show only tasks from a specific department

**Staff:** You see only tasks assigned to you. The heading shows "My Tasks" and the department filter is hidden.

#### Creating a Task (Admin/Manager only)
1. Click **+ New Task**
2. Fill in the form:
   - **Title** (required) — short descriptive name
   - **Description** — detailed explanation of the work
   - **Status** — current state (defaults to "open")
   - **Priority** — urgency level (defaults to "Medium")
   - **Department** — which department this task belongs to
   - **Assigned To** — the staff member responsible
   - **Client** — the client this task relates to (optional)
   - **Due Date** — when the task should be completed
3. Click **Create Task**

#### Editing a Task (Admin/Manager)
1. Click the **✏️ Edit** button on a task row
2. Modify the fields you want to change
3. Click **Save Changes**

#### Updating Task Status (Staff)
1. Find your task in the task list
2. Select the new status from the dropdown — the form submits automatically

> You can only change the status — no other fields can be modified by staff users.

#### Deleting a Task (Admin/Manager only)
1. Click the **🗑️ Delete** button on a task row
2. Confirm the deletion when prompted
3. The task and any attached files will be permanently removed

---

### 6. Client Management (Admin & Manager only)

Staff members do not have access to the Clients page.

#### Viewing Clients
The client list shows all business clients with their company name, contact person, industry, and status.

Use the **Search** box and **Industry/Status** filters to find specific clients.

#### Creating a Client
1. Click **+ New Client**
2. Fill in the form:
   - **Company Name** (required)
   - **Contact Person**
   - **Email**
   - **Phone**
   - **Industry**
   - **Status** (Active/Inactive)
   - **Notes**
3. Click **Create Client**

#### Editing a Client (Admin/Manager)
1. Click the **✏️ Edit** button on a client row
2. Modify the fields
3. Click **Save Changes**

#### Deleting a Client (Admin only)
1. Click the **🗑️ Delete** button
2. If the client has linked tasks, deletion is blocked — you must reassign or delete those tasks first
3. Confirm deletion

> Managers can create and edit clients but cannot delete them. Only admins can delete client records.

---

### 7. File Attachments

#### Uploading a File
1. Open a task (via the edit or detail view)
2. In the Attachments section, click **Choose File**
3. Select a file from your computer
4. Click **Upload**

**Allowed file types:** PDF, Word (.doc, .docx), Excel (.xls, .xlsx), CSV, Text (.txt), Images (.png, .jpg, .jpeg, .gif)

**Maximum file size:** 5 MB

#### Downloading a File
Click the filename in the attachments list to download.

#### Deleting an Attachment
Click the **🗑️** button next to the attachment. You can delete attachments you uploaded. Admin and manager users can delete any attachment.

---

### 8. Troubleshooting

| Problem | Solution |
|---|---|
| Can't log in | Check username and password. Passwords are case-sensitive. |
| "Session expired" error | Your session timed out. Log in again. |
| Can't see Clients link | This is hidden for staff users. This is by design — contact your manager if you believe your role is incorrect. |
| Can't create tasks | Only admin and manager users can create tasks. Staff users can only update the status of their assigned tasks. |
| Can't delete a client | Only admin users can delete clients. If you are admin and still get an error, the client may have linked tasks — delete or reassign those first. |
| File upload fails | Check that the file type is allowed and the file is under 5 MB. |
| Changes not appearing | Try refreshing the page. If the issue persists, log out and log back in. |

---

> **📝 Examiner Note:** The user guide is written for END USERS, not developers. It uses non-technical language and focuses on TASKS the user wants to accomplish. The permissions table is critical — it must accurately match the implemented RBAC rules. Note that staff CANNOT create tasks (this is a common error in student submissions where the user guide doesn't match the code). Screenshots should be added for final submission — each section should show the relevant page from the appropriate role's perspective.
