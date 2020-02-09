(function () {
    var mapOptions = {};

    var lat = 50.115597;
    var lon = 9.242031;
    var hasCoordinates = false;

    if (window.fe && window.fe.event.lat && window.fe.event.lon) {
        hasCoordinates = true;
        lat = window.fe.event.lat;
        lon = window.fe.event.lon;
    }

    var latLon = [lat, lon];

    var map = L.map('map', mapOptions)
        .setView(latLon, 10);

    if (hasCoordinates) {
        var marker = L.marker(latLon).addTo(map);
    }

    L.tileLayer('https://c.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        'attribution': 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        'useCache': true
    }).addTo(map);
})();
