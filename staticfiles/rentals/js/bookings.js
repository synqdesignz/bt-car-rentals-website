//Dynamic Price Change By dates
document.addEventListener("DOMContentLoaded", function() {
    let pricePerDay = parseFloat(document.getElementById("price-per-day").innerText);
    let totalPriceElement = document.getElementById("total-price");

    function calculateTotal() {
        let pickupDate = new Date(document.getElementById("pickup-date").value);
        let dropoffDate = new Date(document.getElementById("dropoff-date").value);

        let dayDifference = (dropoffDate - pickupDate) / (1000 * 60 * 60 * 24); // Convert ms to days

        if (dayDifference > 0) {
            let totalPrice = dayDifference * pricePerDay;
            totalPriceElement.innerText = totalPrice.toFixed(2);
        } else {
            totalPriceElement.innerText = "0.00";
        }
    }

    document.getElementById("pickup-date").addEventListener("change", calculateTotal);
    document.getElementById("dropoff-date").addEventListener("change", calculateTotal);
});

//Display Addons and adjust price to match
document.addEventListener("DOMContentLoaded", function() {
    let pricePerDayElement = document.getElementById("price-per-day");
    let totalPriceElement = document.getElementById("total-price");
    let addonCheckboxes = document.querySelectorAll(".addon-checkbox");

    if (!pricePerDayElement) {
        console.error("Price-per-day element not found!");
        return;
    }

    let pricePerDay = parseFloat(pricePerDayElement.innerText.trim()) || 0;

    function calculateTotal() {
        let pickupDate = new Date(document.getElementById("pickup-date").value);
        let dropoffDate = new Date(document.getElementById("dropoff-date").value);
        let dayDifference = (dropoffDate - pickupDate) / (1000 * 60 * 60 * 24);

        if (dayDifference > 0) {
            let totalPrice = dayDifference * pricePerDay;

            // Add selected add-on prices
            addonCheckboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    let addonPrice = parseFloat(checkbox.getAttribute("data-price")) || 0;
                    totalPrice += addonPrice * dayDifference;
                }
            });

            totalPriceElement.innerText = totalPrice.toFixed(2);
        } else {
            totalPriceElement.innerText = "0.00";
        }
    }

    document.getElementById("pickup-date").addEventListener("change", calculateTotal);
    document.getElementById("dropoff-date").addEventListener("change", calculateTotal);
    addonCheckboxes.forEach(checkbox => checkbox.addEventListener("change", calculateTotal));
});

//Disable Dates for booked cars
document.addEventListener("DOMContentLoaded", function () {
    const pickupDateInput = document.getElementById("pickup-date");
    const dropoffDateInput = document.getElementById("dropoff-date");
    const carId = pickupDateInput.dataset.carId;  // Assume data attribute on input
    
    //Setting Default dates
    const today= new Date();
    const tomorrow = new Date();
    tomorrow.setDate(today.getDate() + 1);

    // Format dates as "YYYY-MM-DD" for DJango
    const todayStr = today.toISOString().split("T")[0];
    const tomorrowStr = tomorrow.toISOString().split("T")[0];
    pickupDateInput.value = todayStr;
    dropoffDateInput.value = tomorrowStr;

    // Fetch booked dates from Django
    fetch(`/get_booked_dates/${carId}/`)
        .then(response => response.json())
        .then(data => {
            const bookedDates = data.booked_dates;

            // Initialize date picker with disabled dates
            flatpickr(pickupDateInput, {
                dateFormat: "Y-m-d",
                disable: bookedDates.concat([{ from: "2000-01-01", to: new Date().toISOString().split("T")[0] }]), // Block past dates
                minDate: "today",
                onChange: function (selectedDates, dateStr) {
                    dropoffDateInput.flatpickr.set("minDate", dateStr);
                }
            });

            flatpickr(dropoffDateInput, {
                dateFormat: "Y-m-d",
                disable: bookedDates,
                minDate: "today"
            });
        })

});


