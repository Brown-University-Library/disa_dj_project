// if being referred by a People Detail page, the URL will have queries in it
/*const current = new URL(window.location.href);
function hasQueryParams(current) {
    return current.includes('?');
    // break the lat, lon, and zoom out from the URL
    function getQueryStringValue(key) {
        return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
    }
    let querylat = getQueryStringValue("lat");
    let querylon = getQueryStringValue("lon");
    let queryzoom = getQueryStringValue("zoom");
}

let cameFrom = new URL(document.referrer);
if (cameFrom == undefined) { let cameFrom = "" }
// if referrer was a people page, set map with query coordinates, else set default map
if (cameFrom.pathname.startsWith("/people/")) {
    let map = L.map('map-container').setView([querylat, querylon], queryzoom);
} else {
    let map = L.map('map-container').setView([41, -71], 5);
}*/
// establish the default map container
let map = L.map('map-container').setView([41, -71], 5);
//the various basemaps
const basemaps = {
    Standard: L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }),
    Watercolor: L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.jpg', {
        attribution: '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        ext: 'jpg'
    })
};

L.control.layers(basemaps, null, { collapsed: false }).addTo(map);
basemaps.Standard.addTo(map);

// fetch the geojson
var geoJsonData = new L.GeoJSON.AJAX(
    leaflet_data_url, {

        // build each point
        onEachFeature: function(feature, layer) {

            //var uuid = feature.properties.Referent_ID;
            var person_name = feature.properties.Name;
            if (person_name = " ") {
                var person_name = "A person whose name we do not know"
            }
            var status = feature.properties.Status;
            if (feature.properties.Year) {
                var person_date = feature.properties.Year;
            }
            else {
                var person_date = "";
            }
            var lat = feature.properties.lat;
            var lng = feature.properties.lon;
            var person_location = feature.properties.from.toString();

            var popupText = person_name + '<br />' + person_location + '<br />' + person_date;
            layer.bindPopup(popupText);
        }

    });

// cluster points
var markers = L.markerClusterGroup({
    chunkedLoading: true,
    maxClusterRadius: 30,
});
//geojson ajax listener
geoJsonData.on('data:loaded', function() {
    // Add the cluster data after the geojson layer has loaded.
    markers.addLayer(geoJsonData);
    map.addLayer(markers);
});
// IDK why `clustermouseover` actually triggers on a click and `clusterclick` triggers on the *second* click of a cluster
// popup shows a cluster's location, taken from the first record in the cluster, and how many records it holds
markers.on('clustermouseover', function(a) {
    var clusterCount = a.layer.getChildCount();
    var clusterChildren = a.layer.getAllChildMarkers();
    var clusterLocation = [];

    let i;
    for (i = 0; i < clusterCount; i++) {
        clusterLocation.push(clusterChildren[i].feature.properties.from);
        var clusterName = clusterLocation.shift();
    };

    var clusterPopup = clusterName + '<br />' + clusterCount + ' people are in the database in this location.';
    a.layer.bindPopup(clusterPopup);
});
