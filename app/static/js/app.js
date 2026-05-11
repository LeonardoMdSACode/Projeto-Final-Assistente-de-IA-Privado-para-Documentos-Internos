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
            question: question
        })
    });

    const data = await response.json();

    responseDiv.innerHTML = data.answer;
}