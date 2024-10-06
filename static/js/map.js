// Load the data using D3
d3.json("data/2024-10-06_accessibility_restaurant_info.json").then(function(data) {

    // Initialize the map
    var map = L.map('map').setView([45.6346, -122.6731], 13);  // Center at Vancouver, WA

    // Add a tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Function to update the restaurant details in the sidebar
    function updateRestaurantInfo(restaurant) {
        const infoDiv = document.getElementById('restaurant-info');
        infoDiv.innerHTML = `
            <h3>${restaurant.name}</h3>
            <p><strong>Address:</strong> ${restaurant.formatted_address || 'Unknown'}</p>
            <p><strong>Wheelchair Accessible Entrance:</strong> ${restaurant.wheelchair_accessible_entrance}</p>
            <p><strong>Wheelchair Accessible Parking:</strong> ${restaurant.wheelchair_accessible_parking || 'Unknown'}</p>
            <p><strong>Wheelchair Accessible Restroom:</strong> ${restaurant.wheelchair_accessible_restroom || 'Unknown'}</p>
            <p><strong>Wheelchair Accessible Seating:</strong> ${restaurant.wheelchair_accessible_seating || 'Unknown'}</p>
        `;
    }

    // Loop through the data and add markers for each restaurant
    data.forEach(function(restaurant) {
        var marker = L.marker([restaurant.latitude, restaurant.longitude]).addTo(map);
        marker.bindPopup(`<b>${restaurant.name}</b>`);

        // When a marker is clicked, update the restaurant details
        marker.on('click', function() {
            updateRestaurantInfo(restaurant);
        });
    });
}).catch(function(error) {
    console.error('Error loading the JSON data:', error);
});
