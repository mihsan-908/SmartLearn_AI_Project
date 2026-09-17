
function generateQuiz() {
    const output = document.getElementById("quizOutput");
    if (!output) return;

    output.className = "output-box";
    output.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';

    const countSelect = document.getElementById("questionCount");
    const count = countSelect ? parseInt(countSelect.value, 10) || 5 : 5;

    const btn = document.querySelector(".action-row button");
    if (btn) btn.disabled = true;

    fetch("/quiz/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question_count: count })
    })
    .then(async (res) => {
        const data = await res.json();
        if (!res.ok || data.error) {
            output.className = "output-box empty-state";
            output.innerText = data.error || "Failed to generate quiz.";
            return;
        }
        output.className = "output-box";
        output.style.whiteSpace = "pre-wrap";
        output.innerText = data.quiz || "No quiz returned.";
    })
    .catch(() => {
        output.className = "output-box empty-state";
        output.innerText = "Something went wrong while generating the quiz.";
    })
    .finally(() => {
        if (btn) btn.disabled = false;
    });
}
