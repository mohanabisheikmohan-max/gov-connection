let selectedDepartment = "Education";

function selectDepartment(button) {
  document.querySelectorAll(".department").forEach(x => x.classList.remove("active"));
  button.classList.add("active");
  selectedDepartment = button.dataset.name;

  const d = window.DEPARTMENTS[selectedDepartment];
  document.getElementById("headerDept").textContent = selectedDepartment;
  document.getElementById("headerIcon").textContent = d.icon;
  document.getElementById("deptTitle").textContent = selectedDepartment;
  document.getElementById("deptDescription").textContent = d.description;

  const chips = document.getElementById("topicChips");
  chips.innerHTML = d.topics.map(t => `<span>${escapeHtml(t)}</span>`).join("");

  addAIMessage(`Department changed to <b>${escapeHtml(selectedDepartment)}</b>.<br>
  You can now ask questions focused on this department.`);
}

function addUserMessage(text) {
  const area = document.getElementById("messages");
  area.insertAdjacentHTML("beforeend", `
    <div class="message user">
      <div class="bubble"><div class="message-name">You</div><p>${escapeHtml(text)}</p></div>
    </div>`);
  scrollMessages();
}

function addAIMessage(html) {
  const area = document.getElementById("messages");
  area.insertAdjacentHTML("beforeend", `
    <div class="message ai">
      <div class="avatar">🤖</div>
      <div class="bubble"><div class="message-name">GovConnect AI</div><p>${html}</p></div>
    </div>`);
  scrollMessages();
}

function addTyping() {
  const area = document.getElementById("messages");
  area.insertAdjacentHTML("beforeend", `
    <div class="message ai" id="typing">
      <div class="avatar">🤖</div>
      <div class="bubble typing"><span></span><span></span><span></span></div>
    </div>`);
  scrollMessages();
}

function removeTyping() {
  const t = document.getElementById("typing");
  if (t) t.remove();
}

async function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;

  input.value = "";
  input.style.height = "auto";
  addUserMessage(message);
  addTyping();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message, department: selectedDepartment})
    });
    const data = await response.json();
    removeTyping();
    addAIMessage(formatAI(data.answer || "No answer returned."));
  } catch (error) {
    removeTyping();
    addAIMessage("The AI service is currently unavailable. Please check the server and Gemini configuration.");
  }
}

function quickAsk(text) {
  document.getElementById("messageInput").value = text;
  sendMessage();
}

async function showUpdates() {
  const modal = document.getElementById("updatesModal");
  const list = document.getElementById("updatesList");
  modal.classList.add("show");
  list.innerHTML = `<div class="loading">Loading updates...</div>`;
  try {
    const data = await fetch("/api/updates").then(r => r.json());
    list.innerHTML = data.map(u => `
      <div class="update-item">
        <div class="update-date">${escapeHtml(u.date)}</div>
        <h3>${escapeHtml(u.title)}</h3>
        <small>${escapeHtml(u.department)}</small>
        <p>${escapeHtml(u.text)}</p>
      </div>`).join("");
  } catch {
    list.innerHTML = `<div class="update-item">Unable to load updates.</div>`;
  }
}

function openAbout() { document.getElementById("aboutModal").classList.add("show"); }
function closeModal(id) { document.getElementById(id).classList.remove("show"); }

function formatAI(text) {
  return escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
    .replace(/\n/g, "<br>");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[c]));
}

function scrollMessages() {
  const area = document.getElementById("messages");
  setTimeout(() => area.scrollTop = area.scrollHeight, 20);
}

const input = document.getElementById("messageInput");
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 130) + "px";
});

window.addEventListener("click", e => {
  if (e.target.classList.contains("modal")) e.target.classList.remove("show");
});

document.addEventListener("DOMContentLoaded", () => {
  const first = document.querySelector(".department.active");
  if (first) selectDepartment(first);
});
