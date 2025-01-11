const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "login.html";
}

// Retrieve username from localStorage (or token if you prefer)
const username = localStorage.getItem("username");

// Display the username in the header
if (username) {
    document.getElementById("username").textContent = `Welcome, ${username}`;
}

async function fetchTasks() {
    try {
        const response = await fetch("http://localhost:8000/task/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        const tasks = await response.json();

        if (response.ok) {
            const taskList = document.getElementById("task-list");
            taskList.innerHTML = "";

            tasks.forEach((task) => {
                const taskRow = document.createElement("tr");

                taskRow.innerHTML = `
                    <td>${task.title}</td>
                    <td>${task.description || "N/A"}</td>
                    <td>${task.completed ? "Done" : "Pending"}</td>
                    <td>
                        <button class="update-btn" data-id="${task.id}">Update</button>
                        <button class="delete-btn" data-id="${task.id}">Delete</button>
                    </td>
                `;

                // Attach event listeners to Update and Delete buttons
                taskRow.querySelector(".update-btn").addEventListener("click", () => openUpdateModal(task));
                taskRow.querySelector(".delete-btn").addEventListener("click", () => deleteTask(task.id));

                taskList.appendChild(taskRow);
            });

            // Show message if no tasks are available
            document.getElementById("no-task-message").style.display = tasks.length === 0 ? "block" : "none";
        } else {
            alert("Failed to fetch tasks.");
        }
    } catch (error) {
        console.error(error);
    }
}

// Open the Update modal with pre-filled values
function openUpdateModal(task) {
    document.getElementById("task-title").value = task.title;
    document.getElementById("task-description").value = task.description || "";
    document.getElementById("completed").checked = task.completed;
    document.getElementById("task-modal").style.display = "block";
    document.getElementById("task-form").setAttribute("data-id", task.id);
}

// Handle task form submission
document.getElementById("task-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const taskId = document.getElementById("task-form").getAttribute("data-id");
    const taskTitle = document.getElementById("task-title").value;
    const taskDescription = document.getElementById("task-description").value;
    const completed = document.getElementById("completed").checked;

    try {
        let response;
        // If `taskId` exists, it's an update (PUT), otherwise create a new task (POST)
        if (taskId) {
            response = await fetch(`http://localhost:8000/task/${taskId}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({
                    title: taskTitle,
                    description: taskDescription,
                    completed: completed,
                }),
            });
        } else {
            response = await fetch("http://localhost:8000/task/create", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({
                    title: taskTitle,
                    description: taskDescription,
                    completed: completed,
                }),
            });
        }

        if (response.ok) {
            fetchTasks();  // Update task list after successful creation or update
            document.getElementById("task-modal").style.display = "none";  // Close the modal
        } else {
            alert("Failed to save task.");
        }
    } catch (error) {
        console.error(error);
        alert("An error occurred while saving the task.");
    }
});

// Delete a task by its ID
async function deleteTask(taskId) {
    try {
        const response = await fetch(`http://localhost:8000/task/${taskId}/`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (response.ok) {
            fetchTasks();  // Refresh task list after successful delete
        } else {
            alert("Failed to delete task.");
        }
    } catch (error) {
        console.error(error);
    }
}

document.getElementById("logout-button").addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
    window.location.href = "login.html";
});

// Modal logic
document.getElementById("create-task-button").addEventListener("click", () => {
    document.getElementById("task-modal").style.display = "block";
    // Clear the form for creating a new task
    document.getElementById("task-form").removeAttribute("data-id");
});

document.getElementById("close-modal").addEventListener("click", () => {
    document.getElementById("task-modal").style.display = "none";
});

fetchTasks();
