document.addEventListener("DOMContentLoaded", function() {
    // Mock auction data
    const auctions = [
        {
            id: 1,
            name: "Metal Scrap Auction",
            date: "2024-10-25",
            time: "10:00 AM",
            companies: ["Company A", "Company B", "Company C"],
            status: "Ongoing",
        },
        {
            id: 2,
            name: "Plastic Waste Auction",
            date: "2024-10-28",
            time: "2:00 PM",
            companies: ["Company D", "Company E"],
            status: "Upcoming",
        },
        {
            id: 3,
            name: "Electronic Waste Auction",
            date: "2024-10-30",
            time: "11:00 AM",
            companies: ["Company F", "Company G", "Company H"],
            status: "Upcoming",
        }
    ];

    const auctionList = document.getElementById("auction-list");
    const auctionDetails = document.getElementById("auction-details");

    // Populate auction list
    auctions.forEach(auction => {
        const auctionItem = document.createElement("div");
        auctionItem.classList.add("auction-item");
        auctionItem.textContent = `${auction.name} - ${auction.date} at ${auction.time}`;
        auctionItem.dataset.auctionId = auction.id;

        auctionList.appendChild(auctionItem);
    });

    // Event listener for selecting an auction
    auctionList.addEventListener("click", function(event) {
        const auctionId = event.target.dataset.auctionId;
        const selectedAuction = auctions.find(auction => auction.id == auctionId);

        if (selectedAuction) {
            auctionDetails.innerHTML = `
                <h3>${selectedAuction.name}</h3>
                <p>Date: ${selectedAuction.date}</p>
                <p>Time: ${selectedAuction.time}</p>
                <p>Status: ${selectedAuction.status}</p>
                <h4>Participating Companies:</h4>
                <ul>
                    ${selectedAuction.companies.map(company => `<li>${company}</li>`).join('')}
                </ul>
            `;
        }
    });
});
