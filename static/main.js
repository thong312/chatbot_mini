let chatHistory = [];

function renderChat() {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";
    chatHistory.forEach(msg => {
        const row = document.createElement("div");
        row.className = "msg-row " + (msg.sender === "user" ? "msg-user" : "msg-bot");
        const bubble = document.createElement("div");
        bubble.className = "msg-bubble";
        bubble.textContent = msg.text;
        row.appendChild(bubble);
        chatBox.appendChild(row);
    });
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("message");
    const msg = input.value.trim();
    if (!msg) return;
    chatHistory.push({ sender: "user", text: msg });
    renderChat();
    input.value = "";
    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    chatHistory.push({ sender: "bot", text: data.reply });
    renderChat();
}

window.onload = renderChat;