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
        let response = await fetch(`/fleet/?page=${page}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
        let data = await response.json();

        let container = document.getElementById("cars-list");
        container.innerHTML = "";

        data.cars.forEach(car => {
            container.innerHTML += `
                <div class="car-card">
                    <img src="${car.car_photo || 'rentals/default.png'}" alt="${car.make}">
                    <h3>${car.make} ${car.model} (${car.year})</h3>
                    <p>Reg: ${car.reg_no}</p>
                    <p>Status: ${car.car_status}</p>
                    <p>Price per day: $${car.price_day}</p>
                </div>
            `;
        });

        document.getElementById("page-info").innerText = `Page ${page}`;
        document.getElementById("prev-btn").disabled = !data.has_previous;
        document.getElementById("next-btn").disabled = !data.has_next;
    }
});
