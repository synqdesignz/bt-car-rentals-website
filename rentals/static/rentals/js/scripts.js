


//Menu
document.addEventListener("DOMContentLoaded", function() {
    const menuButton = document.querySelector(".menu-button");
    const dropdown = document.querySelector(".dropdown");

    menuButton.addEventListener("click", function() {
        dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    });

    // Close dropdown if user clicks outside
    document.addEventListener("click", function(event) {
        if (!menuButton.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.style.display = "none";
        }
    });
});


