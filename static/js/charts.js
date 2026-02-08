/**
 * charts.js — Chart.js rendering for the dashboard.
 *
 * This file is the ONLY significant JavaScript in the application.
 * Chart.js requires JavaScript to draw charts on <canvas> elements —
 * there is no way to render interactive charts with pure HTML/CSS.
 *
 * The data comes from Python via Jinja2's {{ charts | tojson }} filter,
 * which safely converts Python dicts to JSON strings. This file
 * receives that data through the renderCharts() function.
 *
 * Why a separate file?
 * - Keeps JavaScript out of the HTML template
 * - Can be cached by the browser (fewer bytes on repeat visits)
 * - Easier to test and maintain than inline <script> blocks
 */

/**
 * Render all dashboard charts based on role and available data.
 *
 * @param {Object} data  - Chart datasets from the server (labels, data, colours)
 * @param {string} role  - Current user's role (admin, manager, staff)
 */
function renderCharts(data, role) {
  // --- Tasks by Status (all roles) ---
  if (data.tasks_by_status) {
    new Chart(document.getElementById("statusChart"), {
      type: "doughnut",
      data: {
        labels: data.tasks_by_status.labels,
        datasets: [
          {
            data: data.tasks_by_status.data,
            backgroundColor: data.tasks_by_status.backgroundColor,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { position: "bottom" } },
      },
    });
  }

  // --- Tasks by Priority (all roles) ---
  if (data.tasks_by_priority) {
    new Chart(document.getElementById("priorityChart"), {
      type: "doughnut",
      data: {
        labels: data.tasks_by_priority.labels,
        datasets: [
          {
            data: data.tasks_by_priority.data,
            backgroundColor: data.tasks_by_priority.backgroundColor,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { position: "bottom" } },
      },
    });
  }

  // --- Tasks by Department (admin only) ---
  if (data.tasks_by_department && role === "admin") {
    new Chart(document.getElementById("departmentChart"), {
      type: "bar",
      data: {
        labels: data.tasks_by_department.labels,
        datasets: [
          {
            label: "Tasks",
            data: data.tasks_by_department.data,
            backgroundColor: data.tasks_by_department.backgroundColor,
          },
        ],
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
        plugins: { legend: { display: false } },
      },
    });
  }

  // --- Workload by Staff (admin + manager) ---
  if (data.workload_by_user && (role === "admin" || role === "manager")) {
    new Chart(document.getElementById("workloadChart"), {
      type: "bar",
      data: {
        labels: data.workload_by_user.labels,
        datasets: [
          {
            label: "Active Tasks",
            data: data.workload_by_user.data,
            backgroundColor: data.workload_by_user.backgroundColor,
          },
        ],
      },
      options: {
        responsive: true,
        indexAxis: "y",
        scales: { x: { beginAtZero: true, ticks: { stepSize: 1 } } },
        plugins: { legend: { display: false } },
      },
    });
  }
}
