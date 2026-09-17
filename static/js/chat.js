document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatForm");
    const messageInput = document.getElementById("messageInput");
    const chatStream = document.getElementById("chatStream");
    const currentFileName = document.getElementById("currentFileName");

    if (!chatForm || !messageInput || !chatStream) return;

    function scrollToBottom() {
        window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
        chatStream.scrollTop = chatStream.scrollHeight;
    }

    function appendMessage(text, type = "ai") {
        const message = document.createElement("div");
        message.className = `message ${type}`;
        message.style.whiteSpace = "pre-wrap";
        message.textContent = text;
        chatStream.appendChild(message);
        scrollToBottom();
        return message;
    }

    function appendTyping() {
        const loader = document.createElement("div");
        loader.className = "message ai typing-message";
        loader.innerHTML = `
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;
        chatStream.appendChild(loader);
        scrollToBottom();
        return loader;
    }

    function loadCurrentFileInfo() {
        fetch("/upload/text")
            .then(res => res.json())
            .then(data => {
                if (data.filename && currentFileName) {
                    currentFileName.textContent = data.filename;
                }
            })
            .catch(() => {});
    }

    function loadHistory() {
        fetch("/chat/history")
            .then(res => res.json())
            .then(data => {
                if (data.filename && currentFileName) {
                    currentFileName.textContent = data.filename;
                }
                if (data.messages && data.messages.length > 0) {
                    chatStream.innerHTML = "";
                    data.messages.forEach(msg => {
                        appendMessage(msg.content, msg.role === "user" ? "user" : "ai");
                    });
                }
            })
            .catch(() => {});
    }

    loadCurrentFileInfo();
    loadHistory();

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (!message) return;

        appendMessage(message, "user");
        messageInput.value = "";
        messageInput.focus();

        const typing = appendTyping();

        try {
            const response = await fetch("/chat/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            typing.remove();

            if (!response.ok) {
                appendMessage(data.error || "Something went wrong.", "ai");
                return;
            }

            appendMessage(data.response || "No response returned.", "ai");
        } catch (error) {
            typing.remove();
            appendMessage("Unable to connect to the AI server.", "ai");
        }
    });

    messageInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            chatForm.requestSubmit();
        }
    });
});
