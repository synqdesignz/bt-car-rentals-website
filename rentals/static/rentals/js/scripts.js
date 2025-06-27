//Menu
document.addEventListener("DOMContentLoaded", function() {
    const menuButton = document.querySelector(".menu-button");
    const dropdown = document.querySelector(".dropdown");

    menuButton.addEventListener("click", function(e) {
        e.stopPropagation();
        menuButton.classList.toggle('active');
    });

    // Close dropdown if user clicks outside
    document.addEventListener("click", function(event) {
        if (!menuButton.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.style.display = "none";
        }
    });
});


