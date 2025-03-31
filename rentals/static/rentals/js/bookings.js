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
