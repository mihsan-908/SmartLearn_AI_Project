
function generateNotes() {
    const output = document.getElementById("notesOutput");
    if (!output) return;

    output.className = "output-box";
    output.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';

    const btn = document.querySelector(".action-row button");
    if (btn) btn.disabled = true;

    fetch("/notes/", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(async (res) => {
        const data = await res.json();
        if (!res.ok || data.error) {
            output.className = "output-box empty-state";
            output.innerText = data.error || "Failed to generate notes.";
            return;
        }
        output.className = "output-box";
        output.style.whiteSpace = "pre-wrap";
        output.innerText = data.notes || "No notes returned.";
    })
    .catch(() => {
        output.className = "output-box empty-state";
        output.innerText = "Something went wrong while generating notes.";
    })
    .finally(() => {
        if (btn) btn.disabled = false;
    });
}
