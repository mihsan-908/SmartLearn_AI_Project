
function generateSummary(type) {
    const output = document.getElementById("summaryOutput");
    if (!output) return;

    output.className = "output-box";
    output.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';

    const buttons = document.querySelectorAll(".action-row button");
    buttons.forEach(btn => btn.disabled = true);

    fetch("/summary/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ summary_type: type })
    })
    .then(async (res) => {
        const data = await res.json();
        if (!res.ok || data.error) {
            output.className = "output-box empty-state";
            output.innerText = data.error || "Failed to generate summary.";
            return;
        }
        output.className = "output-box";
        output.style.whiteSpace = "pre-wrap";
        output.innerText = data.summary || "No summary returned.";
    })
    .catch(() => {
        output.className = "output-box empty-state";
        output.innerText = "Something went wrong while connecting to the server.";
    })
    .finally(() => {
        buttons.forEach(btn => btn.disabled = false);
    });
}
