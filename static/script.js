const chatWindow = document.getElementById("chat-window");
const composer = document.getElementById("composer");
const input = document.getElementById("message-input");

// A simple per-tab session id, so the backend can keep conversation
// history separate between different browser tabs/visitors.
const sessionId = Math.random().toString(36).slice(2);

function addMessage(text, sender) {
  const row = document.createElement("div");
  row.className = `message ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  row.appendChild(bubble);
  chatWindow.appendChild(row);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return row;
}

function addThinkingIndicator() {
  const row = document.createElement("div");
  row.className = "message bot thinking";
  row.innerHTML = `
    <div class="bubble">
      <span class="dot"></span><span class="dot"></span><span class="dot"></span>
    </div>
  `;
  chatWindow.appendChild(row);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return row;
}

async function sendMessage(message) {
  const thinkingRow = addThinkingIndicator();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId }),
    });

    if (!res.ok) {
      throw new Error(`Server responded with ${res.status}`);
    }

    const data = await res.json();
    thinkingRow.remove();
    addMessage(data.response, "bot");
  } catch (err) {
    thinkingRow.remove();
    addMessage("Something went wrong reaching the server. Is app.py running?", "bot");
    console.error(err);
  }
}

composer.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  sendMessage(text);
});
