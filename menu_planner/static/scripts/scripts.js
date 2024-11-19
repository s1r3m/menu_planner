async function login() {await fetch("login",  {method: "GET"})}


function updateUsername(data) {
    const username = document.querySelector(".username")
    username.textContent = data.username;
}

function updatePlaceholders(data) {
    // Clear all placeholders first
    const placeholders = document.querySelectorAll(".placeholder");
    placeholders.forEach((placeholder) => {
        placeholder.className = "placeholder empty"; // Reset to empty
        placeholder.textContent = ""; // Clear content
    });

    // Fill placeholders based on weeks data
    const weeks = data["weeks"] || [];
    weeks.forEach((week, index) => {
        if (index < placeholders.length) {
            placeholders[index].className = "placeholder created-week";
            placeholders[index].textContent = week.name;
        }
    });

    // Mark the next available placeholder as "add week"
    if (weeks.length < placeholders.length) {
        const nextPlaceholder = placeholders[weeks.length];
        nextPlaceholder.className = "placeholder add-week";
        nextPlaceholder.textContent = "+";
    }
}