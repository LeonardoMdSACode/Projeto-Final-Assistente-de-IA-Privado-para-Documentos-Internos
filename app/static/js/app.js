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

    loadDocuments()
}

async function sendQuestion() {

    const question = document.getElementById("question").value;

    const responseDiv = document.getElementById("response");

    responseDiv.innerHTML = "A processar...";

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question,
            document: document.getElementById(
                "documentSelect"
            ).value
        })
    });

    const data = await response.json();

    responseDiv.innerHTML = data.answer;
}

async function loadDocuments() {

    const response = await fetch("/documents")

    const data = await response.json()

    const select =
        document.getElementById("documentSelect")

    select.innerHTML = ""

    data.documents.forEach(doc => {

        const option =
            document.createElement("option")

        option.value = doc
        option.textContent = doc

        select.appendChild(option)
    })
}

loadDocuments()
