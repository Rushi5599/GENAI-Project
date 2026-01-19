// Ollama local API
const OLLAMA_API = "http://localhost:11434/api/generate";

document.getElementById("chatbot-toggle").onclick = toggleChat;

function toggleChat() {
  const bot = document.getElementById("chatbot");
  bot.style.display = bot.style.display === "block" ? "none" : "block";
}

async function sendMessage() {
  const text = document.getElementById("chatText").value;
  const role = document.getElementById("chatRole").value;

  if (!text) return;

  addMessage(text, "user");
  document.getElementById("chatText").value = "";

  // Role-based prompt
  const rolePrompt = `
You are an AI assistant for transportation & logistics in India.
User role: ${role}

Rules:
- Customer → suggest trucks, price, delivery time
- Driver → route tips, safety, earnings
- Owner → fleet insights, utilization, profit tips

User question:
${text}
`;

  try {
    const res = await fetch(OLLAMA_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "phi",
        prompt: rolePrompt,
        stream: false
      })
    });

    const data = await res.json();
    addMessage(data.response, "bot");
  } catch (err) {
    addMessage("⚠️ Ollama is not running. Please start it.", "bot");
  }
}

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = type === "user" ? "user-msg" : "bot-msg";
  div.innerText = text;
  document.getElementById("chatMessages").appendChild(div);
}
