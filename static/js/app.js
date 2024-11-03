const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

$(document).ready(() => {
    loadAuctions();
});

// Function to place a bid
function placeBid(auctionId) {
    const newBid = prompt("Enter your bid amount:");
    if (newBid && !isNaN(newBid)) {
        socket.emit('place_bid', { auction_id: auctionId, new_bid: parseInt(newBid) });
    }
}

// Function to load auctions from the server
function loadAuctions() {
    $.ajax({
        url: "/api/auctions",
        method: "GET",
        success: function(data) {
            const auctionList = $('#auction-list');
            auctionList.empty();
            data.forEach(item => {
                auctionList.append(`
                    <div class="auction-item" id="auction-${item.id}">
                        <h3>${item.title}</h3>
                        <p>Current Bid: ₹<span class="current-bid">${item.current_bid}</span></p>
                        <button onclick="placeBid(${item.id})">Place Bid</button>
                    </div>
                `);
            });
        }
    });
}

// Listen for updates from the server
socket.on('update_bid', function(data) {
    const auctionItem = $(`#auction-${data.auction_id}`);
    auctionItem.find('.current-bid').text(data.new_bid);
});
