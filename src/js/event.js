(function () {
    var mapOptions = {
        boxZoom: false,
        doubleClickZoom: false,
        dragging: false,
        keyboard: false,
        scrollWheelZoom: false,
        zoomControl: false
    };

    var lon = 8.682222;
    var lat = 50.110556;
    var latLon = [lat, lon];

    var map = L.map('map', mapOptions)
        .setView(latLon, 12);

    var marker = L.marker(latLon).addTo(map);

    /*
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        'attribution': 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        'useCache': true
    }).addTo(map);
     */

    L.tileLayer('https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png', {
        'attribution': 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        'useCache': true
    }).addTo(map);
})();
