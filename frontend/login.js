document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    console.log(password);

    try {
        const response = await fetch("http://localhost:8000/user/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ username, password }),
        });

        const data = await response.json();
        const message = document.getElementById("login-message");

        if (response.ok) {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem('username', data.username);
            message.style.color = "green";
            message.textContent = "Login successful! Redirecting...";
            setTimeout(() => window.location.href = "tasks.html", 2000);
        } else {
            message.style.color = "red";
            message.textContent = data.detail || "Login failed.";
        }
    } catch (error) {
        console.error(error);
    }
});
