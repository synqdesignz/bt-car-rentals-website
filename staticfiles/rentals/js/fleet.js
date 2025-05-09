document.addEventListener("DOMContentLoaded", function() {
    let currentPage = 1;
    loadCars(currentPage);

    document.getElementById("prev-btn").addEventListener("click", function() {
        if (currentPage > 1) {
            currentPage--;
            loadCars(currentPage);
        }
    });

    document.getElementById("next-btn").addEventListener("click", function() {
        currentPage++;
        loadCars(currentPage);
    });

    async function loadCars(page) {
        try {
            console.log("Fetching from:", `/fleet-api/?page=${page}`);
            let response = await fetch(`/fleet-api/?page=${page}`, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });
            
            if (!response.ok) throw new Error("Network response was not ok");
            
            let data = await response.json();
            console.log("Received data:", data);

            let container = document.getElementById("cars-list");
            container.innerHTML = "";

            data.cars.forEach(car => {
                let carImage = car.car_photo || "/static/rentals/images/default.png";
                container.innerHTML += `
                    <div class="car-card">
                        <img src="${carImage}" alt="${car.make}">
                        <h3>${car.make} ${car.model} (${car.year})</h3>
                        <p>Status: ${car.car_status}</p>
                        <p>Price per day: $${car.price_day}</p>
                        <a href="/booking/${car.id}" class="book-now-button">Book Now</a>
                    </div>
                `;
            });

            document.getElementById("page-info").innerText = `Page ${page}`;
            document.getElementById("prev-btn").disabled = !data.has_previous;
            document.getElementById("next-btn").disabled = !data.has_next;
        } catch (error) {
            console.error("Error loading cars:", error);
        }
    }
});