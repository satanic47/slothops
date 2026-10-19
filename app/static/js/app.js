// SlothOps Frontend Application Logic

document.addEventListener("DOMContentLoaded", () => {
  const triageForm = document.getElementById("triage-form");
  const taskContainer = document.getElementById("task-container");
  const memoryForm = document.getElementById("memory-form");
  const memoryContainer = document.getElementById("memory-container");
  const hoursSavedEl = document.getElementById("hours-saved-stat");
  const tasksSlothedEl = document.getElementById("tasks-slothed-stat");

  // Sample Presets for Quick Testing
  const samples = {
    meeting: {
      title: "Quarterly Roadmap Review & Status Sync (60 min)",
      content: "Hey team, let's schedule an hour on Thursday to walk through all 80 Jira sprint tickets and brainstorm blockers for next month. Please check your calendars."
    },
    pr: {
      title: "GitHub PR #114: Fix CSS padding & update README (+12 lines)",
      content: "Automated PR from contributor fixing header alignment. All CI unit tests and linters pass with 0 errors. Diff size: +12 / -4 lines."
    },
    survey: {
      title: "Mandatory Workplace Wellness & Engagement Survey",
      content: "Hi all, please take 30 minutes before Friday to fill out the 50-question internal workplace satisfaction survey on Google Forms."
    }
  };

  window.loadPreset = (key) => {
    if (samples[key]) {
      document.getElementById("task-title").value = samples[key].title;
      document.getElementById("task-content").value = samples[key].content;
    }
  };

  // Handle Task Triage Submission
  if (triageForm) {
    triageForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const submitBtn = triageForm.querySelector("button[type='submit']");
      const title = document.getElementById("task-title").value.trim();
      const content = document.getElementById("task-content").value.trim();

      if (!title || !content) return;

      submitBtn.disabled = true;
      submitBtn.innerHTML = "🦥 Distilling with Tinker...";

      try {
        const res = await fetch("/api/sloth/triage", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title, content })
        });

        if (res.ok) {
          const task = await res.json();
          prependTaskCard(task);
          triageForm.reset();
          updateStats(task.minutes_saved);
        } else {
          alert("Error triaging task. Check server logs.");
        }
      } catch (err) {
        console.error(err);
        alert("Failed to connect to SlothOps backend.");
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = "⚡ Distill with SlothOps";
      }
    });
  }

  function prependTaskCard(task) {
    const card = document.createElement("div");
    card.className = "task-card";
    card.innerHTML = `
      <div class="task-card-top">
        <span class="task-title">${escapeHtml(task.title)}</span>
        <span class="action-pill">${escapeHtml(task.sloth_action)}</span>
      </div>
      <p class="task-summary">${escapeHtml(task.one_line_summary)}</p>
      <div class="draft-box">
        <strong>Auto-Draft:</strong> ${escapeHtml(task.lazy_reply_draft)}
      </div>
      <div class="task-meta">
        <span>⏱ Saved: <strong>${task.minutes_saved}m</strong></span>
        <span>🧠 Model: <em>Tinker LoRA + Backboard RAG</em></span>
        <span class="status-badge">AUTO-EXECUTED</span>
      </div>
    `;
    if (taskContainer) {
      taskContainer.insertBefore(card, taskContainer.firstChild);
    }
  }

  // Handle Memory Rule Addition
  if (memoryForm) {
    memoryForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const input = document.getElementById("memory-rule-input");
      const rule = input.value.trim();
      if (!rule) return;

      try {
        const res = await fetch("/api/memory", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ rule })
        });
        if (res.ok) {
          const mem = await res.json();
          const item = document.createElement("div");
          item.className = "memory-item";
          item.innerHTML = `
            <div class="memory-rule">"${escapeHtml(mem.rule)}"</div>
            <div class="memory-meta">Policy Category: ${escapeHtml(mem.category)} • Stored in Backboard.io</div>
          `;
          memoryContainer.appendChild(item);
          input.value = "";
        }
      } catch (err) {
        console.error(err);
      }
    });
  }

  function updateStats(minutesAdded) {
    if (hoursSavedEl) {
      let currentHours = parseFloat(hoursSavedEl.innerText) || 0;
      hoursSavedEl.innerText = (currentHours + (minutesAdded / 60)).toFixed(1) + "h";
    }
    if (tasksSlothedEl) {
      let count = parseInt(tasksSlothedEl.innerText) || 0;
      tasksSlothedEl.innerText = count + 1;
    }
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
  }
});
