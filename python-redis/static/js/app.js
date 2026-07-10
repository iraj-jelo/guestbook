async function loadMessages() {

    const response =
        await fetch("/api/messages");

    const data =
        await response.json();

    const list =
        document.getElementById("messages");

    list.innerHTML = "";

    data.messages.forEach(msg => {

        const item =
            document.createElement("li");

        item.className =
            "list-group-item";

        item.textContent = msg;

        list.appendChild(item);
    });
}


async function submitMessage() {

    const input =
        document.getElementById("message");

    const message =
        input.value.trim();

    if (!message) {
        return;
    }

    await fetch("/api/messages?message=" +
        encodeURIComponent(message),
    {
        method: "POST"
    });

    input.value = "";

    loadMessages();
}


loadMessages();
