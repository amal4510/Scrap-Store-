document.querySelectorAll('.image-container img').forEach(image => {
    image.onclick = () => {
        document.querySelector('.pop-image').style.display = 'block';
        document.querySelector('.pop-image img').src = image.getAttribute('src');
    }
});

document.querySelector('.pop-image span').onclick = () => {
    document.querySelector('.pop-image').style.display = 'none';
}
// Fetch scrap prices from the server
function fetchScrapPrices() {
    fetch('/getScrapPrices')  // Assuming '/getScrapPrices' is your endpoint
    .then(response => response.json())
    .then(data => {
        // Update the prices in the HTML
        document.getElementById('price-normal-recyclables').innerText = data.normal_recyclables;
            document.getElementById('price-office-paper').innerText = data.office_paper;
            document.getElementById('price-newspaper').innerText = data.newspaper;
            document.getElementById('price-ac-units').innerText = data.ac_units;
            document.getElementById('price-washing-machine').innerText = data.washing_machine;
            document.getElementById('price-fridge').innerText = data.single_door_fridge;
            document.getElementById('price-printer').innerText = data.printer;
            document.getElementById('price-ceiling-fan').innerText = data.ceiling_fan;
            document.getElementById('price-microwave').innerText = data.microwave;
            document.getElementById('price-scrap-laptop').innerText = data.scrap_laptop;
            document.getElementById('price-mobile-phones').innerText = data.mobile_phones;
            document.getElementById('price-cpu').innerText = data.computer_cpu;
        // Add similar lines for other items
    })
    .catch(error => console.error('Error fetching prices:', error));
}

// Call this function every few seconds to update prices
setInterval(fetchScrapPrices, 5000);  // Fetch every 5 seconds
