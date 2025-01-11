document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:8000/user/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        const message = document.getElementById("register-message");

        if (response.ok) {
            message.style.color = "green";
            message.textContent = "Registration successful! Redirecting...";
            setTimeout(() => window.location.href = "login.html", 2000);
        } else {
            message.style.color = "red";
            message.textContent = data.detail || "Registration failed.";
        }
    } catch (error) {
        console.error(error);
    }
});
