const socket = io();

// Function to render scrap items
function renderScrapItems(scrapItems, elementId) {
    const itemList = $(`#${elementId}`);
    itemList.empty(); // Clear previous items
    scrapItems.forEach(item => {
        itemList.append(`
            <div class="scrap-item" id="item-${item.id}">
                <h3>${item.title}</h3>
                <p>Current Bid: <span id="current-bid-${item.id}">${item.current_bid}</span></p>
                <button onclick="placeBid(${item.id})">Place Bid</button>
            </div>
        `);
    });
}

// Fetch available scrap items
function fetchScrapItems() {
    $.get('/api/scrap_items', function(data) {
        renderScrapItems(data, 'scrap-items-list');
        renderScrapItems(data, 'admin-scrap-items-list'); // Admin also sees the same list
    });
}

// Place a bid for a scrap item
function placeBid(itemId) {
    const bidAmount = prompt("Enter your bid amount:");
    if (bidAmount) {
        socket.emit('place_bid', {
            item_id: itemId,
            new_bid: parseFloat(bidAmount),
        });
    }
}

// Listen for updates from the server
socket.on('update_bid', function(data) {
    const { item_id, new_bid } = data;
    $(`#current-bid-${item_id}`).text(new_bid);
});

// Call fetchScrapItems to load items initially
$(document).ready(function() {
    fetchScrapItems();
});
