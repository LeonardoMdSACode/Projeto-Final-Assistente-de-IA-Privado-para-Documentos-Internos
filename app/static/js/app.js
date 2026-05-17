async function uploadFile() {

    const fileInput = document.getElementById("fileInput")
    const uploadStatus = document.getElementById("uploadStatus")
    const spinner = document.getElementById("uploadSpinner")

    const file = fileInput.files[0]

    if (!file) return

    uploadStatus.innerText = "A carregar documento..."
    spinner.classList.remove("hidden")

    const formData = new FormData()
    formData.append("file", file)

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        })

        const data = await response.json()
        uploadStatus.innerText = data.message

    } catch (e) {
        uploadStatus.innerText = "Erro no upload"
    } finally {
        spinner.classList.add("hidden")
    }
}


function addMessage(role, text) {

    const chatBox =
        document.getElementById("chatBox")

    const div =
        document.createElement("div")

    div.className = "msg " + role

    div.textContent = text

    chatBox.appendChild(div)

    chatBox.scrollTop =
        chatBox.scrollHeight
}


async function sendQuestion() {

    const input = document.getElementById("question")
    const sendBtn = document.getElementById("sendBtn")
    const thinkingText = document.getElementById("thinkingText")
    const thinkingSpinner = document.getElementById("thinkingSpinner")

    const question = input.value.trim()
    if (!question) return

    addMessage("user", question)

    input.value = ""

    sendBtn.disabled = true
    thinkingText.classList.remove("hidden")
    thinkingSpinner.classList.remove("hidden")

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        })

        const data = await response.json()

        // 🔥 NUNCA TOQUES NO OUTPUT
        addMessage("assistant", data.answer || "Erro na resposta")

    } finally {
        thinkingText.classList.add("hidden")
        thinkingSpinner.classList.add("hidden")
        sendBtn.disabled = false
    }
}


function handleKey(event) {

    if (
        event.key === "Enter"
        && !event.shiftKey
    ) {

        event.preventDefault()

        sendQuestion()
    }
}


async function clearChat() {

    await fetch("/clear", {
        method: "POST"
    })

    document.getElementById(
        "chatBox"
    ).innerHTML = ""
}
