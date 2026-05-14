async function uploadFile() {

    const fileInput =
        document.getElementById("fileInput")

    const file = fileInput.files[0]

    const formData = new FormData()

    formData.append("file", file)

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    })

    const data = await response.json()

    alert(data.message)
}

function addMessage(role, text) {
    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");
    div.className = "msg " + role;
    div.textContent = text;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendQuestion() {

    const input = document.getElementById("question");
    const question = input.value.trim();

    if (!question) return;

    addMessage("user", question);

    input.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    const data = await response.json();

    addMessage("assistant", data.answer);
}

function handleKey(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendQuestion();
    }
}

async function clearChat() {

    await fetch("/clear", { method: "POST" });

    document.getElementById("chatBox").innerHTML = "";
}
