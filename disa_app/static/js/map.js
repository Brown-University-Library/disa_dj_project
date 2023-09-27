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
    Terrain: L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        minZoom: 1,
        //maxNativeZoom: 19,
        //maxZoom: 15,
        ext: 'png'
    }),
    Textfree: L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}{r}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        minZoom: 1,
        //maxNativeZoom: 19,
        //maxZoom: 8,
        ext: 'png'
    }),
    Labels: L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        //maxNativeZoom: 19,
        //maxZoom: 12,
        ext: 'png'
    }),
    Watercolor: L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        minZoom: 1,
        //maxNativeZoom: 19,
        //maxZoom: 13,
        ext: 'jpg'
    })
};
L.control.layers(basemaps, null, { collapsed: false }).addTo(map);
basemaps.Terrain.addTo(map);

// fetch the geojson
var geoJsonData = new L.GeoJSON.AJAX(
    "/static/data/SR_geo.json", {

        // build each point
        onEachFeature: function(feature, layer) {

            var uuid = feature.properties.Referent_ID;
            var person_name = feature.properties.Name;
            var status = feature.properties.Status;
            var person_date = feature.properties.Year;
            var lat = feature.properties.lat;
            var lng = feature.properties.lon;
            var person_location = feature.properties.from.toString();
            if (person_name != " ") {
                // we can't currently link to the correct person in a point
                //var popupText = '<a href="/people/' + uuid + '">' + name + '</a><br />' + location + '<br />' + date ;
                var popupText = person_name + '<br />' + person_location + '<br />' + person_date;
            } else {
                //var popupText = '<a href="/people/' + uuid + '">A person whose name we do not know</a><br />' + location + '<br/>' + date;
                var popupText = 'A person whose name we do not know<br />' + person_location + '<br />' + person_date;

            };

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

    for (i = 0; i < clusterCount; i++) {
        clusterLocation.push(clusterChildren[i].feature.properties.from);
        var clusterName = clusterLocation.shift();
    };

    var clusterPopup = clusterName + '<br />' + clusterCount + ' people are in the database in this location.';
    a.layer.bindPopup(clusterPopup);
});
