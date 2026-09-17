document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toggle-pass").forEach((btn) => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-target");
            const input = document.getElementById(targetId);

            if (!input) return;

            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";
            btn.textContent = isPassword ? "Hide" : "Show";
        });
    });

    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", (e) => {
            const password = document.getElementById("regPassword")?.value || "";
            const confirmPassword = document.getElementById("confirmPassword")?.value || "";

            if (password.length < 6) {
                e.preventDefault();
                alert("Password should be at least 6 characters long.");
                return;
            }

            if (password !== confirmPassword) {
                e.preventDefault();
                alert("Passwords do not match.");
            }
        });
    }

    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            const username = document.getElementById("username")?.value.trim();
            const password = document.getElementById("password")?.value.trim();

            if (!username || !password) {
                e.preventDefault();
                alert("Please fill in both fields.");
            }
        });
    }
});