(function () {
    var mapOptions = {
        boxZoom: false,
        doubleClickZoom: false,
        dragging: false,
        keyboard: false,
        scrollWheelZoom: false,
        zoomControl: false
    };


    var lat = 50.115597;
    var lon = 9.242031;
    var hasCoordinates = false;
    var zoom = 3;

    if (window.fe && window.fe.event.lat && window.fe.event.lon) {
        lat = window.fe.event.lat;
        lon = window.fe.event.lon;
        hasCoordinates = true;
        zoom = 13;
    }

    var latLon = [lat, lon];

    var map = L.map('map', mapOptions)
        .setView(latLon, zoom);

    if (hasCoordinates) {
        var marker = L.marker(latLon).addTo(map);
    }

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
