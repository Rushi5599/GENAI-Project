const OLLAMA_API = "http://localhost:11434/api/generate";

async function reportEmergency() {
  const type = document.getElementById("emergencyType").value;
  const location = document.getElementById("location").value;
  const result = document.getElementById("result");

  if (!type || !location) {
    alert("Please select emergency type and enter location");
    return;
  }

  result.innerText = "⏳ Generating emergency guidance...";

  const prompt = `
You are an emergency logistics assistant for truck drivers in India.

Emergency type: ${type}
Location: ${location}

Provide:
1. Immediate safety steps
2. Who to contact (police, ambulance, service)
3. What the driver should do next
4. Priority level (High / Medium / Low)

Use clear and calm language.
Do not ask questions.
`;

  try {
    const res = await fetch(OLLAMA_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "phi",
        prompt: prompt,
        stream: false,
        options: { num_predict: 200 }
      })
    });

    const data = await res.json();

    result.innerText =
`🚨 Emergency Type: ${type}
📍 Location: ${location}

${data.response}

📞 National Emergency Numbers:
• Police: 112
• Ambulance: 108
• Roadside Assistance: 1033`;

  } catch (err) {
    result.innerText =
      "⚠️ Ollama is not running. Please start Ollama to get AI guidance.";
  }
}
