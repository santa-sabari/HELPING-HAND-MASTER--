mapboxgl.accessToken = 'pk.eyJ1IjoiamFudXNpaSIsImEiOiJjazl6d2IzdmYxMnJsM21wazB3a2llY2lwIn0.pLRf45aHIwdJ6dypoH0qSA';

var map = new mapboxgl.Map({
    container: 'map', // Container ID
    style: 'mapbox://styles/mapbox/streets-v11', // Map style to use
    center: [76.9558, 11.0168], // Coimbatore [lng, lat]
    zoom: 12, // Starting zoom level
});

var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    marker: true,
    placeholder: 'Search for places in Coimbatore', // Placeholder text
    bbox: [76.6714, 10.8996, 77.2409, 11.1953], // Bounding box for Coimbatore
    proximity: {
        longitude: 76.9558,
        latitude: 11.0168
    } // Coimbatore's coordinates
});

document.getElementById('geocoder').appendChild(geocoder.onAdd(map));
map.addControl(new mapboxgl.NavigationControl());

map.on('load', function() {
    geocoder.on('result', function(ev) {
        var lon = ev.result.geometry.coordinates[0];
        var lat = ev.result.geometry.coordinates[1];
        document.querySelector('#lon').value = lon;
        document.querySelector('#lat').value = lat;
        document.querySelector('#place_name').value = ev.result.text;

        // Add a popup with the place name
        new mapboxgl.Popup()
            .setLngLat(ev.result.geometry.coordinates.slice())
            .setHTML(ev.result.text)
            .addTo(map);
    });
});
