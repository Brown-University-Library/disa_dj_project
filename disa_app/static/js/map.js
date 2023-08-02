//establish the map
var map = L.map('map-container', {
    center: [41, -71],
    zoom: 5,
    //maxZoom: 19
});

//the various basemaps
const basemaps = {
    Terrain: L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        minZoom: 1,
        //maxNativeZoom: 19,
        maxZoom: 8,
        ext: 'png'
    }),
    Textfree: L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}{r}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        minZoom: 1,
        //maxNativeZoom: 19,
        maxZoom: 8,
        ext: 'png'
    }),
    Labels: L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        //maxNativeZoom: 19,
        maxZoom: 12,
        ext: 'png'
    }),
    Watercolor: L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
        attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        minZoom: 1,
        //maxNativeZoom: 19,
        maxZoom: 13,
        ext: 'jpg'
    })
};
L.control.layers(basemaps, null, {collapsed:false}).addTo(map);
basemaps.Terrain.addTo(map);

// fetch the geojson
var geoJsonData = new L.GeoJSON.AJAX(
    "/static/data/stolen_relations_geocoded_wgs84.geojson", {

      // build each point
        onEachFeature: function(feature, layer) {

            var uuid = feature.properties.referent_id;
            var name = feature.properties.Name;
            var status = feature.properties.Status;
            var date = feature.properties.Year;
            var lat = feature.properties.lat;
            var lng = feature.properties.lng;
            var location = feature.properties.Location.toString();
            if (name != null) {
                var popupText = '<a href="/people/' + uuid + '">' + name + '</a><br />' + location + '<br />' + date ;
            } else {
                var popupText = '<a href="/people/' + uuid + '">A person whose name we do not know</a><br />' + location + '<br/>' + date;
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
        clusterLocation.push(clusterChildren[i].feature.properties.Location);
        var clusterName = clusterLocation.shift();
    };

    var clusterPopup = clusterName + '<br />' + clusterCount + ' people are in the database in this location.';
    a.layer.bindPopup(clusterPopup);
});
